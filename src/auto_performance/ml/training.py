from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline

from auto_performance.config import (
    ARTIFACTS_DIR,
    CATEGORICAL_FEATURES,
    FEATURE_IMPORTANCE_PATH,
    METADATA_PATH,
    MODEL_ARTIFACT_PATH,
    MODEL_CARD_PATH,
    MODEL_FEATURES,
    MODEL_VERSION,
    PROCESSED_DATA_PATH,
    RANDOM_STATE,
    TARGET_COLUMN,
    TEST_SIZE,
)
from auto_performance.dataset import (
    dataset_summary,
    load_modeling_dataset,
    load_raw_dataset,
    save_processed_dataset,
)
from auto_performance.ml.pipeline import ModelCandidate, build_candidates


@dataclass(frozen=True)
class CandidateScore:
    name: str
    description: str
    cv_rmse_mean: float
    cv_mae_mean: float
    cv_r2_mean: float


@dataclass(frozen=True)
class TrainingResult:
    selected_model: str
    test_rmse: float
    test_mae: float
    test_r2: float
    candidate_scores: list[CandidateScore]
    feature_importance: list[dict[str, float]]


def evaluate_candidates(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    candidates: list[ModelCandidate],
) -> list[CandidateScore]:
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    scoring = {
        "rmse": "neg_root_mean_squared_error",
        "mae": "neg_mean_absolute_error",
        "r2": "r2",
    }

    results: list[CandidateScore] = []
    for candidate in candidates:
        pipeline = candidate.build_pipeline()
        scores = cross_validate(
            pipeline,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            n_jobs=1,
        )
        results.append(
            CandidateScore(
                name=candidate.name,
                description=candidate.description,
                cv_rmse_mean=float(-scores["test_rmse"].mean()),
                cv_mae_mean=float(-scores["test_mae"].mean()),
                cv_r2_mean=float(scores["test_r2"].mean()),
            )
        )

    return sorted(results, key=lambda item: (item.cv_rmse_mean, -item.cv_r2_mean))


def select_candidate(
    candidates: list[ModelCandidate],
    scores: list[CandidateScore],
    preferred_model: str | None = None,
) -> ModelCandidate:
    if preferred_model is not None:
        return next(candidate for candidate in candidates if candidate.name == preferred_model)

    best_name = scores[0].name
    return next(candidate for candidate in candidates if candidate.name == best_name)


def compute_feature_importance(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> list[dict[str, float]]:
    importance = permutation_importance(
        model,
        X_test,
        y_test,
        scoring="neg_root_mean_squared_error",
        n_repeats=20,
        random_state=RANDOM_STATE,
        n_jobs=1,
    )
    ranked = sorted(
        zip(X_test.columns, importance.importances_mean, importance.importances_std, strict=True),
        key=lambda item: item[1],
        reverse=True,
    )
    return [
        {
            "feature": feature,
            "importance_mean": float(mean_value),
            "importance_std": float(std_value),
        }
        for feature, mean_value, std_value in ranked
    ]


def build_metadata(
    *,
    df: pd.DataFrame,
    raw_df: pd.DataFrame,
    result: TrainingResult,
    feature_ranges: dict[str, dict[str, float | str]],
) -> dict[str, Any]:
    summary = dataset_summary(raw_df, df)
    example_record = df[MODEL_FEATURES].iloc[0].to_dict()
    return {
        "model_version": MODEL_VERSION,
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "selected_model": result.selected_model,
        "problem_type": "regression",
        "target": TARGET_COLUMN,
        "dataset": {
            **asdict(summary),
            "processed_path": str(PROCESSED_DATA_PATH.relative_to(Path.cwd())),
        },
        "features": {
            "numeric": MODEL_FEATURES[:-1],
            "categorical": CATEGORICAL_FEATURES,
            "feature_ranges": feature_ranges,
        },
        "evaluation": {
            "test_rmse": result.test_rmse,
            "test_mae": result.test_mae,
            "test_r2": result.test_r2,
            "candidate_scores": [asdict(score) for score in result.candidate_scores],
        },
        "example_request": example_record,
    }


def feature_ranges(df: pd.DataFrame) -> dict[str, dict[str, float | str]]:
    ranges: dict[str, dict[str, float | str]] = {}
    for column in MODEL_FEATURES:
        if column in CATEGORICAL_FEATURES:
            ranges[column] = {"values": sorted(df[column].unique().tolist())}
        else:
            ranges[column] = {
                "min": float(df[column].min()),
                "max": float(df[column].max()),
                "mean": float(df[column].mean()),
            }
    return ranges


def write_model_card(result: TrainingResult, metadata: dict[str, Any], path: Path) -> None:
    candidate_rows = "\n".join(
        [
            (
                f"| {score.name} | {score.cv_rmse_mean:.3f} | {score.cv_mae_mean:.3f} "
                f"| {score.cv_r2_mean:.3f} |"
            )
            for score in result.candidate_scores
        ]
    )
    top_features = "\n".join(
        [
            f"- {item['feature']}: {item['importance_mean']:.4f}"
            for item in result.feature_importance[:5]
        ]
    )
    lines = [
        "# Model Card",
        "",
        f"- Selected model: `{result.selected_model}`",
        f"- Test RMSE: `{result.test_rmse:.3f}`",
        f"- Test MAE: `{result.test_mae:.3f}`",
        f"- Test R^2: `{result.test_r2:.3f}`",
        "",
        "## Candidate Benchmark",
        "",
        "| Model | CV RMSE | CV MAE | CV R^2 |",
        "| --- | ---: | ---: | ---: |",
        candidate_rows,
        "",
        "## Top Permutation Features",
        "",
        top_features,
        "",
        "## Operational Notes",
        "",
        (
            "- Dataset is stored locally in `data/raw/auto-mpg.data` to avoid "
            "runtime network dependencies."
        ),
        "- Preprocessing is fit only on the training folds and train split to eliminate leakage.",
        "- API contracts and frontend forms are aligned to the persisted metadata schema.",
        "",
        "## Example Request",
        "",
        "```json",
        json.dumps(metadata["example_request"], indent=2),
        "```",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def train_and_persist(
    *,
    artifact_dir: Path = ARTIFACTS_DIR,
    processed_data_path: Path = PROCESSED_DATA_PATH,
    preferred_model: str | None = None,
) -> TrainingResult:
    raw_df = load_raw_dataset()
    df = load_modeling_dataset()
    save_processed_dataset(df, processed_data_path)

    X = df[MODEL_FEATURES].copy()
    y = df[TARGET_COLUMN].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    candidates = build_candidates()
    scores = evaluate_candidates(X_train, y_train, candidates)
    selected_candidate = select_candidate(candidates, scores, preferred_model=preferred_model)

    model = selected_candidate.build_pipeline()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    mae = float(mean_absolute_error(y_test, predictions))
    r2 = float(r2_score(y_test, predictions))
    importance = compute_feature_importance(model, X_test, y_test)

    result = TrainingResult(
        selected_model=selected_candidate.name,
        test_rmse=rmse,
        test_mae=mae,
        test_r2=r2,
        candidate_scores=scores,
        feature_importance=importance,
    )

    artifact_dir.mkdir(parents=True, exist_ok=True)
    feature_range_map = feature_ranges(df)
    metadata = build_metadata(
        df=df,
        raw_df=raw_df,
        result=result,
        feature_ranges=feature_range_map,
    )

    joblib.dump(model, artifact_dir / MODEL_ARTIFACT_PATH.name)
    (artifact_dir / METADATA_PATH.name).write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (artifact_dir / FEATURE_IMPORTANCE_PATH.name).write_text(
        json.dumps(importance, indent=2),
        encoding="utf-8",
    )
    write_model_card(result, metadata, artifact_dir / MODEL_CARD_PATH.name)

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and persist the fuel efficiency model.")
    parser.add_argument(
        "--preferred-model",
        choices=[candidate.name for candidate in build_candidates()],
        default=None,
        help="Force a specific candidate instead of auto-selecting the best CV result.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = train_and_persist(preferred_model=args.preferred_model)
    print(json.dumps(asdict(result), indent=2))


if __name__ == "__main__":
    main()
