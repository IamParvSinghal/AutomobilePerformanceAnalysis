from fastapi.testclient import TestClient

from auto_performance.api.app import app


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "ok"


def test_prediction_endpoint() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={
                "cylinders": 4,
                "displacement": 120.0,
                "horsepower": 95.0,
                "weight": 2300.0,
                "acceleration": 15.0,
                "model_year": 79,
                "origin": "japan",
            },
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["predicted_mpg"] > 0
