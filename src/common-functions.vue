<script lang="ts">
import { IPieSlice } from './components/graphs/PieChart.vue';
import { LatestDataYear } from './constants/globals.vue';

export default {};

/** Colors for our energy mix pie chart for each type of energy use */
export const EnergyBreakdownColors = {
  DistrictChilling: '#01295F',
  DistrictSteam: '#ABABAB',
  Electricity: '#F0E100',
  NaturalGas: '#993300',
};

export interface IBuildingBenchmarkStat {
  count: number;
  min: number;
  max: number;
  mean: number; // note we should generally lean on the median
  std: number; // standard deviation
  twentyFifthPercentile: number;
  median: number;
  seventyFifthPercentile: number;
}

/** The type of building-benchmark-stats.json */
export interface IBuildingBenchmarkStats {
  [statKey: string]: IBuildingBenchmarkStat;
}

/** Property stats do not have a mean or standard deviation */
export interface IPropertyStat {
  count: number;
  min: number;
  max: number;
  twentyFifthPercentile: number;
  median: number;
  seventyFifthPercentile: number;
}

/** The type of each property type in building-statistics-by-property-type.json */
export interface IPropertyStats {
  [statKey: string]: IPropertyStat;
}

/** All the available data anomaly codes from detect_anomalous_buildings.py:anomaly_values */
export enum DataAnomalies {
  gasZeroWithPreviousUse = 'gas:zero-with-prev-use',
  largeGasSwing = 'gas:large-swings',
}

/**
 * An individual building object, with full details
 *
 * TODO: Type this more strictly, maybe with Python generating a types file with
 * all of the parameter types
 */
export interface IBuilding {
  ID: string | number;
  DataYear: number;
  PropertyName: string;
  Address: string;
  PrimaryPropertyType: string;
  Latitude: string;
  Longitude: string;
  DataAnomalies: string;

  // Parsed as float in gridsome.server.js
  DistrictChilledWaterUse: number;
  DistrictSteamUse: number;
  ElectricityUse: number;
  GHGIntensity: number;
  GrossFloorArea: number;
  NaturalGasUse: number;
  TotalGHGEmissions: number;
  YearBuilt: number;

  FirstYearReported: number | null;
  LastYearReported: number | null;
  Owner?: string; // Building owner key (e.g., 'depaul', 'uchicago')

  [buildingKey: string]: string | number | boolean | null | undefined;
}

/** How GraphQL passes back a building */
export interface IBuildingNode {
  node: IBuilding;
}

/**
 * A year of benchmark data, with columns we parse by
 */
export interface IHistoricData {
  ID: string;
  DataYear: number;
  ReportingStatus: string;
  // The actual data
  ChicagoEnergyRating: string;
  ENERGYSTARScore: string;

  // Parsed as float by gridsome.server.js (could also be null)
  DistrictChilledWaterUse: number;
  DistrictSteamUse: number;
  ElectricityUse: number;
  GHGIntensity: number;
  GrossFloorArea: number;
  NaturalGasUse: number;
  SourceEUI: number;
  TotalGHGEmissions: number;
}

/**
 * Determines if a building actually reported meaningful data for a given year.
 * A building is considered to have "reported" if it has valid GHG intensity data,
 * not just if it submitted paperwork.
 */
export function hasReportedData(historicData: IHistoricData): boolean {
  return (
    typeof historicData.GHGIntensity === 'number' &&
    historicData.GHGIntensity > 0
  );
}

export function isZeroOrNull(value: number | null): boolean {
  return value === 0 || value === null;
}

/**
 * Type guard to ensure required building properties exist for calculations
 */
export function validateBuildingProperties<T extends IBuilding>(
  building: T,
  properties: (keyof T)[],
  functionName: string,
): void {
  for (const prop of properties) {
    if (typeof building[prop] === 'undefined') {
      throw new Error(
        `Missing building.${String(prop)} for ${functionName} check!`,
      );
    }
  }
}

/**
 * Whether a building is _fully_ gas free, meaning no gas burned on-site or to heat it
 * through a district heating system. That means it's all electric!
 *
 * We do not mark this as true if we have detected gas use in the past
 */
export function fullyGasFree(building: IBuilding): boolean {
  validateBuildingProperties(
    building,
    ['DataAnomalies', 'NaturalGasUse', 'DistrictSteamUse'],
    'fullyGasFree',
  );

  return (
    !building.DataAnomalies.includes(DataAnomalies.gasZeroWithPreviousUse) &&
    isZeroOrNull(building.NaturalGasUse) &&
    isZeroOrNull(building.DistrictSteamUse)
  );
}

/**
 * Whether a building is "new" - meaning this is the first year it has reported data
 */
export function isNewBuilding(
  building: IBuilding,
  historicData: Array<IHistoricData>,
): boolean {
  if (!historicData) {
    throw new Error('Missing historicData for isNewBuilding check!');
  }
  // No historic data = not reported (so not new)
  else if (historicData.length === 0) {
    return false;
  }

  const reportedYears = historicData
    .filter((data) => hasReportedData(data))
    .map((data) => data.DataYear)
    .sort((a, b) => a - b);

  // Non reporting isn't new
  if (reportedYears.length === 0) {
    return false;
  }

  const currentDataYear = parseInt(building.DataYear.toString(), 10);

  // A building is "new" if:
  // 1. It's currently reporting in the latest data year (2023)
  // 2. AND this is the first year it has ever reported
  // 3. AND it only has one year of reported data
  const isReportingInLatestYear = currentDataYear === LatestDataYear;
  const hasOnlyOneYearOfData = reportedYears.length === 1;
  const firstReportedYear = reportedYears[0];
  const isFirstYearEqualToLatest = firstReportedYear === currentDataYear;

  return (
    isReportingInLatestYear && hasOnlyOneYearOfData && isFirstYearEqualToLatest
  );
}

/**
 * Types for Citywide Stats
 */
export interface DataPoint {
  year: number;
  value: number;
}

export type RegressionLine = {
  x1: number;
  x2: number;
  y1: number;
  y2: number;
};

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

/**
 * A constant for what we use as min and max values for flagged ranks
 */
export const RankConfig = {
  /** Buildings above this rank for a stat are marked very bad and get a 🚨 */
  AlarmRankMax: 10,
  AlarmEmoji: '🚨',
  AlarmMsg: `Top 10 worst in at least one category`,

  /** Buildings above this rank for a stat are marked bad and get a 🚩 */
  FlagRankMax: 50,
  FlagEmoji: '🚩',
  FlagMsg: `Top 50 worst in at least one category`,

  /** Buildings with an _inverted rank_ at or under this get a 🏆 */
  TrophyRankInvertedMax: 30,
  TrophyEmoji: '🏆',
  TrophyMsg: `Top 30 best in at least one category`,
};

/**
 * Rounds a number to whole number if it is greater than 1000,
 * otherwise returns the original number
 * This function always returns a NUMBER
 */
export function roundUpLargeNumber(value: number): number {
  if (value > 1000) {
    return Math.floor(value);
  } else {
    return value;
  }
}

/**
 * Returns a string rank for very bad buildings, or null if not in top 50
 * worst
 */
export function getRankLabel(
  statRank: number,
  isSquareFootage: boolean,
): string | null {
  if (isSquareFootage) {
    return 'Largest';
  } else if (statRank <= RankConfig.AlarmRankMax) {
    return `Highest in Chicago* ${RankConfig.AlarmEmoji}`;
  } else if (statRank <= RankConfig.FlagRankMax) {
    return `Highest in Chicago* ${RankConfig.FlagEmoji}`;
  } else {
    return null;
  }
}

/**
 * Returns a string rank for very bad buildings per primary property
 * type, or null if not in top 50 worst
 */
export function getRankLabelByProperty(
  statRank: number,
  isSquareFootage: boolean,
  propertyTag: string,
): string | null {
  if (isSquareFootage) {
    return `Largest of ${propertyTag}`;
  } else if (statRank <= RankConfig.AlarmRankMax) {
    return `Highest of ${propertyTag} ${RankConfig.AlarmEmoji}`;
  } else if (statRank <= RankConfig.FlagRankMax) {
    return `Highest of ${propertyTag} ${RankConfig.FlagEmoji}`;
  } else {
    return null;
  }
}

/**
 * Columns that have rankings (format of _Rank and _PercentileRank)
 */
export const RankedColumns = [
  'GHGIntensity',
  'TotalGHGEmissions',
  'ElectricityUse',
  'NaturalGasUse',
  'SourceEUI',
  'SiteEUI',
  // 'GrossFloorArea',
];

/**
 * Returns the inverted rank for a statistic (e.g. #1 lowest if rank is 1290/1290)
 *
 * @param {string} statKey
 * @param {number} statRank
 * @param {Object} buildingStats
 * @return {number|null}
 */
export function getStatRankInverted(
  statKey: string,
  statRank: number,
  buildingStats: IBuildingBenchmarkStats,
): number | null {
  if (statRank) {
    const countForStat = buildingStats[statKey].count;

    // Rank 100/100 should invert to #1 lowest, not #0
    return countForStat - statRank + 1;
  }

  return null;
}

/**
 * Returns the multiplier for a building's stat compared to the median (e.g. '3' times median
 * '1/5' median)
 */
export function getMedianMultipleMsg(
  median: number,
  statValueNum: number,
): string | null {
  if (!median) {
    return null;
  }

  const medianMult = statValueNum / median;

  // We can say 2.5x but 5.5x or 40.56x is a bit silly, just round
  if (medianMult > 5) {
    return Math.round(medianMult) + 'x';
  }

  // If the multiple is < 1, make a fraction (e.g. 1/5 the median)
  if (medianMult < 0.5) {
    return `1/${Math.round(1 / medianMult)}`;
  }

  // Base case - if between 0.5 and 5, do 2x, 0.7x, etc.
  return medianMult.toFixed(1) + 'x';
}

/**
 * Calculate concern level for a stat
 * 0 = outstanding performer in category
 * 1 = no concern
 * 2 = medium concern (above median)
 * 3 = high concern (> 1 std. deviation above the mean)
 * 4 = very high concern (top 10 in category)
 */
export function getConcernLevel(
  building: IBuilding,
  statKey: string,
  stats: IBuildingBenchmarkStats,
  colsToHideComparison: string[] = [
    'DistrictSteamUse',
    'DistrictChilledWaterUse',
  ],
): number | null {
  // Some columns never show comparisons, because there's incomplete data
  if (colsToHideComparison.includes(statKey)) {
    return null;
  }

  const statValue = building[statKey] as number;
  const median = stats[statKey].median;
  const mean = stats[statKey].mean;
  const std = stats[statKey].std;
  const statRank = building[statKey + 'Rank'] as string;

  if (!statValue || !median) return null;

  const isAboveMedian = statValue > median;
  const isOneStdDeviationAboveMean = statValue > mean + std;
  const statRankNum = statRank ? Math.round(parseFloat(statRank)) : 1000;

  // Very high concern if top 10
  if (statRankNum <= 10) {
    return 4;
    // High concern if top 30 or well above mean
  } else if (statRankNum <= 30 || isOneStdDeviationAboveMean) {
    return 3;
  } else if (isAboveMedian) {
    return 2;
  } else {
    const statRankInverted = getStatRankInverted(statKey, statRankNum, stats);
    if (statRankInverted && statRankInverted >= 30) {
      return 1;
    } else if (statRankInverted && statRankInverted <= 30) {
      return 0;
    }
  }

  return null;
}

/**
 * Given a building with all of its stats, return the _worst_ emoji applicable
 * based on getRankLabel.
 *
 * Examples:
 * - Keating Hall should return '🚨' because it has the #1 worst GHG intensity
 * - McGowan North should return '🚩' because it has the #14 worst GHG intensity
 * - Marina towers should return '🏆' because it has #1 lowest SEIU
 *
 * @param {Object} building
 * @param {Object} buildingStats
 * @return {{ msg: string, emoji: string }| null} Returns an object with a message and an emoji if
 * an emoji is applicable, otherwise returns null
 */
export function getOverallRankEmoji(
  building: IBuilding,
  buildingStats: IBuildingBenchmarkStats,
): { msg: string; emoji: string } | null {
  let worstEmoji: string | null = null;
  let hasTrophyCategory = false;

  // Loop through all ranked columns to get the worst emoji and whether any stats earn the building
  // a trophy
  RankedColumns.forEach((columnKey) => {
    const val = building[columnKey + 'Rank'];
    const statRank = parseFloat((val ?? '').toString());
    const statRankInverted = getStatRankInverted(
      columnKey,
      statRank,
      buildingStats,
    );

    // Ignore the column if rank is NaN
    if (typeof statRank !== 'number' || isNaN(statRank)) {
      return;
    }

    if (statRank <= RankConfig.AlarmRankMax) {
      // Alarm is always the worst, so we override
      worstEmoji = RankConfig.AlarmEmoji;
    } else if (
      statRank <= RankConfig.FlagRankMax &&
      worstEmoji !== RankConfig.AlarmEmoji
    ) {
      // If the worstEmoji isn't the alarm and we meet the flag rank, set to flag
      worstEmoji = RankConfig.FlagEmoji;
    } else if (
      statRankInverted &&
      statRankInverted <= RankConfig.TrophyRankInvertedMax
    ) {
      hasTrophyCategory = true;
    }
  });

  // If we have no bad emoji and get a trophy, return that, otherwise return the worst emoji
  if (hasTrophyCategory && !worstEmoji) {
    return {
      msg: RankConfig.TrophyMsg,
      emoji: RankConfig.TrophyEmoji,
    };
  } else if (worstEmoji) {
    return {
      emoji: worstEmoji,
      msg:
        worstEmoji === RankConfig.AlarmEmoji
          ? RankConfig.AlarmMsg
          : RankConfig.FlagMsg,
    };
  }

  return null;
}

/**
 * A constant for Chicago avg. utility costs in the latest data year (in dollar per unit of energy),
 * which we use to estimate an upper bound of how much a building would pay for gas or electric
 */
export const UtilityCosts = {
  year: 2021,
  source:
    'https://www.bls.gov/regions/midwest/news-release/AverageEnergyPrices_Chicago.htm',
  electricCostPerKWh: 0.143,
  gasCostPerTherm: 1.192,
};

/**
 * Given an amount of natural gas or electricity used by a building, returns a cost
 * estimate of how much a building would have spent at average retail prices for
 * that energy.
 *
 * For testing, Viktor manually used the 2021 values to calculate:
 *
 * Keating nat gas cost: $708,860.13
 * Keating electric cost: $82,898.53
 */
export function estimateUtilitySpend(
  energyUseKbtu: number,
  isElectric: boolean,
): number {
  const kwhToKbtuMult = 3.412; // 1kWh = 3.412 kBtu
  const thermToKbtuMult = 99.976; // 1th = 99.976 kBtu

  const costPerKbtuNatGas = UtilityCosts.gasCostPerTherm / thermToKbtuMult;
  const costPerKbtuElectric = UtilityCosts.electricCostPerKWh / kwhToKbtuMult;

  const costPerKbtu = isElectric ? costPerKbtuElectric : costPerKbtuNatGas;

  const estimateRaw = costPerKbtu * energyUseKbtu;

  // If > $1,000 round to the nearest 100 (e.g. $12,345 -> $12,000)
  if (estimateRaw > 1_000) {
    return Math.round(estimateRaw / 1_000) * 1_000;
  }
  // If < $1,000 but > $100 round to the nearest 100 (e.g. $812 -> $800)
  else if (estimateRaw > 100) {
    return Math.round(estimateRaw / 100) * 100;
  }
  // If < $100 round to the nearest 10 (e.g. $87.50 -> $90)
  else {
    return Math.round(estimateRaw / 10) * 10;
  }
}

/**
 * Converts a building or benchmark record into pie chart slices and a total energy use
 */
export function calculateEnergyBreakdown(record: IBuilding | IHistoricData): {
  energyBreakdown: Array<IPieSlice>;
  totalEnergyUse: number;
} {
  const energyBreakdown: Array<IPieSlice> = [];

  if (record.ElectricityUse > 0) {
    energyBreakdown.push({
      label: 'Electricity',
      value: parseFloat(record.ElectricityUse.toString()),
      color: EnergyBreakdownColors.Electricity,
    });
  }

  if (record.NaturalGasUse > 0) {
    energyBreakdown.push({
      label: 'Fossil Gas',
      value: parseFloat(record.NaturalGasUse.toString()),
      color: EnergyBreakdownColors.NaturalGas,
    });
  }

  if (record.DistrictSteamUse > 0) {
    energyBreakdown.push({
      label: 'District Steam',
      value: parseFloat(record.DistrictSteamUse.toString()),
      color: EnergyBreakdownColors.DistrictSteam,
    });
  }

  if (record.DistrictChilledWaterUse > 0) {
    energyBreakdown.push({
      label: 'District Chilling',
      value: parseFloat(record.DistrictChilledWaterUse.toString()),
      color: EnergyBreakdownColors.DistrictChilling,
    });
  }

  let totalEnergyUse = 0;
  energyBreakdown.forEach((datum) => (totalEnergyUse += datum.value));

  return {
    energyBreakdown,
    totalEnergyUse,
  };
}

/**
 * Split data anomaly tokens into an array
 */
export function parseAnomalies(dataAnomalies: string): Array<DataAnomalies> {
  if (dataAnomalies.length === 0) {
    return [];
  }

  return dataAnomalies.split(',') as Array<DataAnomalies>;
}

/**
 * A JS based scroll for `<a href="#anchor">` elements, so that we don't need to globally apply
 * smooth scrolling to the whole site
 */
export function smoothlyScrollToAnchor(event: MouseEvent): void {
  event.preventDefault();

  const link = event.currentTarget as HTMLAnchorElement;
  const targetId = link.getAttribute('href')?.substring(1);

  if (targetId) {
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });

      setTimeout(() => {
        // Set focus to the target heading for keyboard users, after a delay for animation
        targetElement.focus();
      }, 350);

      // Update the URL hash (maintaining default browser behavior)
      window.history.pushState(null, '', `#${targetId}`);
    }
  }
}
</script>
