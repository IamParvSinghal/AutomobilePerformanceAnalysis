from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auto_performance.api.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    HealthResponse,
    ModelInfoResponse,
    PredictionRequest,
    PredictionResponse,
)
from auto_performance.api.service import ModelService
from auto_performance.config import API_PREFIX, APP_NAME


def cors_origins() -> list[str]:
    raw = os.getenv("AUTO_PERFORMANCE_CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.model_service = ModelService.load()
    yield


app = FastAPI(title=APP_NAME, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_model_service() -> ModelService:
    return app.state.model_service


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {
        "message": "Automobile Performance Analysis API",
        "docs": "/docs",
        "model_info": f"{API_PREFIX}/model-info",
    }


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health(service: ModelService = Depends(get_model_service)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        selected_model=service.metadata["selected_model"],
        model_version=service.metadata["model_version"],
    )


@app.get(f"{API_PREFIX}/model-info", response_model=ModelInfoResponse, tags=["model"])
def model_info(service: ModelService = Depends(get_model_service)) -> ModelInfoResponse:
    return ModelInfoResponse(
        metadata=service.metadata,
        feature_importance=service.feature_importance,
    )


@app.post(f"{API_PREFIX}/predict", response_model=PredictionResponse, tags=["predictions"])
def predict(
    request: PredictionRequest,
    service: ModelService = Depends(get_model_service),
) -> PredictionResponse:
    prediction = service.predict_one(request.model_dump())
    return PredictionResponse(
        predicted_mpg=round(prediction, 3),
        selected_model=service.metadata["selected_model"],
        model_version=service.metadata["model_version"],
    )


@app.post(
    f"{API_PREFIX}/predict/batch",
    response_model=BatchPredictionResponse,
    tags=["predictions"],
)
def predict_batch(
    request: BatchPredictionRequest,
    service: ModelService = Depends(get_model_service),
) -> BatchPredictionResponse:
    predictions = service.predict_many([record.model_dump() for record in request.records])
    return BatchPredictionResponse(
        predictions=[
            PredictionResponse(
                predicted_mpg=round(prediction, 3),
                selected_model=service.metadata["selected_model"],
                model_version=service.metadata["model_version"],
            )
            for prediction in predictions
        ]
    )
