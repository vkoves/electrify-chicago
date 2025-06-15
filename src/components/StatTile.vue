<template>
  <div
    class="stat-tile"
    :class="{
      '-very-bad': concernLevel === 4,
      '-bad': concernLevel === 3,
      '-medium': concernLevel === 2,
      '-good': concernLevel === 1,
      '-great': concernLevel === 0,
      '-sq-footage': isSquareFootage,
    }"
  >
    <SparkLine
      v-if="historicStatData.length > 0"
      :graph-data="historicStatData"
      :graph-title="statKey"
      :unit="unit"
    />

    <template v-if="typeof building[statKey] === 'number'">
      <!-- The actual stat value-->
      <div class="stat-value">
        {{ statValueStr }} <span class="unit" v-html="unit" />
      </div>

      <div v-if="costEstimate" class="bill-estimate">
        <strong
          >Est.
          {{ statKey === 'NaturalGasUse' ? 'Gas' : 'Electric' }} Bill:</strong
        >
        ${{ Math.round(costEstimate).toLocaleString() }} for
        {{ building.DataYear }}**
      </div>

      <!-- Only show the rank if in the top 50, #102th highest _ doesn't mean much -->
      <div
        v-if="statRank && statRank <= RankConfig.FlagRankMax && rankLabel"
        class="rank"
      >
        #{{ statRank }} {{ rankLabel }}
      </div>

      <!-- Rank amongst property type -->
      <div
        v-if="
          propertyStatRank &&
          propertyStatRank <= RankConfig.FlagRankMax &&
          propertyRankLabel
        "
        class="property-rank"
      >
        #{{ propertyStatRank }} {{ propertyRankLabel }}
      </div>

      <!-- If in the lowest 30, show that unless square footage (TODO: Move to GreatRankMax) -->
      <div
        v-if="
          !isSquareFootage &&
          statRankInverted &&
          statRankInverted <= RankConfig.TrophyRankInvertedMax
        "
        class="rank"
      >
        #{{ statRankInverted }} Lowest in Chicago* 🏆
      </div>

      <!-- If in the lowest 30, show that unless square footage (TODO: Move to GreatRankMax) -->
      <div
        v-if="!isSquareFootage && propertyStatRankInverted"
        class="property-rank"
      >
        #{{ propertyStatRankInverted }} Lowest of
        {{ pluralismForPropertyType }} 🏆
      </div>

      <!-- Only show percentile if we don't have a flag or alarm -->
      <div
        v-if="
          typeof statRankPercent === 'number' &&
          statRank > RankConfig.FlagRankMax
        "
        class="percentile"
      >
        <!-- If stat rank is < 50%, invert it.
        E.g higher than of benchmarked buildings becomes less than 99% of buildings-->
        <template v-if="statRankPercent > 50">
          Higher than {{ statRankPercent }}% of all buildings
        </template>
        <!-- Only show lower than X% if not getting a trophy-->
        <template
          v-else-if="statRankInverted > RankConfig.TrophyRankInvertedMax"
        >
          <!-- Never show lower than 100%, top out at 100%-->
          Lower than {{ Math.min(99, 100 - statRankPercent) }}% of all buildings
        </template>
      </div>

      <div v-if="medianMultipleMsgCityWide" class="median-comparison">
        <div>
          <!-- Only show median multiple if the building stat is > 0, otherwise it's 1/infinity -->
          <span v-if="statValueStr !== '0'" class="median-mult">
            {{ medianMultipleMsgCityWide }} median
          </span>
          <span v-else class="median-label"> Median Chicago Building </span>

          <div class="median-val">
            {{ stats[statKey].median.toLocaleString() }}
            <span v-html="unit" />
          </div>
        </div>

        <div v-if="medianMultiplePropertyType">
          <!-- Only show median multiple if the building stat is > 0, otherwise it's 1/infinity -->
          <span v-if="statValueStr !== '0'" class="median-mult">
            {{ medianMultiplePropertyType }} median {{ propertyType }}
          </span>
          <span v-else class="median-label"> Median {{ propertyType }} </span>

          <div class="median-val">
            {{
              BuildingStatsByPropertyType[propertyType][
                statKey
              ].median.toLocaleString()
            }}
            <span v-html="unit" />
          </div>
        </div>
      </div>
      <p v-else class="no-stat-msg">
        Most buildings don't use
        <span v-if="statKey === 'DistrictSteamUse'">district steam</span>
        <span v-else-if="statKey === 'DistrictChilledWaterUse'"
          >district chilling</span
        >
        <span v-else>this</span>, so we don't currently have comparison data.
      </p>

      <!-- Fossil Gas specific message -->
      <div
        v-if="statValueStr === '0' && statKey === 'NaturalGasUse'"
        class="no-gas-msg"
      >
        <div v-if="fullyGasFree">
          <div class="bold">This Building Didn't Burn Any Fossil Gas! 🎉</div>

          <p class="smaller">
            This building burned no fossil gas on-site and isn't connected to a
            district heating system, meaning it's fully electric! View
            <g-link to="/biggest-gas-free-buildings">
              Chicago's Biggest Gas Free Buildings </g-link
            >.
          </p>
        </div>
        <div v-else-if="building.DataAnomalies" class="panel -warning">
          <div class="bold">
            <span class="emoji">⚠️</span> Likely Reporting Error
          </div>

          <p class="smaller">
            This building has burned gas in the past, so this latest year having
            0 gas use is likely a reporting error.
          </p>
        </div>
        <div v-else>
          <div class="bold">This Building Uses District Heating ❗</div>

          <p class="smaller">
            Although this building didn't burn any fossil gas on site, it's
            connected to a district heating system, a centralized system for
            heating multiple buildings. District heating systems can be fully
            electric, but in Chicago most district heating systems are fossil
            gas powered, meaning this building was most likely still heated with
            fossil gas.
          </p>
        </div>
      </div>
    </template>
    <template v-else>
      Not Reported

      <p class="empty-notice">
        This data was not reported for this building this year, which
        <em>likely</em> means a value of zero for this field.
      </p>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import buildingStatsByPropertyType from '../data/dist/building-statistics-by-property-type.json';

import {
  DataAnomalies,
  estimateUtilitySpend,
  getRankLabel,
  getRankLabelByProperty,
  IBuilding,
  IBuildingBenchmarkStats,
  IHistoricData,
  IPropertyStats,
  RankConfig,
} from '../common-functions.vue';
import SparkLine, { INumGraphPoint } from './graphs/SparkLine.vue';

/**
 * A group of all the core stats by property type (e.g. GHG intensity median)
 */
export interface IStatsByPropertyType {
  [propertyType: string]: IPropertyStats;
}

/**
 * A  tile that can show the stats for a building, including whether it's
 * doing better or worse than median, it's rank and percentile rank
 */
@Component({
  components: {
    SparkLine,
  },
})
export default class StatTile extends Vue {
  @Prop({ required: true }) building!: IBuilding;
  @Prop({ required: true }) statKey!: string;
  @Prop({ required: true }) stats!: IBuildingBenchmarkStats;
  @Prop({ required: true }) unit!: string;
  @Prop() historicData?: Array<IHistoricData>;

  readonly BuildingStatsByPropertyType: IStatsByPropertyType =
    buildingStatsByPropertyType;
  readonly RankConfig: typeof RankConfig = RankConfig;

  readonly ColsToHideComparison = [
    'DistrictSteamUse',
    'DistrictChilledWaterUse',
  ];

  /** The historical data for this stat, for passing to SparkLine */
  historicStatData: Array<INumGraphPoint> = [];

  /** The primary property type of the current building as it shows in the data */
  get propertyType(): string {
    return this.building['PrimaryPropertyType'];
  }

  /**
   * Whether a building is _fully_ gas free, meaning no gas burned on-site or to heat it
   * through a district heating system.
   *
   * We do not mark this as true if we have detected gas use in the past
   */
  get fullyGasFree(): boolean {
    return (
      !this.building.DataAnomalies.includes(
        DataAnomalies.gasZeroWithPreviousUse,
      ) &&
      this.building.NaturalGasUse === 0 &&
      this.building.DistrictSteamUse === 0
    );
  }

  /** The estimated cost for the given utility */
  get costEstimate(): number | null {
    if (this.statKey === 'ElectricityUse') {
      return estimateUtilitySpend(this.building[this.statKey], true);
    } else if (this.statKey === 'NaturalGasUse') {
      return estimateUtilitySpend(this.building[this.statKey], false);
    }

    return null;
  }

  /** TODO: Move this into a generic language helpers file */
  get pluralismForPropertyType(): string {
    let pluralismForProperty;
    let curPropertyType = this.propertyType;

    if (
      [
        'Adult Education',
        'Outpatient Rehabilitation/Physical Therapy',
        'Performing Arts',
        'Multifamily Housing',
      ].includes(curPropertyType)
    ) {
      pluralismForProperty = curPropertyType + ' Buildings';
    } else if (
      [
        'College/University',
        'Laboratory',
        'Mixed Use Property',
        'Residence Hall/Dormitory',
        'Residential Care Facility',
        'Senior Care Community',
        'Senior Living Community',
        'Worship Facility',
      ].includes(curPropertyType)
    ) {
      pluralismForProperty = curPropertyType.slice(0, -1) + 'ies';
    } else if (curPropertyType == 'Hospital (General Medical & Surgical)') {
      pluralismForProperty = 'Hospitals (General Medical & Surgical)';
    } else if (
      [
        'Other',
        'Other - Education',
        'Other - Entertainment/Public Assembly',
        'Other - Mall',
        'Other - Public Services',
        'Other - Recreation',
        'Other - Specialty Hospital',
      ].includes(curPropertyType)
    ) {
      pluralismForProperty = curPropertyType;
    } else {
      pluralismForProperty = curPropertyType + 's';
    }

    return pluralismForProperty;
  }

  get isAboveMedian(): boolean {
    return (
      this.building[this.statKey] !== null &&
      (this.building[this.statKey] as number) > this.stats[this.statKey].median
    );
  }

  /**
   * Whether this stat is > one standard deviation above the mean value (e.g. if GHG intensity has a
   * mean of 7.5 kg/sqft CO2e with a std of 5.5, values over 13 kg/sqft return true)
   */
  get isOneStdDeviationAboveMean(): boolean {
    const statStdDeviation = this.stats[this.statKey]?.std;
    const statMean = this.stats[this.statKey]?.mean;

    if (this.building[this.statKey] === null || !statStdDeviation) {
      return false;
    }

    return (
      (this.building[this.statKey] as number) > statMean + statStdDeviation
    );
  }

  // Square footage isn't directly climate related, so we show stats but treat it as
  // value-neutral - a building isn't worse _just_ because it's bigger
  get isSquareFootage(): boolean {
    return this.unit === 'sqft';
  }

  /**
   * Returns the multiplier for this building's stat compared to the median (e.g. '3' times median
   * '1/5' median)
   *
   * TODO: Move into a generic math helper
   */
  medianMultipleMsg(median: number, statValueNum: number): string | null {
    if (median) {
      const medianMult = statValueNum / median;

      // We can say 2.5x but 5.5x or 40.56x is a bit silly, just round
      if (medianMult > 5) {
        return Math.round(medianMult) + 'x';
      } else if (medianMult > 1) {
        return medianMult.toFixed(1) + 'x';
      } else if (medianMult < 0.5) {
        // If the multiple is < 1, make a fraction (e.g. 1/5 the median)
        return `1/${Math.round(1 / medianMult)}`;
      } else {
        return medianMult.toFixed(1) + 'x';
      }
    }

    return null;
  }

  // Returns the multiplier of the median across the whole city
  get medianMultipleMsgCityWide(): string | null {
    const median = this.stats[this.statKey].median;
    const statValueNum = parseFloat(this.building[this.statKey] as string);

    return this.medianMultipleMsg(median, statValueNum);
  }

  get medianMultiplePropertyType(): string | null {
    if (!this.BuildingStatsByPropertyType[this.propertyType]) {
      return null;
    }
    const median =
      this.BuildingStatsByPropertyType[this.propertyType][this.statKey]?.median;
    const statValueNum = parseFloat(this.building[this.statKey] as string);

    return this.medianMultipleMsg(median, statValueNum);
  }

// FIXED: ADD ROUNDING FOR BIG NUMBERS
  /** The stat value, as a string */              
  get statValueStr(): string {
    const rawValue = parseFloat(this.building[this.statKey] as string);
    if (rawValue < 1000) {
      return rawValue.toLocaleString();
    } else {
      const floorValue = Math.floor(rawValue);
      return floorValue.toLocaleString();
    }
  }

  // Returns a rounded number or undefined if no rank
  get statRank(): number | null {
    const statRank = this.building[this.statKey + 'Rank'] as string;

    if (statRank) {
      return Math.round(parseFloat(statRank));      
    } else {
      return null;
    }
  }

  // Returns the inverse of a rank, so the # lowest in a category
  // E.g rank #100 Highest/100 total in GHG intensity is #1 Lowest
  get statRankInverted(): number | null {
    if (this.statRank) {
      const countForStat = this.stats[this.statKey].count;

      // Rank 100/100 should invert to #1 lowest, not #0
      return countForStat - this.statRank + 1;
    }

    return null;
  }

  /** TODO: Move somewhere more generic */
  get propertiesToAwardThisType(): number {
    // The stats for buildings of this building's type
    const propertyStats = this.BuildingStatsByPropertyType[this.propertyType];

    if (!propertyStats) {
      return 0;
    }

    const numBuildingsOfType = propertyStats[this.statKey]?.count;

    /**
     * The amount of buildings we should give a category specific trophy or alarm to based on the
     * size of the category. E.g, 3: 1 means if we have >= 3 buildings of a type we give out a #1
     * best and #1 worst
     */
    const PropertiesToAwardByMinTypeSize: { [min: number]: number } = {
      3: 1,
      6: 2,
      9: 3,
      20: 5,
      50: 10,
      80: 15,
    };

    let amountToRank = 0;

    Object.entries(PropertiesToAwardByMinTypeSize).forEach(
      ([min, propToRank]) => {
        if (numBuildingsOfType >= parseInt(min)) {
          amountToRank = propToRank;
        }
      },
    );

    return amountToRank;
  }

  /**
   * Return the rank of a building in its property, IF it should be rendered
   */
  get propertyStatRank(): number | null {
    const statRank = this.building[
      this.statKey + 'RankByPropertyType'
    ] as string;

    if (statRank && parseFloat(statRank) <= this.propertiesToAwardThisType) {
      return Math.round(parseFloat(statRank));
    }

    return null;
  }

  /**
   * Returns the inverted rank (#X lowest) for a stat given its property type, IF
   * it should be rendered
   */
  get propertyStatRankInverted(): number | null {
    const propertyStats = this.BuildingStatsByPropertyType[this.propertyType];

    if (!propertyStats) {
      return null;
    }

    const numBuildingsOfType: number = propertyStats[this.statKey]?.count;
    const statRank = this.building[
      this.statKey + 'RankByPropertyType'
    ] as string;

    if (statRank) {
      const statRankNum = Math.round(parseFloat(statRank));
      // Rank 100/100 should invert to #1 lowest, not #0
      const rankInverted = numBuildingsOfType - statRankNum + 1;

      // Only return the inverted rank if it's bad enough for this category
      return rankInverted <= this.propertiesToAwardThisType
        ? rankInverted
        : null;
    }

    return null;
  }

  get rankLabel(): string | null {
    if (!this.statRank) {
      return null;
    }

    return getRankLabel(this.statRank, this.isSquareFootage);
  }

  get propertyRankLabel(): string | null {
    if (!this.propertyStatRank) {
      return null;
    }

    return getRankLabelByProperty(
      this.propertyStatRank,
      this.isSquareFootage,
      this.pluralismForPropertyType,
    );
  }

  // Returns a number 1 - 4 for how concerned we should be about this stat
  // 0 = outstanding performer in category
  // 1 = no concern
  // 2 = medium concern (above median)
  // 3 = high category (top 30 or > 1 std. deviation above the the mean)
  // 4 = very high concern (top 10 in category)
  get concernLevel(): number | null {
    // Some columns never show comparisons, because there's incomplete data (e.g. district steam and
    // district chilling)
    if (this.ColsToHideComparison.includes(this.statKey)) {
      return null;
    }

    // If an older building with no ranking on this stat, pretend its very low ranking and just run
    // checks against  the mean and median
    const statRank = this.statRank ?? 1000;

    // Very high concern if top 10
    if (statRank <= 10) {
      return 4;
      // High concern if top 30 or well above mean
    } else if (statRank <= 30 || this.isOneStdDeviationAboveMean) {
      return 3;
    } else if (this.isAboveMedian) {
      return 2;
    } else if (this.statRankInverted && this.statRankInverted >= 30) {
      return 1;
    } else if (this.statRankInverted && this.statRankInverted <= 30) {
      return 0;
    }

    return null;
  }

  get statRankPercent(): number | null {
    const statRankPercent = this.building[
      this.statKey + 'PercentileRank'
    ] as number;

    if (!statRankPercent) {
      return null;
    }

    return Math.round(statRankPercent * 100);
  }

  /** The component load */
  mounted(): void {
    if (this.historicData) {
      this.historicStatData = this.historicData.map((datum: IHistoricData) => ({
        x: parseInt(datum.DataYear),
        y: this.parseStatValueForGraph(datum),
      }));

      const zeroOrNanOnly = this.historicStatData.every(
        (datum) => datum.y === 0 || isNaN(datum.y),
      );

      if (zeroOrNanOnly) {
        this.historicStatData = [];
      }
    }
  }

  /**
   * Return the related stat value from the historic data, parsed as a float or rounded to an int.
   * If this is a very large number (> 100, like emissions), return an int, otherwise a float e.g.
   * GHG intensity)
   */
  parseStatValueForGraph(datum: IHistoricData): number {
    const statValFloat = parseFloat(
      datum[this.statKey as keyof IHistoricData] as string,
    );

    if (statValFloat > 1_000) {
      return Math.floor(statValFloat);
    } else {
      return statValFloat;
    }
  }
}
</script>

<style lang="scss">
.stat-tile {
  padding: 1rem;
  background-color: $off-white;
  // Use a bottom border to supplementally show how good this stat is
  border-bottom: solid 0.375rem $grey-dark;
  box-sizing: border-box;
  border-radius: $brd-rad-small;

  &.-very-bad {
    background-color: #ffd9d9;
    border-color: red;
  }
  &.-bad {
    background-color: #ffedf0;
    border-color: red;
  }
  // Also be pretty subtle for indicating medium attributes
  &.-medium {
    border-color: #935700;
  }
  // Very subtly highlight good attributes
  &.-good {
    border-color: green;
  }
  // Highlight best in class buildings
  &.-great {
    border-color: green;
    background-color: #e9ffe9;
  }
  // Square footage should override and clear anything since that's not really an
  // environmental factor, just an interesting stat
  &.-sq-footage {
    padding: 0;
    background-color: transparent;
    border: none;
  }

  .spark-graph-cont {
    width: 40%;
    max-width: 13rem;
    float: right;
    margin-left: 1rem;
  }

  .stat-value {
    font-size: 1.375rem;
    font-weight: bold;

    .unit {
      font-weight: normal;
      font-size: 1.125rem;
    }
    img {
      vertical-align: -0.25rem;
    }
  }

  // Apply a semi-bold to rank
  .rank {
    font-weight: 500;
  }

  .property-rank {
    font-size: small;
  }

  .bill-estimate {
    margin-bottom: 0.25rem;
    font-size: small;
  }

  .median-comparison {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin-top: 0.5rem;

    .median-mult {
      font-weight: 500;
      font-size: 0.875rem;
    }

    .median-val {
      font-size: 0.75rem;
      color: $text-mid-light;
      line-height: 1.25;
    }
    .median-label {
      font-size: 0.825rem;
      font-weight: 600;
    }
  }

  .median,
  .percentile {
    font-size: 0.75rem;
  }

  .percentile {
    font-weight: 500;
    margin-bottom: 0.25rem;
  }

  .empty-notice {
    font-size: 0.75rem;
  }

  .no-gas-msg {
    margin-top: 0.75rem;

    p {
      margin: 0.25rem 0 0;
    }
  }

  .no-stat-msg {
    font-size: 0.75rem;
    margin-bottom: 0;
  }

  /** Mobile styling */
  @media (max-width: $mobile-max-width) {
    .spark-graph-cont {
      width: 75%;
      float: none;
      margin: 0;
    }

    // Flip median comparison to row, with wrapping so very long property types (like
    // "Multifamily Housing") can stay in columns
    .median-comparison {
      flex-direction: row;
      gap: 0.25rem 1rem;
      flex-wrap: wrap;
    }
  }
}
</style>
