<script>
import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '../components/DataDisclaimer.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
const BuildingBenchmarkStats = require('../data/dist/building-benchmark-stats.json');

const MaxBuildings = 20;
const QueryParamKey = 'q';

export default {
  components: {
    BuildingsTable,
    DataDisclaimer,
  },
  metaInfo: {
    title: 'Search',
  },
  data() {
    return {
      BuildingBenchmarkStats,
      search: '',
      searchResults: [],
    };
  },
  created: function() {
    // Make sure on load we have some data
    this.searchResults = this.$static.allBuilding.edges.slice(0, MaxBuildings);
  },
  mounted: function() {
    const splitParams = window.location.search.split(`${QueryParamKey}=`);
    // Make sure to URI decode to convert params like 'Jewel%20Osco' -> 'Jewel Osco'
    const urlSearchParam = splitParams.length > 1 ? decodeURI(splitParams[1]) : null;

    if (urlSearchParam) {
      this.search = urlSearchParam;
      this.submitSearch();
    } else {
      this.searchResults = this.$static.allBuilding.edges.slice(0, MaxBuildings);
    }
  },
  methods: {
    submitSearch(event) {
      if (event) {
        event.preventDefault();
      }

      const query = this.search.toLowerCase().trim();

      window.history.pushState(null, null, `/search?${QueryParamKey}=${query}`);

      if (!query) {
        this.searchResults = this.$static.allBuilding.edges.slice(0, MaxBuildings);
        return;
      }

      const results = this.$static.allBuilding.edges.filter((post) => {
        return post.node.PropertyName.toLowerCase().includes(query) ||
            post.node.Address.toLowerCase().includes(query);
      });

      this.searchResults = results.slice(0, MaxBuildings);
    },
  },
};
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
    <h1>Search Benchmarked Buildings</h1>

    <DataDisclaimer/>

    <form class="search-form -page">
        <label for="search">Search Benchmarked Buildings</label>

        <div class="input-cont">
          <input type="text" name="search" id="search"
              placeholder="Search property name or address" v-model="search">
          <button v-on:click="submitSearch" type="submit">Search</button>
        </div>
    </form>

    <BuildingsTable :buildings="searchResults" />

    <div v-if="searchResults.length === 0" class="no-results-msg">
        <h2>No results found!</h2>

        <p>
            There may be a typo in your query or in the underlying data, or the building you are
            looking for may not be in our dataset.
        </p>
    </div>

    <p class="footnote">
      Data Source:
      <!-- eslint-disable-next-line max-len -->
      <a href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
        target="_blank" rel="noopener noreferrer">
        Chicago Energy Benchmarking Data (opens in a new tab)
      </a>
    </p>
  </DefaultLayout>
</template>

<style lang="scss">
form.search-form.-page {
  background: $grey;
  padding: 1rem;
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

    input { border-radius: $border-radius 0 0 $border-radius; }
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
