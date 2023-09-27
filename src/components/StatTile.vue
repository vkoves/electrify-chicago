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
    <template v-if="building[statKey]">
      <!-- The actual stat value-->
      <div class="stat-value">
        {{ statValue }} <span v-html="unit" />

        <!-- Show icons for below or above median if we have a median for this stat -->
        <template v-if="stats[statKey]">
          <img
            v-if="isAboveMedian"
            :src="isSquareFootage ? '/arrow-up-neutral.svg' : '/arrow-up-bad.svg'"
            width="20"
            title="Above median building"
          >
          <img
            v-else
            :src="isSquareFootage ? '/arrow-down-neutral.svg' : '/arrow-down-good.svg'"
            width="20"
            title="Below median building"
          >
        </template>
      </div>

      <div v-if="costEstimate">
        Estimated Cost: ${{ Math.round(costEstimate).toLocaleString() }}
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
        v-if="propertyStatRank && propertyStatRank <= RankConfig.FlagRankMax && propertyRankLabel"
        class="property-rank"
      >
        #{{ propertyStatRank }} {{ propertyRankLabel }}
      </div>

      <!-- If in the lowest 30, show that unless square footage (TODO: Move to GreatRankMax) -->
      <div
        v-if="!isSquareFootage && statRankInverted
          && statRankInverted <= RankConfig.TrophyRankInvertedMax"
        class="rank"
      >
        #{{ statRankInverted }} Lowest in Chicago* 🏆
      </div>

      <!-- If in the lowest 30, show that unless square footage (TODO: Move to GreatRankMax) -->
      <div
        v-if="!isSquareFootage && propertyStatRankInverted"
        class="property-rank"
      >
        #{{ propertyStatRankInverted }} Lowest of {{ pluralismForPropertyType }} 🏆
      </div>

      <!-- Only show percentile if we don't have a flag or alarm -->
      <div
        v-if="typeof statRankPercent === 'number' && statRank > RankConfig.FlagRankMax"
        class="percentile"
      >
        <!-- If stat rank is < 50%, invert it.
        E.g higher than of benchmarked buildings becomes less than 99% of buildings-->
        <template v-if="statRankPercent > 50">
          Higher than {{ statRankPercent }}% of all buildings
        </template>
        <!-- Only show lower than X% if not getting a trophy-->
        <template v-else-if="statRankInverted > RankConfig.TrophyRankInvertedMax">
          <!-- Never show lower than 100%, top out at 100%-->
          Lower than {{ Math.min(99, 100 - statRankPercent) }}% of all buildings
        </template>
      </div>

      <div
        v-if="medianMultipleMsgCityWide"
        class="median-comparison"
      >
        <div>
          <!-- Only show median multiple if value is > 0, otherwise it's 1/infinity -->
          <span
            v-if="stats[statKey] > 0"
            class="val"
          >
            {{ medianMultipleMsgCityWide }} median
          </span>
          <span v-else>
            Median Chicago Building
          </span>

          <div class="median-val">
            {{ stats[statKey].median.toLocaleString() }}
            <span v-html="unit" />
          </div>
        </div>

        <div v-if="medianMultiplePropertyType">
          <!-- Only show median multiple if value is > 0, otherwise it's 1/infinity -->
          <span
            v-if="stats[statKey] > 0"
            class="val"
          >
            {{ medianMultiplePropertyType }} median {{ propertyType }}
          </span>
          <span v-else>
            Median {{ propertyType }}
          </span>

          <div class="median-val">
            {{ BuildingStatsByPropertyType[propertyType][statKey].median.toLocaleString() }}
            <span v-html="unit" />
          </div>
        </div>
      </div>
      <p
        v-else
        class="no-stat-msg"
      >
        Most buildings don't use
        <span v-if="statKey === 'DistrictSteamUse'">district steam</span>
        <span v-else-if="statKey === 'DistrictChilledWaterUse'">district chilling</span>
        <span v-else>this</span>,
        so we don't currently have comparison data.
      </p>

      <!-- Natural Gas specific message -->
      <div
        v-if="statValue === '0' && statKey === 'NaturalGasUse'"
        class="no-gas-msg"
      >
        <div v-if="fullyGasFree">
          <div class="bold">
            This Building Didn't Burn Any Natural Gas! 🎉
          </div>

          <p class="smaller">
            This building burned no natural gas on-site and isn't connected to a district heating
            system, meaning it's fully electric!
          </p>
        </div>
        <div v-else>
          <div class="bold">
            This Building Uses District Heating ❗
          </div>

          <p class="smaller">
            Although this building didn't burn any natural gas on site, it's connected to a district
            heating system, a centralized system for heating multiple buildings. District heating
            systems can be fully electric, but in Chicago most district heating systems are natural
            gas powered, meaning this building was most likely still heated with natural gas.
          </p>
        </div>
      </div>
    </template>
    <template v-else>
      Not Reported

      <p class="empty-notice">
        This data was not reported for this building, which <em>likely</em> means a value of zero
        for this field.
      </p>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import buildingStatsByPropertyType from "../data/dist/building-statistics-by-property-type.json";

import {
  estimateUtilitySpend,
  getRankLabel,
  getRankLabelByProperty,
  IBuilding,
  IBuildingBenchmarkStats,
  RankConfig,
} from '~/common-functions.vue';

export interface PropertyByBuildingStats
{
  [propertyType: string]: IBuildingBenchmarkStats;
}

/**
  * A  tile that can show the stats for a building, including whether it's
  * doing better or worse than median, it's rank and percentile rank
  */
@Component
export default class StatTile extends Vue {
  readonly BuildingStatsByPropertyType:PropertyByBuildingStats = buildingStatsByPropertyType;

  @Prop({required: true}) building!: IBuilding;
  @Prop({required: true}) statKey!: string;
  @Prop({required: true}) stats!: IBuildingBenchmarkStats;
  @Prop({required: true}) unit!: string;

  // Expose RankConfig to template
  RankConfig = RankConfig;

  /** The primary property type of the current building as it shows in the data */
  get propertyType(): string {
    return this.building["PrimaryPropertyType"];
  }


  /**
   * Whether a building is _fully_ gas free, meaning no natural gas burned on-site or to heat it
   * through a district heating system.
   */
  get fullyGasFree(): boolean {
    return parseFloat(this.building.NaturalGasUse) === 0
      && parseFloat(this.building.DistrictSteamUse) === 0;
  }

  /** The estimated cost for the given utility */
  get costEstimate(): number | null {
    if (this.statKey === 'ElectricityUse') {
      console.log('statValue', this.building[this.statKey]);

      return estimateUtilitySpend(parseFloat(this.building[this.statKey] as string), true);
    }
    else if (this.statKey === 'NaturalGasUse') {
      console.log('statValue', this.building[this.statKey]);

      return estimateUtilitySpend(parseFloat(this.building[this.statKey] as string), false);
    }

    return null;
  }

  get pluralismForPropertyType(): string {
    let pluralismForProperty;
    let curPropertyType = this.propertyType;

    if (["Adult Education", "Outpatient Rehabilitation/Physical Therapy", "Performing Arts",
      "Multifamily Housing"].includes(curPropertyType))
    {
      pluralismForProperty = curPropertyType + " Buildings";
    }
    else if (["College/University", "Laboratory", "Mixed Use Property",
      "Residence Hall/Dormitory", "Residential Care Facility", "Senior Care Community",
      "Senior Living Community", "Worship Facility"].includes(curPropertyType))
    {
      pluralismForProperty = curPropertyType.slice(0, -1) + "ies";
    }
    else if (curPropertyType == "Hospital (General Medical & Surgical)")
    {
      pluralismForProperty = "Hospitals (General Medical & Surgical)";
    }
    else if (["Other", "Other - Education", "Other - Entertainment/Public Assembly",
      "Other - Mall", "Other - Public Services", "Other - Recreation",
      "Other - Specialty Hospital"].includes(curPropertyType))
    {
      pluralismForProperty = curPropertyType;
    }
    else
    {
      pluralismForProperty = curPropertyType + "s";
    }

    return pluralismForProperty;
  }

  get isAboveMedian(): boolean {
    return this.building[this.statKey] !== null &&
      this.building[this.statKey] as number > this.stats[this.statKey].median;
  }

  // Square footage isn't directly climate related, so we show stats but treat it as
  // value-neutral - a building isn't worse _just_ because it's bigger
  get isSquareFootage(): boolean {
    return this.unit === 'sqft';
  }

  /**
   * Returns the multiplier for this building's stat compared to the median (e.g. '3' times median
   * '1/5' median)
   */
  medianMultipleMsg(median:number, statValueNum:number): string | null {
    if (median) {
      const medianMult = statValueNum / median;

      // We can say 2.5x but 5.5x or 40.56x is a bit silly, just round
      if (medianMult > 5) {
        return Math.round(medianMult) + 'x';
      } else if (medianMult > 1) {
        return medianMult.toFixed(1) + 'x';
      } else if (medianMult < 0.5) {
        // If the multiple is < 1, make a fraction (e.g. 1/5 the median)
        return `1/${Math.round(1 / medianMult )}`;
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
    const median = this.BuildingStatsByPropertyType[this.propertyType][this.statKey]?.median;
    const statValueNum = parseFloat(this.building[this.statKey] as string);

    return this.medianMultipleMsg(median, statValueNum);
  }

  get statValue(): string {
    return parseFloat(this.building[this.statKey] as string).toLocaleString();
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

  get propertiesToAwardThisType(): number {
    const properStatBlock = this.BuildingStatsByPropertyType[this.propertyType];
    const numBuildingsOfType = properStatBlock[this.statKey]?.count;

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

    Object.entries(PropertiesToAwardByMinTypeSize).forEach(([min, propToRank]) => {
      if (numBuildingsOfType >= parseInt(min)) {
        amountToRank = propToRank;
      }
    });

    return amountToRank;
  }

  /**
   * Return the rank of a building in its property, IF it should be rendered
   */
  get propertyStatRank(): number | null {
    const statRank = this.building[this.statKey + 'RankByPropertyType'] as string;

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
    const properStatBlock = this.BuildingStatsByPropertyType[this.propertyType];
    const numBuildingsOfType: number = properStatBlock[this.statKey]?.count;
    const statRank = this.building[this.statKey + 'RankByPropertyType'] as string;

    if (statRank) {
      const statRankNum = Math.round(parseFloat(statRank));
      // Rank 100/100 should invert to #1 lowest, not #0
      const rankInverted =  numBuildingsOfType - statRankNum + 1;

      // Only return the inverted rank if it's bad enough for this category
      return rankInverted <= this.propertiesToAwardThisType ? rankInverted : null;
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

    return getRankLabelByProperty(this.propertyStatRank, this.isSquareFootage,
      this.pluralismForPropertyType);
  }

  // Returns a number 1 - 4 for how concerned we should be about this stat
  // 0 = outstanding performer in category
  // 1 = no concern
  // 2 = medium concern (above median)
  // 3 = high category (top 30)
  // 4 = very high concern (top 10 in category)
  get concernLevel(): number | null {
    // Return null if we have no stats
    if (!this.statRank) {
      return null;
    }

    if (this.statRank <= 10) {
      return 4;
    } else if (this.statRank <= 30) {
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
    const statRankPercent = this.building[this.statKey + 'PercentileRank'] as number;

    if (!statRankPercent) {
      return null;
    }

    return Math.round(statRankPercent * 100);
  }
}
</script>

<style lang="scss">
.stat-tile {
  padding: 1rem;
  background-color: #f5f5f5;
  border: solid 0.01625rem $grey-dark;
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
  &.-good { border-color: green; }

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

  .stat-value {
    font-size: 1.375rem;
    font-weight: bold;

    img { vertical-align: -0.25rem; }
  }

  // Apply a semi-bold to rank
  .rank { font-weight: 500; }

  .property-rank { font-size: small; }

  .median-comparison {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.25rem;

    .val {
      font-size: large;
      font-weight: 500;
    }

    .median-val { font-size: small; }
  }

  .median, .percentile { font-size: 0.75rem; }

  .percentile {
    font-weight: normal;
    margin-bottom: 0.25rem;
  }

  .empty-notice {
    font-size: 0.75rem;
  }

  .no-gas-msg {
    margin-top: 0.75rem;

    p { margin: 0.25rem 0 0; }
  }

  .no-stat-msg {
    font-size: 0.75rem;
    margin-bottom: 0;
  }
}
</style>
