<script>
import BuildingsTable from '~/components/BuildingsTable.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
const BuildingBenchmarkStats = require('../data/dist/building-benchmark-stats.json');

const MaxBuildings = 20;

export default {
  components: {
    BuildingsTable,
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
    this.searchResults = this.$static.allBuilding.edges.slice(0, MaxBuildings);
  },
  methods: {
    submitSearch(event) {
      event.preventDefault();

      const query = this.search.toLowerCase().trim();

      if (!query) {
        this.searchResults = this.$static.allBuilding.edges.slice(0, MaxBuildings);
        return;
      }

      const results = this.$static.allBuilding.edges.filter((post) => {
        return post.node.PropertyName.toLowerCase().includes(query)
            || post.node.Address.toLowerCase().includes(query);
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

        <p>
      <strong>Note:</strong> This only includes buildings whose emissions are reported
      under the Chicago Energy Benchmarking Ordinance. According to the City &ldquo;As of 2016,
      this list includes all commercial, institutional, and residential buildings larger than
      50,000 square feet.&rdquo; This dataset is also then filtered to only buildings with reported
      emissions > 1,000 metric tons.
      </blockquote>
    </p>

    <form class="search">
        <label for="search">Search Benchmarked Buildings</label>
        <input type="text" name="search" id="search"
            placeholder="Search property name or address" v-model="search">
        <button v-on:click="submitSearch" type="submit">Search</button>
    </form>

    <BuildingsTable :buildings="searchResults" />

    <p class="footnote">
      Data Source:
      <!-- eslint-disable-next-line max-len -->
      <a href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking-Covered-Buildings/g5i5-yz37"
        target="_blank" rel="noopener noreferrer">
        Chicago Energy Benchmarking - Covered Buildings (opens in a new tab)
      </a>
    </p>
  </DefaultLayout>
</template>

<style lang="scss">
form.search {
    background: $grey;
    padding: 1rem;
    border-radius: 0.25rem;
    margin-bottom: 1rem;

    label {
        display: block;
        font-weight: bold;
        margin-bottom: 0.25rem;
    }

    input, button {
       padding: 0.5rem;
       box-sizing: border-box;
       height: 2.5rem;
       border: solid 0.125rem $grey-dark;
    }

    input {
        min-width: 15rem;
        border-right: none;
    }

    button {
        border-left: none;
    }
}
</style>
