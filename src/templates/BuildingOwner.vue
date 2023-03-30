<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { IBuildingBenchmarkStats, IBuilding } from '../common-functions.vue';
import {
  BuildingOwners, IBuildingOwner, BuildingsCustomInfo, IBuildingCustomInfo,
} from '../constants/buildings-custom-info.constant.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';

interface IBuildingEdge { node: IBuilding; }

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    NewTabIcon,
  },
  metaInfo() {
    return { title:  (this.currOwner?.nameShort + ' Buildings') || 'Building Owner' };
  },
})
export default class BiggestBuildings extends Vue {
  readonly BuildingOwners = BuildingOwners;

  /** Expose stats to template */
  BuildingBenchmarkStats: IBuildingBenchmarkStats = BuildingBenchmarkStats;

  /** Set by Gridsome to results of GraphQL query */
  readonly $static: any;
  readonly $context: any;

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
    // Loop through BuildingsCustomInfo to get the slugs of buildings we are looking for
    const ownerBuildingsSlugs: Array<string> = Object.entries(BuildingsCustomInfo)
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      .filter(([ buildingSlug, buildingInfo ]: [string, IBuildingCustomInfo]) => {
        return buildingInfo.owner === ownerId;
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      }).map(([ buildingSlug, buildingInfo ]: [string, IBuildingCustomInfo]) => buildingSlug);

    this.buildingsFiltered =
      this.$static.allBuilding.edges.filter((buildingEdge: IBuildingEdge) => {
        return ownerBuildingsSlugs.some((ownedBuildingSlug) =>
          (buildingEdge.node.path as string).includes(ownedBuildingSlug));
      });
  }

  calculateOwnedBuildingStats(): void {
    let totalGHGEmissions = 0;
    let totalGHGIntensity = 0;

    this.buildingsFiltered.forEach((buildingEdge: IBuildingEdge) => {
      const building: IBuilding = buildingEdge.node;

      totalGHGIntensity += parseFloat(building.GHGIntensity as string);
      totalGHGEmissions += parseFloat(building.TotalGHGEmissions as string);
    });

    this.totalGHGEmissions = Math.round(totalGHGEmissions).toLocaleString();
    const avgGHGIntensity: number = totalGHGIntensity / this.buildingsFiltered.length;
    this.avgGHGIntensity = avgGHGIntensity.toFixed(1);

    this.medianGHGIntensityMultiple =
      (avgGHGIntensity / BuildingBenchmarkStats.GHGIntensity.median).toFixed(0);
    this.medianGHGEmissionsMultiple =
      (totalGHGEmissions / BuildingBenchmarkStats.TotalGHGEmissions.median).toFixed(0);
  }
}
</script>

<!--
  This page grabs all buildings and then filters by owner on the client-side, since that data isn't
  baked into the actual building CSV
-->
<static-query>
  query {
    allBuilding(sortBy: "GHGIntensity") {
      edges {
        node {
          slugSource
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
          ElectricityUse
          ElectricityUseRank
          ElectricityUsePercentileRank
          NaturalGasUse
          NaturalGasUseRank
          NaturalGasUsePercentileRank
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <div class="building-owner-page">
      <h1
        id="main-content"
        tabindex="-1"
      >
        <div class="top-title">
          Buildings Owned By
        </div>

        <img
          :src="currOwner.logoLarge"
          alt=""
        >

        {{ currOwner.name }}
      </h1>

      <p class="constrained -wide">
        These are buildings that we have manually tagged as being owned by {{ currOwner.name }},
        so this may not be a definitive list.
      </p>

      <h2>Building Stats</h2>

      <ul class="stats">
        <li class="bold">
          {{ buildingsFiltered.length }} Tagged Buildings
        </li>

        <li>
          <strong>
            Total Emissions:
            {{ totalGHGEmissions }} metric tons CO<sub>2</sub> equivalent
          </strong>

          <p class="footnote">
            <strong>
              Equivalent to {{ medianGHGEmissionsMultiple }} of the median benchmarked
              building
            </strong>
            ({{ BuildingBenchmarkStats.TotalGHGEmissions.median.toLocaleString() }}
            tons CO<sub>2</sub>e)
          </p>
        </li>

        <li>
          <strong>
            Average GHG Intensity:
            {{ avgGHGIntensity }} kg CO<sub>2</sub>e/sqft
          </strong>

          <p class="footnote">
            <strong>{{ medianGHGIntensityMultiple }}x the median benchmarked building</strong>
            ({{ BuildingBenchmarkStats.GHGIntensity.median }} kg CO<sub>2</sub>/sqft)
          </p>
        </li>
      </ul>

      <DataDisclaimer />

      <BuildingsTable
        :buildings="buildingsFiltered"
      />

      <p class="footnote">
        Data Source:
        <!-- eslint-disable-next-line max-len -->
        <a
          href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
          target="_blank"
          rel="noopener noreferrer"
        >
          Chicago Energy Benchmarking Data <NewTabIcon />
        </a>
      </p>
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
    }
  }

  h2 { margin-bottom: 0.5rem; }

  .stats {
    margin-top: 0;
    padding-left: 1.25rem;

    li + li { margin-top: 0.5rem; }

    .footnote { margin: 0rem; }
  }
}
</style>
