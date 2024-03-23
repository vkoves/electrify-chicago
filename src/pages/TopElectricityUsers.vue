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
          ID
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
    <h1
      id="main-content"
      tabindex="-1"
    >
      Top {{ $static.allBuilding.edges.length }} Electricity Users
    </h1>

    <DataDisclaimer />

    <BuildingsTable
      :buildings="$static.allBuilding.edges"
      :show-electricity-use="true"
    />

    <DataSourceFootnote />
  </DefaultLayout>
</template>

<style lang="scss">
</style>
