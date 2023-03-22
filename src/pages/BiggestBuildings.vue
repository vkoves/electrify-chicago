<script>
import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '../components/DataDisclaimer.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
const BuildingBenchmarkStats = require('../data/dist/building-benchmark-stats.json');

export default {
  components: {
    BuildingsTable,
    DataDisclaimer,
  },
  metaInfo: {
    title: 'Top Gas Users',
  },
  data() {
    return {
      BuildingBenchmarkStats,
    };
  },
};
</script>

<static-query>
  query {
    allBuilding(sortBy: "GrossFloorArea", limit: 20) {
      edges {
        node {
          PropertyName
          Address
          path
          PrimaryPropertyType
          GrossFloorArea
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
          GHGIntensity
          GHGIntensityRank
          GHGIntensityPercentileRank
          TotalGHGEmissions
          TotalGHGEmissionsRank
          TotalGHGEmissionsPercentileRank
          ElectricityUse
          ElectricityUseRank
          ElectricityUsePercentileRank
          NaturalGasUse
          NaturalGasUseRank
          NaturalGasUsePercentileRank
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <h1>Top Buildings By Square Footage</h1>

    <DataDisclaimer/>

    <BuildingsTable :buildings="this.$static.allBuilding.edges" :showSquareFootage="true" />

    <p class="footnote">
      Data Source:
      <!-- eslint-disable-next-line max-len -->
      <a href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
        target="_blank" rel="noopener noreferrer">
        Chicago Energy Benchmarking Data (opens in a new tab)
      </a>
    </p>
  </DefaultLayout>
</template>

<style lang="scss">
</style>