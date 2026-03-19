from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd

from auto_performance.config import FEATURE_IMPORTANCE_PATH, METADATA_PATH, MODEL_ARTIFACT_PATH
from auto_performance.ml.training import train_and_persist


@dataclass
class ModelService:
    model: object
    metadata: dict
    feature_importance: list[dict]

    @classmethod
    def load(
        cls,
        *,
        model_path: Path = MODEL_ARTIFACT_PATH,
        metadata_path: Path = METADATA_PATH,
        feature_importance_path: Path = FEATURE_IMPORTANCE_PATH,
    ) -> ModelService:
        missing_paths = [
            str(path)
            for path in (model_path, metadata_path, feature_importance_path)
            if not path.exists()
        ]
        if missing_paths:
            train_and_persist()

        model = joblib.load(model_path)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        feature_importance = json.loads(feature_importance_path.read_text(encoding="utf-8"))
        return cls(model=model, metadata=metadata, feature_importance=feature_importance)

    def predict_one(self, record: dict) -> float:
        frame = pd.DataFrame([record])
        prediction = self.model.predict(frame)[0]
        return float(prediction)

    def predict_many(self, records: list[dict]) -> list[float]:
        frame = pd.DataFrame(records)
        predictions = self.model.predict(frame)
        return [float(value) for value in predictions]
