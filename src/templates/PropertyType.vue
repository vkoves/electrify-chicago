<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import { IBuildingNode } from '../common-functions.vue';

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
  },
  metaInfo() {
    const propertyType: string = this.$context.propertyType;

    return {
      title: `${propertyType} Buildings`,
      meta: [
        {
          name: 'description',
          content:
            `View all ${propertyType} buildings in Chicago and their ` +
            `greenhouse gas emissions data.`,
        },
      ],
    };
  },
})
export default class PropertyType extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  readonly $page!: { allBuilding: { edges: Array<IBuildingNode> } };
  readonly $context!: { propertyType: string };

  buildingsFiltered: Array<IBuildingNode> = [];

  created(): void {
    // Buildings are pre-filtered by GraphQL query using PrimaryPropertyType field
    this.buildingsFiltered = this.$page.allBuilding.edges;
  }

  get propertyType(): string {
    return this.$context.propertyType;
  }

  get buildingCount(): number {
    return this.buildingsFiltered.length;
  }
}
</script>

<!-- Buildings are filtered by property type at query time using the PrimaryPropertyType field -->
<page-query>
  query($propertyType: String!) {
    allBuilding(
      filter: { PrimaryPropertyType: { eq: $propertyType } }
      sortBy: "GHGIntensity"
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
          GrossFloorArea
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
          YearBuilt
        }
      }
    }
  }
</page-query>

<template>
  <DefaultLayout main-class="layout -full-width">
    <div class="property-type-page">
      <BuildingsHero :buildings="buildingsFiltered.map((edge) => edge.node)">
        <h1 id="main-content" tabindex="-1">{{ propertyType }} Buildings</h1>
        <p class="building-count">
          {{ buildingCount }} building{{ buildingCount !== 1 ? 's' : '' }} in
          Chicago
        </p>
      </BuildingsHero>

      <div class="page-constrained">
        <h2>All {{ propertyType }} Buildings</h2>

        <p class="constrained -wide smaller">
          Showing all {{ propertyType }} buildings that reported their energy
          use and greenhouse gas emissions to the City of Chicago.
        </p>

        <DataDisclaimer />

        <BuildingsTable
          :buildings="buildingsFiltered"
          :show-year-built="true"
          :show-square-footage="true"
        />

        <DataSourceFootnote />
      </div>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.property-type-page {
  h1 {
    font-size: 1.5rem;
  }

  .building-count {
    font-size: 1.125rem;
    font-weight: 600;
    margin-top: 0.5rem;
    color: $white;
  }

  h2 {
    margin-bottom: 0.5rem;
  }
}
</style>
