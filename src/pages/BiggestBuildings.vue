<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { LatestDataYear } from '../constants/globals.vue';
import DataSourceFootnote from '../components/DataSourceFootnote.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';

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
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
  },
  metaInfo() {
    return generatePageMeta(
      'biggest-buildings',
      'Biggest Buildings',
      "Chicago's largest buildings by floor area - discover which massive " +
        'buildings are leading or lagging on energy efficiency in the Windy City.',
    );
  },
})
export default class BiggestBuildings extends Vue {
  readonly LatestDataYear: number = LatestDataYear;
}
</script>

<!-- If this query is updated, make sure to update PageSocialCard as well -->
<static-query>
  query {
    allBuilding(sortBy: "GrossFloorArea", limit: 50) {
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
        Top {{ $static.allBuilding.edges.length }} Buildings By Square Footage
      </h1>
    </BuildingsHero>

    <div class="page-constrained">
      <p class="constrained -wide">
        These are the biggest buildings in our dataset, which should encompass
        all of the largest buildings in the city that submitted their energy use
        for
        {{ LatestDataYear }}. Being a big building does basically guarantee that
        you use a lot of energy (and emit a lot of CO<sub>2</sub>), but a lot of
        big buildings are very energy efficient and use less energy per square
        foot than much smaller buildings!
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
