<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
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
      title: this.currOwner?.nameShort + ' Buildings' || 'Building Owner',
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

    this.buildingsFiltered.forEach((buildingEdge: IBuildingEdge) => {
      const building: IBuilding = buildingEdge.node;

      totalGHGIntensity += building.GHGIntensity;
      totalGHGEmissions += building.TotalGHGEmissions;
    });

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
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <div class="building-owner-page">
      <BuildingsHero :buildings="buildingsFiltered.map((edge) => edge.node)">
        <h1 id="main-content" tabindex="-1">
          <div class="top-title">Buildings Owned By</div>

          <img :src="currOwner.logoLarge" alt="" />

          {{ currOwner.name }}
        </h1>
      </BuildingsHero>

      <p class="constrained -wide">
        These are buildings that we have manually tagged as being owned by
        {{ currOwner.name }}, so this may not be a definitive list.
      </p>

      <h2>Building Stats</h2>

      <ul class="stats">
        <li class="bold">{{ buildingsFiltered.length }} Tagged Buildings</li>

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

      <BuildingsTable :buildings="buildingsFiltered" />

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
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
