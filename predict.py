"""
Predict the environmental sound class of an audio file using the trained SVM.

Usage
  python predict.py <audio_file>
"""

import os
import sys
import warnings

import numpy as np
import librosa
import joblib

from config import MODEL_PATH, SCALER_PATH, SAMPLE_RATE, N_MFCC

# UrbanSound8K class-ID → human-readable label mapping
CLASS_LABELS = {
    0: "air_conditioner",
    1: "car_horn",
    2: "children_playing",
    3: "dog_bark",
    4: "drilling",
    5: "engine_idling",
    6: "gun_shot",
    7: "jackhammer",
    8: "siren",
    9: "street_music",
}

MIN_SIGNAL_LENGTH = 2048


def _pad_if_needed(signal: np.ndarray, min_length: int = MIN_SIGNAL_LENGTH) -> np.ndarray:
    """Zero-pad *signal* to *min_length* if it is shorter."""
    if len(signal) < min_length:
        signal = np.pad(signal, (0, min_length - len(signal)))
    return signal


def extract_features(file_path: str) -> np.ndarray:
    """
    Extract the **86-dimensional** feature vector that matches the trained model:
      40 mean MFCCs  +  40 mean Δ-MFCCs  +  6 mean tonnetz  =  86
    """
    warnings.filterwarnings("ignore", message="n_fft=.*is too large")

    audio, sr = librosa.load(file_path, sr=SAMPLE_RATE)

    # Normalise peak amplitude
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak

    audio = _pad_if_needed(audio)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
    mfcc_mean = np.mean(mfcc.T, axis=0)

    delta = librosa.feature.delta(mfcc)
    delta_mean = np.mean(delta.T, axis=0)

    harmonic = librosa.effects.harmonic(audio)
    tonnetz = librosa.feature.tonnetz(y=harmonic, sr=sr)
    tonnetz_mean = np.mean(tonnetz.T, axis=0)

    warnings.resetwarnings()

    return np.hstack([mfcc_mean, delta_mean, tonnetz_mean])


def predict_audio(file_path: str) -> str:
    """
    Predict the sound class of an audio file using the trained SVM model.
    Returns the predicted class label as a string.
    Used by app/api.py.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at '{MODEL_PATH}'. Run train_model.py first."
        )
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(
            f"Scaler not found at '{SCALER_PATH}'. Run train_model.py first."
        )

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    features = extract_features(file_path).reshape(1, -1)
    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)
    class_id = int(prediction[0])
    return CLASS_LABELS.get(class_id, str(class_id))


# Backward-compatible alias used in some older scripts
classify = predict_audio


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py <audio_file>")
        sys.exit(1)
    result = predict_audio(sys.argv[1])
    print("Predicted class:", result)