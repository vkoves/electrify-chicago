<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
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

  /** Chicago.gov uses a two digit number for wards, so 3 becomes wards/03.html */
  get wardZeroed(): string {
    const ward = this.$context.ward;

    if (parseInt(ward) < 10) {
      return `0${ward}`;
    } else {
      return ward;
    }
  }

  created(): void {
    this.calculateWardStats();
  }

  calculateWardStats(): void {
    let totalGHGEmissions = 0;
    let totalGHGIntensity = 0;

    this.$page.allBuilding.edges.forEach((buildingEdge: IBuildingEdge) => {
      const building: IBuilding = buildingEdge.node;

      totalGHGIntensity += building.GHGIntensity;
      totalGHGEmissions += building.TotalGHGEmissions;
    });

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
            Wards
            YearBuilt
            ZIPCode
            Ward
            GHGIntensityRank
            GHGIntensityPercentileRank
            TotalGHGEmissionsRank
            TotalGHGEmissionsPercentileRank
            ElectricityUseRank
            ElectricityUsePercentileRank
            NaturalGasUseRank
            NaturalGasUsePercentileRank
            GrossFloorAreaRank
            GrossFloorAreaPercentileRank
            SourceEUIRank
            SourceEUIPercentileRank
            SiteEUIRank
            SiteEUIPercentileRank
            GHGIntensityRankByPropertyType
            TotalGHGEmissionsRankByPropertyType
            ElectricityUseRankByPropertyType
            NaturalGasUseRankByPropertyType
            GrossFloorAreaRankByPropertyType
            SourceEUIRankByPropertyType
            SiteEUIRankByPropertyType
            DataAnomalies
            Ward
            # Grade data
            GHGIntensityPercentileGrade,
            GHGIntensityLetterGrade,
            EnergyMixWeightedPctSum,
            EnergyMixPercentileGrade,
            EnergyMixLetterGrade,
            MissingRecordsCount,
            SubmittedRecordsPercentileGrade,
            SubmittedRecordsLetterGrade,
            AvgPercentileGrade,
            AvgPercentileLetterGrade,
        }
    }
  }
}
</page-query>

<template>
  <DefaultLayout>
    <div class="ward-page">
      <g-link to="/wards" class="grey-link back-link">
        <img src="/icons/arrow-back.svg">
        Back to All Wards
      </g-link>

      <h1 id="main-content" tabindex="-1">Ward {{ $context.ward }}</h1>

      <p>
        This page shows all buildings identified as being in Ward
        {{ $context.ward }} that submitted building benchmarking data.
      </p>
      <p>
        Learn more at
        <a
          :href="`https://www.chicago.gov/city/en/about/wards/${wardZeroed}.html`"
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
  </DefaultLayout>
</template>

<style lang="scss">
.ward-page {
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
