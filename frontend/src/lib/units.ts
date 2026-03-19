import type { DistanceUnit, PredictionRequest } from "../types";

const CUBIC_INCH_TO_LITER = 0.016387064;
const POUND_TO_KILOGRAM = 0.45359237;
const MPG_TO_KPL = 0.425143707;

export function displacementToDisplay(value: number, unit: DistanceUnit): number {
  return unit === "miles" ? value : value * CUBIC_INCH_TO_LITER;
}

export function displacementToApi(value: number, unit: DistanceUnit): number {
  return unit === "miles" ? value : value / CUBIC_INCH_TO_LITER;
}

export function weightToDisplay(value: number, unit: DistanceUnit): number {
  return unit === "miles" ? value : value * POUND_TO_KILOGRAM;
}

export function weightToApi(value: number, unit: DistanceUnit): number {
  return unit === "miles" ? value : value / POUND_TO_KILOGRAM;
}

export function mpgToDisplay(value: number, unit: DistanceUnit): number {
  return unit === "miles" ? value : value * MPG_TO_KPL;
}

export function fuelEfficiencyLabel(unit: DistanceUnit): string {
  return unit === "miles" ? "MPG" : "km/L";
}

export function displacementLabel(unit: DistanceUnit): string {
  return unit === "miles" ? "cubic inches" : "liters";
}

export function weightLabel(unit: DistanceUnit): string {
  return unit === "miles" ? "lb" : "kg";
}

export function formatNumber(value: number, decimals = 1): string {
  return value.toFixed(decimals);
}

export function convertPredictionRequest(
  request: PredictionRequest,
  unit: DistanceUnit,
): PredictionRequest {
  return {
    ...request,
    displacement: displacementToApi(request.displacement, unit),
    weight: weightToApi(request.weight, unit),
  };
}
