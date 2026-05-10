from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import sys

# Ensure the project root is on the path so predict.py is importable
# regardless of which directory uvicorn is launched from
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from predict import predict_audio   # fixed: was predict_audio (function now exists)

app = FastAPI(title="Environmental Sound Classifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store temp files relative to this file, not the cwd
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict_audio(file_path)

    # Clean up the temp file after inference
    os.remove(file_path)

    return {"predicted_class": result}