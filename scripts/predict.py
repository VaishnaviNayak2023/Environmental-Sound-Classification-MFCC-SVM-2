import sys
import os
import joblib
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.helpers import load_config
from src.preprocessing.load_audio import load_audio
from src.preprocessing.preprocess_audio import normalize_audio
from src.preprocessing.feature_extraction import extract_features


def predict(audio_file):
    config = load_config()

    model_path = config["model_output"]
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at '{model_path}'. Run scripts/train.py first."
        )

    model = joblib.load(model_path)

    # Load the scaler saved alongside the model by induction_learning.py
    scaler_path = model_path.replace(".pkl", "_scaler.pkl")
    scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None

    signal, sr = load_audio(audio_file, config["sample_rate"])
    signal = normalize_audio(signal)

    features = extract_features(signal, sr, config["mfcc_features"])
    features = features.reshape(1, -1)

    if scaler is not None:
        features = scaler.transform(features)

    prediction = model.predict(features)
    print("Predicted Sound:", prediction[0])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/predict.py <audio_file>")
        sys.exit(1)
    predict(sys.argv[1])