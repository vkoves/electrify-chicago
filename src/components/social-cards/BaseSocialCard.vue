<template>
  <div class="social-card">
    <div class="social-card-content">
      <!-- Hero section with buildings background -->
      <div class="hero-section">
        <BuildingsHero :buildings="buildings" :buildings-count="8">
          <div class="hero-content">
            <slot name="hero-content" />
          </div>
        </BuildingsHero>
      </div>

      <!-- Logo section -->
      <div class="logo-section">
        <img src="/electrify-chicago-logo.svg" alt="Electrify Chicago" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IBuilding } from '../../common-functions.vue';
import BuildingsHero from '../BuildingsHero.vue';

@Component({
  components: {
    BuildingsHero,
  },
})
export default class BaseSocialCard extends Vue {
  @Prop({ required: true }) buildings!: Array<IBuilding>;
}
</script>

<style lang="scss" scoped>
.social-card {
  position: relative;
  width: 75rem;
  height: 39.375rem;
  background: $white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.social-card-content {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
}

.hero-section {
  flex: 1;
  position: relative;
  height: 100%;

  // Override BuildingsHero styles for social card dimensions
  :deep(.buildings-hero) {
    margin-bottom: 0;
    height: 100%;

    .hero-images {
      height: 100%;
      display: flex !important;
      flex-wrap: wrap;
      gap: 0;
      left: 0;
      width: 100%;

      .hero-image {
        flex: 1 1 25% !important; // Each image takes 25% width (4 per row)
        min-width: 0;

        img {
          width: 100%;
          height: 100%;
          aspect-ratio: 1 !important;
          object-fit: cover;
          // Make sure tall buildings show their tops
          object-position: 50% 10%;
        }
      }
    }

    .hero-skyline {
      height: 100% !important;
      
      img {
        height: 100% !important;
        width: 100% !important;
        object-fit: cover !important;
      }
    }

    .hero-overlay {
      padding: 4rem 4rem 8rem 4rem;

      .page-constrained {
        max-width: none;
        width: 100%;
      }
    }
  }
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.logo-section {
  position: absolute;
  right: 0;
  bottom: 0;
  padding: 1rem;
  border-top-left-radius: 1rem;
  z-index: 10;
  background-color: $white;

  img {
    display: block;
    height: 3rem;
  }
}
</style>