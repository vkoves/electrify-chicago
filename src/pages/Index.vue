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
    allBuildings(sortBy: "GHGIntensity", perPage: 10, page: $page) @paginate {
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
        }
      }
    }
  }
</page-query>

<template>
  <Layout>

    <!-- Learn how to use images here: https://gridsome.org/docs/images -->
    <!-- <g-image alt="Example image" src="~/favicon.png" width="135" /> -->

    <h1>All Chicago Properties Sorted by Greenhouse Gas Intensity</h1>

    <table>
      <thead>
        <tr>
          <th scope="col">Property Name / address</th>
          <th scope="col">Address</th>
          <th scope="col">Greenhouse Gas Intensity</th>
        </tr>
      </thead>
      <tr v-for="edge in $page.allBuildings.edges" :key="edge.node.id">
        <td>{{ edge.node.PropertyName || edge.node.Address }}</td>
        <td>{{ edge.node.Address }}</td>
        <td>{{ edge.node.GHGIntensity }} kg CO<sub>2</sub> / sqft</td>
      </tr>
    </table>

    <Pager :info="$page.allBuildings.pageInfo"/>
  </Layout>
</template>

<style lang="scss">
@import "@/scss/colors.scss";

table {
  width: 100%;

  th { text-align: left; }
  th:last-of-type, td:last-of-type {
    text-align: right;
    width: 30%;
  }
}

nav {
  display: inline-flex;
  gap: 1rem;
  margin-top: 1rem;

  a {
    color: $text-main;
    background-color: $grey;
    padding: 0.5rem 1rem;
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
}
</style>
