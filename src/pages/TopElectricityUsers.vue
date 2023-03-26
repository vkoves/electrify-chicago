<script lang="ts">
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
  },
  metaInfo() {
    return { title:  'Top Electricity Users' };
  },
})
export default class TopElectricityUsers extends Vue {
}
</script>

<static-query>
  query {
    allBuilding(sortBy: "ElectricityUse", limit: 50) {
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
</static-query>

<template>
  <DefaultLayout>
    <h1>Top {{ $static.allBuilding.edges.length }} Electricity Users</h1>

    <DataDisclaimer />

    <BuildingsTable :buildings="$static.allBuilding.edges" />

    <p class="footnote">
      Data Source:
      <!-- eslint-disable-next-line max-len -->
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
