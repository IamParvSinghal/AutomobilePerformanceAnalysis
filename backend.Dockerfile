FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .
RUN python -m auto_performance.ml.training

EXPOSE 8000

CMD ["uvicorn", "auto_performance.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
