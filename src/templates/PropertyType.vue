<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import PieChart, { IPieSlice } from '~/components/graphs/PieChart.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import {
  calculateBuildingsStats,
  GradeColors,
  IBuildingBenchmarkStats,
  IBuildingNode,
  pluralizePropertyType,
} from '../common-functions.vue';
import { slugifyPropertyType } from '../constants/property-type-helpers.vue';
import { generatePropertyTypeMeta } from '../constants/meta-helpers.vue';
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';

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
    PieChart,
    DataDisclaimer,
    DataSourceFootnote,
  },
  metaInfo() {
    const propertyType: string = this.$context.propertyType;
    const propertyTypePlural = pluralizePropertyType(propertyType);
    const slug = slugifyPropertyType(propertyType);

    return generatePropertyTypeMeta(slug, propertyTypePlural, propertyType);
  },
})
export default class PropertyType extends Vue {
  /** Expose stats to template */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats =
    BuildingBenchmarkStats;

  /** Set by Gridsome to results of GraphQL query */
  readonly $page!: { allBuilding: { edges: Array<IBuildingNode> } };
  readonly $context!: { propertyType: string };

  buildingsFiltered: Array<IBuildingNode> = [];

  avgGHGIntensity?: string;
  medianGHGIntensityMultiple?: string;
  totalGHGEmissions?: string;
  medianGHGEmissionsMultiple?: string;
  totalSquareFootage?: string;
  gradeDistributionPie: Array<IPieSlice> = [];

  created(): void {
    // Buildings are pre-filtered by GraphQL query using PrimaryPropertyType field
    this.buildingsFiltered = this.$page.allBuilding.edges;
    this.calculatePropertyTypeStats();
  }

  calculatePropertyTypeStats(): void {
    const stats = calculateBuildingsStats(this.$page.allBuilding.edges);

    // Calculations
    this.totalGHGEmissions = Math.round(
      stats.totalGHGEmissions,
    ).toLocaleString();
    const avgGHGIntensity: number = stats.avgGHGIntensity;
    this.avgGHGIntensity = avgGHGIntensity.toFixed(1);

    this.medianGHGIntensityMultiple = (
      avgGHGIntensity / BuildingBenchmarkStats.GHGIntensity.median
    ).toFixed(0);
    this.medianGHGEmissionsMultiple = (
      stats.totalGHGEmissions / BuildingBenchmarkStats.TotalGHGEmissions.median
    ).toFixed(0);

    // Convert to millions
    this.totalSquareFootage = (stats.totalSquareFootage / 1000000).toFixed(1);

    // Build data for Pie Chart
    this.gradeDistributionPie = Object.entries(stats.gradeDistribution)
      .filter(([, count]) => count > 0) // Only include grades that exist
      .sort(([a], [b]) => {
        const gradeOrder = ['A', 'B', 'C', 'D', 'F'];
        return gradeOrder.indexOf(a) - gradeOrder.indexOf(b);
      })
      .map(([grade, count]) => ({
        label: `Grade ${grade}`,
        value: count,
        color: GradeColors[grade] || '#999999',
      }));
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
  query($propertyType: String!) {
    allBuilding(
      filter: { PrimaryPropertyType: { eq: $propertyType } }
      sortBy: "GrossFloorArea"
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
          AvgPercentileLetterGrade
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
        <section class="stats-line">
          <div class="stat-item">
            <div class="stat-number">{{ buildingCount }}</div>
            <div class="stat-label bold">Buildings</div>
          </div>

          <div class="stat-item">
            <div class="stat-number">{{ totalGHGEmissions }}</div>
            <div class="stat-label">
              <strong>Total Emissions</strong> <br />
              (metric tons CO<sub>2</sub>e)
            </div>
          </div>

          <div class="stat-item">
            <div class="stat-number">{{ avgGHGIntensity }}</div>
            <div class="stat-label">
              <strong>Avg GHG Intensity</strong> <br />
              (kg CO<sub>2</sub>e/sqft)
            </div>
          </div>

          <div class="stat-item">
            <div class="stat-number">{{ totalSquareFootage }}M</div>
            <div class="stat-label bold">Total Square Footage</div>
          </div>

          <div
            v-if="gradeDistributionPie.length > 0"
            class="stat-item grade-chart-inline"
          >
            <PieChart
              :graph-data="gradeDistributionPie"
              id-prefix="grade-distribution"
              :show-labels="true"
              :sort-by-largest="false"
              :small="true"
            />
            <div class="stat-label bold no-min">Grade Distribution</div>
          </div>
        </section>

        <h2>All {{ propertyTypePlural }}</h2>

        <p class="constrained -wide smaller">
          Showing {{ propertyTypePlural }} buildings that reported their energy use and
          greenhouse gas emissions to the City of Chicago under energy
          benchmarking.
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

  .stats-line {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin: 2rem 0;
    padding: 0.5rem 1rem;
    background: $off-white;
    border-radius: $brd-rad-medium;
    flex-wrap: wrap;

    @media (max-width: $mobile-max-width) {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      padding: 1rem;
    }

    .stat-item {
      text-align: center;
      flex: 1;
      min-width: 0;
      padding-right: 2rem;
      border-right: $border-thin solid $grey;

      &:last-child {
        border-right: none;
        padding-right: 0;
      }

      @media (max-width: $mobile-max-width) {
        text-align: left;
        border-right: none;
        padding-right: 0;
      }

      &.grade-chart-inline {
        display: flex;
        flex-direction: column;
        align-items: center;

        @media (max-width: $mobile-max-width) {
          grid-column: 1 / -1;
          padding-top: 1.5rem;
          border-top: $border-thin solid $grey;
        }
      }
    }

    .stat-number {
      font-size: 1.75rem;
      font-weight: bold;
      color: $off-black;
      line-height: 1.2;
    }

    .stat-label {
      font-size: 0.875rem;
      color: $text-mid-light;

      &:not(.no-min) {
        // Lock to two lines for alignment
        min-height: 3.2em;
      }
    }
  }
}
</style>
