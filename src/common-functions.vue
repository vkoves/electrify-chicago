<script lang="ts">
export default { };

export interface IBuildingBenchmarkStat {
  count: number;
  min: number;
  max: number;
  twentyFifthPercentile: number;
  median: number;
  seventyFifthPercentile: number;
}

/** The type of building-benchmark-stats.json */
export interface IBuildingBenchmarkStats {
  [statKey: string]: IBuildingBenchmarkStat;
}

/**
 * An individual building object
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


  NaturalGasUse: string;
  DistrictSteamUse: string;

  [buildingKey: string]: string | number | boolean;
}

/** How GraphQL passes back a building */
export interface IBuildingNode { node: IBuilding }

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
 * Returns a string rank for very bad buildings, or null if not in top 50
 * worst
 */
export function getRankLabel(statRank: number, isSquareFootage: boolean): string | null {
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
export function getRankLabelByProperty(statRank: number, isSquareFootage: boolean,
  propertyTag: string): string | null {
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
  statKey: string, statRank: number, buildingStats: IBuildingBenchmarkStats,
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
): { msg: string, emoji: string } | null {
  let worstEmoji: string | null = null;
  let hasTrophyCategory = false;

  // Loop through all ranked columns to get the worst emoji and whether any stats earn the building
  // a trophy
  RankedColumns.forEach((columnKey) => {
    const val = building[columnKey + 'Rank'];
    const statRank = parseFloat((val ?? '').toString());
    const statRankInverted = getStatRankInverted(columnKey, statRank, buildingStats);

    // Ignore the column if rank is NaN
    if (typeof statRank !== 'number' || isNaN(statRank)) {
      return;
    }

    if (statRank <= RankConfig.AlarmRankMax) {
      // Alarm is always the worst, so we override
      worstEmoji = RankConfig.AlarmEmoji;
    } else if (statRank <= RankConfig.FlagRankMax && worstEmoji !== RankConfig.AlarmEmoji) {
      // If the worstEmoji isn't the alarm and we meet the flag rank, set to flag
      worstEmoji = RankConfig.FlagEmoji;
    } else if (statRankInverted && statRankInverted <= RankConfig.TrophyRankInvertedMax) {
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
      msg: worstEmoji === RankConfig.AlarmEmoji ? RankConfig.AlarmMsg : RankConfig.FlagMsg,
    };
  }

  return null;
}

export const UtilityCosts = {
  year: 2021,
  source: 'https://www.bls.gov/regions/midwest/news-release/AverageEnergyPrices_Chicago.htm',
  electricCostPerKWh: 0.147,
  gasCostPerTherm: 1.101,
};

/**
 * Given an amount of natural gas or electricity used by a building, returns a cost
 * estimate of how much a building would have spent at average retail prices for
 * that energy.
 */
export function estimateUtilitySpend(energyUseKbtu: number, isElectric: boolean): number {
  const kwhToKbtuMult = 3.412; // 1kWh = 3.412 kBtu
  const thermToKbtuMult = 99.976; // 1th = 99.976 kBtu

  const costPerKbtuNatGas = UtilityCosts.gasCostPerTherm / thermToKbtuMult;
  const costPerKbtuElectric = UtilityCosts.electricCostPerKWh / kwhToKbtuMult;

  const costPerKbtu = isElectric ? costPerKbtuElectric : costPerKbtuNatGas;

  return costPerKbtu * energyUseKbtu;

  // Keating nat gas cost: $708,860.13
  // Keating electric cost: $82,898.53026
}
</script>
