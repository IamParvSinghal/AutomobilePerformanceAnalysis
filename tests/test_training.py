import shutil
from pathlib import Path

from auto_performance.ml.training import train_and_persist


def test_training_writes_expected_artifacts() -> None:
    output_dir = Path(".tmp/test-training-output")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = train_and_persist(
        artifact_dir=output_dir,
        processed_data_path=output_dir / "processed.csv",
    )

    assert result.test_r2 > 0.7
    assert (output_dir / "model.joblib").exists()
    assert (output_dir / "model_metadata.json").exists()
    assert (output_dir / "feature_importance.json").exists()
    assert (output_dir / "model_card.md").exists()
