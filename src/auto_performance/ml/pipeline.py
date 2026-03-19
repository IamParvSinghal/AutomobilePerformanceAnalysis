from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from auto_performance.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, RANDOM_STATE


@dataclass(frozen=True)
class ModelCandidate:
    name: str
    description: str
    build_pipeline: Callable[[], Pipeline]


def build_ridge_pca_pipeline() -> Pipeline:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("pca", PCA(n_components=0.95, svd_solver="full")),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", Ridge(alpha=1.0)),
        ]
    )


def build_random_forest_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", SimpleImputer(strategy="median"), NUMERIC_FEATURES),
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=500,
                    min_samples_leaf=2,
                    random_state=RANDOM_STATE,
                    n_jobs=1,
                ),
            ),
        ]
    )


def build_gradient_boosting_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", SimpleImputer(strategy="median"), NUMERIC_FEATURES),
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "encoder",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                        ),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
        ],
        sparse_threshold=0.0,
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "regressor",
                GradientBoostingRegressor(
                    learning_rate=0.05,
                    max_depth=3,
                    min_samples_leaf=3,
                    n_estimators=250,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def build_candidates() -> list[ModelCandidate]:
    return [
        ModelCandidate(
            name="ridge_pca",
            description="Leak-free PCA baseline for dimensionality-aware regression.",
            build_pipeline=build_ridge_pca_pipeline,
        ),
        ModelCandidate(
            name="random_forest",
            description="Tree ensemble that captures nonlinear feature interactions.",
            build_pipeline=build_random_forest_pipeline,
        ),
        ModelCandidate(
            name="gradient_boosting",
            description="Boosted decision trees optimized for tabular regression.",
            build_pipeline=build_gradient_boosting_pipeline,
        ),
    ]
