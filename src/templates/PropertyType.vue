<script lang="ts">
// Gridsome doesn't have types, so can't import it properly
// eslint-disable-next-line @typescript-eslint/no-require-imports
const Pager = require('gridsome').Pager;

import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import { IBuildingNode, pluralizePropertyType } from '../common-functions.vue';

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
    Pager,
  },
  metaInfo() {
    const propertyType: string = this.$context.propertyType;
    const propertyTypePlural = pluralizePropertyType(propertyType);

    return {
      title: propertyTypePlural,
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
  readonly $page!: {
    allBuilding: {
      edges: Array<IBuildingNode>;
      pageInfo: {
        currentPage: number;
        totalPages: number;
        perPage: number;
        hasNextPage: boolean;
        hasPreviousPage: boolean;
      };
    };
  };
  readonly $context!: { propertyType: string };

  buildingsFiltered: Array<IBuildingNode> = [];
  pageInput = 0;

  created(): void {
    // Buildings are pre-filtered by GraphQL query using PrimaryPropertyType field
    this.buildingsFiltered = this.$page.allBuilding.edges;
    this.pageInput = this.$page.allBuilding.pageInfo.currentPage;
  }

  get propertyType(): string {
    return this.$context.propertyType;
  }

  get propertyTypePlural(): string {
    return pluralizePropertyType(this.$context.propertyType);
  }

  get buildingCount(): number {
    return this.buildingsFiltered.length;
  }
}
</script>

<!-- Buildings are filtered by property type at query time using the PrimaryPropertyType field -->
<page-query>
  query($propertyType: String!, $page: Int) {
    allBuilding(
      filter: { PrimaryPropertyType: { eq: $propertyType } }
      sortBy: "GrossFloorArea"
      perPage: 15
      page: $page
    ) @paginate {
      pageInfo {
        hasNextPage
        totalPages
        currentPage
        perPage
        hasPreviousPage
      }
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
        <h1 id="main-content" tabindex="-1">{{ propertyTypePlural }}</h1>
        <p class="building-count">
          {{ buildingCount }} building{{ buildingCount !== 1 ? 's' : '' }} in
          Chicago
        </p>
      </BuildingsHero>

      <div class="page-constrained">
        <h2>All {{ propertyTypePlural }}</h2>

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

        <div class="pager-cont">
          <div>
            <div class="page-number">
              Page {{ $page.allBuilding.pageInfo.currentPage }} of
              {{ $page.allBuilding.pageInfo.totalPages }}

              (Building #{{
                1 +
                ($page.allBuilding.pageInfo.currentPage - 1) *
                  $page.allBuilding.pageInfo.perPage
              }}
              to #{{
                ($page.allBuilding.pageInfo.currentPage - 1) *
                  $page.allBuilding.pageInfo.perPage +
                $page.allBuilding.edges.length
              }})
            </div>

            <Pager class="pager" :info="$page.allBuilding.pageInfo" />
          </div>
        </div>

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

  .pager-cont {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-top: 1rem;
    gap: 1rem;

    .pager {
      margin-top: 0;
    }

    .page-number {
      font-weight: bold;
      font-size: smaller;
      margin-bottom: 0.25rem;
    }
  }

  @media (max-width: $mobile-max-width) {
    .pager-cont {
      flex-direction: column;
      align-items: flex-start;
    }
  }
}
</style>
