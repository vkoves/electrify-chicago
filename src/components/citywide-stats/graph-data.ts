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
export function extractMetricData(
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

export const graphConfigs = [
  {
    data: extractMetricData('GHGIntensity', '50%'),
    containerId: 'ghg-intensity-chart',
    title: 'Median GHG Intensity',
    yAxisLabel: 'kg CO2e/sq ft',
    strokeColor: 'chart-stroke-red',
    fillColor: 'chart-fill-red',
    description: [
      'Buildings are responsible for about 40% of global greenhouse gas emissions, making them ' +
        'a critical piece of the climate puzzle. GHG intensity shows how much climate pollution ' +
        'a building produces per square foot of space (measured in kg CO2e/sq ft).',
      "Think of this as your building's carbon footprint per square foot. A typical " +
        'Chicago office ' +
        "building might emit 15-25 kg CO2e per square foot annually — that's like the " +
        'emissions from ' +
        'driving 30-50 miles in a gas car, but for every square foot of the building, every year.',
      'Lower intensity means the building is either more energy-efficient or using cleaner ' +
        'energy sources. ' +
        'This metric helps level the playing field between a small café and a massive skyscraper.',
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
      'This tracks the total climate impact of buildings — all the greenhouse gases they produce ' +
        'from electricity, heating, and cooling combined. Every kilowatt-hour of electricity and ' +
        "every therm of gas burned adds to a building's total emissions.",
      'One metric ton of CO2e equals about 2,200 pounds of carbon pollution — roughly what a ' +
        'typical ' +
        'gas car produces driving 2,500 miles. A large Chicago office building might emit ' +
        'hundreds or ' +
        'even thousands of metric tons per year.',
      "Unlike intensity metrics, total emissions show a building's absolute climate impact. " +
        'A highly ' +
        "efficient skyscraper might still have high total emissions simply because it's " +
        'massive, while ' +
        'an inefficient small building could have relatively low total emissions.',
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
      'Electricity powers everything in modern buildings — lights, computers, elevators, ' +
        'air conditioning, ' +
        'and increasingly, heating and hot water too. As more buildings electrify to reduce ' +
        'emissions, ' +
        'understanding electricity use becomes even more important.',
      'One kilowatt-hour (kWh) powers a desktop computer for about 3-4 hours, or runs your ' +
        'microwave ' +
        'for an hour. A typical Chicago office building uses thousands of kWh daily — ' +
        'enough to power ' +
        'hundreds of homes.',
      'The climate impact of electricity varies dramatically based on the energy source. ' +
        'In Illinois, ' +
        'where about half our electricity comes from nuclear and renewables, each kWh ' +
        'produces less ' +
        'emissions than in coal-heavy states. This is why electrification can be a climate win.',
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
      'Fossil gas (often called "natural gas") is the biggest source of building emissions ' +
        'in Chicago. ' +
        'Most buildings use it for heating, hot water, and cooking — and every therm burned ' +
        'releases ' +
        'carbon directly into the atmosphere.',
      'One therm equals about 100 cubic feet of gas and produces roughly 11 pounds of CO2 ' +
        'when burned. ' +
        'A typical Chicago building might use hundreds or thousands of therms during winter ' +
        'months. ' +
        "That adds up fast when you consider the city's long, cold winters.",
      'Unlike electricity, which can get cleaner as the grid adds more renewables, burning ' +
        'fossil gas ' +
        "will always produce emissions. That's why many climate strategies focus on " +
        'electrifying heating ' +
        'and switching to heat pumps, electric water heaters, and induction cooking.',
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
      'Source EUI captures the total energy demand a building places on our energy system — ' +
        'not just ' +
        'what shows up on the utility bill, but including all the energy lost generating and ' +
        'delivering ' +
        'that power to the building.',
      'For every kWh that reaches your building, about 2-3 kWh of primary energy was needed ' +
        'at the ' +
        'power plant due to conversion and transmission losses. One kBtu is roughly the energy ' +
        'in a ' +
        'wooden kitchen match — buildings typically use tens of thousands of kBtu per square ' +
        'foot annually.',
      'This metric matters because it reflects the true demand buildings place on our energy ' +
        'infrastructure. ' +
        'A building with high source EUI is straining the broader system more, requiring more ' +
        'power plants, ' +
        'gas wells, and transmission lines to support it.',
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
      'Site EUI measures the energy actually delivered to and consumed by the building ' +
        'itself — ' +
        "what you'd see on your utility bills. This is the most straightforward way to " +
        'understand ' +
        'how much energy a building uses per square foot.',
      'A well-insulated, efficient building in Chicago might use 50-80 kBtu per square foot ' +
        'annually, ' +
        "while an older, inefficient building could use 150+ kBtu per square foot. That's " +
        'the difference ' +
        'between a warm sweater and a thin t-shirt in a Chicago winter.',
      "Site EUI is the go-to metric for comparing building performance because it's " +
        'directly tied to ' +
        'what building owners can control — insulation, windows, HVAC efficiency, and ' +
        'occupant behavior. ' +
        "It's also what most energy benchmarking programs use to set targets and requirements.",
    ],
  },
] as const;
