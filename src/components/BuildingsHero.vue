<template>
  <div class="buildings-hero">
    <div
      v-if="buildingsWithImages.length > 0"
      class="hero-images"
      :class="{ 'few-buildings': displayedBuildings.length < buildingsCount }"
    >
      <div
        v-for="building in displayedBuildings"
        :key="String(building.ID)"
        class="hero-image"
      >
        <img
          :src="getBuildingImage(building)?.imgUrl"
          :alt="`${building.PropertyName || building.Address}`"
        />
      </div>
    </div>
    <div v-else class="hero-skyline">
      <img src="/home/skyline-1920.webp" alt="Chicago skyline" />
    </div>
    <div class="hero-overlay">
      <slot />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import { IBuilding } from '../common-functions.vue';
import { getBuildingImage } from '../constants/building-images.constant.vue';

/**
 * BuildingsHero component - displays a row of building images as a hero section
 *
 * Takes an array of buildings and shows the first N buildings that have images,
 * displaying them in an attractive row layout perfect for showcasing featured buildings.
 */
@Component({})
export default class BuildingsHero extends Vue {
  @Prop({ required: true }) buildings!: Array<IBuilding>;
  @Prop({ default: 8 }) buildingsCount!: number;

  /**
   * Import the getBuildingImage function to use in template
   */
  getBuildingImage = getBuildingImage;

  /**
   * Get buildings that have images available
   */
  get buildingsWithImages(): Array<IBuilding> {
    return this.buildings.filter(
      (building) => getBuildingImage(building) !== null,
    );
  }

  /**
   * Get buildings that have tall images available
   */
  get buildingsWithTallImages(): Array<IBuilding> {
    return this.buildings.filter((building) => {
      const buildingImg = getBuildingImage(building);
      return buildingImg !== null && buildingImg.isTall === true;
    });
  }

  /**
   * Get the buildings to display (limited by buildingsCount)
   * Prioritizes tall images if we can meet the target count with just tall images
   */
  get displayedBuildings(): Array<IBuilding> {
    // If we have enough tall images to meet the target, use only tall images
    if (this.buildingsWithTallImages.length >= this.buildingsCount) {
      return this.buildingsWithTallImages.slice(0, this.buildingsCount);
    }
    // Otherwise, fall back to all available images
    return this.buildingsWithImages.slice(0, this.buildingsCount);
  }
}
</script>

<style lang="scss" scoped>
@import '~/scss/global.scss';

.buildings-hero {
  margin: 2rem 0;
  position: relative;
  border-radius: $brd-rad-medium;
  overflow: hidden;

  .hero-images {
    display: flex;
    overflow: hidden;
    height: 18rem; // Fixed height to match skyline

    .hero-image {
      flex: 1;

      img {
        width: 100%;
        height: 100%;
        min-width: 7.5rem; // 120px minimum
        aspect-ratio: 1/2;
      }
    }

    &.few-buildings .hero-image .image-link img {
      aspect-ratio: unset; // Remove aspect ratio constraint when there are few buildings
    }
  }

  .hero-skyline {
    img {
      width: 100%;
      height: 18rem; // Same height as building images (aspect-ratio 1/2 * 11.25rem * 4)
    }
  }

  img {
    object-fit: cover;
    display: block;
    filter: brightness(80%);
  }

  .hero-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(
      to top,
      rgba(0, 0, 0, 0.8) 0%,
      transparent 100%
    );
    padding: 2rem 1rem 1rem;
    color: white;

    h1,
    h2 {
      margin: 0;
      font-size: 1.75rem;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
  }

  // Mobile responsive adjustments
  @media (max-width: $mobile-max-width) {
    .hero-images {
      height: 17.5rem; // Reduce height on mobile

      .hero-image .image-link img {
        min-width: 6rem; // 96px minimum on mobile
      }
    }

    .hero-skyline img {
      height: 17.5rem; // Reduce height on mobile
    }

    .hero-overlay {
      padding: 1.5rem 0.75rem 0.75rem;

      h1,
      h2 {
        font-size: 1.5rem;
      }
    }
  }

  @media (max-width: $small-mobile-max-width) {
    .hero-images {
      height: 15rem; // Further reduce height on small mobile

      .hero-image .image-link img {
        min-width: 5rem; // 80px minimum on small mobile
      }
    }

    .hero-skyline img {
      height: 15rem; // Further reduce height on small mobile
    }

    .hero-overlay {
      padding: 1rem 0.5rem 0.5rem;

      h1,
      h2 {
        font-size: 1.25rem;
      }
    }
  }
}
</style>
