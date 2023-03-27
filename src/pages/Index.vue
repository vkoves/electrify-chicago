<script lang="ts">
// Gridsome doesn't have types, so can't import it properly
// eslint-disable-next-line @typescript-eslint/no-var-requires, no-undef
const Pager = require('gridsome').Pager;

import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    NewTabIcon,
    Pager,
  },
  metaInfo() {
    return { title:  'Biggest Buildings' };
  },
})
export default class BiggestBuildings extends Vue {
}
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
    <h1 id="main-content">
      Electrify Chicago
    </h1>

    <p class="constrained">
      <!-- TODO: Move to consolidated sources object-->
      According to the <a
        ref="noopener noreferrer"
        href="https://www.chicago.gov/city/en/sites/climate-action-plan/home.html"
        target="_blank"
      >
        2022 Chicago Climate Action Plan<NewTabIcon />
      </a>, a whopping <strong>69% of Chicago's emissions come from buildings</strong>, making it
      our biggest challenge and <em>our biggest opportunity</em> as a city to tackle climate change.
      At Electrify Chicago we want to showcase some of the best and worst performing buildings in
      the city using publicly available data and manual annotations to add building photographs and
      label owners.
    </p>

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
