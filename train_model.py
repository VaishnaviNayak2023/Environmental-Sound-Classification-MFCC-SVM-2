"""
Environmental Sound Classification — End-to-end training pipeline.

Steps
  1. Extract MFCC + Δ-MFCC + tonnetz features from UrbanSound8K audio
     (cached to .npy files so re-runs skip extraction).
  2. Train an SVM (RBF kernel) with StandardScaler.
  3. Print a classification report on the held-out test set.
  4. Save the trained model and scaler to ``models/``.

Usage
  python train_model.py            # full pipeline
  python train_model.py --force    # re-extract features even if cached
"""

import os
import sys
import warnings
import argparse
import time

# Suppress all librosa / audioread / numpy warnings so they don't flood output
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import librosa
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report

from config import (
    DATASET_PATH,
    METADATA_PATH,
    FEATURES_PATH,
    LABELS_PATH,
    MODEL_PATH,
    SCALER_PATH,
    SAMPLE_RATE,
    N_MFCC,
    TEST_SIZE,
    RANDOM_STATE,
)

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

# Minimum number of samples an audio clip must have after loading.
# Clips shorter than this are zero-padded so that MFCC / tonnetz
# computation does not fail.
MIN_SIGNAL_LENGTH = 2048


# ── feature helpers ──────────────────────────────────────────────
def _pad_if_needed(signal: np.ndarray, min_length: int = MIN_SIGNAL_LENGTH) -> np.ndarray:
    """Zero-pad *signal* to *min_length* if it is shorter."""
    if len(signal) < min_length:
        signal = np.pad(signal, (0, min_length - len(signal)))
    return signal


def extract_features(file_path: str) -> np.ndarray:
    """
    Return an 86-dim feature vector:
      40 mean MFCCs + 40 mean Δ-MFCCs + 6 mean tonnetz = 86
    """
    signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)

    # Normalise peak amplitude
    peak = np.max(np.abs(signal))
    if peak > 0:
        signal = signal / peak

    # Pad short clips to avoid librosa warnings / errors
    signal = _pad_if_needed(signal)

    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=N_MFCC)
    mfcc_mean = np.mean(mfcc.T, axis=0)

    delta = librosa.feature.delta(mfcc)
    delta_mean = np.mean(delta.T, axis=0)

    harmonic = librosa.effects.harmonic(signal)
    tonnetz = librosa.feature.tonnetz(y=harmonic, sr=sr)
    tonnetz_mean = np.mean(tonnetz.T, axis=0)

    return np.hstack([mfcc_mean, delta_mean, tonnetz_mean])


# ── pipeline stages ──────────────────────────────────────────────
def extract_all_features(force: bool = False):
    """Walk the dataset, extract features, and cache to .npy files."""

    if not force and os.path.exists(FEATURES_PATH) and os.path.exists(LABELS_PATH):
        print(f"[INFO] Cached features found — loading {FEATURES_PATH}")
        X = np.load(FEATURES_PATH)
        y = np.load(LABELS_PATH)
        print(f"[INFO] Loaded {len(X)} samples from cache.")
        return X, y

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

    # Suppress librosa n_fft warnings for very short signals (we pad them)
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
        except Exception as exc:
            skipped += 1
            print(f"  [WARN] Skipping {file_path}: {exc}")

        # Progress report every 500 files
        done = idx + 1
        if done % 500 == 0 or done == total:
            elapsed = time.time() - start
            rate = done / elapsed if elapsed > 0 else 0
            eta = (total - done) / rate if rate > 0 else 0
            print(
                f"  [{done:>5}/{total}] "
                f"{done / total * 100:5.1f}%  "
                f"({rate:.0f} clips/s, ETA {eta:.0f}s)",
                flush=True,
            )

    # Restore default warning behaviour
    warnings.resetwarnings()

    X = np.array(features)
    y = np.array(labels)

    np.save(FEATURES_PATH, X)
    np.save(LABELS_PATH, y)

    print(f"[INFO] Extraction done — {len(features)} OK, {skipped} skipped.")
    print(f"[INFO] Features saved to {FEATURES_PATH}")
    print(f"[INFO] Labels  saved to {LABELS_PATH}")

    return X, y


def train(X: np.ndarray, y: np.ndarray):
    """Split, scale, train SVM, evaluate, and persist artefacts."""

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print(f"\n[INFO] Training SVM (RBF, C=10) on {len(X_train)} samples …")
    model = SVC(kernel="rbf", C=10, gamma="scale")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Build target names in class-ID order for the report
    unique_ids = sorted(set(y_test))
    target_names = [CLASS_LABELS.get(i, str(i)) for i in unique_ids]

    print("\n── Classification Report (test set) ─────────────────────")
    print(classification_report(y_test, y_pred, target_names=target_names))

    # Save artefacts
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print(f"[INFO] Model  saved → {MODEL_PATH}")
    print(f"[INFO] Scaler saved → {SCALER_PATH}")


# ── entry point ──────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Train an SVM on UrbanSound8K MFCC features."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-extract features even if cached .npy files exist.",
    )
    args = parser.parse_args()

    X, y = extract_all_features(force=args.force)
    train(X, y)


if __name__ == "__main__":
    main()