<script>
import {Pager} from 'gridsome';

export default {
  components: {
    Pager,
  },
  metaInfo: {
    title: 'Home',
  },
};
</script>

<page-query>
  query ($page: Int) {
    allBuilding(sortBy: "GHGIntensity", perPage: 20, page: $page) @paginate {
      pageInfo {
        totalPages
        currentPage
      }
      edges {
        node {
          Address
          PropertyName
          PrimaryPropertyType
          GHGIntensity
          GrossFloorArea
          TotalGHGEmissions
          YearBuilt
          ElectricityUse
          NaturalGasUse
          path
        }
      }
    }
  }
</page-query>

<template>
  <DefaultLayout>
    <h1>Electrify Chicago</h1>

    <h2>Chicago Buildings by Greenhouse Gas Intensity</h2>

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
        <tr v-for="edge in $page.allBuilding.edges" :key="edge.node.id">
          <td class="property-name">
            <g-link :to="edge.node.path">
              {{ edge.node.PropertyName || edge.node.Address }}
            </g-link> <br/>
            <span class="prop-address">{{ edge.node.Address }}</span>
          </td>
          <td>{{ edge.node.PrimaryPropertyType }}</td>
          <td class="numeric">
            <template v-if="edge.node.GHGIntensity">
              {{ edge.node.GHGIntensity }}
            </template>
            <template v-else>?</template>
          </td>
          <td class="numeric">
            <template v-if="edge.node.TotalGHGEmissions">
              {{ edge.node.TotalGHGEmissions }}
            </template>
            <template v-else>?</template>
            </td>
          <td class="numeric">
            <template v-if="edge.node.NaturalGasUse">
              {{ edge.node.NaturalGasUse }}
            </template>
            <template v-else>?</template>
          </td>
          <td class="numeric">
            <template v-if="edge.node.ElectricityUse">
              {{ edge.node.ElectricityUse }}
            </template>
            <template v-else>?</template>
          </td>
        </tr>
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
      font-size: 1.125rem;
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

    tr:nth-of-type(2n + 2) { background-color: $grey; }

    th, td {
      padding: 0.5rem;
      line-height: 1.25;

      &:first-of-type { padding-left: 1rem; }
      &:last-of-type { padding-right: 1rem; }
      &.numeric { text-align: right; }
    }

    .prop-address { font-size: 0.75rem; }
  }

  @media (max-width: $mobile-max-width) {
    // Make table screen full width on mobile
    width: calc(100% + 2rem);
    margin: 0 -1rem;

    table {
      width: 60rem;

      // Shrink table font-size on mobile to fit more
      td { font-size: 0.75rem; }
      td.property-name, td.property-address { width: 10rem; }
    }
  }
}

</style>
