import os

CONFIG_FILE_PATH = os.path.join("config", "config.yaml")

ARTIFACT_DIR = "artifacts"

LOG_DIR = "logs"

RAW_DATA_DIR = os.path.join(ARTIFACT_DIR, "raw_data")

PROCESSED_DATA_DIR = os.path.join(
    ARTIFACT_DIR,
    "processed_data"
)