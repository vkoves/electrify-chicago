<template>
  <div class="overall-rank-emoji-cont" :class="{ '-large': largeView }">
    <!-- Don't show rankings if we think the data is wrong -->
    <span
      v-if="overallRank && !hasAnomalousData"
      class="emoji overall-rank-emoji"
      :title="overallRank.msg"
    >
      {{ overallRank.emoji }}
    </span>

    <!-- Show image emoji on tables -->
    <span
      v-if="hasBuildingImg && !largeView"
      class="emoji has-img-emoji"
      title="Has building photograph"
    >
      📷
    </span>

    <span
      v-if="isGasFree && !largeView"
      class="emoji has-img-emoji"
      title="All Electric!"
    >
      ⚡
    </span>

    <span
      v-if="hasNeverSubmitted && !largeView"
      class="emoji has-img-emoji"
      title="Building Never Submitted Data"
    >
      ❌
    </span>

    <span
      v-if="!hasNeverSubmitted && isOldData && !largeView"
      class="emoji has-img-emoji"
      title="Outdated data (did not submit in the latest year)"
    >
      🕰️
    </span>

    <span
      v-if="hasAnomalousData && !largeView"
      class="emoji"
      title="Has anomalous data, likely indicating reporting errors"
    >
      ⚠️
    </span>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import {
  fullyGasFree,
  getOverallRankEmoji,
  IBuilding,
  IBuildingBenchmarkStats,
} from '../common-functions.vue';
import { getBuildingImage } from '../constants/building-images.constant.vue';
import { LatestDataYear } from '../constants/globals.vue';

/**
 * A component that shows an emoji to summarize a building, showing the worse of the alarm or flag
 * emoji if those apply, or the trophy emoji if there's no flags and the building gets a trophy.
 *
 * Requires columns
 *
 * - DataAnomalies
 * - NaturalGasUse
 */
@Component
export default class OverallRankEmoji extends Vue {
  @Prop({ required: true }) building!: IBuilding;
  @Prop({ required: true }) stats!: IBuildingBenchmarkStats;

  /** Whether this is a large view of the emoji (e.g. in the title of the details page) */
  @Prop({ default: false }) largeView!: boolean;

  get overallRank(): { msg: string; emoji: string } | null {
    return getOverallRankEmoji(this.building, this.stats);
  }

  get hasBuildingImg(): boolean {
    return Boolean(getBuildingImage(this.building));
  }

  /** Whether this building's latest data is old, not matching the latest data year */
  get isOldData(): boolean {
    if (typeof this.building.DataYear === 'undefined') {
      return false;
    }

    return parseInt(this.building.DataYear.toString()) < LatestDataYear;
  }

  get hasAnomalousData(): boolean {
    if (typeof this.building.DataAnomalies === 'undefined') {
      throw new Error(
        'Building does not have DataAnomalies! Make sure to add it to GraphQL query',
      );
    }

    return this.building.DataAnomalies.length > 0;
  }

  get isGasFree(): boolean {
    return fullyGasFree(this.building);
  }

  get hasNeverSubmitted(): boolean {
    return this.building.FirstYearReported === null;
  }
}
</script>

<style lang="scss">
.overall-rank-emoji-cont {
  display: inline;

  .emoji {
    vertical-align: 0.1em;
    cursor: help;
    text-shadow: 0.0625rem 0.0625rem 0 rgba(0, 0, 0, 0.25);
  }

  .overall-rank-emoji {
    font-size: 0.925em;
  }

  &.-large {
    .overall-rank-emoji {
      font-size: 0.8em;
    }
  }
}
</style>
