<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import BuildingsMap from '~/components/BuildingsMap.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';

/**
 * Never Submitted Buildings page - shows buildings that are covered by Chicago's energy
 * benchmarking ordinance but have never submitted any data
 */
/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    BuildingsTable,
    BuildingsHero,
    BuildingsMap,
    DataDisclaimer,
    DataSourceFootnote,
  },
  metaInfo() {
    return generatePageMeta(
      'Never Submitted Buildings',
      "Buildings covered by Chicago's energy benchmarking ordinance that have " +
        'never submitted any energy data.',
    );
  },
})
export default class NeverSubmitted extends Vue {}
</script>

<static-query>
  query {
    allBuilding(
      filter: { FirstYearReported: { eq: null } },
      sortBy: "Address"
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
          Latitude
          Longitude
          PrimaryPropertyType
          GHGIntensity
          GHGIntensityRank
          GHGIntensityPercentileRank
          TotalGHGEmissions
          TotalGHGEmissionsRank
          TotalGHGEmissionsPercentileRank
          NaturalGasUse
          DistrictSteamUse
          AvgPercentileLetterGrade
          DataAnomalies
          FirstYearReported
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
        Chicago's {{ $static.allBuilding.edges.length }} Never Submitted
        Buildings
      </h1>
    </BuildingsHero>

    <div class="page-constrained">
      <p class="constrained -wide">
        These buildings are covered by Chicago's energy benchmarking ordinance
        (based on being present in the city's data), but have
        <strong>never submitted any energy data</strong>, so we have no
        emissions or energy use information to show for them.
      </p>

      <p class="constrained -wide">
        <strong>Note:</strong> Since these buildings have never reported data,
        most stats below will show as blank. They're excluded from our other
        rankings and top lists since we have nothing to rank them by, but are
        listed here so they're still findable.
      </p>

      <DataDisclaimer />

      <BuildingsMap
        :buildings="$static.allBuilding.edges"
        filter-label="never submitted"
      />

      <BuildingsTable
        :buildings="$static.allBuilding.edges"
        :show-square-footage="true"
      />

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss"></style>
