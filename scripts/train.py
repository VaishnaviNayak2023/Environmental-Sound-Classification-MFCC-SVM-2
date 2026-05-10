import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.helpers import load_config
from src.learning.induction_learning import train_model

config = load_config()
train_model(config)