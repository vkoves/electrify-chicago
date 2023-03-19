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
    allBuildings(sortBy: "GHGIntensity", perPage: 20, page: $page) @paginate {
      pageInfo {
        totalPages
        currentPage
      }
      edges {
        node {
          ID
          Address
          PropertyName
          GHGIntensity
          GrossFloorArea
          TotalGHGEmissions
          YearBuilt
          ElectricityUse
          NaturalGasUse
        }
      }
    }
  }
</page-query>

  <template>
  <Layout>
    <h1>All Chicago Properties Sorted by Greenhouse Gas Intensity</h1>

    <div class="table-cont">
      <table>
        <thead>
          <tr>
            <th scope="col">Property Name / address</th>
            <th scope="col">Address</th>
            <th scope="col" class="numeric">Greenhouse Gas Intensity</th>
            <th scope="col" class="numeric">
              Total Greenhouse Emissions<br>
              (metric tons CO<sub>2</sub>)
            </th>
            <th scope="col" class="numeric">Natural Gas Use</th>
            <th scope="col" class="numeric">Electricity Use</th>
          </tr>
        </thead>
        <tr v-for="edge in $page.allBuildings.edges" :key="edge.node.id">
          <td>{{ edge.node.PropertyName || edge.node.Address }}</td>
          <td>{{ edge.node.Address }}</td>
          <td class="numeric">
            <template v-if="edge.node.GHGIntensity">
              {{ edge.node.GHGIntensity }} <span class="unit">kg CO<sub>2</sub>/sqft</span>
            </template>
            <template v-else>?</template>
          </td>
          <td class="numeric">
            <template v-if="edge.node.TotalGHGEmissions">
              {{ edge.node.TotalGHGEmissions }} <span class="unit">tons CO<sub>2</sub></span>
            </template>
            <template v-else>?</template>
            </td>
          <td class="numeric">
            <template v-if="edge.node.NaturalGasUse">
              {{ edge.node.NaturalGasUse }} <span class="unit">kBtu</span>
            </template>
            <template v-else>?</template>
          </td>
          <td class="numeric">
            <template v-if="edge.node.ElectricityUse">
              {{ edge.node.ElectricityUse }} <span class="unit">kBtu</span>
            </template>
            <template v-else>?</template>
          </td>
        </tr>
      </table>
    </div>

    <Pager class="pager" :info="$page.allBuildings.pageInfo"/>
  </Layout>
</template>

<style lang="scss">
@import "@/scss/colors.scss";

.table-cont {
  width: 100%;
  overflow-x: auto;
  border: solid 0.0625rem $grey-dark;
}

table {
  width: 90rem;
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

  .unit { font-size: 0.75rem; }
}

// Pager styling
nav.pager {
  display: inline-flex;
  gap: 1rem;
  margin-top: 1rem;

  a {
    display: flex;
    align-items: center;
    justify-content: center;
    color: $text-main;
    background-color: $grey;
    width: 2.5rem;
    aspect-ratio: 1;
    text-align: center;
    border-radius: 0.25rem;
    text-decoration: none;
    font-weight: bold;

    &:hover, &:focus {
      background-color: $grey-dark;
    }

    &.active {
      background-color: $orange;
      cursor: default;
    }
  }

  @media (max-width: $mobile-max-width) {
    gap: 0.25rem;

    a { width: 2rem; }
  }
}
</style>
