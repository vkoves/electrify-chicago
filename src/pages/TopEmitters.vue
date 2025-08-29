<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import generatePageSocialMeta from '../constants/page-social-meta';

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
    return generatePageSocialMeta(
      'top-emitters',
      'Top Emitters',
      "Chicago's highest greenhouse gas emitting buildings",
    );
  },
})
export default class TopEmitters extends Vue {}
</script>

<static-query>
  query {
    allBuilding(sortBy: "TotalGHGEmissions", limit: 50) {
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
          AvgPercentileLetterGrade
          DistrictSteamUse
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
        Top {{ $static.allBuilding.edges.length }} Buildings by Greenhouse Gas
        Emissions
      </h1>
    </BuildingsHero>

    <div class="page-constrained">
      <p class="constrained -wide">
        These buildings are the biggest emitters of greenhouse gases in Chicago,
        both directly (like by burning fossil gas on site for heating) and
        indirectly (by using electricity that is still produced with some fossil
        fuels).
      </p>

      <p class="constrained -wide">
        Many of these buildings are very large, which is a big part of why they
        use so much energy and have such high emissions. Several of these
        buildings, however, are not that large, but are instead incredibly
        inefficient - they use a lot of energy to heat and cool relatively small
        buildings.
      </p>

      <p class="bold">
        Curious to see buildings sorted by their emissions
        <em>intensity</em> instead?
        <g-link to="/"> Check out the homepage! </g-link>
      </p>

      <DataDisclaimer />

      <BuildingsTable :buildings="$static.allBuilding.edges" />

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss"></style>
