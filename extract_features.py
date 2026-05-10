"""
Standalone feature-extraction script.

Walks the UrbanSound8K dataset and produces:
  - X_features.npy   (N × 86 float32 matrix)
  - y_labels.npy      (N,)   int array

The 86 dimensions are:
  40 mean MFCCs  +  40 mean Δ-MFCCs  +  6 mean tonnetz
"""

import os
import sys
import time
import warnings

import numpy as np
import pandas as pd
import librosa

from config import (
    DATASET_PATH,
    METADATA_PATH,
    FEATURES_PATH,
    LABELS_PATH,
    SAMPLE_RATE,
    N_MFCC,
)

MIN_SIGNAL_LENGTH = 2048


def _pad_if_needed(signal: np.ndarray, min_length: int = MIN_SIGNAL_LENGTH) -> np.ndarray:
    """Zero-pad *signal* to *min_length* if it is shorter."""
    if len(signal) < min_length:
        signal = np.pad(signal, (0, min_length - len(signal)))
    return signal


def extract_features(file_path: str) -> np.ndarray:
    """
    Extract the 86-dimensional feature vector:
      40 mean MFCCs  +  40 mean Δ-MFCCs  +  6 mean tonnetz  =  86
    """
    audio, sr = librosa.load(file_path, sr=SAMPLE_RATE)

    # Normalise peak amplitude
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak

    # Pad short clips to avoid librosa warnings / errors
    audio = _pad_if_needed(audio)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
    mfcc_mean = np.mean(mfcc.T, axis=0)

    delta = librosa.feature.delta(mfcc)
    delta_mean = np.mean(delta.T, axis=0)

    harmonic = librosa.effects.harmonic(audio)
    tonnetz = librosa.feature.tonnetz(y=harmonic, sr=sr)
    tonnetz_mean = np.mean(tonnetz.T, axis=0)

    return np.hstack([mfcc_mean, delta_mean, tonnetz_mean])


def build_dataset():
    """Walk the dataset and produce cached .npy feature files."""
    if not os.path.exists(METADATA_PATH):
        sys.exit(
            f"[ERROR] Metadata CSV not found at {METADATA_PATH}.\n"
            "       Download UrbanSound8K and place it under data/UrbanSound8K/"
        )

    metadata = pd.read_csv(METADATA_PATH)
    total = len(metadata)
    print(f"[INFO] Extracting features from {total} audio clips …")

    features = []
    labels = []
    skipped = 0
    start = time.time()

    warnings.filterwarnings("ignore", message="n_fft=.*is too large")

    for idx, row in metadata.iterrows():
        fold = f"fold{row['fold']}"
        file_name = row["slice_file_name"]
        label = row["classID"]
        file_path = os.path.join(DATASET_PATH, fold, file_name)

        try:
            feat = extract_features(file_path)
            features.append(feat)
            labels.append(label)
        except Exception as e:
            skipped += 1
            print(f"  [WARN] Skipping {file_path}: {e}")
            continue

        done = idx + 1
        if done % 500 == 0 or done == total:
            elapsed = time.time() - start
            rate = done / elapsed if elapsed > 0 else 0
            eta = (total - done) / rate if rate > 0 else 0
            print(
                f"  [{done:>5}/{total}] "
                f"{done / total * 100:5.1f}%  "
                f"({rate:.0f} clips/s, ETA {eta:.0f}s)"
            )

    warnings.resetwarnings()

    np.save(FEATURES_PATH, np.array(features))
    np.save(LABELS_PATH, np.array(labels))

    print(f"\n[INFO] Feature extraction completed — {len(features)} OK, {skipped} skipped.")
    print(f"[INFO] Saved to {FEATURES_PATH} and {LABELS_PATH}")


if __name__ == "__main__":
    build_dataset()