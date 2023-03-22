<template>
    <span v-if="overallRank">
        <span class="overall-rank-emoji" :title="overallRank.msg">
            {{ overallRank.emoji }}
        </span>
    </span>
</template>

<script>
import {getOverallRankEmoji} from '../common-functions';

/**
 * A component that shows an emoji to summarize a building, showing the worse of the alarm or flag
 * emoji if those apply, or the trophy emoji if there's no flags and the building gets a trophy
 */
export default {
  name: 'OverallRankEmoji',
  props: {
    building: Object,
    stats: Object,
  },
  methods: {
    // Expose getOverallRankEmoji to template
    getOverallRankEmoji,
  },
  computed: {
    overallRank() {
      return getOverallRankEmoji(this.building, this.stats);
    },
  },
};
</script>

<style lang="scss">
.overall-rank-emoji {
  font-size: 0.8em;
  vertical-align: 0.2em;
}
</style>
