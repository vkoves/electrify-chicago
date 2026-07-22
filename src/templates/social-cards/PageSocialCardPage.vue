<page-query>
query {
  # Get all buildings for filtering
  allBuilding(sortBy: "GrossFloorArea", order: DESC) {
    edges {
      node {
        ID
        Address
        PropertyName
        GrossFloorArea
        AvgPercentileLetterGrade
        GHGIntensityLetterGrade
        EnergyMixLetterGrade
        SubmittedRecordsLetterGrade
        GHGIntensity
        TotalGHGEmissions
        ElectricityUse
        NaturalGasUse
        DistrictSteamUse
        DistrictChilledWaterUse
      }
    }
  }
}
</page-query>

<template>
  <PageSocialCard />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import PageSocialCard from '../../components/social-cards/PageSocialCard.vue';

import { getPageSocialConfig } from '../../constants/page-social-images/page-social-configs.vue';
import type { IPageSocialConfig } from '../../constants/page-social-images/page-social-configs.vue';

/**
 * The page for page social cards, found at `/page-social-card/:pageId`
 */
@Component({
  components: {
    PageSocialCard,
  },
})
export default class PageSocialCardTemplate extends Vue {
  /** Context passed from gridsome.server.js */
  readonly $context!: { pageId: string };

  /** Get page config from context (passed from gridsome.server.js) */
  get pageConfig(): IPageSocialConfig {
    // pageId is available from GraphQL context
    const pageId = this.$context.pageId;

    return (
      getPageSocialConfig(pageId) || {
        id: 'default',
        title: 'Electrify Chicago',
        description: 'Explore Chicago building energy data',
        filter: 'largest',
      }
    );
  }
}
</script>
