<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';

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
    return generatePageMeta(
      'top-electricity-users',
      'Top Electricity Users',
      "Chicago's biggest consumers of electricity - these buildings use the " +
        'most power and offer the greatest potential for renewable energy adoption.',
    );
  },
})
export default class TopElectricityUsers extends Vue {}
</script>

<!-- If this query is updated, make sure to update PageSocialCard as well -->
<static-query>
  query {
    allBuilding(sortBy: "ElectricityUse", limit: 50) {
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
        Top {{ $static.allBuilding.edges.length }} Electricity Users
      </h1>
    </BuildingsHero>

    <div class="page-constrained">
      <DataDisclaimer />

      <BuildingsTable
        :buildings="$static.allBuilding.edges"
        :show-electricity-use="true"
      />

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss"></style>
