<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import PieChart, { IPieSlice } from '~/components/graphs/PieChart.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import {
  calculateBuildingsStats,
  IBuildingBenchmarkStats,
  IBuilding,
  IBuildingNode,
} from '../common-functions.vue';
import {
  BuildingOwners,
  IBuildingOwner,
} from '../constants/buildings-custom-info.constant.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import { generateOwnerMeta } from '../constants/meta-helpers.vue';

interface IBuildingEdge {
  node: IBuilding;
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
    BuildingsHero,
    PieChart,
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
  },
  metaInfo() {
    const ownerId: string = this.$context.ownerId;
    const owner = BuildingOwners[ownerId];

    if (owner) {
      return generateOwnerMeta(owner.key, owner.name);
    }
    return {
      title: 'Building Owner',
    };
  },
})
export default class BiggestBuildings extends Vue {
  readonly BuildingOwners = BuildingOwners;

  /** Expose stats to template */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats =
    BuildingBenchmarkStats;

  /** Set by Gridsome to results of GraphQL query */
  readonly $page!: { allBuilding: { edges: Array<IBuildingNode> } };
  readonly $context!: { ownerId: string };

  currOwner?: IBuildingOwner;

  buildingsFiltered: Array<IBuildingEdge> = [];

  avgGHGIntensity?: string;
  medianGHGIntensityMultiple?: string;

  totalGHGEmissions?: string;
  medianGHGEmissionsMultiple?: string;

  totalSquareFootage?: string;
  avgBuildingAge?: string;
  gradeDistributionPie: Array<IPieSlice> = [];

  created(): void {
    // Pull owner ID from the context provided in the gridsome.server page creation
    const ownerId: string = this.$context.ownerId;

    if (BuildingOwners[ownerId]) {
      this.currOwner = BuildingOwners[ownerId];

      // Buildings are pre-filtered by GraphQL query using Owner field
      this.buildingsFiltered = this.$page.allBuilding.edges;
      this.calculateOwnedBuildingStats();
    }
  }

  calculateOwnedBuildingStats(): void {
    const stats = calculateBuildingsStats(this.buildingsFiltered);

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

    // Convert millions
    this.totalSquareFootage = (stats.totalSquareFootage / 1000000).toFixed(1);

    if (stats.buildingsWithYear > 0) {
      const currentYear = new Date().getFullYear();
      this.avgBuildingAge = Math.round(
        currentYear - stats.avgYearBuilt,
      ).toString();
    } else {
      this.avgBuildingAge = 'N/A';
    }

    // Grade distribution for pie chart
    const gradeColors: Record<string, string> = {
      A: '#009f49', // $grade-a-green
      B: '#7fa52e', // $grade-b-green
      C: '#b36a15', // $grade-c-orange
      D: '#972222', // $grade-d-red
      F: '#d60101', // $grade-f-red
    };

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
        color: gradeColors[grade] || '#999999',
      }));
  }
}
</script>

<!-- Buildings are filtered by owner at query time using the Owner field -->
<page-query>
  query($ownerId: String!) {
    allBuilding(filter: { Owner: { eq: $ownerId } }, sortBy: "GHGIntensity") {
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
          Owner
        }
      }
    }
  }
</page-query>

<template>
  <DefaultLayout main-class="layout -full-width">
    <div class="building-owner-page">
      <BuildingsHero :buildings="buildingsFiltered.map((edge) => edge.node)">
        <h1 id="main-content" tabindex="-1">
          <div class="top-title">Buildings Owned By</div>

          <img :src="currOwner.logoLarge" alt="" />

          {{ currOwner.name }}
        </h1>
      </BuildingsHero>

      <div class="page-constrained">
        <g-link to="/large-owners" class="back-link grey-link">
          <img src="/icons/arrow-back.svg" alt="" />
          Back to All Owners
        </g-link>

        <section class="stats-overview -three-col-max">
          <h2>{{ currOwner.name }} Quick Stats</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-number">{{ buildingsFiltered.length }}</div>
              <div class="stat-label">Tagged Buildings</div>
            </div>

            <div class="stat-card">
              <div class="stat-label">Total Emissions</div>
              <div class="stat-number">{{ totalGHGEmissions }}</div>
              <div class="stat-description">
                metric tons CO<sub>2</sub> equivalent
              </div>
              <div class="stat-footnote">
                {{ medianGHGEmissionsMultiple }}x the median building ({{
                  BuildingBenchmarkStats.TotalGHGEmissions.median.toLocaleString()
                }}
                tons CO<sub>2</sub>e)
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-label">Avg GHG Intensity</div>
              <div class="stat-number">{{ avgGHGIntensity }}</div>
              <div class="stat-description">kg CO<sub>2</sub>e/sqft</div>
              <div class="stat-footnote">
                {{ medianGHGIntensityMultiple }}x the median building ({{
                  BuildingBenchmarkStats.GHGIntensity.median
                }}
                kg CO<sub>2</sub>/sqft)
              </div>
            </div>
          </div>
        </section>

        <section
          v-if="gradeDistributionPie.length > 0"
          class="grade-distribution"
        >
          <div class="grade-content">
            <div class="grade-chart-container">
              <h3>Grade Distribution</h3>

              <PieChart
                :graph-data="gradeDistributionPie"
                id-prefix="grade-distribution"
                :show-labels="true"
                :sort-by-largest="false"
              />
            </div>
            <div class="supplementary-stats stats-overview">
              <div class="stats-grid">
                <div class="stat-card">
                  <div class="stat-label">Total Square Footage</div>
                  <div class="stat-number">{{ totalSquareFootage }}M</div>
                  <div class="stat-description">
                    million sq ft under management
                  </div>
                </div>

                <div class="stat-card">
                  <div class="stat-label">Avg Building Age</div>
                  <div class="stat-number">{{ avgBuildingAge }}</div>
                  <div class="stat-description">years old</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <h2>{{ currOwner.name }} Buildings List</h2>

        <p class="constrained -wide smaller">
          <strong>Note:</strong> Building owners are manually tagged, so this
          may not be a definitive or perfect list.
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
@import '../scss/stat-tiles.scss';

.building-owner-page {
  h1 {
    font-size: 1.5rem;

    .top-title {
      font-size: 0.825rem;
      margin-bottom: 0.5rem;
    }

    img {
      display: block;
      width: 20rem;
      margin-bottom: 1rem;
      background: $white;
      padding: 0.5rem;
      border-radius: $brd-rad-medium;
    }
  }

  .stats-overview {
    margin: 1rem 0;

    .stat-description {
      font-weight: 600;
      font-size: 1rem;
      line-height: 1;
    }

    .stat-number {
      margin-top: 0.5rem;
    }

    // Override grid for 3 cards layout
    &.-three-col-max .stats-grid {
      // Mobile: 2 columns
      grid-template-columns: repeat(2, 1fr);

      // Desktop: 3 columns (one row with 3 cards)
      @media (min-width: $desktop-min-width) {
        grid-template-columns: repeat(3, 1fr);
      }
    }
  }

  .grade-distribution {
    margin: 2rem 0;

    h2 {
      font-size: 1rem;
      margin: 0;
    }

    .grade-content {
      display: grid;
      grid-template-columns: 1fr;
      gap: 2rem;
      align-items: center;

      @media (min-width: $desktop-min-width) {
        grid-template-columns: 1fr 3fr;
        align-items: flex-start;
      }
    }

    .supplementary-stats {
      // Override the default margin from stats-overview
      margin: 0;

      .stats-grid {
        // Override default 4-column layout for our 2 stats
        grid-template-columns: 1fr;

        @media (min-width: $mobile-max-width) {
          grid-template-columns: repeat(2, 1fr);
        }

        // Keep it at 2 columns even on large desktop
        @media (min-width: $large-desktop-min-width) {
          grid-template-columns: repeat(2, 1fr);
        }
      }
    }
  }

  h2 {
    margin-bottom: 0.5rem;
  }
}
</style>
