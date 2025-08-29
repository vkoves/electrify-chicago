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
import PageSocialCard from '../components/PageSocialCard.vue';

import {
  getPageSocialConfig,
  IPageSocialConfig,
} from '../constants/page-social-configs';

/**
 * The page for page social cards, found at `/page-social-card/:pageId`
 */
@Component({
  components: {
    PageSocialCard,
  },
})
export default class PageSocialCardTemplate extends Vue {
  /** Get page config from context (passed from gridsome.server.js) */
  get pageConfig(): IPageSocialConfig {
    // pageId is available from GraphQL context
    const pageId = (this as any).$context.pageId;

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
