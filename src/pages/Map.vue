<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import * as Leaflet from 'leaflet';

import RankText from '~/components/RankText.vue';
import OverallRankEmoji from '~/components/OverallRankEmoji.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { IBuildingBenchmarkStats, IBuilding, IBuildingNode } from '../common-functions.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import BuildingImage from '../components/BuildingImage.vue';
import { array } from 'prop-types';

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
export default class MapPage extends Vue {
  static readonly MaxBuildingsCount = 50;

  /** Expose stats to template */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats = BuildingBenchmarkStats;

  readonly MapConfig = {
    DefaultZoom: 11,
    // Center of Chicago at Madison & State
    Center: [41.882051, -87.627831] as [ number, number ],
  };

  /** Set by Gridsome to results of GraphQL query */
  $page!: any;

  /** VueJS template refs */
  $refs!: { 'mapPopup': any };

  currBuilding?: IBuilding;

  formZip: number | string = '';

  map?: Leaflet.Map;

  mainFeatureGroup?: Leaflet.FeatureGroup;

  zipCodes: Array<number> = [];

  /* Declare dynamic template data for VueJS */
  data(): any {
    return { currBuilding: this.currBuilding };
  }

  mounted(): void {
    this.setupMap();
    this.setupZipCodes();
  }

  setupMap(): void {
    // Fix Leaflet markers not working. Source: https://stackoverflow.com/a/65761448
    delete (Leaflet.Icon.Default.prototype as any)._getIconUrl;

    Leaflet.Icon.Default.mergeOptions({
      iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
      iconUrl: require('leaflet/dist/images/marker-icon.png'),
      shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
    });

    this.map = Leaflet.map('buildings-map').setView(this.MapConfig.Center, this.MapConfig.DefaultZoom);

    Leaflet.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(this.map!);

    this.mainFeatureGroup = Leaflet.featureGroup().addTo(this.map);

    this.mapDefaultBuildings();
  }

  /**
   * Map the default buildings which is the top `MapPage.MaxBuildingsCount` buildings sorted by
   * GHG intensity
   */
  mapDefaultBuildings(): void {
    const buildingNodes = this.$page.allBuilding.edges;

    // limit to the first MaxBuildingsCount buildings, that means those N highest GHG
    // intensity buildings are shown
    const topBuildings = buildingNodes.slice(0, MapPage.MaxBuildingsCount);

    this.addBuildingsToMap(topBuildings);
  }

  setupZipCodes(): void {
    const buildingNodes = this.$page.allBuilding.edges;
    const allZipCodes: Array<number> = buildingNodes
      .filter((buildingNode: IBuildingNode) => (buildingNode.node.ZIPCode as string).trim().length)
      .map((buildingNode: IBuildingNode) => parseInt(buildingNode.node.ZIPCode as string));

    this.zipCodes = this.unique(allZipCodes).sort();
  }

  reset(): void {
    this.clearMarkers();
    this.mapDefaultBuildings();
  }

  submitFilters(): void {
    this.clearMarkers();

    const buildingNodes = this.$page.allBuilding.edges;

    console.log('zipcode', this.formZip);

    const filteredBuildings = buildingNodes
      .filter((buildingNode: IBuildingNode) => buildingNode.node.ZIPCode === this.formZip.toString());

    this.addBuildingsToMap(filteredBuildings);
    this.autofitMap();
  }

  /**
   * Add a given array of building nodes to the map as markers with popups - does not clear
   * existing markers
   */
  addBuildingsToMap(buildingNodes: Array<IBuildingNode>): void {
    buildingNodes
      .forEach((buildingNode: IBuildingNode) => {
        const currBuilding: IBuilding = buildingNode.node;

        const buildingCoords: [ number, number ] = [
          parseFloat(currBuilding.Latitude),
          parseFloat(currBuilding.Longitude),
        ];

        const MarkerOptions: Leaflet.MarkerOptions = {
          riseOnHover: true,
        };

        const marker = Leaflet.marker(buildingCoords, MarkerOptions).addTo(this.mainFeatureGroup!);

        marker.bindPopup(() => {
          this.currBuilding = currBuilding;

          return this.$refs.mapPopup;
        });
      });
  }

  private clearMarkers(): void {
    this.mainFeatureGroup?.clearLayers();
  }

  private autofitMap(): void {
    this.map!.fitBounds(this.mainFeatureGroup!.getBounds());
  }

  private unique<T>(array: Array<T>): Array<T> {
    function onlyUnique(value: T, index: number, array: Array<T>): boolean {
      return array.indexOf(value) === index;
    }

    return array.filter(onlyUnique);
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
          ZIPCode
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

      <form>
        <h2>Filter Buildings</h2>

        <label>Filter Zip Code</label>
        <select
          id="zipcode"
          v-model="formZip"
        >
          <option
            disabled
            :value="''"
          >
            Choose Zipcode
          </option>
          <option
            v-for="zipcode in zipCodes"
            :key="zipcode"
            :value="zipcode"
          >
            {{ zipcode }}
          </option>"
        </select>

        <div class="button-row">
          <button
            type="button"
            @click="reset"
          >
            Reset
          </button>

          <button
            type="button"
            @click="submitFilters"
          >
            Submit
          </button>
        </div>
      </form>

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
              :href="currBuilding.path"
              class="details-link"
            >View More Details</a>
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
    margin-top: 1rem;
  }

  form {
    background-color: $grey-light;
    padding: 1rem;
    max-width: 20rem;
    border-radius: $brd-rad-medium;

    h2 {
      margin: 0;
      font-size: 1.25rem;
    }

    label, select { display: block; }

    .button-row {
      display: flex;
      gap: 1rem;
      margin-top: 0.5rem;
    }
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
      margin: 0.5rem 0;
      font-weight: bold;
      font-size: 1rem;
    }
  }
}
</style>
