<!-- Note that $id here is the GraphQL node ID, while $ID is the building ID (building.ID) -->
<page-query>
query ($id: ID!, $ID: String) {
  building(id: $id) {
    slugSource
    path
    ID
    DataYear
    Address
    ChicagoEnergyRating
    CommunityArea
    ENERGYSTARScore
    DistrictChilledWaterUse
    DistrictSteamUse
    ElectricityUse
    GHGIntensity
    GrossFloorArea
    NaturalGasUse
    NumberOfBuildings
    PrimaryPropertyType
    PropertyName
    SiteEUI
    SourceEUI
    TotalGHGEmissions
    Wards
    YearBuilt
    ZIPCode
    GHGIntensityRank
    GHGIntensityPercentileRank
    TotalGHGEmissionsRank
    TotalGHGEmissionsPercentileRank
    ElectricityUseRank
    ElectricityUsePercentileRank
    NaturalGasUseRank
    NaturalGasUsePercentileRank
    GrossFloorAreaRank
    GrossFloorAreaPercentileRank
    SourceEUIRank
    SourceEUIPercentileRank
    SiteEUIRank
    SiteEUIPercentileRank
    GHGIntensityRankByPropertyType
    TotalGHGEmissionsRankByPropertyType
    ElectricityUseRankByPropertyType
    NaturalGasUseRankByPropertyType
    GrossFloorAreaRankByPropertyType
    SourceEUIRankByPropertyType
    SiteEUIRankByPropertyType
  }
  allBenchmark(filter: { ID: { eq: $ID } }, sortBy: "DataYear", order: ASC) {
    edges {
        node {
          ID
          DataYear
          GrossFloorArea
          ChicagoEnergyRating
          ENERGYSTARScore
          SourceEUI
          SiteEUI
          GHGIntensity
          TotalGHGEmissions
          ElectricityUse
          NaturalGasUse
          DistrictSteamUse
        }
    }
  }
}
</page-query>

<template>
  <DefaultLayout>
    <div class="building-details-page">
      <div
        class="building-header"
        :class="{
          '-has-img': Boolean(buildingImg),
          // The layout is better for tall images, so keeping it there
          '-img-tall': Boolean(buildingImg?.isTall || true),
        }"
      >
        <div class="building-header-text">
          <div>
            <h1 id="main-content" tabindex="-1">
              {{
                $page.building.PropertyName || $page.building.Address
              }}&nbsp;<OverallRankEmoji
                :building="$page.building"
                :stats="BuildingBenchmarkStats"
                :large-view="true"
              />
            </h1>
          </div>

          <div class="address">
            {{ $page.building.Address }}, Chicago IL,
            {{ $page.building.ZIPCode }}
            <a
              :href="'https://www.google.com/maps/search/' + encodedAddress"
              class="google-maps-link"
              target="_blank"
              rel="noopener"
            >
              Find on Google Maps <NewTabIcon />
            </a>
          </div>

          <p class="building-id">
            Chicago Building ID: {{ $page.building.ID }}
          </p>
        </div>

        <div class="building-img-cont">
          <BuildingImage :building="$page.building" />

          <!-- Button opens Popup for "Email This Building" -->
          <button class="email-btn" @click="isModalOpen = true">
            <img src="/email.svg" alt="" />
            Email This Building
          </button>
        </div>

        <div class="details-cont">
          <div v-if="dataYear < LatestDataYear" class="building-banner">
            <span class="emoji">⚠️</span> This building did not report data in
            {{ LatestDataYear }},
            <span class="bold">this data is from {{ dataYear }}</span
            >, the latest year reported
          </div>

          <div class="building-top-info">
            <h2>Building Info</h2>

            <dl>
              <div>
                <dt>Square Footage</dt>
                <dd>
                  <StatTile
                    :building="$page.building"
                    :stat-key="'GrossFloorArea'"
                    :stats="BuildingBenchmarkStats"
                    :unit="'sqft'"
                  />
                </dd>
              </div>

              <div>
                <dt>Built</dt>
                <dd>{{ Math.round($page.building.YearBuilt) }}</dd>
              </div>

              <div>
                <dt>Primary Property Type</dt>
                <dd>
                  <g-link
                    class="nav-link"
                    :to="`/search?type=${propertyTypeEncoded}`"
                  >
                    {{ $page.building.PrimaryPropertyType }}
                  </g-link>
                </dd>
              </div>

              <!-- Only show building count if set and > 1, most are 1 -->
              <div
                v-if="
                  $page.building.NumberOfBuildings &&
                  $page.building.NumberOfBuildings > 1
                "
              >
                <dt>Building Count</dt>
                <dd>{{ $page.building.NumberOfBuildings }}</dd>
              </div>

              <div>
                <dt>Community Area</dt>
                <dd>{{ $page.building.CommunityArea | titlecase }}</dd>
              </div>

              <!-- Show energy rating if it's a float value (not blank or NaN) -->
              <div
                v-if="!isNaN(parseFloat($page.building.ChicagoEnergyRating))"
              >
                <dt>
                  <a
                    href="https://www.chicago.gov/city/en/progs/env/ChicagoEnergyRating.html"
                    target="_blank"
                    rel="noopener"
                  >
                    Chicago Energy Rating
                    <NewTabIcon />
                  </a>
                </dt>
                <dd>{{ $page.building.ChicagoEnergyRating }} / 4</dd>
              </div>

              <div v-if="$page.building.ENERGYSTARScore">
                <dt>
                  <a
                    href="https://www.energystar.gov/buildings/benchmark/understand_metrics/how_score_calculated"
                    target="_blank"
                    rel="noopener"
                  >
                    Energy Star Score
                    <NewTabIcon />
                  </a>
                </dt>
                <dd>{{ $page.building.ENERGYSTARScore }} / 100</dd>
              </div>

              <div>
                <dt>Owner</dt>
                <OwnerLogo :building="$page.building" />
              </div>

              <div v-if="customLinks">
                <dt>Extra Resources</dt>

                <dd>
                  <a
                    v-for="link in customLinks"
                    :key="link.url"
                    :href="link.url"
                    target="_blank"
                    rel="noopener"
                  >
                    {{ link.text }}
                    <NewTabIcon />
                  </a>
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>

      <div class="main-cols">
        <div class="stat-tiles-col">
          <h2>Emissions & Energy Information for {{ dataYear }}</h2>

          <dl class="stat-tiles">
            <div>
              <dt>Greenhouse Gas Intensity</dt>
              <dd>
                <StatTile
                  :building="$page.building"
                  :stat-key="'GHGIntensity'"
                  :stats="BuildingBenchmarkStats"
                  :historic-data="historicData"
                  :unit="'kg CO<sub>2</sub>e / sqft'"
                />
              </dd>
            </div>

            <div>
              <dt>Total Greenhouse Gas Emissions</dt>
              <dd>
                <StatTile
                  :building="$page.building"
                  :stat-key="'TotalGHGEmissions'"
                  :stats="BuildingBenchmarkStats"
                  :historic-data="historicData"
                  :unit="'tons CO<sub>2</sub>e'"
                />
              </dd>
            </div>
          </dl>
          <div class="reporting-tiles">
            <ReportingTile :historic-data="historicData" />
          </div>
          <div class="stat-tiles-col">
            <h2>Energy Breakdown</h2>

            <dl class="stat-tiles">
              <div>
                <dt>Fossil Gas Use (aka Natural Gas)</dt>
                <dd>
                  <StatTile
                    :building="$page.building"
                    :stat-key="'NaturalGasUse'"
                    :stats="BuildingBenchmarkStats"
                    :historic-data="historicData"
                    :unit="'kBtu'"
                  />
                </dd>
              </div>

              <div>
                <dt>Electricity Use</dt>
                <dd>
                  <StatTile
                    :building="$page.building"
                    :stat-key="'ElectricityUse'"
                    :stats="BuildingBenchmarkStats"
                    :historic-data="historicData"
                    :unit="'kBtu'"
                  />
                </dd>
              </div>

              <!-- Most buildings don't use district steam, so only show if > 0 -->
              <div v-if="$page.building.DistrictSteamUse > 0">
                <dt>District Steam Use</dt>
                <dd>
                  <StatTile
                    :building="$page.building"
                    :stat-key="'DistrictSteamUse'"
                    :stats="BuildingBenchmarkStats"
                    :historic-data="historicData"
                    :unit="'kBtu'"
                  />
                </dd>
              </div>

              <!-- Most buildings don't use district chilling, so only show if > 0 -->
              <div v-if="$page.building.DistrictChilledWaterUse > 0">
                <dt>District Chilled Water Use</dt>
                <dd>
                  <StatTile
                    :building="$page.building"
                    :stat-key="'DistrictChilledWaterUse'"
                    :stats="BuildingBenchmarkStats"
                    :historic-data="historicData"
                    :unit="'kBtu'"
                  />
                </dd>
              </div>
            </dl>
          </div>
        </div>

        <div class="chart-cont">
          <h2>Energy Mix</h2>
          <p>
            <strong>Total Energy Use:</strong>
            {{ Math.round(totalEnergyUsekBTU).toLocaleString() }} kBTU
          </p>

          <PieChart :graph-data="energyBreakdownData" />
        </div>
      </div>

      <details>
        <summary class="bold">View Extra Technical Info</summary>

        <div class="details-content">
          <dl class="stat-tiles -supp">
            <div>
              <dt>Source Energy Usage Intensity</dt>
              <dd>
                <StatTile
                  :building="$page.building"
                  :stat-key="'SourceEUI'"
                  :stats="BuildingBenchmarkStats"
                  :historic-data="historicData"
                  :unit="'kBtu / sqft'"
                />
              </dd>
            </div>

            <div>
              <dt>Site Energy Usage Intensity</dt>
              <dd>
                <StatTile
                  :building="$page.building"
                  :stat-key="'SiteEUI'"
                  :stats="BuildingBenchmarkStats"
                  :unit="'kBtu / sqft'"
                />

                {{ $page.buildingSiteEUIRank }}
              </dd>
            </div>
          </dl>

          <h2>Full Historical Data Table</h2>

          <HistoricalBuildingDataTable :historic-benchmarks="historicData" />
        </div>
      </details>

      <p class="constrained">
        <strong>* Note on Rankings:</strong> Rankings and medians are among
        <em>included</em> buildings, which are those who reported under the
        Chicago Energy Benchmarking Ordinance for the year {{ LatestDataYear }},
        which only applies to buildings over 50,000 square feet.
      </p>

      <p class="constrained">
        <strong>** Note on Bill Estimates:</strong>
        Estimates for gas and electric bills are based on average electric and
        gas <em>retail</em> prices for Chicago in {{ UtilityCosts.year }} and
        are rounded. We expect large buildings would negotiate lower rates with
        utilities, but these estimates serve as an upper bound of cost and help
        understand the volume of energy a building is used by comparing it to
        your own energy bills! See our
        <a :href="UtilityCosts.source" target="_blank" rel="noopener">
          Chicago Gas & Electric Costs Source <NewTabIcon />
        </a>
        for the original statistics.
      </p>

      <DataSourceFootnote />

      <h2>What Should We Do About This?</h2>

      <a href="/take-action-tips"> Own this Building? Take Action. </a>

      <email-building-modal
        v-if="isModalOpen"
        :building="$page.building"
        @close="isModalOpen = false"
      />
    </div>
  </DefaultLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import { LatestDataYear } from '../constants/globals.vue';
import BarGraph from '~/components/graphs/BarGraph.vue';
import BuildingImage from '~/components/BuildingImage.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import HistoricalBuildingDataTable from '~/components/HistoricalBuildingDataTable.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import OverallRankEmoji from '~/components/OverallRankEmoji.vue';
import OwnerLogo from '~/components/OwnerLogo.vue';
import StatTile from '~/components/StatTile.vue';
import ReportingTile from '~/components/ReportingTile.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import {
  getBuildingImage,
  IBuildingImage,
} from '../constants/building-images.constant.vue';
import {
  IBuilding,
  IHistoricData,
  UtilityCosts,
  IBuildingBenchmarkStats,
} from '../common-functions.vue';
import { IGraphPoint } from '../components/graphs/BarGraph.vue';
import PieChart, { IPieSlice } from '../components/graphs/PieChart.vue';
import {
  getBuildingCustomInfo,
  ILink,
} from '../constants/buildings-custom-info.constant.vue';
import EmailBuildingModal from '../components/EmailBuildingModal.vue';
import { VTooltip } from 'v-tooltip';

const EnergyBreakdownColors = {
  DistrictChilling: '#01295F',
  DistrictSteam: '#ABABAB',
  Electricity: '#F0E100',
  NaturalGas: '#993300',
};

@Component<any>({
  metaInfo() {
    return {
      title: this.$page.building.PropertyName,
    };
  },
  components: {
    BarGraph,
    BuildingImage,
    DataSourceFootnote,
    HistoricalBuildingDataTable,
    NewTabIcon,
    OverallRankEmoji,
    OwnerLogo,
    PieChart,
    StatTile,
    ReportingTile,
    EmailBuildingModal,
  },
  filters: {
    titlecase(value: string) {
      return value
        .toLowerCase()
        .replace(/(?:^|\s|-)\S/g, (x) => x.toUpperCase());
    },
  },
})
export default class BuildingDetails extends Vue {
  // TODO: Move to constant
  graphTitles = {
    TotalGHGEmissions: 'Total GHG Emissions (metric tons CO<sub>2</sub>e)',
    GHGIntensity: 'GHG Intensity (metric tons CO<sub>2</sub>e/sqft)',
    ElectricityUse: 'Electricity Use (kBTU)',
    NaturalGasUse: 'Fossil Gas Use (kBTU)',
  };

  /** Expose stats to template */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats =
    BuildingBenchmarkStats;

  /** Expose UtilityCosts to template */
  readonly UtilityCosts: typeof UtilityCosts = UtilityCosts;

  /**
   * The year most/the latest buildings data is from - if this building's year is older than this,
   *  we show a warning that the data is old
   */
  readonly LatestDataYear: number = LatestDataYear;

  /** Set by Gridsome to results of GraphQL query */
  $page: any;

  energyBreakdownData!: Array<IPieSlice>;

  /** All benchmarks (reported and not) for this building */
  historicData!: Array<IHistoricData>;

  /** The data we are currently rendering in the historic data graph */
  currGraphData?: Array<IGraphPoint> = [];
  currGraphTitle?: string = '';

  /** The key from the historical data we are graphing */
  colToGraph = 'TotalGHGEmissions';

  totalEnergyUsekBTU!: number;

  isModalOpen = false;

  /** A helper to get the current building, but with proper typing */
  get building(): IBuilding {
    return this.$page.building;
  }

  /** The primary property type of the current building as it shows in the data */
  get propertyType(): string {
    return this.building.PrimaryPropertyType;
  }

  /** The year of the data for this specific building */
  get dataYear(): number {
    return this.building.DataYear as number;
  }

  /** The primary property type of the current building, URL encoded for a link */
  get propertyTypeEncoded(): string {
    return encodeURIComponent(this.propertyType);
  }

  /**
   * A URL encoded complete address of the current building to use as a query param for a Google
   * Maps link
   */
  get encodedAddress(): string {
    const propertyName = this.building.PropertyName;
    const propertyAddr = this.building.Address + ' , Chicago IL';

    // If we know the property name, providing it in our Google Maps search may improve accuracy
    if (propertyName) {
      // Slashes break the URL, so just swap them for spaces
      const propertyNameCleaned = propertyName.replace(/\//g, ' ');

      return encodeURI(`${propertyNameCleaned} ${propertyAddr}`);
    } else {
      return encodeURI(propertyAddr);
    }
  }

  get buildingImg(): IBuildingImage | null {
    return getBuildingImage(this.building);
  }

  get customLinks(): Array<ILink> | null {
    const buildingCustomInfo = getBuildingCustomInfo(this.building);

    if (buildingCustomInfo?.links) {
      return buildingCustomInfo.links;
    }

    return null;
  }

  created(): void {
    this.historicData =
      this.$page.allBenchmark.edges.map(
        (nodeObj: { node: IHistoricData }) => nodeObj.node,
      ) || [];

    this.calculateEnergyBreakdown();
    this.updateGraph();
  }

  calculateEnergyBreakdown(): void {
    const energyBreakdown = [];

    if ((this.building.ElectricityUse as unknown as number) > 0) {
      energyBreakdown.push({
        label: 'Electricity',
        value: parseFloat(this.building.ElectricityUse.toString()),
        color: EnergyBreakdownColors.Electricity,
      });
    }

    if ((this.building.NaturalGasUse as unknown as number) > 0) {
      energyBreakdown.push({
        label: 'Fossil Gas',
        value: parseFloat(this.building.NaturalGasUse.toString()),
        color: EnergyBreakdownColors.NaturalGas,
      });
    }

    if ((this.building.DistrictSteamUse as unknown as number) > 0) {
      energyBreakdown.push({
        label: 'District Steam',
        value: parseFloat(this.building.DistrictSteamUse.toString()),
        color: EnergyBreakdownColors.DistrictSteam,
      });
    }

    if ((this.building.DistrictChilledWaterUse as unknown as number) > 0) {
      energyBreakdown.push({
        label: 'District Chilling',
        value: parseFloat(this.building.DistrictChilledWaterUse.toString()),
        color: EnergyBreakdownColors.DistrictChilling,
      });
    }

    let totalEnergyUse = 0;
    energyBreakdown.forEach((datum) => (totalEnergyUse += datum.value));
    this.totalEnergyUsekBTU = totalEnergyUse;

    this.energyBreakdownData = energyBreakdown;
  }

  updateGraph(event?: Event): void {
    event?.preventDefault();

    this.currGraphData = this.historicData.map((datum: IHistoricData) => ({
      x: datum.DataYear,
      y: parseFloat((datum as any)[this.colToGraph] as string),
    }));

    this.currGraphTitle = (this.graphTitles as any)[this.colToGraph];
  }
}
</script>

<style lang="scss">
.building-details-page {
  // Style the header specifically for when we have an image
  .building-header.-has-img {
    position: relative;
    min-height: 8rem;

    // For tall images we have the title and building details on the left
    &.-img-tall {
      display: grid;
      align-items: center;
      justify-content: space-between;
      gap: 0 2rem;
      grid-template-areas:
        'title img'
        'details img';

      .building-header-text {
        grid-area: title;
        align-self: end;
      }
      .details-cont {
        grid-area: details;
        align-self: start;
      }
      .building-img-cont {
        grid-area: img;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
      }
      .building-banner {
        grid-area: banner;
      }
    }

    &:not(.-img-tall) {
      display: grid;
      grid-template-areas:
        'img'
        'details';

      .building-header-text {
        grid-area: img;
      }
      .building-banner {
        grid-area: banner;
      }
      .building-img-cont {
        grid-area: img;
        width: 80%;
      }
      .details-cont {
        grid-area: details;
        align-self: start;
      }

      .building-header-text {
        position: absolute;
        z-index: 10;
        backdrop-filter: blur(0.0625rem);
        background: rgb(255 255 255 / 75%);
        bottom: 2.5rem;
        width: 60%;
        padding: 0.5rem 1rem;
        border-top-right-radius: 0.5rem;
        border-bottom-right-radius: 0.5rem;

        h1,
        .address {
          margin: 0;
        }
      }
    }
  }

  h1 {
    margin: 0;
  }

  h2 {
    margin: 2.5rem 0 0;
    font-size: 1.25rem;
  }

  .building-banner {
    padding: 1rem;
    background-color: $warning-background;
    border: dashed 0.125rem $warning-border;
    border-radius: $brd-rad-small;
    margin: 1rem 0;
    justify-self: flex-start;

    span.emoji {
      margin-right: 0.5rem;
    }
  }

  .address {
    font-size: 1.25rem;

    .google-maps-link {
      font-size: 0.825rem;
      margin-left: 0.5rem;
    }
  }

  .building-id {
    font-size: 0.75rem;
    margin-top: 0;
  }

  .building-top-info {
    background: #ededed;
    border-radius: $brd-rad-medium;
    padding: 1rem 1.5rem;
    margin-top: 1rem;

    h2 {
      margin-top: 0;
    }
  }

  .email-btn {
    display: flex;
    align-self: flex-end;
    justify-content: space-around;
    padding: 0.8rem 1.5rem;
    min-width: 18.75rem;
    margin-top: 1rem;
    background-color: $blue-dark;
    border: none;
    color: $white;
    font-size: 1.25rem;
    font-weight: bold;
    border-radius: $brd-rad-medium;

    &:hover,
    &:focus {
      background-color: $blue-very-dark;
    }

    img {
      border-radius: 0;
      height: 1.5rem;
    }
  }

  .main-cols {
    display: flex;
    gap: 2rem;

    .stat-tiles-col {
      flex-basis: 70%;
    }
    .chart-cont {
      flex-basis: 30%;
      flex-shrink: 0;
      margin-top: 1rem;

      .pie-chart-cont {
        margin-top: 1rem;
        background-color: $off-white;
        border-radius: $brd-rad-medium;
        max-width: 24rem;
      }
    }
  }

  dl {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    margin: 0;
  }

  .stat-tiles {
    // Layout of [tile 48%] [gap 4%] [tile 48%]
    gap: 2rem 4%;
    margin-top: 0.5rem;
    margin-bottom: 1rem;

    > div {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      flex-basis: 48%;
      // Make sure all stat tiles have some minimum height, even district steam with no medians
      max-width: 30rem;
      min-height: 14rem;
    }

    dt {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }

    dd,
    .stat-tile {
      height: 100%;
    }

    .stat-tile {
      min-width: 18rem;
    }
  }

  .reporting-tile {
    margin-top: 2.5rem;
    margin-bottom: 3rem;
  }

  details {
    margin: 2rem 0;

    .stat-tiles dt {
      font-size: 1.25rem;
    }
  }

  ul {
    margin-top: 0.5rem;

    li + li {
      margin-top: 0.25rem;
    }
  }

  /** Small desktop sizing - split to just two columns from three */
  @media (max-width: 1200px) {
    .main-cols {
      flex-direction: column-reverse;
    }
  }

  /**
   * Mobile styling
   */
  @media (max-width: $mobile-max-width) {
    .building-header {
      .building-img-cont,
      .building-header-text {
        width: 100%;
      }
      .email-btn {
        align-self: flex-start;
      }

      .building-header-text {
        position: relative;
      }

      &.-has-img {
        &:not(.-img-tall),
        &.-img-tall {
          grid-template-areas:
            'title'
            'img'
            'details';
        }

        &:not(.-img-tall) {
          .building-header-text {
            grid-area: title;
            position: relative;
            bottom: 0;
            width: 100%;
            background: none;
            padding: 0 0 1rem 0;
          }

          // On mobile wide images can go full width
          .building-img-cont {
            width: 100%;
          }
        }

        &.-img-tall {
          // Constrain tall images on mobile so they don't take up the whole view height
          .building-img-cont {
            width: 75%;
          }
        }
      }

      .building-top-info dl {
        gap: 1rem;
      }
    }

    .main-cols .chart-cont {
      margin-top: 0;
    }

    // Break GMaps link to new line
    .address .google-maps-link {
      display: block;
      margin-left: 0;
    }

    .building-top-info {
      padding: 1rem;
    }

    // Make stat tiles full width
    .stat-tiles > div {
      flex-basis: 100%;
      max-width: none;
    }
  }
}
</style>
