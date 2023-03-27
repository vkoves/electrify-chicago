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
    return { title:  'Biggest Natural Gas Users' };
  },
})
export default class TopGasUsers extends Vue {
}
</script>

<static-query>
  query {
    allBuilding(sortBy: "NaturalGasUse", limit: 50) {
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
    <h1 id="main-content">
      Top {{ $static.allBuilding.edges.length }} Buildings by Natural Gas Use
    </h1>

    <p class="constrained -wide">
      These buildings are the largest consumers of natural gas (methane) in the city. Natural gas
      in these buildings is typically used for heating gas and water, and since electrifying the
      grid won't clean up these emissions it's an important set of buildings to focus on!
    </p>

    <DataDisclaimer />

    <BuildingsTable
      :buildings="$static.allBuilding.edges"
      :show-gas-use="true"
    />

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
