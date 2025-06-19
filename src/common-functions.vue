<script lang="ts">
import { IPieSlice } from './components/graphs/PieChart.vue';

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

  [buildingKey: string]: string | number | boolean;
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
  DataYear: string;
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
 * Calculate how many typical gas cars' worth of emissions a building produces annually
 * Based on EPA estimate of 4.6 metric tons CO2 per year for a typical passenger vehicle
 * Source: https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle
 */
export function calculateGasCarEquivalent(totalGHGEmissions: number): number {
  const TONS_CO2_PER_CAR_ANNUALLY = 4.6;
  return Math.round(totalGHGEmissions / TONS_CO2_PER_CAR_ANNUALLY);
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
</script>
