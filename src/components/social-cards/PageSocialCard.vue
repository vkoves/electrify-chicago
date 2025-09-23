<template>
  <BaseSocialCard :buildings="buildings">
    <template #hero-content>
      <h1 class="page-title">{{ pageTitle }}</h1>
      <p v-if="pageDescription" class="page-description">
        {{ pageDescription }}
      </p>
    </template>
  </BaseSocialCard>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IBuilding } from '../../common-functions.vue';
import type { IPageSocialConfig } from '../../constants/page-social-images/page-social-configs.vue';
import BaseSocialCard from './BaseSocialCard.vue';

@Component({
  components: {
    BaseSocialCard,
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

    /**
     * TODO: We should write some tests for this, or figure out a less brittle way to tie this into
     * social pages
     */
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
</style>
