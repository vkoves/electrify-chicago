<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import PieChart, { IPieSlice } from '~/components/graphs/PieChart.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import {
  IBuildingBenchmarkStats,
  IBuilding,
  IBuildingNode,
} from '../common-functions.vue';
import { BuildingOwners } from '../constants/buildings-custom-info.constant.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import NewTabIcon from '../components/NewTabIcon.vue';

interface IBuildingEdge {
  node: IBuilding;
}

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
    // Grade distribution for pie chart
    const gradeColors: Record<string, string> = {
      A: '#009f49', // $grade-a-green
      B: '#7fa52e', // $grade-b-green
      C: '#b36a15', // $grade-c-orange
      D: '#972222', // $grade-d-red
      F: '#d60101', // $grade-f-red
    };

    // Aggregate Ward stats for calculations
    this.$page.allBuilding.edges.forEach((buildingEdge: IBuildingEdge) => {
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

    // Finish calculations from aggregated ward stats
    this.totalSquareFootage = (totalSquareFootage / 1000000).toFixed(1); // Convert to millions

    if (buildingsWithYear > 0) {
      const avgYearBuilt = totalYearBuilt / buildingsWithYear;
      const currentYear = new Date().getFullYear();
      this.avgBuildingAge = Math.round(currentYear - avgYearBuilt).toString();
    } else {
      this.avgBuildingAge = 'N/A';
    }
    this.totalGHGEmissions = Math.round(totalGHGEmissions).toLocaleString();
    const avgGHGIntensity: number =
      totalGHGIntensity / this.$page.allBuilding.edges.length;
    this.avgGHGIntensity = avgGHGIntensity.toFixed(1);

    this.medianGHGIntensityMultiple = (
      avgGHGIntensity / BuildingBenchmarkStats.GHGIntensity.median
    ).toFixed(0);
    this.medianGHGEmissionsMultiple = (
      totalGHGEmissions / BuildingBenchmarkStats.TotalGHGEmissions.median
    ).toFixed(0);

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

        <h2>Ward Stats</h2>

        <ul class="stats">
          <li class="bold">{{ $page.allBuilding.edges.length }} Buildings</li>

          <li>
            <strong>
              Total Emissions:
              {{ totalGHGEmissions }} metric tons CO<sub>2</sub> equivalent
            </strong>

            <p class="footnote">
              <strong>
                Equivalent to {{ medianGHGEmissionsMultiple }} of the median
                benchmarked building
              </strong>
              ({{
                BuildingBenchmarkStats.TotalGHGEmissions.median.toLocaleString()
              }}
              tons CO<sub>2</sub>e)
            </p>
          </li>

          <li>
            <strong>
              Average GHG Intensity:
              {{ avgGHGIntensity }} kg CO<sub>2</sub>e/sqft
            </strong>

            <p class="footnote">
              <strong
                >{{ medianGHGIntensityMultiple }}x the median benchmarked
                building</strong
              >
              ({{ BuildingBenchmarkStats.GHGIntensity.median }} kg
              CO<sub>2</sub>/sqft)
            </p>
          </li>
        </ul>

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
}
</style>
