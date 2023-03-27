<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    NewTabIcon,
  },
  metaInfo() {
    return { title:  'Biggest Natural Gas Users' };
  },
})
export default class TopGasUsers extends Vue {
  /** Expose BuildingBenchmarkStats to template */
  BuildingBenchmarkStats = BuildingBenchmarkStats;
}
</script>

<static-query>
  query {
    allBuilding(sortBy: "GHGIntensity", order: ASC, limit: 50) {
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
    <h1 id="main-content">
      Cleanest {{ $static.allBuilding.edges.length }} Buildings by Greenhouse Gas Intensity
    </h1>

    <p class="constrained">
      The median building in our dataset emits {{ BuildingBenchmarkStats.GHGIntensity.median }}
      CO<sub>2</sub> kg / square foot, but these buildings are Chicago's best in class and emit
      <em>way</em> less! Some, like
      <g-link to="/building/marina-towers-condominium-association/">
        Marina Towers
      </g-link>, are
      large residential buildings, but other buildings in this list include offices, hotels, and
      even schools like <g-link to="/building/king-college-prep-cps/">
        King College Prep
      </g-link>.
      Most buildings in this list have an Energy Star score over 90, which means they are typically
      officially certified as being energy-efficient.
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
