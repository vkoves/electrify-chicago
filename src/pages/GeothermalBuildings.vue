<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import { IBuildingNode } from '../common-functions.vue';
import {
  BuildingTags,
  validateTaggedBuildings,
} from '../constants/buildings-custom-info.constant.vue';

interface IBuildingEdge {
  node: IBuildingNode['node'];
}

/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    DataSourceFootnote,
  },
  metaInfo() {
    return { title: 'Chicago Buildings with Geothermal Heat Pumps' };
  },
})
export default class GeothermalBuildings extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  readonly $static!: { allBuilding: { edges: Array<IBuildingEdge> } };

  buildingsFiltered: Array<IBuildingEdge> = [];

  created(): void {
    validateTaggedBuildings(
      BuildingTags.hasGeothermalHeatPump,
      this.$static.allBuilding.edges.map((e) => e.node.ID.toString()),
    );
    this.buildingsFiltered = this.$static.allBuilding.edges;
  }
}
</script>

<!--
  This page lists buildings with geothermal heat pumps. It uses a hard-coded GraphQL filter for
  performance optimization. The IDs MUST match buildings tagged with hasGeothermalHeatPump in
  buildings-custom-info.constant.vue (validated at runtime via validateTaggedBuildings).
-->
<static-query>
  query {
    # PERFORMANCE OPTIMIZATION: Hard-coded filter for buildings with hasGeothermalHeatPump tag
    # These IDs MUST match buildings-custom-info.constant.vue (validated at runtime)
    # When adding/removing geothermal buildings, update both this query AND the constant
    allBuilding(
      sortBy: "GHGIntensity",
      filter: {
        ID: {
          in: ["175895", "256537"]
        }
      }
    ) {
      edges {
        node {
          slugSource
          ID
          DataYear
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
          AvgPercentileLetterGrade
          NaturalGasUse
          DistrictSteamUse
          DataAnomalies
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <div class="geothermal-page">
      <h1 id="main-content" tabindex="-1">
        Chicago Buildings with Geothermal Heat Pumps
      </h1>

      <p class="constrained -wide">
        These buildings use geothermal heat pump systems, which leverage the
        earth's stable underground temperature to heat and cool the building
        more efficiently than conventional HVAC systems.
      </p>

      <DataDisclaimer />

      <BuildingsTable :buildings="buildingsFiltered" />

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.geothermal-page {
}
</style>
