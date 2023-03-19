<script>
import { Pager } from 'gridsome';

export default {
  components: {
    Pager
  },
  metaInfo: {
    title: 'Home'
  }
}
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
          id
          Address
          PropertyName
          slugSource
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
  <Layout>
    <h1>Electrify Chicago</h1>

    <h2>Chicago Buildings by Greenhouse Gas Intensity</h2>

    <div class="table-cont">
      <!-- Add tabindex for keyboard access to scrollable area -->
      <table tabindex="0">
        <thead>
          <tr>
            <th scope="col">Property Name / address</th>
            <th scope="col">Address</th>
            <th scope="col" class="numeric">
              Greenhouse Gas Intensity<br>
              (kg CO<sub>2</sub>/sqft)
            </th>
            <th scope="col" class="numeric">
              Total Greenhouse Emissions<br>
              (metric tons CO<sub>2</sub>)
            </th>
            <th scope="col" class="numeric">Natural Gas Use (kBtu)</th>
            <th scope="col" class="numeric">Electricity Use (kBtu)</th>
          </tr>
        </thead>
        <tr v-for="edge in $page.allBuildings.edges" :key="edge.node.id">
          <td class="property-name">
            <a :href="edge.node.path">
              {{ edge.node.PropertyName || edge.node.Address }}
            </a>
          </td>
          <td class="property-address">{{ edge.node.Address }}</td>
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

    <Pager class="pager" :info="$page.allBuildings.pageInfo"/>

    <p class="footnote">
      Data Source:
      <a href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking-Covered-Buildings/g5i5-yz37"
        target="_blank" rel="noopener noreferrer">
        Chicago Energy Benchmarking - Covered Buildings (opens in a new tab)
      </a>
    </p>
  </Layout>
</template>

<style lang="scss">
.table-cont {
  width: 100%;
  overflow-x: auto;
  border: solid 0.0625rem $grey-dark;
  box-sizing: border-box;

  table {
    width: 80rem;
    border-collapse: collapse;

    thead {
      border-bottom: solid 0.125rem $grey-dark;

      tr { background-color: $grey-dark; }
    }

    tr:nth-of-type(2n + 2) { background-color: $grey; }

    th, td {
      padding: 0.5rem;

      &.numeric { text-align: right; }
    }

    th {
      text-align: left;
      font-size: 0.75rem;
      padding-top: 0;
      padding-bottom: 0;
    }
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
