import os

# Absolute base path — config.py lives at the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dataset paths (relative to project root)
DATASET_PATH = os.path.join(BASE_DIR, "data", "UrbanSound8K", "audio")
METADATA_PATH = os.path.join(BASE_DIR, "data", "UrbanSound8K", "metadata", "UrbanSound8K.csv")

# Feature storage
FEATURES_PATH = os.path.join(BASE_DIR, "X_features.npy")
LABELS_PATH = os.path.join(BASE_DIR, "y_labels.npy")

# Model paths — must match the filenames produced by train_model.py
MODEL_PATH = os.path.join(BASE_DIR, "models", "trained_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "trained_model_scaler.pkl")

SAMPLE_RATE = 22050
N_MFCC = 40
TEST_SIZE = 0.2
RANDOM_STATE = 42