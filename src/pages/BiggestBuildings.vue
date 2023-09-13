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
    return { title:  'Biggest Buildings' };
  },
})
export default class BiggestBuildings extends Vue {
}
</script>

<static-query>
  query {
    allBuilding(sortBy: "GrossFloorArea", limit: 50) {
      edges {
        node {
          slugSource
          ID
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
    <h1
      id="main-content"
      tabindex="-1"
    >
      Top {{ $static.allBuilding.edges.length }} Buildings By Square Footage
    </h1>

    <p class="constrained -wide">
      These are the biggest buildings in our dataset, which should encompass all of the largest
      buildings in the city that submitted their energy use for 2020. Being a big building does
      basically guarantee that you use a lot of energy (and emit a lot of CO<sub>2</sub>), but a lot
      of big buildings are very energy efficient and use less energy per square foot than much
      smaller buildings!
    </p>

    <DataDisclaimer />

    <BuildingsTable
      :buildings="$static.allBuilding.edges"
      :show-square-footage="true"
    />

    <DataSourceFootnote />
  </DefaultLayout>
</template>

<style lang="scss">
</style>
