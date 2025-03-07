<template>
  <div
    v-if="buildingImg"
    class="building-img-cont"
    :class="{ '-tall': Boolean(buildingImg.isTall) }"
  >
    <!-- TODO: Figure out how to do alt text for these images - skipping for now -->
    <img :src="buildingImg.imgUrl" alt="" />

    <p class="attribution -no-margin">
      <strong>Attribution:</strong>
      {{ buildingImg.fromGoogleMaps ? '© Google ' + currentYear : '' }}
      <a ref="noopener" :href="buildingImg.attributionUrl" target="_blank">
        Image Source
        <NewTabIcon /> </a
      >. Cropped from original.
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import { IBuilding } from '../common-functions.vue';
import {
  getBuildingImage,
  IBuildingImage,
} from '../constants/building-images.constant.vue';
import NewTabIcon from './NewTabIcon.vue';

/**
 * A component that given a building shows the logo of its owner if one is set in
 * BuildingsCustomInfo
 */
@Component({
  components: {
    NewTabIcon,
  },
})
export default class BuildingImage extends Vue {
  @Prop({ required: true }) building!: IBuilding;

  /**
   * Returns the image object associated with this image
   */
  get buildingImg(): IBuildingImage | null {
    return getBuildingImage(this.building);
  }

  get currentYear(): number {
    return new Date().getFullYear();
  }
}
</script>

<style lang="scss">
.building-img-cont {
  &.-tall {
    text-align: right;

    img {
      max-height: 35rem;
    }
    p {
      text-align: left;
    }
  }

  img {
    border-radius: $brd-rad-medium;
    max-height: 25rem;
  }

  .attribution {
    font-size: 0.75rem;
    margin-top: 0.25rem;
  }

  @media (max-width: $mobile-max-width) {
    &.-tall {
      text-align: left;
    }
  }
}
</style>
