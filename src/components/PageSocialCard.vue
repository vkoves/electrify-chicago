<template>
  <div class="page-social-card">
    <div class="page-social-card-content">
      <!-- Hero section with buildings -->
      <div class="hero-section">
        <BuildingsHero :buildings="buildings" :buildings-count="8">
          <div class="hero-content">
            <h1 class="page-title">{{ pageTitle }}</h1>
            <p v-if="pageDescription" class="page-description">
              {{ pageDescription }}
            </p>
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
import { Component, Vue } from 'vue-property-decorator';
import { IBuilding } from '../common-functions.vue';
import BuildingsHero from './BuildingsHero.vue';

interface IPageSocialConfig {
  id: string;
  title: string;
  description?: string;
  filter?: 'best' | 'worst' | 'largest';
}

@Component({
  components: {
    BuildingsHero,
  },
})
export default class PageSocialCard extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  $page!: {
    allBuilding: {
      edges: Array<{ node: IBuilding }>;
    };
  };

  /** Get the current page configuration from parent */
  get pageConfig(): IPageSocialConfig {
    return (
      (this.$parent as any).pageConfig || {
        id: 'default',
        title: 'Electrify Chicago',
        description: 'Explore Chicago building energy data',
        filter: 'largest',
      }
    );
  }

  /** Get page title */
  get pageTitle(): string {
    return this.pageConfig.title;
  }

  /** Get page description */
  get pageDescription(): string | null {
    return this.pageConfig.description || null;
  }

  /** Get buildings for the hero section */
  get buildings(): Array<IBuilding> {
    const allBuildings = this.$page.allBuilding.edges.map((edge) => edge.node);

    // Apply filtering based on page ID
    const pageId = this.pageConfig.id;

    switch (pageId) {
      case 'top-emitters':
        return allBuildings
          .sort(
            (a, b) => (b.TotalGHGEmissions || 0) - (a.TotalGHGEmissions || 0),
          )
          .slice(0, 50);

      case 'biggest-buildings':
        return allBuildings
          .sort((a, b) => (b.GrossFloorArea || 0) - (a.GrossFloorArea || 0))
          .slice(0, 50);

      case 'all-electric':
        return allBuildings
          .filter(
            (b) =>
              (b.NaturalGasUse || 0) <= 0 && (b.DistrictSteamUse || 0) <= 0,
          )
          .sort((a, b) => (b.GrossFloorArea || 0) - (a.GrossFloorArea || 0))
          .slice(0, 50);

      case 'cleanest-buildings':
        return allBuildings
          .filter(
            (b) =>
              b.AvgPercentileLetterGrade === 'A' ||
              b.AvgPercentileLetterGrade === 'B',
          )
          .sort(
            (a, b) =>
              (a.GHGIntensity || Infinity) - (b.GHGIntensity || Infinity),
          )
          .slice(0, 50);

      case 'top-gas-users':
        return allBuildings
          .sort((a, b) => (b.NaturalGasUse || 0) - (a.NaturalGasUse || 0))
          .slice(0, 50);

      case 'top-electricity-users':
        return allBuildings
          .sort((a, b) => (b.ElectricityUse || 0) - (a.ElectricityUse || 0))
          .slice(0, 50);

      default:
        // Default: return top 50 buildings sorted by floor area
        return allBuildings
          .sort((a, b) => (b.GrossFloorArea || 0) - (a.GrossFloorArea || 0))
          .slice(0, 50);
    }
  }
}
</script>

<style lang="scss" scoped>
.page-social-card {
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

.page-social-card-content {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
}

.hero-section {
  flex: 1;
  position: relative;

  // Override BuildingsHero styles for social card dimensions
  :deep(.buildings-hero) {
    margin-bottom: 0;
    height: 100%;

    .hero-images,
    .hero-skyline img {
      height: 100%;
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

  .page-title {
    font-size: 6rem !important;
    font-weight: bold;
    line-height: 1;
    margin: 0;
  }

  .page-description {
    font-size: 2.5rem;
    margin: 0;
    line-height: 1;
  }
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
