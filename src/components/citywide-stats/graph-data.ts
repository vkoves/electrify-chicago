import { DataPoint, MetricDetail, MetricStats, YearData } from './types';
import HistoricStats from '../../data/dist/historic-stats.json';

const detailKeyMap: Record<MetricDetail, keyof MetricStats> = {
  count: 'count',
  mean: 'mean',
  std: 'std',
  min: 'min',
  max: 'max',
  '25%': 'twentyFifthPercentile',
  '50%': 'median',
  '75%': 'seventyFifthPercentile',
};

export function extractMetricData(
  metricName: keyof YearData,
  detail: MetricDetail,
): DataPoint[] {
  const historicStats = HistoricStats as Record<string, YearData>;
  return Object.entries(historicStats)
    .map(([year, yearData]) => {
      const stats = yearData[metricName];
      const value = stats ? stats[detailKeyMap[detail]] : undefined;
      return {
        year: parseInt(year),
        value: value ?? 0,
      };
    })
    .filter((d) => d.value !== 0)
    .sort((a, b) => a.year - b.year);
}

export const graphConfigs = [
  {
    data: extractMetricData('GHGIntensity', '50%'),
    containerId: 'ghg-intensity-chart',
    title: 'GHG Intensity',
    yAxisLabel: 'kg CO2e/sq ft',
    color: '#e74c3c',
  },
  {
    data: extractMetricData('TotalGHGEmissions', '50%'),
    containerId: 'total-ghg-chart',
    title: 'Total GHG Emissions',
    yAxisLabel: 'metric tons CO2e',
    color: '#3498db',
  },
  {
    data: extractMetricData('ElectricityUse', '50%'),
    containerId: 'electricity-chart',
    title: 'Electricity Use',
    yAxisLabel: 'kWh',
    color: '#f39c12',
  },
  {
    data: extractMetricData('NaturalGasUse', '50%'),
    containerId: 'natural-gas-chart',
    title: 'Natural Gas Use',
    yAxisLabel: 'therms',
    color: '#27ae60',
  },
  {
    data: extractMetricData('SourceEUI', '50%'),
    containerId: 'source-eui-chart',
    title: 'Source EUI',
    yAxisLabel: 'kBtu/sq ft',
    color: '#9b59b6',
  },
  {
    data: extractMetricData('SiteEUI', '50%'),
    containerId: 'site-eui-chart',
    title: 'Site EUI',
    yAxisLabel: 'kBtu/sq ft',
    color: '#1abc9c',
  },
] as const;
