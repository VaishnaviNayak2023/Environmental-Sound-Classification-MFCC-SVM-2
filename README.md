# 🔊 Environmental Sound Classification

AI-powered urban sound classification using **SVM** (Support Vector Machine) trained on **MFCC** features from the [UrbanSound8K](https://urbansounddataset.weebly.com/urbansound8k.html) dataset.

## Sound Classes (10)

| ID | Class             | Emoji |
|----|-------------------|-------|
| 0  | Air Conditioner   | ❄️    |
| 1  | Car Horn          | 🚗    |
| 2  | Children Playing  | 🧒    |
| 3  | Dog Bark          | 🐕    |
| 4  | Drilling          | 🔧    |
| 5  | Engine Idling     | ⚙️    |
| 6  | Gun Shot          | 💥    |
| 7  | Jackhammer        | 🔨    |
| 8  | Siren             | 🚨    |
| 9  | Street Music      | 🎵    |

## Features (86-dimensional vector)

Each audio file is converted into an **86-feature** vector:

- **40** Mean MFCCs (Mel-Frequency Cepstral Coefficients)
- **40** Mean Δ-MFCCs (first-order deltas)
- **6** Mean Tonnetz (tonal centroid features)

## Project Structure

```
├── config.py                    # Paths & hyperparameters
├── config/config.yaml           # YAML config for src/ pipeline
├── extract_features.py          # Build dataset (86-feature vectors)
├── train_model.py               # Train SVM + StandardScaler
├── evaluate.py                  # Evaluate on held-out test set
├── predict.py                   # Single-file prediction
├── requirements.txt             # Python dependencies
│
├── app/
│   └── api.py                   # FastAPI backend (/predict endpoint)
│
├── src/                         # Modular source package
│   ├── preprocessing/           # Audio loading, normalization, feature extraction
│   ├── learning/                # SVM training (induction_learning.py)
│   ├── evaluation/              # Model evaluation
│   ├── knowledge/               # Sound frame definitions
│   ├── search/                  # BFS, Best-First, Hill Climbing
│   └── utils/                   # Config loader helpers
│
├── scripts/
│   ├── train.py                 # Train via src/ pipeline
│   └── predict.py               # Predict via src/ pipeline
│
├── models/
│   ├── trained_model.pkl        # Trained SVM model
│   └── trained_model_scaler.pkl # StandardScaler
│
├── data/UrbanSound8K/           # Dataset (audio + metadata)
│
└── frontend/                    # React + Vite + Tailwind UI
    └── src/
        ├── pages/Home.jsx       # Upload & classify interface
        ├── pages/Login.jsx      # Login page
        ├── pages/SignUp.jsx     # Registration page
        └── components/Navbar.jsx
```

## Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Backend API

```bash
python -m uvicorn app.api:app --host 0.0.0.0 --port 8000
```

The API exposes a single endpoint:

```
POST /predict  →  { "predicted_class": "dog_bark" }
```

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### 4. Classify a Sound

Upload a `.wav` file through the web UI or use the API directly:

```bash
# CLI
python predict.py path/to/audio.wav

# API (curl)
curl -X POST http://localhost:8000/predict \
  -F "file=@path/to/audio.wav"
```

## Retraining the Model

If you have the UrbanSound8K audio files in `data/UrbanSound8K/audio/`:

```bash
# Step 1: Extract 86-dimensional features from all audio files
python extract_features.py

# Step 2: Train the SVM model
python train_model.py

# Step 3: Evaluate on the test set
python evaluate.py
```

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| ML Model | scikit-learn SVM (RBF kernel, C=10) |
| Features | librosa (MFCC, delta, tonnetz)      |
| Backend  | FastAPI + Uvicorn                   |
| Frontend | React 19 + Vite + Tailwind CSS      |
