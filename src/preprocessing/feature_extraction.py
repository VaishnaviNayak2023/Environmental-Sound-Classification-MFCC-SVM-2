import librosa
import numpy as np

MIN_SIGNAL_LENGTH = 2048


def _pad_if_needed(signal, min_length=MIN_SIGNAL_LENGTH):
    """Zero-pad *signal* to *min_length* if it is shorter."""
    if len(signal) < min_length:
        signal = np.pad(signal, (0, min_length - len(signal)))
    return signal


def extract_features(signal, sr, n_mfcc):
    """
    Extract the 86-dimensional feature vector matching the trained model:
      40 mean MFCCs  +  40 mean Δ-MFCCs  +  6 mean tonnetz  =  86
    """
    signal = _pad_if_needed(signal)

    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfcc)
    mfcc_scaled = np.mean(mfcc.T, axis=0)

    delta = librosa.feature.delta(mfcc)
    delta_mean = np.mean(delta.T, axis=0)

    harmonic = librosa.effects.harmonic(signal)
    tonnetz = librosa.feature.tonnetz(y=harmonic, sr=sr)
    tonnetz_mean = np.mean(tonnetz.T, axis=0)

    features = np.hstack([mfcc_scaled, delta_mean, tonnetz_mean])
    return features