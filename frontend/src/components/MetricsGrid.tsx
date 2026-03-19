import type { ModelMetadata } from "../types";

interface MetricsGridProps {
  metadata: ModelMetadata;
}

function metricValue(value: number, digits = 3): string {
  return value.toFixed(digits);
}

export function MetricsGrid({ metadata }: MetricsGridProps) {
  const { evaluation, dataset } = metadata;

  return (
    <section className="metrics-grid">
      <article className="metric-card">
        <span className="metric-label">Test R²</span>
        <strong>{metricValue(evaluation.test_r2)}</strong>
        <p>Holdout explanatory power after cross-validated model selection.</p>
      </article>
      <article className="metric-card">
        <span className="metric-label">Test RMSE</span>
        <strong>{metricValue(evaluation.test_rmse)}</strong>
        <p>Root mean squared error in MPG on unseen records.</p>
      </article>
      <article className="metric-card">
        <span className="metric-label">Test MAE</span>
        <strong>{metricValue(evaluation.test_mae)}</strong>
        <p>Average absolute prediction error across the holdout split.</p>
      </article>
      <article className="metric-card">
        <span className="metric-label">Rows dropped</span>
        <strong>{dataset.rows_removed}</strong>
        <p>Rows removed during cleaning because horsepower was missing.</p>
      </article>
    </section>
  );
}

