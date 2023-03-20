<template>
  <div class="rank-text">
    <div class="stat-value">
      <template v-if="round">{{ Math.round(statValue).toLocaleString() }}</template>
      <template v-else>{{ statValue.toFixed(1) }}</template>

      <!-- Show icons for below or above average if we have an average for this stat -->
      <template v-if="stats[statKey]">
        <img v-if="isAboveMedian"
          src="/arrow-up-bad.svg" width="20" title="Above Median Building" />
        <img v-else
          src="/arrow-down-good.svg" width="20" title="Below Median Building" />
      </template>
    </div>

    <div class="rank-label">
      <!-- Only show the rank if in the top 50, #102th highest _ doesn't mean much -->
      <div v-if="statRank && statRank <= 10" class="rank">
        <span class="rank-num">#{{ statRank }}</span> {{ rankLabel }}
      </div>
      <!-- Don't show percentile if the top 10, it'll just be 'Higher than 100%' -->
      <div v-else-if="statRankPercent" class="percentile">
        <!-- If stat rank is < 50%, invert it.
          E.g higher than of other buildings becomes less than 99% of buildings-->
        <template v-if="statRankPercent > 50">
          Highest {{ 100 - statRankPercent }}%
        </template>
        <template v-else>
          Lowest {{ statRankPercent }}%
        </template>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * A  tile that can show the stats for a building, including whether it's
 * doing better or worse than average, it's rank and percentile rank
 */
export default {
  name: 'RankText',
  props: {
    building: Object,
    round: Boolean,
    statKey: String,
    stats: Object,
  },
  computed: {
    isAboveMedian() {
      return this.building[this.statKey] &&
        this.building[this.statKey] > this.stats[this.statKey].median;
    },

    statValue() {
      return parseFloat(this.building[this.statKey]);
    },

    // Returns a rounded number or undefined if no rank
    statRank() {
      const statRank = this.building[this.statKey + 'Rank'];

      if (statRank) {
        return Math.round(parseFloat(statRank));
      } else {
        return undefined;
      }
    },

    rankLabel() {
      return `Highest`;
    },

    statRankPercent() {
      const statRankPercent = this.building[this.statKey + 'PercentileRank'];

      if (!statRankPercent) {
        return undefined;
      }

      return Math.round(statRankPercent * 100);
    },
  },
};
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

  .rank, .percentile { font-size: smaller; }

  .rank-label { margin-top: 0.25rem; }
}
</style>
