import { FormEvent, useEffect, useState } from "react";

import {
  displacementLabel,
  displacementToDisplay,
  formatNumber,
  fuelEfficiencyLabel,
  mpgToDisplay,
  weightLabel,
  weightToDisplay,
} from "../lib/units";
import type {
  DistanceUnit,
  ModelMetadata,
  PredictionRequest,
  PredictionResponse,
} from "../types";

interface PredictionFormProps {
  distanceUnit: DistanceUnit;
  metadata: ModelMetadata;
  prediction: PredictionResponse | null;
  isSubmitting: boolean;
  onDistanceUnitChange: (unit: DistanceUnit) => void;
  onSubmit: (payload: PredictionRequest) => Promise<void>;
}

export function PredictionForm({
  distanceUnit,
  metadata,
  prediction,
  isSubmitting,
  onDistanceUnitChange,
  onSubmit,
}: PredictionFormProps) {
  const [formState, setFormState] = useState<PredictionRequest>(metadata.example_request);

  useEffect(() => {
    setFormState(metadata.example_request);
  }, [metadata]);

  const ranges = metadata.features.feature_ranges;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await onSubmit(formState);
  }

  function displayValue(field: keyof PredictionRequest): number | string {
    const value = formState[field];
    if (typeof value !== "number") {
      return value;
    }

    if (field === "displacement") {
      return formatNumber(
        displacementToDisplay(value, distanceUnit),
        distanceUnit === "miles" ? 1 : 2,
      );
    }

    if (field === "weight") {
      return formatNumber(weightToDisplay(value, distanceUnit), distanceUnit === "miles" ? 0 : 1);
    }

    return value;
  }

  function displayedMin(field: "displacement" | "weight"): number {
    if (field === "displacement") {
      return distanceUnit === "miles"
        ? (ranges.displacement.min ?? 0)
        : displacementToDisplay(ranges.displacement.min ?? 0, distanceUnit);
    }

    return distanceUnit === "miles"
      ? (ranges.weight.min ?? 0)
      : weightToDisplay(ranges.weight.min ?? 0, distanceUnit);
  }

  function displayedMax(field: "displacement" | "weight"): number {
    if (field === "displacement") {
      return distanceUnit === "miles"
        ? (ranges.displacement.max ?? 0)
        : displacementToDisplay(ranges.displacement.max ?? 0, distanceUnit);
    }

    return distanceUnit === "miles"
      ? (ranges.weight.max ?? 0)
      : weightToDisplay(ranges.weight.max ?? 0, distanceUnit);
  }

  function updateField<K extends keyof PredictionRequest>(field: K, value: string) {
    setFormState((current) => ({
      ...current,
      [field]:
        field === "origin"
          ? value
          : field === "displacement"
            ? distanceUnit === "miles"
              ? Number(value)
              : Number(value) / 0.016387064
            : field === "weight"
              ? distanceUnit === "miles"
                ? Number(value)
                : Number(value) / 0.45359237
              : Number(value),
    }));
  }

  const displayedPrediction = prediction
    ? mpgToDisplay(prediction.predicted_mpg, distanceUnit)
    : null;

  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <div className="eyebrow">Interactive scoring</div>
          <h2>Estimate fuel efficiency for a vehicle profile</h2>
        </div>
        <p>
          Choose miles or kilometers, enter a vehicle profile, and the app will convert values to
          the model&apos;s expected units automatically.
        </p>
      </div>
      <div className="unit-toggle" role="group" aria-label="Distance unit">
        <button
          className={distanceUnit === "miles" ? "unit-toggle-button active" : "unit-toggle-button"}
          type="button"
          onClick={() => onDistanceUnitChange("miles")}
        >
          Miles
        </button>
        <button
          className={
            distanceUnit === "kilometers" ? "unit-toggle-button active" : "unit-toggle-button"
          }
          type="button"
          onClick={() => onDistanceUnitChange("kilometers")}
        >
          Kilometers
        </button>
      </div>
      <form className="prediction-form" onSubmit={handleSubmit}>
        <label>
          Cylinders (count)
          <input
            type="number"
            min={ranges.cylinders.min}
            max={ranges.cylinders.max}
            value={displayValue("cylinders")}
            onChange={(event) => updateField("cylinders", event.target.value)}
          />
        </label>
        <label>
          Engine displacement ({displacementLabel(distanceUnit)})
          <input
            type="number"
            min={displayedMin("displacement")}
            max={displayedMax("displacement")}
            step={distanceUnit === "miles" ? "0.1" : "0.01"}
            value={displayValue("displacement")}
            onChange={(event) => updateField("displacement", event.target.value)}
          />
        </label>
        <label>
          Horsepower (hp)
          <input
            type="number"
            min={ranges.horsepower.min}
            max={ranges.horsepower.max}
            step="0.1"
            value={displayValue("horsepower")}
            onChange={(event) => updateField("horsepower", event.target.value)}
          />
        </label>
        <label>
          Weight ({weightLabel(distanceUnit)})
          <input
            type="number"
            min={displayedMin("weight")}
            max={displayedMax("weight")}
            step={distanceUnit === "miles" ? "1" : "0.1"}
            value={displayValue("weight")}
            onChange={(event) => updateField("weight", event.target.value)}
          />
        </label>
        <label>
          Acceleration (seconds)
          <input
            type="number"
            min={ranges.acceleration.min}
            max={ranges.acceleration.max}
            step="0.1"
            value={displayValue("acceleration")}
            onChange={(event) => updateField("acceleration", event.target.value)}
          />
        </label>
        <label>
          Model year (2-digit)
          <input
            type="number"
            min={ranges.model_year.min}
            max={ranges.model_year.max}
            value={displayValue("model_year")}
            onChange={(event) => updateField("model_year", event.target.value)}
          />
        </label>
        <label>
          Manufacturing region
          <select value={formState.origin} onChange={(event) => updateField("origin", event.target.value)}>
            {ranges.origin.values?.map((origin) => (
              <option key={origin} value={origin}>
                {origin}
              </option>
            ))}
          </select>
        </label>
        <button className="primary-button" type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Scoring..." : `Predict ${fuelEfficiencyLabel(distanceUnit)}`}
        </button>
      </form>
      <div className="prediction-result">
        <span className="metric-label">Predicted fuel efficiency</span>
        <strong>
          {displayedPrediction
            ? `${displayedPrediction.toFixed(2)} ${fuelEfficiencyLabel(distanceUnit)}`
            : "--"}
        </strong>
        <p>
          {prediction
            ? `Served by ${prediction.selected_model} (${prediction.model_version}).`
            : "Submit a profile to generate a prediction."}
        </p>
      </div>
    </section>
  );
}
