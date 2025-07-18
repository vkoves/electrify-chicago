export interface DataPoint {
  year: number;
  value: number;
}

export interface MetricStats {
  count: number;
  mean: number;
  std: number;
  min: number;
  max: number;
  twentyFifthPercentile: number;
  median: number;
  seventyFifthPercentile: number;
}

export interface YearData {
  GHGIntensity?: MetricStats;
  TotalGHGEmissions?: MetricStats;
  ElectricityUse?: MetricStats;
  NaturalGasUse?: MetricStats;
  SourceEUI?: MetricStats;
  SiteEUI?: MetricStats;
}

export type MetricDetail =
  | 'count'
  | 'mean'
  | 'std'
  | 'min'
  | 'max'
  | '25%'
  | '50%'
  | '75%';
