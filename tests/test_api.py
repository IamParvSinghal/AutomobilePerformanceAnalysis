from fastapi.testclient import TestClient

from auto_performance.api.app import app


def test_root_endpoint_exposes_navigation_links() -> None:
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        payload = response.json()
        assert payload["message"] == "Automobile Performance Analysis API"
        assert payload["docs"] == "/docs"
        assert payload["model_info"] == "/api/v1/model-info"


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "ok"


def test_docs_endpoint_returns_custom_html() -> None:
    with TestClient(app) as client:
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Automobile Performance Analysis API" in response.text


def test_model_info_endpoint_returns_metadata_bundle() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/model-info")
        assert response.status_code == 200
        payload = response.json()
        assert payload["metadata"]["selected_model"]
        assert payload["metadata"]["evaluation"]["candidate_scores"]
        assert payload["feature_importance"] is not None


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


def test_batch_prediction_endpoint_returns_multiple_predictions() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict/batch",
            json={
                "records": [
                    {
                        "cylinders": 4,
                        "displacement": 120.0,
                        "horsepower": 95.0,
                        "weight": 2300.0,
                        "acceleration": 15.0,
                        "model_year": 79,
                        "origin": "japan",
                    },
                    {
                        "cylinders": 6,
                        "displacement": 200.0,
                        "horsepower": 110.0,
                        "weight": 3000.0,
                        "acceleration": 14.0,
                        "model_year": 76,
                        "origin": "usa",
                    },
                ]
            },
        )
        assert response.status_code == 200
        payload = response.json()
        assert len(payload["predictions"]) == 2
        assert all(item["predicted_mpg"] > 0 for item in payload["predictions"])


def test_prediction_endpoint_rejects_invalid_payload() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/predict",
            json={
                "cylinders": 4,
                "displacement": 120.0,
                "horsepower": 95.0,
                "weight": 2300.0,
                "acceleration": 15.0,
                "model_year": 99,
                "origin": "japan",
            },
        )
        assert response.status_code == 422
