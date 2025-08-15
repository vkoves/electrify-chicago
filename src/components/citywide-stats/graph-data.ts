import {
  DataPoint,
  MetricDetail,
  MetricStats,
  YearData,
} from '../../common-functions.vue';
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
/**
 * Extracts and processes metric data from historic statistics for visualization or analysis.
 *
 * This function takes a specific metric name and detail level, then processes the historic
 * data to return a clean array of data points suitable for charting or further analysis.
 * It filters out zero values and sorts the results chronologically.
 *
 * @param metricName - The key of the metric to extract from each year's data
 * @param detail - The specific detail/granularity level of the metric to extract
 * @returns An array of DataPoint objects containing year and value pairs, sorted by year ascending
 *
 * @example
 * ```typescript
 * // Extract the mean values for a temperature metric
 * const avgTemperature = extractMetricData('temperature', 'mean');
 * // Returns: [{ year: 2020, value: 15.2 }, { year: 2021, value: 15.8 }, ...]
 *
 * // Extract the 75th percentile for a sales metric
 * const salesP75 = extractMetricData('sales', '75%');
 * ```
 *
 * @remarks
 * - Zero values are automatically filtered out from the results
 * - Missing or undefined values are treated as 0 and subsequently filtered out
 * - Results are sorted chronologically by year in ascending order
 * - Uses the `detailKeyMap` to map the detail parameter to the appropriate data key
 */
function extractMetricData(
  metricName: keyof YearData,
  detail: MetricDetail,
): DataPoint[] {
  const historicStats = HistoricStats as Record<string, YearData>;
  return Object.entries(historicStats)
    .map(([year, yearData]: [string, YearData]) => {
      const stats = yearData[metricName];
      const value = stats ? stats[detailKeyMap[detail]] : undefined;
      return {
        year: parseInt(year),
        value: value ?? 0,
      };
    })
    .filter((d: DataPoint) => d.value !== 0)
    .sort((a: DataPoint, b: DataPoint) => a.year - b.year);
}

const graphConfigs = [
  {
    data: extractMetricData('GHGIntensity', '50%'),
    containerId: 'ghg-intensity-chart',
    title: 'Median GHG Intensity',
    yAxisLabel: 'kg CO2e/sq ft',
    strokeColor: 'chart-stroke-red',
    fillColor: 'chart-fill-red',
    description: [
      'This chart shows the median greenhouse gas (GHG) emissions intensity of ' +
        'buildings. It is measured in kilograms of CO2-equivalent per square foot ' +
        '(kg CO2e/sq ft).',
      'This unit expresses how much climate pollution a building emits per square ' +
        'foot of space, helping to normalize for building size. Lower numbers ' +
        'suggest better efficiency or cleaner energy use.',
    ],
  },
  {
    data: extractMetricData('TotalGHGEmissions', '50%'),
    containerId: 'total-ghg-chart',
    title: 'Median GHG Emissions',
    yAxisLabel: 'metric tons CO2e',
    strokeColor: 'chart-stroke-blue',
    fillColor: 'chart-fill-blue',
    description: [
      'Displays the median total greenhouse gas emissions per building, measured ' +
        'in metric tons of CO2-equivalent (CO2e).',
      'This includes emissions from electricity, fossil gas, and other sources. A ' +
        'metric ton equals 1,000 kilograms — roughly the emissions from driving a ' +
        'typical gasoline car for over 2,000 miles.',
    ],
  },
  {
    data: extractMetricData('ElectricityUse', '50%'),
    containerId: 'electricity-chart',
    title: 'Median Electricity Use',
    yAxisLabel: 'kWh',
    strokeColor: 'chart-stroke-orange',
    fillColor: 'chart-fill-orange',
    description: [
      'Shows median annual electricity consumption in kilowatt-hours (kWh).',
      'One kWh is the amount of energy used by a 1,000-watt appliance running for ' +
        'one hour — for example, a clothes dryer for 45 minutes or 10 LED bulbs ' +
        'for 10 hours. This metric reflects how much power buildings are drawing ' +
        'from the grid.',
    ],
  },
  {
    data: extractMetricData('NaturalGasUse', '50%'),
    containerId: 'natural-gas-chart',
    title: 'Median Fossil Gas Use',
    yAxisLabel: 'therms',
    strokeColor: 'chart-stroke-green',
    fillColor: 'chart-fill-green',
    description: [
      'Indicates the median fossil gas consumption per building, measured in ' +
        'therms.',
      'One therm is roughly equivalent to burning 100 cubic feet of fossil gas ' +
        'and releases about 5.3 kg of CO2. This metric tracks building heating and ' +
        'hot water use, which are major sources of wintertime emissions.',
    ],
  },
  {
    data: extractMetricData('SourceEUI', '50%'),
    containerId: 'source-eui-chart',
    title: 'Median Source EUI',
    yAxisLabel: 'kBtu/sq ft',
    strokeColor: 'chart-stroke-purple',
    fillColor: 'chart-fill-purple',
    description: [
      'Source Energy Use Intensity (Source EUI) measures the total energy used ' +
        'per square foot (kBtu/sq ft), including generation and transmission ' +
        'losses.',
      'One kBtu (1,000 British thermal units) is about the energy in a kitchen ' +
        'match. This metric gives a full picture of energy demands on the wider ' +
        'energy system.',
    ],
  },
  {
    data: extractMetricData('SiteEUI', '50%'),
    containerId: 'site-eui-chart',
    title: 'Median Site EUI',
    yAxisLabel: 'kBtu/sq ft',
    strokeColor: 'chart-stroke-teal',
    fillColor: 'chart-fill-teal',
    description: [
      'Site Energy Use Intensity (Site EUI) reflects the amount of energy ' +
        'consumed per square foot at the building site itself, measured in ' +
        'kBtu/sq ft.',
      'It excludes upstream losses and focuses purely on what the building uses. ' +
        'It’s commonly used to benchmark and compare buildings’ operational ' +
        'efficiency.',
    ],
  },
] as const;

export { extractMetricData, graphConfigs };
