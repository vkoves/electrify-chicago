<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import PieChart, { IPieSlice } from '~/components/graphs/PieChart.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import {
  IBuildingBenchmarkStats,
  IBuilding,
  IBuildingNode,
} from '../common-functions.vue';
import {
  BuildingOwners,
  IBuildingOwner,
  BuildingsCustomInfo,
  IBuildingCustomInfo,
} from '../constants/buildings-custom-info.constant.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import { generateOwnerSocialMeta } from '../constants/page-social-meta.vue';

interface IBuildingEdge {
  node: IBuilding;
}

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
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
      return generateOwnerSocialMeta(owner.key, owner.name);
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
  readonly $static!: { allBuilding: { edges: Array<IBuildingNode> } };
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

      this.filterBuildings(ownerId);
      this.calculateOwnedBuildingStats();
    }
  }

  filterBuildings(ownerId: string): void {
    // Loop through BuildingsCustomInfo to get the IDs of buildings we are looking for
    const ownerBuildingsSlugs: Array<string> = Object.entries(
      BuildingsCustomInfo,
    )
      .filter(([, buildingInfo]: [string, IBuildingCustomInfo]) => {
        return buildingInfo.owner === ownerId;
      })
      .map(([buildingID]: [string, IBuildingCustomInfo]) => buildingID);

    this.buildingsFiltered = this.$static.allBuilding.edges.filter(
      (buildingEdge: IBuildingEdge) => {
        return ownerBuildingsSlugs.some(
          (ownedBuildingID) => buildingEdge.node.ID === ownedBuildingID,
        );
      },
    );
  }

  calculateOwnedBuildingStats(): void {
    let totalGHGEmissions = 0;
    let totalGHGIntensity = 0;
    let totalSquareFootage = 0;
    let totalYearBuilt = 0;
    let buildingsWithYear = 0;
    const gradeCounts: Record<string, number> = {
      A: 0,
      B: 0,
      C: 0,
      D: 0,
      F: 0,
    };

    this.buildingsFiltered.forEach((buildingEdge: IBuildingEdge) => {
      const building: IBuilding = buildingEdge.node;

      totalGHGIntensity += building.GHGIntensity;
      totalGHGEmissions += building.TotalGHGEmissions;
      totalSquareFootage += building.GrossFloorArea || 0;

      // Calculate average building age
      if (building.YearBuilt) {
        const yearBuilt = parseInt(building.YearBuilt.toString(), 10);
        if (
          !isNaN(yearBuilt) &&
          yearBuilt > 1800 &&
          yearBuilt <= new Date().getFullYear()
        ) {
          totalYearBuilt += yearBuilt;
          buildingsWithYear++;
        }
      }

      // Count grade distribution
      const grade = building.AvgPercentileLetterGrade;
      if (grade && typeof grade === 'string' && grade in gradeCounts) {
        gradeCounts[grade]++;
      }
    });

    // Existing calculations
    this.totalGHGEmissions = Math.round(totalGHGEmissions).toLocaleString();
    const avgGHGIntensity: number =
      totalGHGIntensity / this.buildingsFiltered.length;
    this.avgGHGIntensity = avgGHGIntensity.toFixed(1);

    this.medianGHGIntensityMultiple = (
      avgGHGIntensity / BuildingBenchmarkStats.GHGIntensity.median
    ).toFixed(0);
    this.medianGHGEmissionsMultiple = (
      totalGHGEmissions / BuildingBenchmarkStats.TotalGHGEmissions.median
    ).toFixed(0);

    // New calculations
    this.totalSquareFootage = (totalSquareFootage / 1000000).toFixed(1); // Convert to millions

    if (buildingsWithYear > 0) {
      const avgYearBuilt = totalYearBuilt / buildingsWithYear;
      const currentYear = new Date().getFullYear();
      this.avgBuildingAge = Math.round(currentYear - avgYearBuilt).toString();
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

    this.gradeDistributionPie = Object.entries(gradeCounts)
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

<!--
  This page grabs all buildings and then filters by owner on the client-side, since that data isn't
  baked into the actual building CSV
-->
<static-query>
  query {
    # BuildingOwner page only needs core BuildingsTable fields (no conditional fields)
    allBuilding(sortBy: "GHGIntensity") {
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
</static-query>

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
          <img src="/icons/arrow-back.svg" />
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
