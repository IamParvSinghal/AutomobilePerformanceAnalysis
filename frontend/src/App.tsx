import { useEffect, useState } from "react";

import { BenchmarkTable } from "./components/BenchmarkTable";
import { Hero } from "./components/Hero";
import { PredictionForm } from "./components/PredictionForm";
import { fetchModelInfo, predict } from "./lib/api";
import { convertPredictionRequest } from "./lib/units";
import type {
  DistanceUnit,
  ModelInfoResponse,
  PredictionRequest,
  PredictionResponse,
} from "./types";

export default function App() {
  const [distanceUnit, setDistanceUnit] = useState<DistanceUnit>("miles");
  const [modelInfo, setModelInfo] = useState<ModelInfoResponse | null>(null);
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchModelInfo();
        setModelInfo(data);
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Unable to load model info.");
      } finally {
        setIsLoading(false);
      }
    }

    void load();
  }, []);

  async function handlePrediction(payload: PredictionRequest) {
    setError(null);
    setIsSubmitting(true);
    try {
      const response = await predict(convertPredictionRequest(payload, distanceUnit));
      setPrediction(response);
    } catch (predictionError) {
      setError(
        predictionError instanceof Error ? predictionError.message : "Prediction request failed.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoading) {
    return (
      <main className="app-shell">
        <section className="loading-panel">Loading model metadata...</section>
      </main>
    );
  }

  if (!modelInfo) {
    return (
      <main className="app-shell">
        <section className="loading-panel error-panel">{error ?? "No model data found."}</section>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <div className="background-orb background-orb-left" />
      <div className="background-orb background-orb-right" />
      <div className="content-stack">
        <Hero />
        {error ? <section className="inline-error">{error}</section> : null}
        <PredictionForm
          distanceUnit={distanceUnit}
          metadata={modelInfo.metadata}
          prediction={prediction}
          isSubmitting={isSubmitting}
          onDistanceUnitChange={setDistanceUnit}
          onSubmit={handlePrediction}
        />
        <BenchmarkTable
          candidates={modelInfo.metadata.evaluation.candidate_scores}
          selectedModel={modelInfo.metadata.selected_model}
        />
      </div>
    </main>
  );
}
