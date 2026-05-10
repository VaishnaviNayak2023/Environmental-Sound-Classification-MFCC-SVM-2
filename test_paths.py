import pandas as pd
from config import METADATA_PATH, DATASET_PATH  # fixed: was METADATA_FILE (undefined)
import os

print("CSV exists:         ", os.path.exists(METADATA_PATH))
print("Audio folder exists:", os.path.exists(DATASET_PATH))

# Try reading first 5 rows
metadata = pd.read_csv(METADATA_PATH)
print(metadata.head())