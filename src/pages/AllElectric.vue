<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { generatePageSocialMeta } from '../constants/page-social-meta';

/**
 * All Electric Buildings page - shows the largest all-electric buildings in Chicago
 *
 * NOTE: This page was previously located at /biggest-gas-free-buildings before Aug. 27th, 2025.
 * The old route redirects to this new location for backwards compatibility.
 */
// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    BuildingsHero,
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
  },
  metaInfo() {
    const description =
      'Chicago buildings that are already all-electric! These innovative buildings show ' +
      'the path forward - if the John Hancock Center can run on electricity alone, ' +
      'so can your building.';

    return generatePageSocialMeta(
      'all-electric',
      'All Electric Buildings',
      description,
    );
  },
})
export default class AllElectric extends Vue {}
</script>

<static-query>
  query {
    allBuilding(
      filter: {
        DataYear: { eq: "2023" },
        # Use lte: 0 to capture buildings with 0, null, or empty values for gas usage
        NaturalGasUse: { lte: 0 },
        DistrictSteamUse: { lte: 0 },
        # Exclude buildings that previously used gas but now report zero
        DataAnomalies: { nin: ["gasZeroWithPreviousUse"] }
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
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
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
  <DefaultLayout main-class="layout -full-width">
    <BuildingsHero
      :buildings="$static.allBuilding.edges.map((edge) => edge.node)"
    >
      <h1 id="main-content" tabindex="-1">
        Chicago's {{ $static.allBuilding.edges.length }} All Electric Buildings
      </h1>
    </BuildingsHero>

    <div class="page-constrained">
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
    </div>
  </DefaultLayout>
</template>

<style lang="scss"></style>
