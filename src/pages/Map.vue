<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

// For types, we actually set window.Leaflet for runtime
import type * as Leaflet from 'leaflet';

import RankText from '~/components/RankText.vue';
import OverallRankEmoji from '~/components/OverallRankEmoji.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';

import {
  IBuildingBenchmarkStats,
  IBuilding,
  IBuildingNode,
  getOverallRankEmoji,
  RankConfig,
} from '../common-functions.vue';

import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import BuildingImage from '../components/BuildingImage.vue';

/** The ID of the google maps <script> tag, so we can tack on an onload */
const GoogleMapsScriptId = 'google-maps-script';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingImage,
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
    OverallRankEmoji,
    RankText,
  },
  metaInfo() {
    return {
      title: 'Map',
      link: [
        {
          // Leaflet CSS
          href: 'https://unpkg.com/leaflet@1.9.3/dist/leaflet.css',
          rel: 'stylesheet',
        },
      ],
    };
  },
})
export default class MapPage extends Vue {
  static readonly MaxBuildingsCount = 100;

  static readonly OneMileInMeters = 1609.344 /* eq. to 1mi */;

  /** Expose stats to template */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats =
    BuildingBenchmarkStats;

  readonly MapConfig = {
    DefaultZoom: 11,
    // Center of Chicago at Madison & State
    Center: [41.86, -87.627831] as [number, number],
    // How many px of scroll equals one zoom level - default is 60, we go higher since the whole
    // dataset is just Chicago
    WheelPxPerZoomLevel: 480,
    // How much the + and - icons adjust zoom
    ZoomDelta: 0.25,
    ZoomSnap: 0.25,
  };

  /** Set by Gridsome to results of GraphQL query */
  $page!: { allBuilding: { edges: Array<IBuildingNode> } };

  /** VueJS template refs */
  $refs!: {
    mapPopup: any;
    googleMapsSearchInput: any;
  };

  Leaflet!: typeof Leaflet;

  currBuilding?: IBuilding;

  errorMessage?: string | null = null;

  icons: { [iconName: string]: Leaflet.Icon } = {};

  formZip: number | string = '';
  /** The coordinates of the place the user searched in the Google Maps box */
  formPointCoords: [number, number] | null = null;
  formSearchDistanceMiles = 1;

  map?: Leaflet.Map;

  /** A message indicating what is being shown on the map */
  mapStatus = '';

  mainFeatureGroup?: Leaflet.FeatureGroup;

  zipCodes: Array<number> = [];

  /* Declare dynamic template data for VueJS */
  data(): any {
    return { currBuilding: this.currBuilding };
  }

  async mounted(): Promise<void> {
    // Do nothing if rendering the static HTML files - there's nothing we can do map wise and
    // Gridsome gets cranky importing Leaflet
    if (typeof window !== 'undefined') {
      // Runtime Leaflet imports
      this.Leaflet = require('leaflet');
      require('leaflet.gridlayer.googlemutant');

      this.setupMap();
      this.setupZipCodes();

      // Wait a bit so the <script> tags get added
      setTimeout(() => {
        this.setupGoogleMapsSearch();
      });
    }
  }

  setupMap(): void {
    this.setupMapIcons();

    this.map = this.Leaflet.map('buildings-map', {
      zoomDelta: this.MapConfig.ZoomDelta,
      wheelPxPerZoomLevel: this.MapConfig.WheelPxPerZoomLevel,
      zoomSnap: this.MapConfig.ZoomSnap,
    }).setView(this.MapConfig.Center, this.MapConfig.DefaultZoom);

    const UsingGoogle = true;

    if (UsingGoogle) {
      this.setupGoogleMutant();
    } else {
      this.Leaflet.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution:
          '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(this.map!);
    }

    this.mainFeatureGroup = this.Leaflet.featureGroup().addTo(this.map);

    this.mapDefaultBuildings();
  }

  setupMapIcons(): void {
    // Fix Leaflet markers not working. Source: https://stackoverflow.com/a/65761448
    delete (this.Leaflet.Icon.Default.prototype as any)._getIconUrl;

    this.Leaflet.Icon.Default.mergeOptions({
      iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
      iconUrl: require('leaflet/dist/images/marker-icon.png'),
      shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
    });

    const CustomMarkerIcon = this.Leaflet.Icon.extend({
      options: {
        iconSize: [25, 41],
        iconAnchor: [13, 10],
        shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
      },
    });

    this.icons.red = new (CustomMarkerIcon as any)({
      iconUrl: '/map-markers/marker-red.png',
    }) as Leaflet.Icon;

    this.icons.green = new (CustomMarkerIcon as any)({
      iconUrl: '/map-markers/marker-green.png',
    }) as Leaflet.Icon;

    this.icons.orange = new (CustomMarkerIcon as any)({
      iconUrl: '/map-markers/marker-orange.png',
    }) as Leaflet.Icon;

    this.icons.grey = new (CustomMarkerIcon as any)({
      iconUrl: '/map-markers/marker-grey.png',
    }) as Leaflet.Icon;

    this.icons.blue = new (CustomMarkerIcon as any)({
      iconUrl: '/map-markers/marker-blue.png',
    }) as Leaflet.Icon;
  }

  setupGoogleMutant(): void {
    (this.Leaflet.gridLayer as any)
      .googleMutant({
        type: 'roadmap', // valid values are 'roadmap', 'satellite', 'terrain' and 'hybrid'
        styles: [
          // Disable icons for other points of interest, but keep neighborhood & street labels
          { elementType: 'labels.icon', stylers: [{ visibility: 'off' }] },
        ],
      })
      .addTo(this.map);
  }

  /** Setup the Google Maps search box */
  setupGoogleMapsSearch(): void {
    // Create a <script> element to import Google Maps, then hook into it for the autocomplete input
    const googleMapsScriptElem = document.createElement('script');
    googleMapsScriptElem.id = GoogleMapsScriptId;
    googleMapsScriptElem.src =
      'https://maps.googleapis.com/maps/api/js?key=AIzaSyChJYejLT7Vxh_UZhJkccsy0xqZTHX8fzU&libraries=places';
    document.body.appendChild(googleMapsScriptElem);

    googleMapsScriptElem.onload = () => {
      const searchInput = this.$refs.googleMapsSearchInput;
      const google = (window as any).google;

      // NW edge of O'Hare down to long of South edge
      const southwest = { lat: 41.644624, lng: -87.93976 };
      // SE edge of Chicago but up at Northern edge of O'hare
      const northeast = { lat: 42.00743, lng: -87.524611 };
      const chicagoBounds = new google.maps.LatLngBounds(southwest, northeast);

      // Limit search to Chicago strictly, if we can't find an address in Chicago we should show
      // nothing
      const searchOptions = {
        bounds: chicagoBounds,
        strictBounds: true,
      };

      // Setup places searchbox, learn more here:
      // https://developers.google.com/maps/documentation/javascript/examples/places-searchbox
      const searchBox = new google.maps.places.SearchBox(
        searchInput,
        searchOptions,
      );

      // Hook into places being selected
      searchBox.addListener('places_changed', () => {
        const places = searchBox.getPlaces();

        if (places.length === 0) {
          return;
        }

        // Clear form zip and store the coordinates
        this.formZip = '';

        this.formPointCoords = [
          places[0].geometry.location.lat(),
          places[0].geometry.location.lng(),
        ];
      });
    };
  }

  /**
   * Show buildings around a given point, so users can put in an address and see what properties are
   * in the dataset nearby
   */
  showBuildingsAroundPoint(coordinates: [number, number]): void {
    this.clearMarkers();

    const MarkerOptions: Leaflet.MarkerOptions = {
      riseOnHover: false,
      icon: this.icons.grey,
      opacity: 0.95,
    };

    // Create a default marker for the search location
    this.Leaflet.marker(coordinates, MarkerOptions).addTo(
      this.mainFeatureGroup!,
    );

    const SearchRadiusMeters =
      MapPage.OneMileInMeters * this.formSearchDistanceMiles;
    this.Leaflet.circle(coordinates, { radius: SearchRadiusMeters }).addTo(
      this.mainFeatureGroup!,
    );

    const inputPoint = this.Leaflet.latLng(coordinates);
    const buildingNodes = this.$page.allBuilding.edges;

    // Calculate the distance to each building and filter by those within a mile
    const pointsNearInputPoint = buildingNodes.filter(
      (buildingNode: IBuildingNode) => {
        // Make sure we actually have coordinates before we do calculations on them
        const latFloat = parseFloat(buildingNode.node.Latitude);
        const lonFloat = parseFloat(buildingNode.node.Longitude);
        if (!isNaN(latFloat) && !isNaN(lonFloat)) {
          const buildingPoint = this.Leaflet.latLng(latFloat, lonFloat);
          const buildingDistanceToPointMeters =
            buildingPoint.distanceTo(inputPoint);

          return buildingDistanceToPointMeters <= SearchRadiusMeters;
        } else {
          return false;
        }
      },
    );

    this.addBuildingsToMap(pointsNearInputPoint);
    this.autofitMap();
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

    this.mapStatus =
      `Top ${MapPage.MaxBuildingsCount} highest GHG intensity buildings of ` +
      `${buildingNodes.length.toLocaleString()} total`;
  }

  setupZipCodes(): void {
    const buildingNodes = this.$page.allBuilding.edges;
    const allZipCodes: Array<number> = buildingNodes
      .filter(
        (buildingNode: IBuildingNode) =>
          (buildingNode.node.ZIPCode as string).trim().length,
      )
      .map((buildingNode: IBuildingNode) =>
        parseInt(buildingNode.node.ZIPCode as string),
      );

    this.zipCodes = this.unique(allZipCodes).sort();
  }

  reset(): void {
    this.clearSearch();
    this.formZip = '';
    this.formSearchDistanceMiles = 1;
    this.errorMessage = '';

    this.clearMarkers();
    this.mapDefaultBuildings();
    this.map!.setView(this.MapConfig.Center, this.MapConfig.DefaultZoom);
  }

  cancelEvent(event: Event): void {
    event.preventDefault();
  }

  applyFilters(event: Event): void {
    event.preventDefault();

    // Exit if neither zipcode or address specified and show error
    if (!this.formZip && !this.formPointCoords) {
      this.errorMessage = 'Pick an address to filter around or a zipcode!';
      return;
    }

    this.clearMarkers();
    this.errorMessage = '';

    // Prioritize zipcode, since clicking a place in search will clear zip
    if (this.formZip) {
      this.clearSearch();

      const buildingNodes = this.$page.allBuilding.edges;
      const filteredBuildings = buildingNodes.filter(
        (buildingNode: IBuildingNode) =>
          buildingNode.node.ZIPCode === this.formZip.toString(),
      );

      this.addBuildingsToMap(filteredBuildings);
      this.mapStatus = `Buildings in Zipcode ${this.formZip} (according to dataset)`;
    } else {
      this.showBuildingsAroundPoint(this.formPointCoords!);
      this.mapStatus = `Buildings within ${this.formSearchDistanceMiles} mile of point`;
    }

    this.autofitMap();
  }

  /**
   * Add a given array of building nodes to the map as markers with popups - does not clear
   * existing markers
   */
  addBuildingsToMap(buildingNodes: Array<IBuildingNode>): void {
    buildingNodes.forEach((buildingNode: IBuildingNode) => {
      const currBuilding: IBuilding = buildingNode.node;

      const buildingCoords: [number, number] = [
        parseFloat(currBuilding.Latitude),
        parseFloat(currBuilding.Longitude),
      ];

      const MarkerOptions: Leaflet.MarkerOptions = {
        riseOnHover: true,
        icon: this.getBuildingIcon(currBuilding),
      };

      const marker = this.Leaflet.marker(buildingCoords, MarkerOptions).addTo(
        this.mainFeatureGroup!,
      );

      marker.bindPopup(
        () => {
          this.currBuilding = currBuilding;
          return this.$refs.mapPopup;
        },
        {
          // Fix popup max-width
          maxWidth: 'auto',
          // eslint-disable-next-line
        } as any,
      );
    });
  }

  /**
   * Return a color coded icon for a building based on it's rank emoji (e.g. a trophy maps to green
   * while an alarm is red)
   */
  getBuildingIcon(building: IBuilding): Leaflet.Icon {
    const rankEmoji: string | undefined = getOverallRankEmoji(
      building,
      this.BuildingBenchmarkStats,
    )?.emoji;

    if (rankEmoji === RankConfig.AlarmEmoji) {
      return this.icons.red;
    } else if (rankEmoji === RankConfig.FlagEmoji) {
      return this.icons.orange;
    } else if (rankEmoji === RankConfig.TrophyEmoji) {
      return this.icons.green;
    } else {
      return this.icons.blue;
    }
  }

  private clearMarkers(): void {
    this.mainFeatureGroup?.clearLayers();
  }

  private clearSearch(): void {
    this.$refs.googleMapsSearchInput.value = '';
    this.formPointCoords = null;
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
      edges {
        node {
          slugSource
          ID
          DataYear
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
          DataAnomalies
        }
      }
    }
  }
</page-query>

<template>
  <DefaultLayout>
    <div class="map-page">
      <h1 id="main-content" tabindex="-1">Map</h1>

      <DataDisclaimer />

      <details class="filter-details">
        <summary>Filter Buildings</summary>
        <form>
          <h2>Filter Buildings</h2>

          <p v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </p>

          <label for="addr-input">Find Buildings Near Address or Place</label>
          <input
            id="addr-input"
            ref="googleMapsSearchInput"
            type="text"
            placeholder="Type address or place"
            @keydown.enter="cancelEvent"
          />

          <label for="search-dist">Search Distance</label>
          <select id="search-dist" v-model="formSearchDistanceMiles">
            <option :value="0.25">1/4 mile</option>
            <option :value="0.5">1/2 mile</option>
            <option :value="1">1 mile</option>
            <option :value="2">2 miles</option>
          </select>

          <hr />

          <label for="zipcode">Or Filter Zip Code</label>
          <select id="zipcode" v-model="formZip">
            <option disabled :value="''">Choose Zipcode</option>
            <option v-for="zipcode in zipCodes" :key="zipcode" :value="zipcode">
              {{ zipcode }}
            </option>
            "
          </select>

          <div class="button-row">
            <button type="button" @click="reset">Reset</button>

            <button type="submit" @click="applyFilters">Submit</button>
          </div>
        </form>
      </details>

      <p class="map-status"><strong>Filtering By:</strong> {{ mapStatus }}</p>

      <div id="buildings-map" />

      <div v-show="false">
        <!-- The map popup used by Leaflet, so we can do Vue things -->
        <div ref="mapPopup" class="map-popup">
          <div v-if="currBuilding">
            <h1>
              {{
                currBuilding.PropertyName || currBuilding.Address
              }}&nbsp;<OverallRankEmoji
                :building="currBuilding"
                :stats="BuildingBenchmarkStats"
              />
            </h1>

            {{ currBuilding.PropertyName ? currBuilding.Address : '' }}

            <div class="popup-main">
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
            </div>

            <a :href="currBuilding.path" class="details-link"
              >View More Details</a
            >
          </div>
        </div>
      </div>

      <!--
        <BuildingsTable :buildings="$page.allBuilding.edges" />
      -->

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.map-page {
  .map-status {
    background-color: $grey-light;
    padding: 0.5rem 1rem;
    margin-bottom: 0;
  }

  #buildings-map {
    max-width: 100%;
    width: 100%;
    aspect-ratio: 1.7/1;
  }

  details.filter-details {
    summary {
      font-weight: bold;
      font-size: 1.25rem;
    }
  }

  form {
    background-color: $grey-light;
    padding: 1rem;
    border-radius: $brd-rad-medium;

    h2 {
      margin: 0;
      font-size: 1.25rem;
    }

    .error-message {
      color: $chicago-red;
      background: $white;
      border-bottom: solid $border-medium $chicago-red;
      padding: 0.1rem 0.5rem;
      font-weight: bold;
    }

    input[type='text'] {
      width: 100%;
      padding: 0.5rem 1rem;
      box-sizing: border-box;
    }

    label,
    select {
      display: block;
    }

    label {
      font-size: 0.825rem;
      margin-top: 0.25rem;
    }

    .button-row {
      display: flex;
      gap: 1rem;
      margin-top: 0.5rem;
    }
  }

  .map-popup {
    width: 20rem;
    min-height: 10rem;
    font-size: 1rem;

    .popup-main {
      display: flex;
      gap: 1rem;
    }

    h1 {
      font-size: 1.25rem;
      margin-bottom: 0.25rem;
    }

    .stats-list {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      gap: 1rem;
      margin-top: 0.5rem;

      .rank-label {
        margin-top: 0;
        font-size: small;
      }
    }

    h2 {
      font-size: 0.875rem;
      margin: 0;
    }

    .building-img-cont {
      text-align: left;

      &,
      img {
        max-width: 10rem;
      }

      img {
        max-height: 8rem;
      }
    }

    a.details-link {
      display: block;
      margin: 0.5rem 0 0.75rem 0;
      font-weight: bold;
      font-size: 1rem;
    }
  }

  @media (max-width: $mobile-max-width) {
    #buildings-map {
      // flip map to square to fit portrait displays
      aspect-ratio: 1;
    }
  }
}
</style>
