<script>
import {Pager} from 'gridsome';
import RankText from '~/components/RankText.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
const BuildingBenchmarkStats = require('../data/dist/building-benchmark-stats.json');

export default {
  components: {
    Pager,
    RankText,
  },
  metaInfo: {
    title: 'Home',
  },
  data() {
    return {
      BuildingBenchmarkStats,
    };
  },
};
</script>

<page-query>
  query ($page: Int) {
    allBuilding(sortBy: "GHGIntensity", perPage: 15, page: $page) @paginate {
      pageInfo {
        totalPages
        currentPage
      }
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
          GrossFloorArea
          YearBuilt
        }
      }
    }
  }
</page-query>

<template>
  <DefaultLayout>
    <h1>Electrify Chicago</h1>

    <h2>Chicago Buildings by Greenhouse Gas Intensity</h2>

    <p>
      <strong>Note:</strong> This only includes buildings whose emissions are reported
      under the Chicago Energy Benchmarking Ordinance. According to the City &ldquo;As of 2016,
      this list includes all commercial, institutional, and residential buildings larger than
      50,000 square feet.&rdquo; This dataset is also then filtered to only buildings with reported
      emissions > 1,000 metric tons.
      </blockquote>
    </p>

    <div class="table-cont">
      <table>
        <thead>
          <tr>
            <th scope="col">Property Name / address</th>
            <th scope="col">Primary Property Type</th>
            <th scope="col" class="numeric">
              Greenhouse Gas Intensity<br/>
              (kg CO<sub>2</sub>/sqft)
            </th>
            <th scope="col" class="numeric">
              Total Greenhouse Emissions<br/>
              (metric tons CO<sub>2</sub>)
            </th>
            <th scope="col" class="numeric">
              Natural Gas Use<br/>
              (kBtu)
            </th>
            <th scope="col" class="numeric">
              Electricity Use<br/>
              (kBtu)
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="edge in $page.allBuilding.edges" :key="edge.node.id">
            <td class="property-name">
              <g-link :to="edge.node.path">
                {{ edge.node.PropertyName || edge.node.Address }}
              </g-link> <br/>
              <div class="prop-address">{{ edge.node.Address }}</div>
            </td>
            <td>{{ edge.node.PrimaryPropertyType }}</td>
            <td class="numeric">
              <template v-if="edge.node.GHGIntensity">
                <RankText
                  :building="edge.node"
                  :stats="BuildingBenchmarkStats" statKey="GHGIntensity"/>
              </template>
              <template v-else>-</template>
            </td>
            <td class="numeric">
              <template v-if="edge.node.TotalGHGEmissions">
                <RankText
                  :building="edge.node"
                  :round="true"
                  :stats="BuildingBenchmarkStats" statKey="TotalGHGEmissions"/>
              </template>
              <template v-else>-</template>
              </td>
            <td class="numeric">
              <template v-if="edge.node.NaturalGasUse">
                <RankText
                  :building="edge.node"
                  :round="true"
                  :stats="BuildingBenchmarkStats" statKey="NaturalGasUse"/>
              </template>
              <template v-else>-</template>
            </td>
            <td class="numeric">
              <template v-if="edge.node.ElectricityUse">
                <RankText
                  :building="edge.node"
                  :round="true"
                  :stats="BuildingBenchmarkStats" statKey="ElectricityUse"/>
              </template>
              <template v-else>-</template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Pager class="pager" :info="$page.allBuilding.pageInfo"/>

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
.table-cont {
  width: 100%;
  overflow-x: auto;
  border: solid 0.0625rem $grey-dark;
  box-sizing: border-box;

  table {
    width: 100%;
    /// Scroll if we get below desktop size table
    min-width: 60rem;
    border-collapse: collapse;

    a {
      font-weight: bold;
      font-size: 1.125em;
      text-decoration: none;
      white-space: nowrap;
    }

    thead {
      tr { background-color: $grey-dark; }

      th {
        text-align: left;
        font-size: 0.75rem;
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
      }
    }

    th, td {
      padding: 0.75rem;
      line-height: 1.25;

      &:first-of-type { padding-left: 1rem; }
      &:last-of-type { padding-right: 1rem; }
      &.numeric { text-align: right; }
    }

    tr:nth-of-type(2n + 2) { background-color: $grey; }

    .prop-address {
      font-size: 0.75em;
      margin-top: 0.25em;
    }
  }

  @media (max-width: $mobile-max-width) {
    // Make table screen full width on mobile
    width: calc(100% + 2rem);
    margin: 0 -1rem;

    table {
      width: 60rem;

      // Shrink table font-size on mobile to fit more
      td { font-size: 0.825rem; }
      td.property-name, td.property-address { width: 10rem; }
    }
  }
}

</style>
