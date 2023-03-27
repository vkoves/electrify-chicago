<template>
  <div
    v-if="overallRank"
    class="overall-rank-emoji-cont"
    :class="{ '-large': largeView }"
  >
    <span
      class="overall-rank-emoji"
      :title="overallRank.msg"
    >
      {{ overallRank.emoji }}
    </span>

    <!-- Show image emoji on tables -->
    <span
      v-if="hasBuildingImg && !largeView"
      class="has-img-emoji"
      title="Has Image"
    >
      📷
    </span>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import {getOverallRankEmoji, IBuilding, IBuildingBenchmarkStats} from '~/common-functions.vue';
import { getBuildingImage } from '../constants/building-images.constant.vue';

/**
 * A component that shows an emoji to summarize a building, showing the worse of the alarm or flag
 * emoji if those apply, or the trophy emoji if there's no flags and the building gets a trophy
 */
@Component
export default class OverallRankEmoji extends Vue {
  @Prop({required: true}) building!: IBuilding;
  @Prop({required: true}) stats!: IBuildingBenchmarkStats;

  /** Whether this is a large view of the emoji (e.g. in an <h1> on the details page) */
  @Prop({default: false}) largeView!: boolean;

  get overallRank(): { msg: string, emoji: string } | null {
    return getOverallRankEmoji(this.building, this.stats);
  }

  get hasBuildingImg(): boolean {
    return Boolean(getBuildingImage(this.building));
  }
}
</script>

<style lang="scss">
.overall-rank-emoji-cont {
  display: inline;
  white-space: nowrap;

  .overall-rank-emoji, .has-img-emoji {
    vertical-align: 0.2em;
  }

  .overall-rank-emoji { font-size: 0.925em; }

  &.-large {
    .overall-rank-emoji { font-size: 0.8em; }
  }
}
</style>
