import type { CandidateScore } from "../types";

interface BenchmarkTableProps {
  candidates: CandidateScore[];
  selectedModel: string;
}

export function BenchmarkTable({ candidates, selectedModel }: BenchmarkTableProps) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <div className="eyebrow">Benchmarking</div>
          <h2>Cross-validated model comparison</h2>
        </div>
        <p>
          The production model is selected from multiple candidates using the same evaluation
          workflow.
        </p>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Model</th>
              <th>Description</th>
              <th>CV RMSE</th>
              <th>CV MAE</th>
              <th>CV R^2</th>
            </tr>
          </thead>
          <tbody>
            {candidates.map((candidate) => (
              <tr
                key={candidate.name}
                className={candidate.name === selectedModel ? "selected-row" : undefined}
              >
                <td>{candidate.name}</td>
                <td>{candidate.description}</td>
                <td>{candidate.cv_rmse_mean.toFixed(3)}</td>
                <td>{candidate.cv_mae_mean.toFixed(3)}</td>
                <td>{candidate.cv_r2_mean.toFixed(3)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
