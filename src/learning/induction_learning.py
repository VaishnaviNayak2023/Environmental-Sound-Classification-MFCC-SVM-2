import numpy as np
import os
import sys
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.preprocessing.load_audio import load_audio
from src.preprocessing.preprocess_audio import normalize_audio
from src.preprocessing.feature_extraction import extract_features


def train_model(config):
    import pandas as pd

    metadata = pd.read_csv(config["metadata_path"])

    features = []
    labels = []

    for _, row in metadata.iterrows():
        fold = f"fold{row['fold']}"
        file_name = row["slice_file_name"]
        label = row["classID"]   # numeric class id
        file_path = os.path.join(config["dataset_audio_path"], fold, file_name)

        try:
            signal, sr = load_audio(file_path, config["sample_rate"])
            signal = normalize_audio(signal)
            feat = extract_features(signal, sr, config["mfcc_features"])
            features.append(feat)
            labels.append(label)
        except Exception as e:
            print(f"Skipping {file_path}: {e}")
            continue

    X = np.array(features)
    y = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = SVC(kernel="rbf", C=10, gamma="scale")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    model_path = config["model_output"]
    os.makedirs(os.path.dirname(os.path.abspath(model_path)), exist_ok=True)
    joblib.dump(model, model_path)

    # Derive scaler path alongside the model
    scaler_path = model_path.replace(".pkl", "_scaler.pkl")
    joblib.dump(scaler, scaler_path)

    print(f"Model saved to:  {model_path}")
    print(f"Scaler saved to: {scaler_path}")
