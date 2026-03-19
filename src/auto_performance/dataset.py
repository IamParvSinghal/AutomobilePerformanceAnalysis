from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from auto_performance.config import (
    MODEL_FEATURES,
    NUMERIC_FEATURES,
    ORIGIN_LABELS,
    PROCESSED_DATA_PATH,
    RAW_COLUMNS,
    RAW_DATA_PATH,
    RENAME_MAP,
    TARGET_COLUMN,
)


@dataclass(frozen=True)
class DatasetSummary:
    total_rows: int
    rows_after_cleaning: int
    rows_removed: int
    target_mean: float
    target_std: float


def load_raw_dataset(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    records: list[list[str]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=8)
        if len(parts) != len(RAW_COLUMNS):
            raise ValueError(f"Unable to parse dataset row: {raw_line}")
        parts[-1] = parts[-1].strip('"')
        records.append(parts)

    return pd.DataFrame(records, columns=RAW_COLUMNS)


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.rename(columns=RENAME_MAP).copy()
    for column in [TARGET_COLUMN, *NUMERIC_FEATURES]:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    cleaned["origin"] = pd.to_numeric(cleaned["origin"], errors="coerce").map(ORIGIN_LABELS)
    cleaned = cleaned.dropna(subset=[TARGET_COLUMN, *MODEL_FEATURES]).reset_index(drop=True)
    cleaned["cylinders"] = cleaned["cylinders"].astype(int)
    cleaned["model_year"] = cleaned["model_year"].astype(int)
    return cleaned


def load_modeling_dataset(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    return clean_dataset(load_raw_dataset(path))


def dataset_summary(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> DatasetSummary:
    return DatasetSummary(
        total_rows=len(df_raw),
        rows_after_cleaning=len(df_clean),
        rows_removed=len(df_raw) - len(df_clean),
        target_mean=float(df_clean[TARGET_COLUMN].mean()),
        target_std=float(df_clean[TARGET_COLUMN].std()),
    )


def save_processed_dataset(df: pd.DataFrame, path: Path = PROCESSED_DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
