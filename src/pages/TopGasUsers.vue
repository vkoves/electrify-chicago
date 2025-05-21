<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
  },
  metaInfo() {
    return { title: 'Biggest Fossil Gas Users' };
  },
})
export default class TopGasUsers extends Vue {}
</script>

<static-query>
  query {
    allBuilding(sortBy: "NaturalGasUse", limit: 50) {
      edges {
        node {
          slugSource
          ID
          DataYear
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
          # AvgPercentileLetterGrade
          DataAnomalies
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <h1 id="main-content" tabindex="-1">
      Top {{ $static.allBuilding.edges.length }} Buildings by Fossil Gas Use
    </h1>

    <p class="constrained -wide">
      These buildings are the largest consumers of fossil gas (methane) in the
      city. Fossil gas in these buildings is typically used for heating gas and
      water, and since electrifying the grid won't clean up these emissions it's
      an important set of buildings to focus on!
    </p>

    <DataDisclaimer />

    <BuildingsTable
      :buildings="$static.allBuilding.edges"
      :show-gas-use="true"
    />

    <DataSourceFootnote />
  </DefaultLayout>
</template>

<style lang="scss"></style>
