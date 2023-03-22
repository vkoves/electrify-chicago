<template>
  <div class="stat-tile" :class="{
    '-very-bad': concernLevel === 4,
    '-bad': concernLevel === 3,
    '-medium': concernLevel === 2,
    '-good': concernLevel === 1,
    '-great': concernLevel === 0,
    '-sq-footage': isSquareFootage,
  }">
  <template v-if="building[statKey]">
    <!-- The actual stat value-->
    <div class="stat-value">
      {{ statValue }} <span v-html="unit"/>

      <!-- Show icons for below or above median if we have a median for this stat -->
      <template v-if="stats[statKey]">
        <img v-if="isAboveMedian"
          :src="isSquareFootage ? '/arrow-up-neutral.svg' : '/arrow-up-bad.svg'"
          width="20" title="Above median building" />
        <img v-else
          :src="isSquareFootage ? '/arrow-down-neutral.svg' : '/arrow-down-good.svg'"
          width="20" title="Below median building" />
      </template>
    </div>

    <!-- Only show the rank if in the top 50, #102th highest _ doesn't mean much -->
    <div v-if="statRank && statRank <= RankConfig.FlagRankMax && rankLabel" class="rank">
      #{{ statRank }} {{ rankLabel }}
    </div>

    <!-- If in the lowest 30, show that unless square footage (TODO: Move to GreatRankMax) -->
    <div v-if="!isSquareFootage && statRankInverted
      && statRankInverted <= RankConfig.TrophyRankInvertedMax"
      class="rank">
        #{{ statRankInverted }} Lowest 🏆
    </div>

    <!-- Don't show percentile if the top 20, it'll just be 'Higher than 100%' -->
    <div v-if="typeof statRankPercent === 'number' && statRank > FlagRankMax" class="percentile">
      <!-- If stat rank is < 50%, invert it.
        E.g higher than of benchmarked buildings becomes less than 99% of buildings-->
        <template v-if="statRankPercent > 50">
          Higher than {{ statRankPercent }}% of others
        </template>
        <!-- Only show lower than X% if not getting a trophy-->
        <template v-else-if="statRankInverted > RankConfig.TrophyRankInvertedMax">
          <!-- Never show lower than 100%, top out at 100%-->
          Lower than {{ Math.min(99, 100 - statRankPercent) }}% of others
        </template>
      </div>

      <div v-if="medianMultipleMsg" class="median-comparison">
        <span class="val">{{ medianMultipleMsg }}</span> the median
      </div>

      <div  v-if="stats[statKey]" class="median">
        Median benchmarked building*: <br/>
        <div class="median-val">
          {{ stats[statKey].median.toLocaleString() }} <span v-html="unit"/>
        </div>
      </div>
    </template>
    <template v-else>
      Not Reported

      <p class="empty-notice">
        This data was not reported for this building. <br>
        This may mean a value of zero for this field.
      </p>
    </template>
  </div>
</template>

<script>
import {RankConfig, getRankLabel} from '../common-functions';

/**
  * A  tile that can show the stats for a building, including whether it's
  * doing better or worse than median, it's rank and percentile rank
  */
export default {
  name: 'StatTile',
  props: {
    building: Object,
    statKey: String,
    stats: Object,
    unit: String,
  },
  data: () => ({
    // Expose RankConfig to template
    RankConfig,
  }),
  computed: {
    isAboveMedian() {
      return this.building[this.statKey] &&
        this.building[this.statKey] > this.stats[this.statKey].median;
    },

    // Square footage isn't directly climate related, so we show stats but treat it as
    // value-neutral - a building isn't worse _just_ because it's bigger
    isSquareFootage() {
      return this.unit === 'sqft';
    },

    /**
     * Returns the multipier for this building's stat compared to the median (e.g. '3' times median
     * '1/5' median)
     *
     * @return {string|null}
     */
    medianMultipleMsg() {
      const median = this.stats[this.statKey].median;
      const statValueNum = parseFloat(this.building[this.statKey]);

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
        return null;
      }
    },

    // Returns the inverse of a rank, so the # lowest in a category
    // E.g rank #100 Highest/100 total in GHG intensity is #1 Lowest
    statRankInverted() {
      if (this.statRank) {
        const countForStat = this.stats[this.statKey].count;

        // Rank 100/100 should invert to #1 lowest, not #0
        return countForStat - this.statRank + 1;
      }

      return null;
    },

    rankLabel() {
      return getRankLabel(this.statRank, this.isSquareFootage);
    },

    // Returns a number 1 - 4 for how concerned we should be about this stat
    // 0 = outstanding performer in category
    // 1 = no concern
    // 2 = medium concern (above median)
    // 3 = high category (top 30)
    // 4 = very high concern (top 10 in category)
    concernLevel() {
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
      } else if (this.statRankInverted >= 30 && this.building[this.statKey]) {
        return 1;
      } else if (this.statRankInverted <= 30) {
        return 0;
      }

      return null;
    },

    statRankPercent() {
      const statRankPercent = this.building[this.statKey + 'PercentileRank'];

      if (!statRankPercent) {
        return null;
      }

      return Math.round(statRankPercent * 100);
    },
  },
};
</script>

<style lang="scss">
.stat-tile {
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

  .median-comparison {
    font-size: 0.75rem;

    .val {
      font-size: 0.875rem;
      font-weight: bold;
    }
  }

  .median, .percentile { font-size: 0.75rem; }

  .median {
    margin-top: 0.5rem;

    .median-val {
      font-weight: 500;
      font-size: larger;
    }
  }

  .percentile {
    font-weight: normal;
    margin-bottom: 0.25rem;
  }

  .empty-notice {
    font-size: 0.75rem;
  }
}
</style>
