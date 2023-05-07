<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import * as Leaflet from 'leaflet';

import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { IBuilding } from '../common-functions.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    DataDisclaimer,
    NewTabIcon,
  },
  metaInfo() {
    return {
     title:  'Map',
    };
  },
})
export default class BiggestBuildings extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  $page: any;

  pageInput = 0;

  created(): void {
    this.pageInput = this.$page.allBuilding.pageInfo.currentPage;
  }

  mounted(): void {
    this.setupMap();
  }

  setupMap(): void {
    // Center of Chicago at Madison & State
    const MapCenter: [ number, number ] = [41.882051, -87.627831];

    delete (Leaflet.Icon.Default.prototype as any)._getIconUrl;

    Leaflet.Icon.Default.mergeOptions({
      iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
      iconUrl: require('leaflet/dist/images/marker-icon.png'),
      shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
    });

    const map = Leaflet.map('buildings-map').setView(MapCenter, 13);

    Leaflet.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    const buildingNodes = this.$page.allBuilding.edges;


    console.log('buildingNodes[0]', buildingNodes[0].node);

    buildingNodes.forEach((buildingNode: { node: IBuilding }, index: number) => {
      const buildingObj: IBuilding = buildingNode.node;

      if (index > 5) {
        return;
      }

      const buildingCoords: [ number, number ] = [
        parseFloat(buildingObj.Latitude),
        parseFloat(buildingObj.Longitude)
      ];

      Leaflet.marker(buildingCoords).addTo(map);
    });


  }
}
</script>

<page-query>
  query {
    allBuilding(sortBy: "GHGIntensity") {
      pageInfo {
        totalPages
        currentPage
      }
      edges {
        node {
          slugSource
          PropertyName
          Address
          Latitude
          Longitude
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
</page-query>

<template>
  <DefaultLayout>
    <!-- Leaflet CSS -->
    <link
      rel="stylesheet"
      href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
      integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI="
      crossorigin=""
    >

    <div class="map-page">
      <h1
        id="main-content"
        tabindex="-1"
      >
        Buildings Map
      </h1>

      <p>
        <strong>Note:</strong> This is only buildings who reported data under Chicago's Energy
        Benchmarking data in 2020 and had emissions > 1,000 metric tons CO<sub>2e</sub>. Learn more
        about our sources on <g-link
          class="nav-link"
          to="/about"
        >
          the about page
        </g-link>.
      </p>

      <div id="buildings-map" />

      <!--
        <BuildingsTable :buildings="$page.allBuilding.edges" />
      -->

      <p class="footnote">
        Data Source:
        <a
          href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
          target="_blank"
          rel="noopener noreferrer"
        >
          Chicago Energy Benchmarking Data <NewTabIcon />
        </a>
      </p>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.map-page {
  #buildings-map {
    width: 40rem;
    height: 40rem;
  }
}
</style>
