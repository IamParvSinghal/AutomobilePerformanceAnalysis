from __future__ import annotations

from fastapi.responses import HTMLResponse


def render_docs_page() -> HTMLResponse:
    return HTMLResponse(
        """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Automobile Performance Analysis API Docs</title>
    <style>
      :root {
        color-scheme: light;
        --bg: #f3ede2;
        --panel: rgba(255, 250, 242, 0.9);
        --panel-strong: #fff8ef;
        --text: #16222d;
        --muted: #52606c;
        --accent: #264653;
        --accent-soft: #e5efe8;
        --border: rgba(22, 34, 45, 0.09);
        --shadow: 0 18px 42px rgba(22, 34, 45, 0.08);
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        font-family: "Aptos", "Segoe UI", sans-serif;
        background:
          radial-gradient(circle at top left, rgba(244, 162, 97, 0.2), transparent 28%),
          radial-gradient(circle at bottom right, rgba(38, 70, 83, 0.18), transparent 30%),
          linear-gradient(180deg, #f7f2e8 0%, var(--bg) 100%);
        color: var(--text);
        line-height: 1.55;
      }

      .page {
        width: min(1180px, calc(100% - 40px));
        margin: 32px auto 56px;
      }

      .hero,
      .section,
      .endpoint,
      .note {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: var(--shadow);
      }

      .hero {
        padding: 32px;
        margin-bottom: 20px;
      }

      .eyebrow {
        color: #b66a1e;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 12px;
      }

      h1, h2, h3 {
        font-family: "Bahnschrift", "Arial Narrow", sans-serif;
        margin: 0;
        letter-spacing: 0.01em;
      }

      h1 {
        font-size: clamp(2rem, 4vw, 3.4rem);
        line-height: 0.98;
      }

      h2 {
        font-size: 1.55rem;
        margin-bottom: 14px;
      }

      h3 {
        font-size: 1.08rem;
        margin-bottom: 10px;
      }

      p {
        margin: 0;
        color: var(--muted);
      }

      .hero p {
        margin-top: 14px;
        max-width: 820px;
        font-size: 1.02rem;
      }

      .section {
        padding: 24px 26px;
        margin-bottom: 18px;
      }

      .section-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 18px;
      }

      .mini-card {
        background: var(--panel-strong);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 18px 18px 16px;
      }

      .list {
        margin: 14px 0 0;
        padding-left: 18px;
        color: var(--muted);
      }

      .list li + li {
        margin-top: 8px;
      }

      .endpoint {
        padding: 20px 22px;
      }

      .endpoint + .endpoint {
        margin-top: 14px;
      }

      .endpoint-head {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 14px;
        flex-wrap: wrap;
      }

      .method {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 58px;
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        color: white;
        background: var(--accent);
      }

      .path {
        font-family: Consolas, monospace;
        font-size: 0.98rem;
        background: rgba(22, 34, 45, 0.06);
        border-radius: 10px;
        padding: 7px 10px;
      }

      .endpoint-grid {
        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        gap: 16px;
      }

      .block {
        background: var(--panel-strong);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 16px 16px 14px;
      }

      .block p + p {
        margin-top: 10px;
      }

      code,
      pre {
        font-family: Consolas, monospace;
      }

      pre {
        margin: 12px 0 0;
        padding: 14px;
        overflow-x: auto;
        border-radius: 16px;
        background: #152028;
        color: #f6f2e8;
        font-size: 0.9rem;
      }

      .tag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 14px;
      }

      .tag {
        padding: 8px 12px;
        border-radius: 999px;
        background: var(--accent-soft);
        color: #1f5a34;
        font-size: 0.9rem;
        font-weight: 600;
      }

      .note {
        padding: 18px 20px;
        margin-top: 18px;
      }

      .note strong {
        display: block;
        margin-bottom: 8px;
      }

      @media (max-width: 920px) {
        .section-grid,
        .endpoint-grid {
          grid-template-columns: 1fr;
        }

        .page {
          width: min(100% - 24px, 1180px);
          margin: 14px auto 28px;
        }

        .hero,
        .section,
        .endpoint,
        .note {
          border-radius: 18px;
        }
      }
    </style>
  </head>
  <body>
    <main class="page">
      <section class="hero">
        <div class="eyebrow">Backend Documentation</div>
        <h1>Automobile Performance Analysis API</h1>
        <p>
          This backend loads the trained MPG prediction model, exposes model metadata,
          and serves single or batch predictions to the frontend. This page is written
          as reviewer-facing documentation rather than an interactive API console.
        </p>
      </section>

      <section class="section">
        <h2>What The Backend Does</h2>
        <div class="section-grid">
          <div class="mini-card">
            <h3>Startup behavior</h3>
            <ul class="list">
              <li>Creates a FastAPI application with CORS enabled for the frontend.</li>
              <li>Loads a shared <code>ModelService</code> on startup.</li>
              <li>
                Reads the trained model artifact, metadata, and feature importance
                from <code>artifacts/</code>.
              </li>
              <li>If those files are missing, it runs the training pipeline to recreate them.</li>
            </ul>
          </div>
          <div class="mini-card">
            <h3>Runtime responsibility</h3>
            <ul class="list">
              <li>Returns health and model-status information.</li>
              <li>
                Returns model metadata used by the frontend to build forms and
                explanatory sections.
              </li>
              <li>Accepts vehicle data and returns an MPG prediction.</li>
              <li>Supports batch prediction for multiple vehicle records in one request.</li>
            </ul>
          </div>
        </div>
        <div class="tag-row">
          <span class="tag">Group: meta</span>
          <span class="tag">Group: model</span>
          <span class="tag">Group: predictions</span>
          <span class="tag">Primary format: JSON</span>
        </div>
      </section>

      <section class="section">
        <h2>How The API Is Grouped</h2>
        <div class="section-grid">
          <div class="mini-card">
            <h3><code>meta</code></h3>
            <p>Endpoints that confirm the API is alive and tell a reviewer where to look next.</p>
          </div>
          <div class="mini-card">
            <h3><code>model</code></h3>
            <p>
              Endpoints that describe the trained model, evaluation results,
              feature ranges, and feature importance.
            </p>
          </div>
          <div class="mini-card">
            <h3><code>predictions</code></h3>
            <p>
              Endpoints that accept vehicle features and return MPG predictions
              using the selected production model.
            </p>
          </div>
          <div class="mini-card">
            <h3><code>/docs</code></h3>
            <p>
              This page. It exists to explain the backend clearly without
              requiring Swagger or source inspection first.
            </p>
          </div>
        </div>
      </section>

      <section class="section">
        <h2>Endpoints</h2>

        <article class="endpoint">
          <div class="endpoint-head">
            <span class="method">GET</span>
            <span class="path">/</span>
          </div>
          <div class="endpoint-grid">
            <div class="block">
              <h3>Purpose</h3>
              <p>
                Simple root endpoint that identifies the backend and points to
                the main docs and model-info route.
              </p>
              <p><strong>Why it exists:</strong> Lightweight sanity check and service discovery.</p>
            </div>
            <div class="block">
              <h3>Response shape</h3>
              <pre>{
  "message": "Automobile Performance Analysis API",
  "docs": "/docs",
  "model_info": "/api/v1/model-info"
}</pre>
            </div>
          </div>
        </article>

        <article class="endpoint">
          <div class="endpoint-head">
            <span class="method">GET</span>
            <span class="path">/health</span>
          </div>
          <div class="endpoint-grid">
            <div class="block">
              <h3>Purpose</h3>
              <p>Confirms that the API is running and the model service loaded successfully.</p>
              <p>
                <strong>What it returns:</strong> backend health, selected model
                name, and model version.
              </p>
            </div>
            <div class="block">
              <h3>Response example</h3>
              <pre>{
  "status": "ok",
  "selected_model": "random_forest",
  "model_version": "1.0.0"
}</pre>
            </div>
          </div>
        </article>

        <article class="endpoint">
          <div class="endpoint-head">
            <span class="method">GET</span>
            <span class="path">/api/v1/model-info</span>
          </div>
          <div class="endpoint-grid">
            <div class="block">
              <h3>Purpose</h3>
              <p>
                Returns the descriptive information about the trained model.
                This is the main "explain the model" endpoint.
              </p>
              <p>
                <strong>What it includes:</strong> dataset stats, feature
                ranges, selected model, evaluation metrics, candidate benchmark
                scores, example request payload, and permutation feature
                importance.
              </p>
            </div>
            <div class="block">
              <h3>Why it matters</h3>
              <p>
                The frontend uses this endpoint to build its form, display
                benchmark context, and show model insight without hardcoded
                values.
              </p>
            </div>
          </div>
        </article>

        <article class="endpoint">
          <div class="endpoint-head">
            <span class="method">POST</span>
            <span class="path">/api/v1/predict</span>
          </div>
          <div class="endpoint-grid">
            <div class="block">
              <h3>Purpose</h3>
              <p>Accepts one vehicle record and returns one MPG prediction.</p>
              <p><strong>Expected fields:</strong></p>
              <ul class="list">
                <li><code>cylinders</code>: cylinder count</li>
                <li><code>displacement</code>: cubic inches</li>
                <li><code>horsepower</code>: horsepower</li>
                <li><code>weight</code>: pounds</li>
                <li><code>acceleration</code>: seconds</li>
                <li><code>model_year</code>: two-digit year from 70 to 82</li>
                <li>
                  <code>origin</code>: <code>usa</code>, <code>europe</code>,
                  or <code>japan</code>
                </li>
              </ul>
            </div>
            <div class="block">
              <h3>Request / response example</h3>
              <pre>{
  "cylinders": 4,
  "displacement": 120.0,
  "horsepower": 95.0,
  "weight": 2300.0,
  "acceleration": 15.0,
  "model_year": 79,
  "origin": "japan"
}</pre>
              <pre>{
  "predicted_mpg": 31.729,
  "selected_model": "random_forest",
  "model_version": "1.0.0"
}</pre>
            </div>
          </div>
        </article>

        <article class="endpoint">
          <div class="endpoint-head">
            <span class="method">POST</span>
            <span class="path">/api/v1/predict/batch</span>
          </div>
          <div class="endpoint-grid">
            <div class="block">
              <h3>Purpose</h3>
              <p>
                Accepts multiple vehicle records and returns multiple
                predictions in one request.
              </p>
              <p>
                <strong>Use case:</strong> bulk scoring or future expansion
                beyond the single-record demo UI.
              </p>
            </div>
            <div class="block">
              <h3>Request format</h3>
              <pre>{
  "records": [
    {
      "cylinders": 4,
      "displacement": 120.0,
      "horsepower": 95.0,
      "weight": 2300.0,
      "acceleration": 15.0,
      "model_year": 79,
      "origin": "japan"
    }
  ]
}</pre>
            </div>
          </div>
        </article>
      </section>

      <section class="note">
        <strong>Important implementation detail</strong>
        <p>
          The frontend may let a user work in miles or kilometers, but the backend contract stays
          aligned to the training dataset units. The frontend converts user-facing values into the
          backend's expected units before calling the prediction endpoints.
        </p>
      </section>
    </main>
  </body>
</html>
        """
    )
