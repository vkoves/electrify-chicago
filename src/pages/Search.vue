<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import {
  fullyGasFree,
  IBuilding,
  IBuildingBenchmarkStats,
  IBuildingNode,
  IHistoricData,
  isNewBuilding,
  normalizeForSearch,
} from '../common-functions.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import PropertyTypesConstant from '../data/dist/property-types.json';
import DataSourceFootnote from '../components/DataSourceFootnote.vue';

interface IBuildingEdge {
  node: IBuilding;
}

interface ISelectOption {
  label: string;
  value: string;
}

interface IFilter {
  isActive: boolean;
  apply: (buildings: Array<IBuildingEdge>) => Array<IBuildingEdge>;
}

interface INormalizedFields {
  name: string;
  address: string;
  type: string;
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
  metaInfo: {
    title: 'Search',
  },
})
export default class Search extends Vue {
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats =
    BuildingBenchmarkStats;
  readonly MaxBuildings = 100;

  /** Pre-computed index of building ID to historical data for performance */
  private historicalDataIndex: Map<string | number, Array<IHistoricData>> =
    new Map();

  readonly QueryParamKeys = {
    search: 'q',
    propertyType: 'type',
  };

  /** Set by Gridsome to results of GraphQL query */
  readonly $static!: {
    allBuilding: { edges: Array<IBuildingNode> };
    allBenchmark: { edges: Array<{ node: IHistoricData }> };
  };

  // readonly $page!: { allBuilding: { edges: Array<IBuildingNode> } };

  /** The search query */
  searchFilter = '';

  /** The selected property type filter */
  propertyTypeFilter = '';

  /** The current sorted field (column) */
  sortedField = 'GHGIntensity';

  /** The direction of the sorted field (column) */
  sortedDirection: 'asc' | 'desc' = 'desc';

  /** Flags 'true' when any filter is applied,
   * so that column sort (asc, desc) applies only to filtered results */
  hasFilteredResults = false;

  gradeFilter = '';
  gradeQuintileFilter = '';

  /** Filter for all electric buildings */
  allElectricFilter = false;

  /** Filter for new buildings */
  newBuildingsFilter = false;

  propertyTypeOptions: Array<ISelectOption> = [
    { label: 'Select Property Type', value: '' },
  ].concat(
    PropertyTypesConstant.propertyTypes.map((type) => ({
      label: type,
      value: type,
    })),
  );

  letterGradeOptions: Array<ISelectOption> = [
    { label: 'Select Grade', value: '' },
    { label: 'A', value: 'A' },
    { label: 'B', value: 'B' },
    { label: 'C', value: 'C' },
    { label: 'D', value: 'D' },
    { label: 'F', value: 'F' },
  ];

  searchResults: Array<IBuildingEdge> = [];
  totalResultsCount = 0;

  /** Dropdown information on database details */
  dataDisclaimer!: HTMLDetailsElement;

  /**
   * Precomputed normalized PropertyName/Address/PrimaryPropertyType for each
   * building edge. Built once so searches don't re-normalize ~6k records per
   * keystroke. Keyed by edge so the table can keep using the original nodes.
   */
  normalizedCache: Map<IBuildingEdge, INormalizedFields> = new Map();

  created(): void {
    // Initialize performance index for historical data
    this.initializeHistoricalDataIndex();

    // Precompute normalized search fields for all buildings
    this.buildNormalizedCache();

    // Make sure on load we have some data
    this.setSearchResults(this.$static.allBuilding.edges);
  }

  buildNormalizedCache(): void {
    for (const edge of this.$static.allBuilding.edges) {
      this.normalizedCache.set(edge, {
        name: normalizeForSearch(edge.node.PropertyName ?? ''),
        address: normalizeForSearch(edge.node.Address ?? ''),
        type: normalizeForSearch(edge.node.PrimaryPropertyType ?? ''),
      });
    }
  }

  getNormalized(edge: IBuildingEdge): INormalizedFields {
    return (
      this.normalizedCache.get(edge) ?? { name: '', address: '', type: '' }
    );
  }

  mounted(): void {
    const urlParams = new URLSearchParams(window.location.search);
    const urlSearchParam = urlParams.get(this.QueryParamKeys.search);
    const urlPropertyTypeParam = urlParams.get(
      this.QueryParamKeys.propertyType,
    );

    if (urlSearchParam) {
      this.searchFilter = urlSearchParam;
    }

    if (urlPropertyTypeParam) {
      this.propertyTypeFilter = urlPropertyTypeParam;
    }

    this.submitSearch();
  }

  searchRank(buildingEdge: IBuildingEdge, normalizedQuery: string): number {
    const fields = this.getNormalized(buildingEdge);
    let matchScore = 0;

    if (fields.name.includes(normalizedQuery)) {
      matchScore += 3;
    } else if (fields.address.includes(normalizedQuery)) {
      matchScore += 2;
    } else if (fields.type.includes(normalizedQuery)) {
      matchScore += 1;
    }

    return matchScore;
  }

  /**
   * Get all active filter configurations
   */
  private getActiveFilters(): Array<IFilter> {
    const normalizedQuery = normalizeForSearch(this.searchFilter);

    return [
      // Text search filter
      {
        isActive: Boolean(normalizedQuery),
        apply: (buildings: Array<IBuildingEdge>) => {
          const filtered = buildings.filter((buildingEdge: IBuildingEdge) => {
            const fields = this.getNormalized(buildingEdge);
            return (
              fields.name.includes(normalizedQuery) ||
              fields.address.includes(normalizedQuery) ||
              fields.type.includes(normalizedQuery)
            );
          });

          // Sort by relevance
          return filtered.sort(
            (a: IBuildingEdge, b: IBuildingEdge) =>
              this.searchRank(b, normalizedQuery) -
              this.searchRank(a, normalizedQuery),
          );
        },
      },
      // Property type filter
      {
        isActive: Boolean(this.propertyTypeFilter),
        apply: (buildings: Array<IBuildingEdge>) =>
          this.filterResults(
            buildings,
            'PrimaryPropertyType',
            this.propertyTypeFilter,
          ),
      },
      // Grade filter
      {
        isActive: Boolean(this.gradeFilter),
        apply: (buildings: Array<IBuildingEdge>) =>
          this.filterResults(
            buildings,
            'AvgPercentileLetterGrade',
            this.gradeFilter,
          ),
      },
      // All electric filter
      {
        isActive: this.allElectricFilter,
        apply: (buildings: Array<IBuildingEdge>) =>
          buildings.filter((edge) => fullyGasFree(edge.node)),
      },
      // New buildings filter
      {
        isActive: this.newBuildingsFilter,
        apply: (buildings: Array<IBuildingEdge>) =>
          buildings.filter((edge) =>
            isNewBuilding(this.getHistoricalDataForBuilding(edge.node.ID)),
          ),
      },
    ];
  }

  submitSearch(event?: Event): void {
    if (event) {
      event.preventDefault();
    }

    const rawQuery = this.searchFilter.trim();

    const propertyFilterEncoded = encodeURIComponent(this.propertyTypeFilter);

    // Keep the URL bar showing what the user typed, not the normalized form
    let newUrl = `/search?${this.QueryParamKeys.search}=${encodeURIComponent(rawQuery)}`;

    if (propertyFilterEncoded) {
      newUrl += `&${this.QueryParamKeys.propertyType}=${propertyFilterEncoded}`;
    }

    window.history.pushState(null, '', newUrl);

    const filters = this.getActiveFilters();
    const activeFilters = filters.filter((f) => f.isActive);

    // If no filters are active, return all results
    if (activeFilters.length === 0) {
      this.hasFilteredResults = false;
      this.setSearchResults(this.$static.allBuilding.edges);
      return;
    }

    // Apply all active filters in sequence
    let buildingsResults: Array<IBuildingEdge> = this.$static.allBuilding.edges;
    for (const filter of activeFilters) {
      buildingsResults = filter.apply(buildingsResults);
    }

    this.hasFilteredResults = true;
    this.setSearchResults(buildingsResults);
  }

  /** Handles clicks on numeric columns in
   * BuildingsTable and sorts (desc, asc) */
  handleSort(field: string): void {
    // if clicking on the same field,
    // this will toggle between 'desc' and 'asc'
    if (this.sortedField === field) {
      this.sortedDirection = this.sortedDirection === 'desc' ? 'asc' : 'desc';
    } else {
      // else if clicking on a new field, set sortedField state
      // to the new field AND set initial sortedDirection to 'desc'
      this.sortedField = field;
      this.sortedDirection = 'desc';
    }

    /** If there are filtered results (type, grade, search results)
     * pass to runSort. If not, sort all. */
    let buildingsToSort;
    if (this.hasFilteredResults) {
      buildingsToSort = [...this.searchResults];
    } else {
      buildingsToSort = [...this.$static.allBuilding.edges];
    }

    this.runSort(buildingsToSort);
  }

  /** Called from handleSort, this function sorts
   * according to sortedField and sortedDirection state values */
  runSort(buildings: Array<IBuildingNode>): void {
    const sortedBuildings = buildings.sort(
      (buildingEdgeA: IBuildingEdge, buildingEdgeB: IBuildingEdge) => {
        const valueA = Number(buildingEdgeA.node[this.sortedField]);
        const valueB = Number(buildingEdgeB.node[this.sortedField]);

        if (this.sortedDirection === 'desc') {
          return valueB - valueA;
        } else {
          return valueA - valueB;
        }
      },
    );
    // calls setSearchResults to update state and set to 100 buildings
    this.setSearchResults(sortedBuildings);
  }

  /**
   * Filter building results by a column and a value
   */
  filterResults(
    results: Array<IBuildingEdge>,
    column: string,
    value: string,
  ): Array<IBuildingEdge> {
    return results.filter(
      (buildingEdge: IBuildingEdge) => buildingEdge.node[column] === value,
    );
  }

  /**
   * Set the searchResults to a trimmed version of
   */
  setSearchResults(allResults: Array<IBuildingEdge>): void {
    this.totalResultsCount = allResults.length;
    this.searchResults = allResults.slice(0, this.MaxBuildings);
  }

  /**
   * Initialize the historical data index for O(1) lookups
   */
  private initializeHistoricalDataIndex(): void {
    this.historicalDataIndex.clear();

    for (const edge of this.$static.allBenchmark.edges) {
      const buildingId = edge.node.ID;
      if (!this.historicalDataIndex.has(buildingId)) {
        this.historicalDataIndex.set(buildingId, []);
      }
      this.historicalDataIndex.get(buildingId)!.push(edge.node);
    }
  }

  /**
   * Get historical data for a specific building ID (O(1) lookup)
   */
  getHistoricalDataForBuilding(
    buildingId: string | number,
  ): Array<IHistoricData> {
    return this.historicalDataIndex.get(buildingId) || [];
  }

  /**
   * Apply current filters and run search
   */
  applyFilters(): void {
    this.submitSearch();
  }

  /**
   * Clear all filters and reset to default search
   */
  clearFilters(): void {
    this.propertyTypeFilter = '';
    this.gradeFilter = '';
    this.gradeQuintileFilter = '';
    this.allElectricFilter = false;
    this.newBuildingsFilter = false;
    this.submitSearch();
  }

  /**
   * Toggles DataDisclaimer open from the no-results message
   */
  openDataDisclaimer(): void {
    this.dataDisclaimer = document.getElementById(
      'data-disclaimer',
    ) as HTMLDetailsElement;
    this.dataDisclaimer.open = true;
  }
}
</script>

<static-query>
  query {
    # Search page only needs core BuildingsTable fields (no conditional fields)
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
    # Get all historical data for new building detection
    allBenchmark(sortBy: "DataYear", order: ASC) {
      edges {
        node {
          ID
          DataYear
          GHGIntensity
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <div class="search-page">
      <h1 id="main-content" tabindex="-1">Search Buildings</h1>

      <p>
        Search all of Chicago's benchmarked buildings by name or type! Note that
        results are limited to the first {{ MaxBuildings }} matches.
      </p>

      <DataDisclaimer id="data-disclaimer" />

      <form class="search-form">
        <div>
          <label for="page-search"> Building Name </label>
          <div class="input-cont">
            <input
              id="page-search"
              v-model="searchFilter"
              type="text"
              name="search"
              placeholder="Search property name, type, or address"
            />
            <button type="submit" class="-grey" @click="submitSearch">
              <img src="/search.svg" alt="" width="15" height="15" />
              Search
            </button>
          </div>
        </div>
      </form>

      <details class="filters-section">
        <summary>Advanced Filters</summary>
        <div class="details-content">
          <div class="filter-grid">
            <div class="select-row">
              <div>
                <label for="property-type">Property Type</label>
                <select id="property-type" v-model="propertyTypeFilter">
                  <option
                    v-for="propertyType in propertyTypeOptions"
                    :key="propertyType.value ?? propertyType"
                    :value="propertyType.value ?? propertyType"
                  >
                    {{ propertyType.label || propertyType }}
                  </option>
                </select>
              </div>

              <div>
                <label for="grade-filter">Grade</label>
                <select id="grade-filter" v-model="gradeFilter">
                  <option
                    v-for="gradeOpt in letterGradeOptions"
                    :key="gradeOpt.value"
                    :value="gradeOpt.value"
                  >
                    {{ gradeOpt.label }}
                  </option>
                </select>
              </div>
            </div>

            <div class="checkbox-row">
              <div>
                <input
                  id="all-electric-filter"
                  v-model="allElectricFilter"
                  type="checkbox"
                />
                <label for="all-electric-filter">⚡ All Electric</label>
              </div>

              <div>
                <input
                  id="new-buildings-filter"
                  v-model="newBuildingsFilter"
                  type="checkbox"
                />
                <label for="new-buildings-filter">New</label>
              </div>
            </div>
          </div>

          <div class="filter-actions">
            <button class="-grey" type="button" @click="applyFilters">
              Apply Filters
            </button>
            <button class="-grey" type="button" @click="clearFilters">
              Clear Filters
            </button>
          </div>
        </div>
      </details>

      <BuildingsTable
        :buildings="searchResults"
        :sorted-field="sortedField"
        :sorted-direction="sortedDirection"
        :show-sort="true"
        @sort="handleSort"
      />

      <div v-if="searchResults.length === 0" class="no-results-msg">
        <h2>No results found!</h2>

        <p class="layout-constrained">
          There may be a typo in your search, the building name may be different
          in the underlying data, or the building you are looking for may not be
          in our dataset (buildings in Chicago over 50,000 square feet - see
          <a href="#data-disclaimer" @click="openDataDisclaimer"
            >dataset disclaimer</a
          >).
        </p>

        <p>
          <strong>Note:</strong> Addresses generally follow the format
          <em>123 W Main St</em>
        </p>
      </div>

      <p class="results-count">
        Showing
        <strong>
          {{ Math.min(MaxBuildings, totalResultsCount) }} of total
          {{ totalResultsCount }}
        </strong>
        matching buildings
      </p>

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.search-page {
  form {
    display: flex;
    align-items: flex-end;
    gap: 0.5rem;
    border-radius: $brd-rad-small;
    margin-bottom: 1rem;

    label {
      display: block;
      margin-bottom: 0.25rem;
      font-size: 0.75rem;
      font-weight: 500;
    }

    input {
      width: 20rem;
    }

    select {
      padding: 0.5rem;
      max-width: 12rem;
    }

    /** Mobile Styling */
    @media (max-width: $mobile-max-width) {
      padding: 0.5rem;
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  }

  .filters-section {
    margin: 1rem 0;

    summary {
      padding: 0.5rem 1rem;
      font-size: 0.75rem;
    }

    .filter-grid {
      display: flex;
      gap: 1rem;
    }

    .select-row,
    .checkbox-row {
      display: flex;
      gap: 0 1rem;
      flex-wrap: wrap;
    }

    .select-row {
      margin-bottom: 1rem;

      > div {
        display: flex;
        flex-direction: column;
      }

      select {
        padding: 0.5rem;
        max-width: 12rem;
      }

      label {
        font-size: 0.75rem;
      }
    }

    .checkbox-row {
      > div {
        display: flex;
        align-items: center;
        gap: 0.5rem;
      }

      input[type='checkbox'] {
        margin: 0;
        width: 1rem;
        height: 1rem;
      }

      label {
        margin: 0;
        font-size: 0.875rem;
        font-weight: 600;
        cursor: pointer;
      }
    }

    .filter-actions {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
  }

  .no-results-msg {
    background-color: $grey;
    padding: 1rem 0 2rem 0;
    text-align: center;
  }

  @media (max-width: $mobile-max-width) {
    form {
      background-color: $off-white;
    }

    .no-results-msg {
      margin: 0 -1rem;
    }
    .results-count {
      font-size: 0.8125rem;
    }
  }
}
</style>
