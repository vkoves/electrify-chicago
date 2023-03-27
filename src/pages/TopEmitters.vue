<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    NewTabIcon,
  },
  metaInfo() {
    return { title:  'Top Emitters' };
  },
})
export default class TopEmitters extends Vue {
}
</script>

<static-query>
  query {
    allBuilding(sortBy: "TotalGHGEmissions", limit: 50) {
      edges {
        node {
          slugSource
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
      Top {{ $static.allBuilding.edges.length }} Buildings by Greenhouse Gas Emissions
    </h1>

    <p class="constrained -wide">
      These buildings are the biggest emitters of greenhouse gases in Chicago, both directly (like
      by burning natural gas on site for heating) and indirectly (by using electricity that is
      still produced with some fossil fuels).
    </p>

    <p class="constrained -wide">
      Many of these buildings are very large, which is a big part of why they use so much energy and
      have such high emissions. Several of these buildings, however, are not that large, but are
      instead incredibly inefficient - they use a lot of energy to heat and cool relatively small
      buildings.
    </p>

    <p class="bold">
      Curious to see buildings sorted by their emissions <em>intensity</em> instead? <g-link to="/">
        Check out the homepage!
      </g-link>
    </p>

    <DataDisclaimer />

    <BuildingsTable :buildings="$static.allBuilding.edges" />

    <p class="footnote">
      Data Source:
      <!-- eslint-disable-next-line max-len -->
      <a
        href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
        target="_blank"
        rel="noopener noreferrer"
      >
        Chicago Energy Benchmarking Data <NewTabIcon />
      </a>
    </p>
  </DefaultLayout>
</template>

<style lang="scss">
</style>
