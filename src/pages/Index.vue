<script>
import {Pager} from 'gridsome';
import BuildingsTable from '~/components/BuildingsTable.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import DataDisclaimer from '../components/DataDisclaimer.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
const BuildingBenchmarkStats = require('../data/dist/building-benchmark-stats.json');

export default {
  components: {
    BuildingsTable,
    Pager,
    NewTabIcon,
    DataDisclaimer,
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
          slugSource
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

    <DataDisclaimer />

    <BuildingsTable :buildings="$page.allBuilding.edges" />

    <Pager
      class="pager"
      :info="$page.allBuilding.pageInfo"
    />

    <p class="footnote">
      Data Source:
      <a
        href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
        target="_blank"
        rel="noopener noreferrer"
      >
        Chicago Energy Benchmarking Data <NewTabIcon />
      </a>
    </p>
  </DefaultLayout>
</template>

<style lang="scss">

</style>
