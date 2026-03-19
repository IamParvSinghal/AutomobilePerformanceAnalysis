import type { FeatureImportanceEntry } from "../types";

interface FeatureImportanceChartProps {
  featureImportance: FeatureImportanceEntry[];
}

export function FeatureImportanceChart({
  featureImportance,
}: FeatureImportanceChartProps) {
  const topFeatures = featureImportance.slice(0, 6);
  const maxImportance = Math.max(...topFeatures.map((item) => item.importance_mean), 0.0001);

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <div className="eyebrow">Model insight</div>
          <h2>Permutation feature importance</h2>
        </div>
        <p>Higher scores indicate larger degradation in RMSE when that feature is shuffled.</p>
      </div>
      <div className="importance-list">
        {topFeatures.map((item) => (
          <div key={item.feature} className="importance-item">
            <div className="importance-row">
              <span>{item.feature}</span>
              <strong>{item.importance_mean.toFixed(3)}</strong>
            </div>
            <div className="importance-bar-shell">
              <div
                className="importance-bar-fill"
                style={{ width: `${(item.importance_mean / maxImportance) * 100}%` }}
              />
            </div>
            <span className="importance-std">± {item.importance_std.toFixed(3)}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

