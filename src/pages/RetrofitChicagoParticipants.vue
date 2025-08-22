<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { IBuilding, IBuildingNode } from '../common-functions.vue';
import {
  BuildingsCustomInfo,
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
    this.validateRetrofitBuildings();
    this.buildingsFiltered = this.$static.allBuilding.edges;
  }

  /**
   * IMPORTANT: This page uses a hard-coded GraphQL filter for performance optimization.
   * The building IDs in the GraphQL query MUST match the IDs tagged with hasRetrofitCaseStudy
   * in buildings-custom-info.constant.vue. This validation ensures they stay in sync.
   *
   * If you add/remove buildings with hasRetrofitCaseStudy tags, you MUST also update
   * the GraphQL query filter in this file.
   */
  validateRetrofitBuildings(): void {
    const expectedIds = Object.entries(BuildingsCustomInfo)
      .filter(([, info]) =>
        info.tags?.includes(BuildingTags.hasRetrofitCaseStudy),
      )
      .map(([id]) => id)
      .sort();

    const actualIds = this.$static.allBuilding.edges
      .map((edge) => edge.node.ID.toString())
      .sort();

    const missing = expectedIds.filter((id) => !actualIds.includes(id));
    const extra = actualIds.filter((id) => !expectedIds.includes(id));

    if (missing.length > 0 || extra.length > 0) {
      const details = [
        missing.length > 0 && `Missing: [${missing.join(', ')}]`,
        extra.length > 0 && `Extra: [${extra.join(', ')}]`,
      ]
        .filter(Boolean)
        .join(', ');

      throw new Error(
        `RetrofitChicagoParticipants: GraphQL query mismatch. ${details}. ` +
          'Update GraphQL query to match hasRetrofitCaseStudy tags.',
      );
    }

    console.log(`✅ Retrofit validation: ${actualIds.length} buildings`);
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
