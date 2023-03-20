<script>
import {Pager} from 'gridsome';
import BuildingsTable from '~/components/BuildingsTable.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
const BuildingBenchmarkStats = require('../data/dist/building-benchmark-stats.json');

export default {
  components: {
    BuildingsTable,
    Pager,
  },
  metaInfo: {
    title: 'Home',
  },
  data() {
    return {
      BuildingBenchmarkStats,
    };
  },
};
</script>

<page-query>
  query ($page: Int) {
    allBuilding(sortBy: "GHGIntensity", perPage: 15, page: $page) @paginate {
      pageInfo {
        totalPages
        currentPage
      }
      edges {
        node {
          PropertyName
          Address
          path
          PrimaryPropertyType
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
</page-query>

<template>
  <DefaultLayout>
    <h1>Electrify Chicago</h1>

    <h2>Chicago Buildings by Greenhouse Gas Intensity</h2>

    <p>
      <strong>Note:</strong> This only includes buildings whose emissions are reported
      under the Chicago Energy Benchmarking Ordinance. According to the City &ldquo;As of 2016,
      this list includes all commercial, institutional, and residential buildings larger than
      50,000 square feet.&rdquo; This dataset is also then filtered to only buildings with reported
      emissions > 1,000 metric tons.
      </blockquote>
    </p>

    <BuildingsTable :buildings="$page.allBuilding.edges" />

    <Pager class="pager" :info="$page.allBuilding.pageInfo"/>

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
