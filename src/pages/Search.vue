<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import { IBuilding, IBuildingBenchmarkStats } from '~/common-functions.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';

interface IBuildingEdge {
  node: IBuilding;
}

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
  readonly   BuildingBenchmarkStats: IBuildingBenchmarkStats = BuildingBenchmarkStats;
  readonly MaxBuildings = 50;
  readonly QueryParamKey = 'q';

  search = '';

  searchResults: Array<IBuilding> = [];

  /** Set by Gridsome to results of GraphQL query */
  $static: any;

  created(): void {
    // Make sure on load we have some data
    this.searchResults = this.$static.allBuilding.edges.slice(0, this.MaxBuildings);
  }

  mounted(): void {
    const splitParams = window.location.search.split(`${this.QueryParamKey}=`);
    // Make sure to URI decode to convert params like 'Jewel%20Osco' -> 'Jewel Osco'
    const urlSearchParam = splitParams.length > 1 ? decodeURI(splitParams[1]) : null;

    if (urlSearchParam) {
      this.search = urlSearchParam;
      this.submitSearch();
    } else {
      this.searchResults = this.$static.allBuilding.edges.slice(0, this.MaxBuildings);
    }
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

    const query = this.search.toLowerCase().trim();

    window.history.pushState(null, '', `/search?${this.QueryParamKey}=${query}`);

    if (!query) {
      this.searchResults = this.$static.allBuilding.edges.slice(0, this.MaxBuildings);
      return;
    }

    let results = this.$static.allBuilding.edges.filter((buildingEdge: IBuildingEdge) => {
      return buildingEdge.node.PropertyName.toLowerCase().includes(query) ||
        buildingEdge.node.Address.toLowerCase().includes(query) ||
        buildingEdge.node.PrimaryPropertyType.toLowerCase().includes(query);
    });

    // Sort by name matches, then address, then property type
    results = results.sort((buildingEdgeA: IBuildingEdge, buildingEdgeB: IBuildingEdge) => {
      return this.searchRank(buildingEdgeB, query) - this.searchRank(buildingEdgeA, query);
    });

    this.searchResults = results.slice(0, this.MaxBuildings);
  }
}
</script>

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
    <h1 id="main-content">
      Search Benchmarked Buildings
    </h1>

    <p>
      Note that results are limited to the first {{ MaxBuildings }} matches.
    </p>

    <DataDisclaimer />

    <form class="search-form -page">
      <label for="search">Search Benchmarked Buildings</label>

      <div class="input-cont">
        <input
          id="search"
          v-model="search"
          type="text"
          name="search"
          placeholder="Search property name, type, or address"
        >
        <button
          type="submit"
          @click="submitSearch"
        >
          Search
        </button>
      </div>
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
  </DefaultLayout>
</template>

<style lang="scss">
form.search-form.-page {
  border-radius: 0.25rem;
  margin-bottom: 1rem;

  label {
    display: block;
    margin-bottom: 0.25rem;
    margin-left: 0.5rem;
    font-size: 0.75rem;
    font-weight: 500;
  }

  .input-cont {
    width: 25rem;
    max-width: 100%;

    // Slightly round search instead of full pill
    $border-radius: 0.25rem;

    input {
      border-radius: $border-radius 0 0 $border-radius;
      font-size: 1rem;
    }
    button { border-radius: 0 $border-radius $border-radius 0; }
  }

  @media (max-width: $mobile-max-width) {
    padding: 0.5rem;
  }
}

.no-results-msg {
  background-color: $grey;
  padding: 1rem;
  text-align: center;
}
</style>
