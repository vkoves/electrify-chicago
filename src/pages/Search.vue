<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import { IBuilding, IBuildingBenchmarkStats } from '../common-functions.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import PropertyTypesConstant from '../data/dist/property-types.json';

interface IBuildingEdge { node: IBuilding; }

@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    NewTabIcon,
  },
  metaInfo: {
    title: 'Search',
  },
})
export default class Search extends Vue {
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats = BuildingBenchmarkStats;
  readonly MaxBuildings = 100;

  readonly QueryParamKeys = {
    search: 'q',
    propertyType: 'type',
  };

  /** Set by Gridsome to results of GraphQL query */
  readonly $static: any;

  /** The search query */
  searchFilter = '';

  /** The selected property type filter */
  propertyTypeFilter = '';

  propertyTypeOptions: Array<{ label: string, value: string} | string> = [
    { label: 'Select Property Type', value: '' },
  ].concat(PropertyTypesConstant.propertyTypes as any);

  searchResults: Array<IBuildingEdge> = [];
  totalResultsCount = 0;

  created(): void {
    // Make sure on load we have some data
    this.setSearchResults(this.$static.allBuilding.edges);
  }

  mounted(): void {
    const urlParams = new URLSearchParams(window.location.search);
    const urlSearchParam = urlParams.get(this.QueryParamKeys.search);
    const urlPropertyTypeParam = urlParams.get(this.QueryParamKeys.propertyType);

    if (urlSearchParam) {
      this.searchFilter = urlSearchParam;
    }

    if (urlPropertyTypeParam) {
      this.propertyTypeFilter = urlPropertyTypeParam;
    }

    this.submitSearch();
  }

  searchRank(buildingEdge: IBuildingEdge, query: string): number {
    let matchScore = 0;

    if (buildingEdge.node.PropertyName.toLowerCase().includes(query)) {
      matchScore += 3;
    } else if (buildingEdge.node.Address.toLowerCase().includes(query)) {
      matchScore += 2;
    } else if (buildingEdge.node.PrimaryPropertyType.toLowerCase().includes(query)) {
      matchScore += 1;
    }

    return matchScore;
  }

  submitSearch(event?: Event): void {
    if (event) {
      event.preventDefault();
    }

    const query = this.searchFilter.toLowerCase().trim();

    const propertyFilterEncoded = encodeURIComponent(this.propertyTypeFilter);

    // Update URL bar with search query so refresh persists search
    let newUrl = `/search?${this.QueryParamKeys.search}=${query}`;

    if (propertyFilterEncoded) {
      newUrl += `&${this.QueryParamKeys.propertyType}=${propertyFilterEncoded}`;
    }

    window.history.pushState(null, '', newUrl);

    let buildingsResults: Array<IBuildingEdge> = this.$static.allBuilding.edges;

    // If no filters are provided, return our max number
    if (!query && !this.propertyTypeFilter) {
      this.setSearchResults(buildingsResults);
      return;
    }

    buildingsResults = buildingsResults.filter((buildingEdge: IBuildingEdge) => {
      return buildingEdge.node.PropertyName.toLowerCase().includes(query) ||
        buildingEdge.node.Address.toLowerCase().includes(query) ||
        buildingEdge.node.PrimaryPropertyType.toLowerCase().includes(query);
    });

    // Sort by name matches, then address, then property type
    buildingsResults = buildingsResults
    .sort((buildingEdgeA: IBuildingEdge, buildingEdgeB: IBuildingEdge) =>
      this.searchRank(buildingEdgeB, query) - this.searchRank(buildingEdgeA, query));

    // If property type filter is specified, filter down by that
    if (this.propertyTypeFilter) {
      buildingsResults = buildingsResults.filter((buildingEdge: IBuildingEdge) => {
        return buildingEdge.node.PrimaryPropertyType.toLowerCase()
          === this.propertyTypeFilter.toLowerCase();
      });

      this.setSearchResults(buildingsResults);
    }
    else {
     this.setSearchResults(buildingsResults);
    }
  }

  /**
   * Set the searchResults to a trimmed version of
   */
  setSearchResults(allResults: Array<IBuildingEdge>): void {
    this.totalResultsCount = allResults.length;
    this.searchResults = allResults.slice(0, this.MaxBuildings);
  }
}
</script>

<static-query>
  query {
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
    <div class="search-page">
      <h1
        id="main-content"
        tabindex="-1"
      >
        Search Benchmarked Buildings
      </h1>

      <p>
        Note that results are limited to the first {{ MaxBuildings }} matches.
      </p>

      <DataDisclaimer />

      <form>
        <div>
          <label for="page-search">
            Search Benchmarked Buildings
          </label>
          <input
            id="page-search"
            v-model="searchFilter"
            type="text"
            name="search"
            placeholder="Search property name, type, or address"
          >
        </div>

        <div>
          <label for="property-type">Filter Property Type</label>
          <select
            id="property-type"
            v-model="propertyTypeFilter"
          >
            <option
              v-for="propertyType in propertyTypeOptions"
              :key="propertyType.value ?? propertyType"
              :value="propertyType.value ?? propertyType"
            >
              {{ propertyType.label || propertyType }}
            </option>
          </select>
        </div>

        <button
          type="submit"
          class="-grey"
          @click="submitSearch"
        >
          Search
        </button>
      </form>

      <BuildingsTable :buildings="searchResults" />

      <div
        v-if="searchResults.length === 0"
        class="no-results-msg"
      >
        <h2>No results found!</h2>

        <p>
          There may be a typo in your query or in the underlying data, or the building you are
          looking for may not be in our dataset.
        </p>
      </div>

      <p>
        Showing {{ Math.min(MaxBuildings, totalResultsCount) }} of total {{ totalResultsCount }}
        matching buildings
      </p>

      <p class="footnote">
        Data Source:
        <!-- eslint-disable-next-line max-len -->
        <a
          href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
          target="_blank"
          rel="noopener"
        >
          Chicago Energy Benchmarking Data <NewTabIcon />
        </a>
      </p>
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

    input, select { padding: 0.5rem; }

    input[type="text"] { width: 15rem; }

    button { padding: 0.5rem 1rem; }

    select { max-width: 12rem; }

    /** Mobile Styling */
    @media (max-width: $mobile-max-width) {
      padding: 0.5rem;
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  }

  .no-results-msg {
    background-color: $grey;
    padding: 1rem;
    text-align: center;
  }
}
</style>
