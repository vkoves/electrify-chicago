<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { LatestDataYear } from '../constants/globals.vue';
import DataSourceFootnote from '../components/DataSourceFootnote.vue';
import {
  IBuilding,
  IBuildingNode,
  IHistoricData,
  hasReportedData,
  smoothlyScrollToAnchor,
} from '../common-functions.vue';

@Component<any>({
  components: {
    BuildingsTable,
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
    latestYearBenchmarks: { edges: Array<{ node: IHistoricData }> };
    previousYearBenchmarks: { edges: Array<{ node: IHistoricData }> };
    allPreviousYearsBenchmarks: { edges: Array<{ node: IHistoricData }> };
  };

  mounted(): void {}

  // Import the smooth scroll function from common-functions
  readonly smoothlyScrollToAnchor = smoothlyScrollToAnchor;

  get newBuildings(): Array<{ node: IBuilding }> {
    // Get all buildings that submitted in the latest year (already filtered by GraphQL)
    const latestYearSubmitted = new Set(
      this.$static.latestYearBenchmarks.edges
        .filter((edge: { node: IHistoricData }) => hasReportedData(edge.node))
        .map((edge: { node: IHistoricData }) => edge.node.ID),
    );

    // Get all buildings that submitted in any previous year (already filtered by GraphQL)
    const previousYearsSubmitted = new Set(
      this.$static.allPreviousYearsBenchmarks.edges
        .filter((edge: { node: IHistoricData }) => hasReportedData(edge.node))
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

  get consistentReportersCount(): number {
    // Get buildings that reported in both years (already filtered by GraphQL)
    const latestYearSubmitted = new Set(
      this.$static.latestYearBenchmarks.edges
        .filter((edge: { node: IHistoricData }) => hasReportedData(edge.node))
        .map((edge: { node: IHistoricData }) => edge.node.ID),
    );

    const previousYearSubmitted = new Set(
      this.$static.previousYearBenchmarks.edges
        .filter((edge: { node: IHistoricData }) => hasReportedData(edge.node))
        .map((edge: { node: IHistoricData }) => edge.node.ID),
    );

    // Count buildings that reported in BOTH years
    return Array.from(latestYearSubmitted).filter((id) =>
      previousYearSubmitted.has(id),
    ).length;
  }

  get netChangeInReporting(): number {
    return this.newBuildings.length - this.stoppedReportingBuildings.length;
  }

  get stoppedReportingBuildings(): Array<{ node: IBuilding }> {
    // Get buildings that submitted in the previous year (already filtered by GraphQL)
    const previousYearSubmitted = new Set(
      this.$static.previousYearBenchmarks.edges
        .filter((edge: { node: IHistoricData }) => hasReportedData(edge.node))
        .map((edge: { node: IHistoricData }) => edge.node.ID),
    );

    // Get buildings that submitted in the latest year (already filtered by GraphQL)
    const latestYearSubmitted = new Set(
      this.$static.latestYearBenchmarks.edges
        .filter((edge: { node: IHistoricData }) => hasReportedData(edge.node))
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
    # Building details for display in tables (name, address, rankings, grades)
    allBuilding {
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
          path
          PrimaryPropertyType
          YearBuilt
          GrossFloorArea
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
          GHGIntensity
          GHGIntensityRank
          GHGIntensityPercentileRank
          TotalGHGEmissions
          TotalGHGEmissionsRank
          TotalGHGEmissionsPercentileRank
          NaturalGasUse
          DistrictSteamUse
          AvgPercentileLetterGrade
          DataAnomalies
        }
      }
    }
    # Latest year (2023) benchmark data for identifying current reporters
    latestYearBenchmarks: allBenchmark(filter: { DataYear: { eq: 2023 } }) {
      edges {
        node {
          ID
          GHGIntensity
        }
      }
    }
    # Previous year (2022) benchmark data for consistent reporter count
    previousYearBenchmarks: allBenchmark(filter: { DataYear: { eq: 2022 } }) {
      edges {
        node {
          ID
          GHGIntensity
        }
      }
    }
    # All pre-2023 benchmark data for identifying truly new buildings
    allPreviousYearsBenchmarks: allBenchmark(filter: { DataYear: { lt: 2023 } }) {
      edges {
        node {
          ID
          GHGIntensity
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <h1 id="main-content" tabindex="-1">
      Latest Updates - Changes with {{ LatestDataYear }} Data
    </h1>

    <p class="constrained -wide">
      This page shows buildings that are new to Chicago's energy benchmarking
      program in {{ LatestDataYear }} (first time submitting data) and buildings
      that stopped reporting (submitted data in {{ PreviousDataYear }} but not
      in {{ LatestDataYear }}).
    </p>

    <h2>Want To See How Chicago Buildings Have Changed Over Time?</h2>

    <p class="constrained -wide">
      Check out our new
      <g-link to="/citywide-stats" class="bold"
        >City Wide Statistics Page</g-link
      >
      or view
      <a
        href="https://www.chicago.gov/content/dam/city/depts/doe/Reports/43360-20250404-DOE-Sustainability%20Report_C.pdf"
        class="bold"
        target="_blank"
        rel="noopener"
        >Chicago's 2022 - 2023 Chicago Energy Benchmarking Report
        <NewTabIcon />
      </a>
      for more analysis!
    </p>

    <!-- Quick Stats Section -->
    <section class="stats-overview">
      <h2>Quick Stats</h2>
      <div class="stats-grid">
        <a
          href="#new-buildings"
          class="stat-card-link"
          @click="smoothlyScrollToAnchor"
        >
          <div class="stat-card positive -clickable">
            <div class="stat-number">
              {{ newBuildings.length.toLocaleString() }}
            </div>
            <div class="stat-label">New Buildings</div>
            <div class="stat-description">
              Reported for the first time in {{ LatestDataYear }}
            </div>
          </div>
        </a>

        <a
          href="#stopped-reporting"
          class="stat-card-link"
          @click="smoothlyScrollToAnchor"
        >
          <div class="stat-card negative -clickable">
            <div class="stat-number">
              {{ stoppedReportingBuildings.length.toLocaleString() }}
            </div>
            <div class="stat-label">Stopped Reporting</div>
            <div class="stat-description">
              Reported in {{ PreviousDataYear }} but not {{ LatestDataYear }}
            </div>
          </div>
        </a>

        <div
          class="stat-card"
          :class="{
            positive: netChangeInReporting > 0,
            negative: netChangeInReporting < 0,
            'net-zero': netChangeInReporting === 0,
          }"
        >
          <div class="stat-number">
            {{ netChangeInReporting > 0 ? '+' : ''
            }}{{ netChangeInReporting.toLocaleString() }}
          </div>
          <div class="stat-label">Net Change</div>
          <div class="stat-description">
            {{
              netChangeInReporting > 0
                ? 'More'
                : netChangeInReporting < 0
                  ? 'Fewer'
                  : 'Same'
            }}
            buildings reporting vs {{ PreviousDataYear }}
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-number">
            {{ consistentReportersCount.toLocaleString() }}
          </div>
          <div class="stat-label">Consistent Reporters</div>
          <div class="stat-description">
            Reported in both {{ PreviousDataYear }} and {{ LatestDataYear }}
          </div>
        </div>
      </div>
    </section>

    <!-- New Buildings Section -->
    <section>
      <h2 id="new-buildings" tabindex="-1">
        New Buildings In {{ LatestDataYear }} ({{ newBuildings.length }})
      </h2>
      <p>
        These buildings first submitted data in {{ LatestDataYear }} - they may
        be new buildings, or just started reporting after non-compliance. Sorted
        by square footage (largest first).
      </p>

      <p v-if="newBuildings.length === 0" class="no-results">
        No new buildings submitted data for the first time in
        {{ LatestDataYear }}.
      </p>

      <BuildingsTable
        v-else
        :buildings="newBuildings"
        :show-square-footage="true"
        :show-year-built="true"
      />
    </section>

    <!-- Stopped Reporting Section -->
    <section>
      <h2 id="stopped-reporting" tabindex="-1">
        Stopped Reporting In {{ LatestDataYear }} ({{
          stoppedReportingBuildings.length
        }})
      </h2>
      <p>
        These buildings submitted data in {{ PreviousDataYear }} but not
        {{ LatestDataYear }}, meaning they either fell into non-compliance or
        were demolished. Sorted by square footage (largest first).
      </p>

      <p v-if="stoppedReportingBuildings.length === 0" class="no-results">
        All buildings that submitted data in {{ PreviousDataYear }} also
        submitted in {{ LatestDataYear }}.
      </p>

      <div v-else class="stopped-reporting-note">
        <p>
          These buildings submitted data in {{ PreviousDataYear }} but did not
          submit in {{ LatestDataYear }}. Data shown is from their most recent
          submission.
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
@import '../scss/stat-tiles.scss';

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
    scroll-margin-top: 1rem;

    + p {
      margin-bottom: 1rem;
    }
  }

  .buildings-table-cont {
    margin-top: 1rem;
  }
}
</style>
