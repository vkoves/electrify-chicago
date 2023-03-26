<template>
  <span v-if="overallRank">
    <span
      class="overall-rank-emoji"
      :title="overallRank.msg"
    >
      {{ overallRank.emoji }}
    </span>
  </span>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import {getOverallRankEmoji, IBuilding, IBuildingBenchmarkStats} from '~/common-functions.vue';

/**
 * A component that shows an emoji to summarize a building, showing the worse of the alarm or flag
 * emoji if those apply, or the trophy emoji if there's no flags and the building gets a trophy
 */
@Component
export default class OverallRankEmoji extends Vue {
  @Prop({required: true}) building!: IBuilding;
  @Prop({required: true}) stats!: IBuildingBenchmarkStats;

  get overallRank(): { msg: string, emoji: string } | null {
    return getOverallRankEmoji(this.building, this.stats);
  }
}
</script>

<style lang="scss">
.overall-rank-emoji {
  font-size: 0.8em;
  vertical-align: 0.2em;
}
</style>
