import yaml
import os

# Project root is two levels up from this file (src/utils/helpers.py → project root)
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_config(path=None):
    if path is None:
        path = os.path.join(_PROJECT_ROOT, "config", "config.yaml")
    with open(path, "r") as file:
        config = yaml.safe_load(file)

    # Resolve relative paths in the config to absolute paths from the project root
    for key in ("dataset_audio_path", "metadata_path", "model_output"):
        if key in config and not os.path.isabs(config[key]):
            config[key] = os.path.join(_PROJECT_ROOT, config[key])

    return config