from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Origin = Literal["usa", "europe", "japan"]


class PredictionRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    cylinders: int = Field(..., ge=3, le=12)
    displacement: float = Field(..., gt=0)
    horsepower: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    acceleration: float = Field(..., gt=0)
    model_year: int = Field(..., ge=70, le=82)
    origin: Origin


class BatchPredictionRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    records: list[PredictionRequest] = Field(..., min_length=1, max_length=100)


class PredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    predicted_mpg: float
    selected_model: str
    model_version: str


class BatchPredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    predictions: list[PredictionResponse]


class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    status: Literal["ok"]
    selected_model: str
    model_version: str


class ModelInfoResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    metadata: dict[str, Any]
    feature_importance: list[dict[str, float | str]]
