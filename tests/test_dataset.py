from auto_performance.dataset import load_modeling_dataset


def test_dataset_is_clean_and_model_ready() -> None:
    df = load_modeling_dataset()

    assert len(df) == 392
    assert df["horsepower"].isna().sum() == 0
    assert set(df["origin"].unique()) == {"usa", "europe", "japan"}
    assert {"mpg", "model_year", "car_name"}.issubset(df.columns)

