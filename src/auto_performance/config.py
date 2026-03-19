from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "Automobile Performance Analysis Platform"
MODEL_VERSION = "1.0.0"
API_PREFIX = "/api/v1"


def _discover_root_dir() -> Path:
    env_root = os.getenv("AUTO_PERFORMANCE_ROOT")
    candidates: list[Path] = []

    if env_root:
        candidates.append(Path(env_root).resolve())

    candidates.append(Path.cwd().resolve())
    candidates.extend(Path(__file__).resolve().parents)

    for candidate in candidates:
        data_path = candidate / "data" / "raw" / "auto-mpg.data"
        if data_path.exists():
            return candidate
        if (candidate / "pyproject.toml").exists():
            return candidate

    return Path.cwd().resolve()


ROOT_DIR = _discover_root_dir()
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "auto-mpg.data"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "auto_mpg_clean.csv"
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
MODEL_ARTIFACT_PATH = ARTIFACTS_DIR / "model.joblib"
METADATA_PATH = ARTIFACTS_DIR / "model_metadata.json"
FEATURE_IMPORTANCE_PATH = ARTIFACTS_DIR / "feature_importance.json"
MODEL_CARD_PATH = ARTIFACTS_DIR / "model_card.md"

TARGET_COLUMN = "mpg"
RAW_COLUMNS = [
    "mpg",
    "cylinders",
    "displacement",
    "horsepower",
    "weight",
    "acceleration",
    "model year",
    "origin",
    "car name",
]

RENAME_MAP = {
    "model year": "model_year",
    "car name": "car_name",
}

NUMERIC_FEATURES = [
    "cylinders",
    "displacement",
    "horsepower",
    "weight",
    "acceleration",
    "model_year",
]
CATEGORICAL_FEATURES = ["origin"]
MODEL_FEATURES = [*NUMERIC_FEATURES, *CATEGORICAL_FEATURES]

ORIGIN_LABELS = {
    1: "usa",
    2: "europe",
    3: "japan",
}

RANDOM_STATE = 42
TEST_SIZE = 0.2
