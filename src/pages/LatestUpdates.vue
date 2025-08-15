<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { LatestDataYear } from '../constants/globals.vue';
import DataSourceFootnote from '../components/DataSourceFootnote.vue';
import {
  IBuilding,
  IBuildingNode,
  IHistoricData,
} from '../common-functions.vue';

@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
  },
  metaInfo() {
    return { title: 'Latest Updates' };
  },
})
export default class LatestUpdates extends Vue {
  readonly LatestDataYear: number = LatestDataYear;
  readonly PreviousDataYear: number = LatestDataYear - 1;

  /** Set by Gridsome to results of GraphQL query */
  readonly $static!: {
    allBuilding: { edges: Array<IBuildingNode> };
    allBenchmark: { edges: Array<{ node: IHistoricData }> };
  };

  mounted(): void {
    console.log(this.$static.allBuilding);
  }

  get newBuildings(): Array<{ node: IBuilding }> {
    // Get all buildings that submitted in the latest year
    const latestYearSubmitted = new Set(
      this.$static.allBenchmark.edges
        .filter(
          (edge: { node: IHistoricData }) =>
            edge.node.DataYear === this.LatestDataYear &&
            ['Submitted', 'Submitted Data'].includes(edge.node.ReportingStatus),
        )
        .map((edge: { node: IHistoricData }) => edge.node.ID),
    );

    // Get all buildings that submitted in any previous year
    const previousYearsSubmitted = new Set(
      this.$static.allBenchmark.edges
        .filter(
          (edge: { node: IHistoricData }) =>
            edge.node.DataYear < this.LatestDataYear &&
            ['Submitted', 'Submitted Data'].includes(edge.node.ReportingStatus),
        )
        .map((edge: { node: IHistoricData }) => edge.node.ID),
    );

    // New buildings are those that submitted in latest year but never before
    const newBuildingIds = Array.from(latestYearSubmitted).filter(
      (id) => !previousYearsSubmitted.has(id),
    );

    // Return building details for new buildings, sorted by square footage
    return this.$static.allBuilding.edges
      .filter((edge: { node: IBuilding }) =>
        newBuildingIds.includes(edge.node.ID.toString()),
      )
      .sort((a, b) => b.node.GrossFloorArea - a.node.GrossFloorArea);
  }

  get stoppedReportingBuildings(): Array<{ node: IBuilding }> {
    // Get buildings that submitted in the previous year
    const previousYearSubmitted = new Set(
      this.$static.allBenchmark.edges
        .filter(
          (edge: { node: IHistoricData }) =>
            edge.node.DataYear === this.PreviousDataYear &&
            ['Submitted', 'Submitted Data'].includes(edge.node.ReportingStatus),
        )
        .map((edge: { node: IHistoricData }) => edge.node.ID),
    );

    // Get buildings that submitted in the latest year
    const latestYearSubmitted = new Set(
      this.$static.allBenchmark.edges
        .filter(
          (edge: { node: IHistoricData }) =>
            edge.node.DataYear === this.LatestDataYear &&
            ['Submitted', 'Submitted Data'].includes(edge.node.ReportingStatus),
        )
        .map((edge: { node: IHistoricData }) => edge.node.ID),
    );

    // Stopped reporting are those that submitted in previous year but not latest
    const stoppedBuildingIds = Array.from(previousYearSubmitted).filter(
      (id) => !latestYearSubmitted.has(id),
    );

    // Get building details from the current building dataset (which includes their names/addresses)
    // Most non-reporting buildings are still in the current dataset with their latest submission
    return this.$static.allBuilding.edges
      .filter((edge: { node: IBuilding }) =>
        stoppedBuildingIds.includes(edge.node.ID.toString()),
      )
      .sort((a, b) => b.node.GrossFloorArea - a.node.GrossFloorArea);
  }
}
</script>

<static-query>
  query {
    allBuilding {
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
          ZIPCode
          path
          PrimaryPropertyType
          GrossFloorArea
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
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
          AvgPercentileLetterGrade
          DataAnomalies
        }
      }
    }
    allBenchmark {
      edges {
        node {
          ID
          DataYear
          ReportingStatus
          GrossFloorArea
          TotalGHGEmissions
          GHGIntensity
          ElectricityUse
          NaturalGasUse
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <h1 id="main-content" tabindex="-1">
      Latest Updates: {{ LatestDataYear }} Reporting Changes
    </h1>

    <p class="constrained -wide">
      This page shows buildings that are new to Chicago's energy benchmarking
      program in {{ LatestDataYear }} (first time submitting data) and buildings
      that stopped reporting (submitted data in {{ PreviousDataYear }} but not
      in {{ LatestDataYear }}).
    </p>

    <DataDisclaimer />

    <!-- New Buildings Section -->
    <section>
      <h2>New Buildings ({{ newBuildings.length }})</h2>
      <p>
        First submitted data in {{ LatestDataYear }}, sorted by square footage
        (largest first)
      </p>

      <p v-if="newBuildings.length === 0" class="no-results">
        No new buildings submitted data for the first time in
        {{ LatestDataYear }}.
      </p>

      <BuildingsTable
        v-else
        :buildings="newBuildings"
        :show-square-footage="true"
      />
    </section>

    <!-- Stopped Reporting Section -->
    <section>
      <h2>Stopped Reporting ({{ stoppedReportingBuildings.length }})</h2>
      <p>
        Submitted data in {{ PreviousDataYear }} but not {{ LatestDataYear }},
        sorted by square footage (largest first)
      </p>

      <p v-if="stoppedReportingBuildings.length === 0" class="no-results">
        All buildings that submitted data in {{ PreviousDataYear }} also
        submitted in {{ LatestDataYear }}.
      </p>

      <div v-else class="stopped-reporting-note">
        <p>
          <strong>Note:</strong> These buildings submitted data in
          {{ PreviousDataYear }} but did not submit in {{ LatestDataYear }}.
          Data shown is from their most recent submission.
        </p>
      </div>

      <BuildingsTable
        v-if="stoppedReportingBuildings.length > 0"
        :buildings="stoppedReportingBuildings"
        :show-square-footage="true"
      />
    </section>

    <DataSourceFootnote />
  </DefaultLayout>
</template>

<style lang="scss">
@import '../scss/global';

.no-results {
  padding: 2rem;
  text-align: center;
  background-color: $grey-light;
  border-radius: $brd-rad-medium;
  margin: 1rem 0;
}

.stopped-reporting-note {
  background-color: $warning-background;
  border: $border-thin solid $warning-border;
  border-radius: $brd-rad-medium;
  padding: 1rem;
  margin: 1rem 0;

  p {
    margin: 0;
    font-size: 0.9rem;
  }
}

section {
  margin: 3rem 0;

  h2 {
    margin-bottom: 0;
  }
  h2 + p {
    margin-bottom: 1rem;
  }
}
</style>
