<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { Links } from '../constants/links.constant.vue';
import { IBuilding, IBuildingNode } from '../common-functions.vue';
import {
  BuildingTags,
  validateTaggedBuildings,
} from '../constants/buildings-custom-info.constant.vue';

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
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
  },
  metaInfo() {
    return { title: 'Retrofit Chicago Participant Case Studies' };
  },
})
export default class ChicagoRetrofitParticipants extends Vue {
  readonly Links: typeof Links = Links;

  /** Set by Gridsome to results of GraphQL query */
  readonly $static!: { allBuilding: { edges: Array<IBuildingNode> } };

  buildingsFiltered: Array<IBuildingEdge> = [];

  created(): void {
    validateTaggedBuildings(
      BuildingTags.hasRetrofitCaseStudy,
      this.$static.allBuilding.edges.map((e) => e.node.ID.toString()),
    );
    this.buildingsFiltered = this.$static.allBuilding.edges;
  }
}
</script>

<!--
  This page grabs all buildings and then filters by owner on the client-side, since that data isn't
  baked into the actual building CSV
-->
<static-query>
  query {
    # PERFORMANCE OPTIMIZATION: Hard-coded filter for buildings with hasRetrofitCaseStudy tag
    # These IDs MUST match buildings-custom-info.constant.vue (validated at runtime)
    # When adding/removing retrofit buildings, update both this query AND the constant
    allBuilding(
      sortBy: "GHGIntensity",
      filter: {
        ID: {
          in: ["103721", "101920", "102336", "101852", "251328", "252064", "256405", "252065"]
        }
      }
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
        <a :href="Links.ChicagoRetrofitParticipants">
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
