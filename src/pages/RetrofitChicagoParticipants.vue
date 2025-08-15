<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { IBuilding, IBuildingNode } from '../common-functions.vue';
import {
  BuildingsCustomInfo,
  IBuildingCustomInfo,
  BuildingTags,
} from '../constants/buildings-custom-info.constant.vue';

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
    return { title: 'Retrofit Chicago Participant Case Studies' };
  },
})
export default class ChicagoRetrofitParticipants extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  readonly $static!: { allBuilding: { edges: Array<IBuildingNode> } };

  buildingsFiltered: Array<IBuildingEdge> = [];

  created(): void {
    this.filterBuildings();
  }

  filterBuildings(): void {
    // Loop through BuildingsCustomInfo to get the IDs of buildings we are looking for
    const retrofitBuildingSlugs: Array<string> = Object.entries(
      BuildingsCustomInfo,
    )
      .filter(([, buildingInfo]: [string, IBuildingCustomInfo]) => {
        return buildingInfo.tags?.includes(BuildingTags.hasRetrofitCaseStudy);
      })
      .map(([buildingID]: [string, IBuildingCustomInfo]) => buildingID);

    this.buildingsFiltered = this.$static.allBuilding.edges.filter(
      (buildingEdge: IBuildingEdge) => {
        return retrofitBuildingSlugs.some(
          (ownedBuildingID) => buildingEdge.node.ID === ownedBuildingID,
        );
      },
    );
  }
}
</script>

<!--
  This page grabs all buildings and then filters by owner on the client-side, since that data isn't
  baked into the actual building CSV
-->
<static-query>
  query {
    # Retrofit page only needs core BuildingsTable fields (no conditional fields)
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
          DataAnomalies
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <div class="retrofit-page">
      <h1 id="main-content" tabindex="-1">
        Retrofit Chicago Participant Case Studies
      </h1>

      <p class="constrained -wide">
        These buildings participated in the Retrofit Chicago program and have
        published case studies, so you can learn more about how they became more
        efficient!
      </p>

      <p>
        Buildings sourced from
        <a
          href="https://www.chicago.gov/city/en/sites/retrofit-chicago2/home/participant-achievments/past-participants.html#case-studies"
        >
          City of Chicago - Retrofit Chicago </a
        >.
      </p>

      <DataDisclaimer />

      <BuildingsTable :buildings="buildingsFiltered" />

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.retrofit-page {
}
</style>
