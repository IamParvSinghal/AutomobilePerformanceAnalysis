# Automobile Performance Analysis

Production-grade fuel efficiency prediction platform built from the UCI Auto MPG dataset. The project combines a reproducible machine learning pipeline, a typed API, a React + TypeScript dashboard, and a Dockerized local deployment path.

## Project structure

```text
.
|-- artifacts/                  # Generated model artifacts and model card
|-- data/
|   |-- raw/auto-mpg.data       # Vendored source dataset
|   `-- processed/              # Generated cleaned dataset
|-- frontend/                   # React + TypeScript client
|-- src/auto_performance/       # Backend package, training pipeline, API
|-- tests/                      # Backend and API tests
|-- backend.Dockerfile
|-- frontend.Dockerfile
`-- docker-compose.yml
```

## Backend architecture

- `src/auto_performance/dataset.py`
  - Loads the raw dataset from disk, normalizes schema, cleans missing horsepower values, and maps origin codes to labels.
- `src/auto_performance/ml/pipeline.py`
  - Defines three candidate regressors:
    - `ridge_pca`: linear baseline with PCA inside the pipeline
    - `random_forest`: nonlinear ensemble model
    - `gradient_boosting`: boosted tree model for tabular regression
- `src/auto_performance/ml/training.py`
  - Benchmarks candidates with cross-validation, selects the best model, evaluates on a holdout split, computes permutation importance, and writes artifacts.
- `src/auto_performance/api/app.py`
  - Serves health checks, model metadata, single prediction, and batch prediction endpoints.
  - Automatically bootstraps model artifacts on first startup if they do not already exist.

## Frontend experience

The React client surfaces:

- live vehicle scoring with miles/kilometers input support
- cross-validated candidate comparison
- permutation feature importance
- an interactive scoring form powered by artifact metadata

## Local development

### Backend

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
python -m auto_performance.ml.training
uvicorn auto_performance.api.app:app --reload
```

### Frontend

This repository is configured for `pnpm` through Corepack:

```bash
cd frontend
corepack enable
corepack prepare pnpm@9.15.4 --activate
pnpm install
pnpm dev
```

The Vite dev server proxies `/api` and `/health` to the backend on port `8000`.

## Docker workflow

```bash
docker compose up --build
```

Services:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Training outputs

Running `python -m auto_performance.ml.training` writes:

- `artifacts/model.joblib`
- `artifacts/model_metadata.json`
- `artifacts/feature_importance.json`
- `artifacts/model_card.md`
- `data/processed/auto_mpg_clean.csv`

## Quality bar

This project is designed to present well in a senior-engineering review:

- deterministic local dataset instead of runtime downloads
- explicit train/test separation and cross-validation
- serialized metadata for UI and API alignment
- typed contracts across backend and frontend
- containerized deployment for reproducible demos
- tests covering data loading, training output generation, and API inference
