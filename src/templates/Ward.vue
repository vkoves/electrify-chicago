<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import PieChart, { IPieSlice } from '~/components/graphs/PieChart.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import {
  calculateBuildingsStats,
  IBuildingBenchmarkStats,
  IBuildingNode,
} from '../common-functions.vue';
import { BuildingOwners } from '../constants/buildings-custom-info.constant.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import NewTabIcon from '../components/NewTabIcon.vue';

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
    return {
      title: `Ward ${this.$context.ward} Buildings`,
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
  readonly $context!: { ward: string };

  avgGHGIntensity?: string;
  medianGHGIntensityMultiple?: string;

  totalGHGEmissions?: string;
  medianGHGEmissionsMultiple?: string;

  totalSquareFootage?: string;
  avgBuildingAge?: string;
  gradeDistributionPie: Array<IPieSlice> = [];

  created(): void {
    this.calculateWardStats();
  }

  calculateWardStats(): void {
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

<!-- Filter to buildings with the given `ward` from the context -->
<page-query>
query ($ward: String) {
  allBuilding(
    filter: {
        Ward: { eq: $ward }
    }
    sortBy: "GrossFloorArea", limit: 500
  ) {
    edges {
        node {
            slugSource
            path
            ID
            DataYear
            Address
            ChicagoEnergyRating
            CommunityArea
            ENERGYSTARScore
            DistrictChilledWaterUse
            DistrictSteamUse
            ElectricityUse
            GHGIntensity
            GrossFloorArea
            NaturalGasUse
            NumberOfBuildings
            PrimaryPropertyType
            PropertyName
            SiteEUI
            SourceEUI
            TotalGHGEmissions
            YearBuilt
            ZIPCode
            Ward
            GHGIntensityRank
            GHGIntensityPercentileRank
            TotalGHGEmissionsRank
            TotalGHGEmissionsPercentileRank
            NaturalGasUse
            DistrictSteamUse
            GrossFloorAreaRank
            GrossFloorAreaPercentileRank
            DataAnomalies
            AvgPercentileGrade,
            AvgPercentileLetterGrade,
        }
    }
  }
}
</page-query>

<template>
  <DefaultLayout main-class="layout -full-width">
    <div class="ward-page">
      <BuildingsHero
        :buildings="$page.allBuilding.edges.map((edge) => edge.node)"
      >
        <h1 id="main-content" tabindex="-1">Ward {{ $context.ward }}</h1>
      </BuildingsHero>

      <div class="page-constrained">
        <g-link to="/wards" class="grey-link back-link">
          <img src="/icons/arrow-back.svg" />
          Back to All Wards
        </g-link>

        <section class="stats-overview -three-col-max">
          <h2>Ward {{ $context.ward }} Quick Stats</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-number">
                {{ $page.allBuilding.edges.length }}
              </div>
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

        <p>
          This page shows all buildings identified as being in Ward
          {{ $context.ward }} that submitted building benchmarking data.
        </p>
        <p>
          Learn more at
          <a
            :href="`https://www.chicago.gov/city/en/about/wards/${$context.ward.padStart(2, '0')}.html`"
            target="_blank"
            rel="noopener"
          >
            The City of Chicago - Ward {{ $context.ward }}

            <NewTabIcon />
          </a>
        </p>

        <DataDisclaimer />

        <BuildingsTable
          :buildings="$page.allBuilding.edges"
          :show-square-footage="true"
        />

        <DataSourceFootnote />
      </div>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.ward-page {
  .back-link {
    margin-bottom: 1rem;
  }

  h2 {
    margin-bottom: 0.5rem;
  }

  .stats {
    margin-top: 0;
    padding-left: 1.25rem;

    li + li {
      margin-top: 0.5rem;
    }

    .footnote {
      margin: 0rem;
    }
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
}
</style>
