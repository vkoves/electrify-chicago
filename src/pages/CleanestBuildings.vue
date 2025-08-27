<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    BuildingsHero,
    DataDisclaimer,
    NewTabIcon,
    DataSourceFootnote,
  },
  metaInfo() {
    return { title: 'Cleanest Buildings' };
  },
})
export default class CleanestBuildings extends Vue {
  /** Expose BuildingBenchmarkStats to template */
  BuildingBenchmarkStats = BuildingBenchmarkStats;
}
</script>

<static-query>
  query {
    allBuilding(
      filter: {
        DataYear: { eq: "2023" },
        # Later on, we could filter to just larger buildings or ignore buildings flagged as
        # anomalous
        # DataAnomalies: { eq: "" },
        # TotalGHGEmissions: { gt: 1000.0 }
        # GrossFloorArea: { gt: 1000.0 }
        AvgPercentileLetterGrade: { eq: "A" }
        # EnergyMixLetterGrade: { eq: "A" }
      },
      sortBy: "GHGIntensity", order: ASC, limit: 50
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
          PrimaryPropertyType
          GrossFloorArea
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
          EnergyMixLetterGrade
          DataAnomalies
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout main-class="layout -full-width">
    <BuildingsHero
      :buildings="$static.allBuilding.edges.map((edge) => edge.node)"
    >
      <h1 id="main-content" tabindex="-1">
        Cleanest {{ $static.allBuilding.edges.length }} Buildings by Greenhouse
        Gas Intensity
      </h1>
    </BuildingsHero>

    <div class="page-constrained">
    <p class="constrained">
      The median building in our dataset emits
      {{ BuildingBenchmarkStats.GHGIntensity.median }} CO<sub>2</sub> kg /
      square foot, but these buildings are Chicago's best in class and emit
      <em>way</em> less! Some, like
      <g-link to="/building-id/239096"> Marina Towers </g-link>, are large
      residential buildings, but other buildings in this list include offices,
      hotels, and even schools like
      <g-link to="/building-id/101572"> King College Prep </g-link>. Most
      buildings in this list have an Energy Star score over 90, which means they
      are typically officially certified as being energy-efficient.
    </p>

    <DataDisclaimer />

    <BuildingsTable :buildings="$static.allBuilding.edges" />

    <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss"></style>
