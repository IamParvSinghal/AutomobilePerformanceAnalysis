export type Origin = "usa" | "europe" | "japan";
export type DistanceUnit = "miles" | "kilometers";

export interface PredictionRequest {
  cylinders: number;
  displacement: number;
  horsepower: number;
  weight: number;
  acceleration: number;
  model_year: number;
  origin: Origin;
}

export interface PredictionResponse {
  predicted_mpg: number;
  selected_model: string;
  model_version: string;
}

export interface CandidateScore {
  name: string;
  description: string;
  cv_rmse_mean: number;
  cv_mae_mean: number;
  cv_r2_mean: number;
}

export interface FeatureRange {
  min?: number;
  max?: number;
  mean?: number;
  values?: string[];
}

export interface ModelMetadata {
  model_version: string;
  generated_at_utc: string;
  selected_model: string;
  problem_type: string;
  target: string;
  dataset: {
    total_rows: number;
    rows_after_cleaning: number;
    rows_removed: number;
    target_mean: number;
    target_std: number;
    processed_path: string;
  };
  features: {
    numeric: string[];
    categorical: string[];
    feature_ranges: Record<string, FeatureRange>;
  };
  evaluation: {
    test_rmse: number;
    test_mae: number;
    test_r2: number;
    candidate_scores: CandidateScore[];
  };
  example_request: PredictionRequest;
}

export interface FeatureImportanceEntry {
  feature: string;
  importance_mean: number;
  importance_std: number;
}

export interface ModelInfoResponse {
  metadata: ModelMetadata;
  feature_importance: FeatureImportanceEntry[];
}
