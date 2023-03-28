<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { IBuilding } from '../common-functions';
import {
  BuildingOwners, IBuildingOwner, BuildingsCustomInfo, IBuildingCustomInfo,
} from '../constants/buildings-custom-info.constant.vue';

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
    return { title:  'Biggest Buildings' };
  },
})
export default class BiggestBuildings extends Vue {
  readonly BuildingOwners = BuildingOwners;

  /** Set by Gridsome to results of GraphQL query */
  readonly $static: any;

  currOwner?: IBuildingOwner;
  buildingsFiltered: Array<IBuilding> = [];

  created(): void {
    const ownerId: string = window.location.pathname.split('/owner/')[1];

    if (BuildingOwners[ownerId]) {
      this.currOwner = BuildingOwners[ownerId];

      this.filterBuildings(ownerId);
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

      <!-- TODO: Add intro text
      <p class="constrained -wide">
        Lorem ipsum
      </p>
      -->

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
}
</style>
