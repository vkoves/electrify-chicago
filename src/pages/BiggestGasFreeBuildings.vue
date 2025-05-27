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
    return { title: 'Biggest Gas Free Buildings' };
  },
})
export default class TopGasUsers extends Vue {}
</script>

<static-query>
  query {
    allBuilding(
      filter: {
        DataYear: { eq: "2022" },
        NaturalGasUse: { eq: 0 },
        DistrictSteamUse: { eq: 0 }
      },
      sortBy: "GrossFloorArea", limit: 500
    ) {
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
          ZIPCode
          path
          GrossFloorArea
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
          DistrictSteamUse
          AvgPercentileLetterGrade
          DataAnomalies
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <h1 id="main-content" tabindex="-1">
      Chicago's {{ $static.allBuilding.edges.length }} Fully Gas Free Buildings
    </h1>

    <p class="constrained -wide">
      These buildings are already all-electric, and feature some of the most
      famous buildings in the city! If even the John Hancock center or Marina
      Towers can run off of only electricity, your building can too.
    </p>

    <p class="constrained -wide">
      <strong>Note:</strong> This list is of buildings that use neither fossil
      gas nor a district steam system, since all district steam systems in the
      city are currently powered by burning fossil gas (to the best of our
      knowledge).
    </p>

    <DataDisclaimer />

    <BuildingsTable
      :buildings="$static.allBuilding.edges"
      :show-square-footage="true"
    />

    <DataSourceFootnote />
  </DefaultLayout>
</template>

<style lang="scss"></style>
