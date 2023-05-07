<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import * as Leaflet from 'leaflet';

import RankText from '~/components/RankText.vue';
import OverallRankEmoji from '~/components/OverallRankEmoji.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { IBuildingBenchmarkStats, IBuilding } from '../common-functions.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import BuildingImage from '../components/BuildingImage.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingImage,
    DataDisclaimer,
    NewTabIcon,
    OverallRankEmoji,
    RankText,
  },
  metaInfo() {
    return {
     title:  'Map',
    };
  },
})
export default class BiggestBuildings extends Vue {
  /** Expose stats to template */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats = BuildingBenchmarkStats;

  /** Set by Gridsome to results of GraphQL query */
  $page!: any;

  /** VueJS template refs */
  $refs!: { 'mapPopup': any };

  currBuilding?: IBuilding;

  /* Declare dynamic template data for VueJS */
  data(): any {
    return { currBuilding: this.currBuilding };
  }

  mounted(): void {
    this.setupMap();
  }

  setupMap(): void {
    // Center of Chicago at Madison & State
    const MapCenter: [ number, number ] = [41.882051, -87.627831];

    // Fix Leaflet markers not working. Source: https://stackoverflow.com/a/65761448
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

    const MaxBuildings = 100;

    buildingNodes
    .slice(0, MaxBuildings)
    .forEach((buildingNode: { node: IBuilding }, index: number) => {
      const currBuilding: IBuilding = buildingNode.node;

      const buildingCoords: [ number, number ] = [
        parseFloat(currBuilding.Latitude),
        parseFloat(currBuilding.Longitude),
      ];

      const marker = Leaflet.marker(buildingCoords).addTo(map);

      marker.bindPopup(() => {
        (this as any).currBuilding = currBuilding;
         console.log('this.$refs.mapPopup', this.$refs.mapPopup);

        return this.$refs.mapPopup;
      });
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
          GrossFloorArea
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
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

      <DataDisclaimer />

      <div id="buildings-map" />

      <div v-show="false">
        <!-- The map popup used by Leaflet, so we can do Vue things -->
        <div
          ref="mapPopup"
          class="map-popup"
        >
          <div v-if="currBuilding">
            <h1>
              {{ currBuilding.PropertyName || currBuilding.Address }}

              <OverallRankEmoji
                :building="currBuilding"
                :stats="BuildingBenchmarkStats"
              />
            </h1>

            {{ currBuilding.PropertyName ? currBuilding.Address : '' }}

            <BuildingImage :building="currBuilding" />

            <div class="stats-list">
              <div>
                <h2>Square Footage</h2>

                <RankText
                  :building="currBuilding"
                  :should-round="true"
                  :stats="BuildingBenchmarkStats"
                  :unit="'sqft'"
                  stat-key="GrossFloorArea"
                />
              </div>

              <div>
                <h2>GHG Intensity</h2>

                <RankText
                  :building="currBuilding"
                  :stats="BuildingBenchmarkStats"
                  stat-key="GHGIntensity"
                  :unit="'kg/sqft'"
                />
              </div>

              <div>
                <h2>Total GHG Emissions</h2>

                <RankText
                  :building="currBuilding"
                  :should-round="true"
                  :stats="BuildingBenchmarkStats"
                  stat-key="TotalGHGEmissions"
                  :unit="'tons'"
                />
              </div>
            </div>

            <a
              href="${currBuilding.path}"
              class="details-link"
            >View Details</a>
          </div>
        </div>
      </div>

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
    max-width: 100%;
    width: 100%;
    aspect-ratio: 1.8/1;
  }

  .map-popup {
    width: 20rem;
    font-size: 1rem;

    h1 {
      font-size: 1.25rem;
      margin-bottom: 0.25rem;
    }

    .stats-list {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem 2rem;
    }

    h2 {
      font-size: 0.875rem;
      margin: 0;
    }

    .building-img-cont {
      text-align: left;

      img {
        max-width: 16rem;
        max-height: 12rem;
      }
    }

    a.details-link {
      display: block;
      margin-top: 0.5rem;
      font-weight: bold;
      font-size: 1rem;
    }
  }
}
</style>
