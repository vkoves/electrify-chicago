<template>
  <div class="stat-tile" :class="{
    '-very-bad': concernLevel === 4,
    '-bad': concernLevel === 3,
    '-medium': concernLevel === 2,
    '-good': concernLevel === 1,
    '-sq-footage': unit === 'sqft',
  }">
  <template v-if="building[statKey]">
    <!-- The actual stat value-->
    <div class="stat-value">
      {{ statValue }} <span v-html="unit"/>

      <!-- Show icons for below or above average if we have an average for this stat -->
      <template v-if="stats[statKey]">
        <img v-if="isAboveAverage"
          src="/arrow-up-bad.svg" width="20" title="Above Average" />
        <img v-else
          src="/arrow-down-good.svg" width="20" title="Below Average" />
      </template>
    </div>

    <!-- Only show the rank if in the top 50, #102th highest _ doesn't mean much -->
    <div v-if="statRank && statRank <= 50" class="rank">
      #{{ statRank }} {{ rankLabel }}
    </div>

    <!-- Don't show percentile if the top 20, it'll just be 'Higher than 100%' -->
    <div v-if="statRankPercent && statRank > 20" class="percentile">
      <!-- If stat rank is < 50%, invert it.
        E.g higher than of other buildings becomes less than 99% of buildings-->
        <template v-if="statRankPercent > 50">
          Higher than {{ statRankPercent }}% of other buildings
        </template>
        <template v-else>
          Lower than {{ 100 - statRankPercent }}% of other buildings
        </template>
      </div>

      <div class="average" v-if="stats[statKey]">
        Average benchmarked building: <br/>
        {{ stats[statKey].mean.toLocaleString() }} <span v-html="unit"/><br/>
      </div>
    </template>
    <template v-else>
      ?
    </template>
  </div>
</template>

<script>
/**
  * A  tile that can show the stats for a building, including whether it's
  * doing better or worse than average, it's rank and percentile rank
  */
export default {
  name: 'StatTile',
  props: {
    building: Object,
    statKey: String,
    stats: Object,
    unit: String,
  },
  computed: {
    isAboveAverage() {
      return this.building[this.statKey] &&
        this.building[this.statKey] > this.stats[this.statKey].mean;
    },

    statValue() {
      return parseFloat(this.building[this.statKey]).toLocaleString();
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
      if (this.unit === 'sqft') {
        return 'Largest';
      } else if (this.statRank <= 10) {
        return 'Highest in Chicago 🚨 ';
      } else {
        return 'Highest in Chicago 🚩';
      }
    },

    // Returns a number 1 - 4 for how concerned we should be about this stat
    // 1 = no concern
    // 2 = medium concern (above average)
    // 3 = high category (top 30)
    // 4 = very high concern (top 10 in category)
    concernLevel() {
      if (this.statRank <= 10) {
        return 4;
      } else if (this.statRank <= 30) {
        return 3;
      } else if (this.isAboveAverage) {
        return 2;
      } else if (this.building[this.statKey]) {
        return 1;
      } else {
        // Return 0 if we have no value
        return 0;
      }
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
.stat-tile {
  min-width: 18rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border: solid 0.01625rem $grey-dark;
  box-sizing: border-box;
  border-radius: 0.25rem;

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

  // Square footage should override and clear anything since that's not really an
  // environmental factor, just an interesting stat
  &.-sq-footage {
    padding: 0;
    background-color: transparent;
    border: none;
  }

  .stat-value {
    font-size: 1.25rem;

    img { vertical-align: -0.25rem; }
  }

  .rank {
    font-weight: bold;
  }

  .average, .percentile { font-size: 0.75rem; }

  .average { margin-top: 0.5rem; }

  .percentile {
    font-weight: normal;
    margin-bottom: 0.25rem;
  }
}
</style>
