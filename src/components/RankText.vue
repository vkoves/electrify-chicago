<template>
  <div class="rank-text">
    <div class="stat-value">
      <span v-if="shouldRound">{{ Math.round(statValue).toLocaleString() }}</span>
      <span v-else>{{ statValue.toFixed(1) }}</span>

      <!-- Show icons for below or above average if we have an average for this stat -->
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

    <div class="rank-label">
      <!-- Only show the rank if in the top 50, #102th highest _ doesn't mean much -->
      <div
        v-if="statRank && statRank <= RankConfig.FlagRankMax"
        class="rank"
      >
        <span class="rank-num">#{{ statRank }}</span> {{ rankLabel }}
      </div>
      <!-- Don't show percentile if the top 10, it'll just be 'Higher than 100%' -->
      <div
        v-else-if="typeof statRankPercent === 'number'"
        class="percentile"
      >
        <!-- If stat rank is < 50%, invert it.
          E.g higher than of other buildings becomes less than 99% of buildings-->
        <template v-if="statRankPercent > 50">
          Highest {{ 100 - statRankPercent }}%
        </template>
        <!-- Show lowest 30 instead of percentiles -->
        <template v-else-if="statRankInverted <= RankConfig.TrophyRankInvertedMax">
          #{{ statRankInverted }} Lowest
        </template>
        <template v-else>
          <!-- Never show Lowest 0%, show Lowest 1% -->
          Lowest {{ Math.max(statRankPercent, 1) }}%
        </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import { RankConfig, IBuilding, IBuildingBenchmarkStats } from '~/common-functions';

/**
 * A  tile that can show the stats for a building, including whether it's
 * doing better or worse than average, it's rank and percentile rank
 */
@Component
export default class RankText extends Vue {
  @Prop({required: true}) building!: IBuilding;
  @Prop({required: true}) statKey!: string;
  @Prop({required: true}) stats!: IBuildingBenchmarkStats;
  @Prop({default: false}) shouldRound!: boolean;

  // Expose RankConfig to template
  RankConfig = RankConfig;

  get isAboveMedian(): boolean {
    return typeof this.building[this.statKey] &&
      this.building[this.statKey] as number > this.stats[this.statKey].median;
  }

  get isSquareFootage(): boolean {
    return this.statKey === 'GrossFloorArea';
  }

  get statValue(): number {
    return parseFloat(this.building[this.statKey] as string);
  }

  // Returns a rounded number or null if no rank
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
      const countForStat = this.stats[this.statKey]?.count;

      // Rank 100/100 should invert to #1 lowest, not #0
      return countForStat - this.statRank + 1;
    }

    return null;
  }

  get rankLabel(): string {
    return `Highest`;
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
.rank-text {
  .stat-value {
    white-space: nowrap;

    img {
      width: 1.25em;
      margin-right: -0.5rem;
      vertical-align: -0.25em;
    }
  }

  .rank, .percentile { font-size: x-small; }

  .rank-label { margin-top: 0.25rem; }
}
</style>
