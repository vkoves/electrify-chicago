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
    YearBuilt
    ZIPCode
    Ward
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
    DataAnomalies
    # Grade data
    GHGIntensityPercentileGrade,
    GHGIntensityLetterGrade,
    EnergyMixWeightedPctSum,
    EnergyMixPercentileGrade,
    EnergyMixLetterGrade,
    MissingRecordsCount,
    SubmittedRecordsPercentileGrade,
    SubmittedRecordsLetterGrade,
    AvgPercentileGrade,
    AvgPercentileLetterGrade,
    ReportingStatus,
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
          DistrictChilledWaterUse
          # Grade data
          GHGIntensityPercentileGrade,
          GHGIntensityLetterGrade,
          EnergyMixWeightedPctSum,
          EnergyMixPercentileGrade,
          EnergyMixLetterGrade,
          MissingRecordsCount,
          SubmittedRecordsPercentileGrade,
          SubmittedRecordsLetterGrade,
          AvgPercentileGrade,
          AvgPercentileLetterGrade,
          ReportingStatus,
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
          // TODO: Drop -img-tall and combine with -has-img
          '-img-tall': Boolean(buildingImg?.isTall || true),
        }"
      >
        <div class="building-header-text">
          <div>
            <h1 id="main-content" tabindex="-1">
              {{ propertyName }}&nbsp;<OverallRankEmoji
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
              class="google-maps-link no-print"
              target="_blank"
              rel="noopener"
            >
              Find on Google Maps <NewTabIcon />
            </a>
          </div>

          <p class="building-id -no-margin no-print">
            Chicago Building ID: {{ $page.building.ID }}
          </p>

          <div class="pills-cont">
            <g-link
              v-if="fullyGasFree"
              class="pill -all-electric"
              to="/all-electric"
            >
              <span class="icon">⚡</span>
              <span class="text">All Electric</span>
            </g-link>

            <g-link
              v-if="isNew"
              class="pill -new"
              to="/latest-updates#new-buildings"
            >
              <span class="text">New!</span>
            </g-link>
          </div>
        </div>

        <div class="building-img-cont">
          <BuildingImage :building="$page.building" />

          <div class="cta-btns">
            <button class="action-btn" @click="isEmailModalOpen = true">
              <img src="/email.svg" alt="" />
              Email Building
            </button>

            <!-- Print Flyer button -->
            <button class="action-btn -print" @click="printPage">
              <img src="/icons/printer.svg" alt="Print Flyer" />
            </button>

            <!-- Share button -->
            <ShareButton :title="propertyName" :text="shareText" />
          </div>
        </div>

        <div class="details-cont">
          <!-- Show warning container if we have anomalies our out of date data -->
          <div
            v-if="buildingAnomalies.length > 0 || dataYear < LatestDataYear"
            class="building-banner"
          >
            <div v-for="anomaly in buildingAnomalies" :key="anomaly">
              <div v-if="anomaly === DataAnomalies.gasZeroWithPreviousUse">
                <h2>
                  <span class="emoji">⚠️</span> Anomaly Detected - Likely Not
                  Gas Free
                </h2>

                <p>
                  This building did not report fossil gas use in the most recent
                  year, but has used gas in the past, which may be a reporting
                  error. Take a look at how this building has used energy over
                  time under "Extra Technical & Historic Info".
                </p>
              </div>
              <div v-if="anomaly === DataAnomalies.largeGasSwing">
                <h2>
                  <span class="emoji">⚠️</span> Anomaly Detected - Inconsistent
                  Gas Use
                </h2>

                <p>
                  This building has had extremely large changes in gas use,
                  which is likely to indicate errors in reporting.
                </p>
              </div>
            </div>

            <div v-if="dataYear < LatestDataYear">
              <h2><span class="emoji">🕰️</span> Out Of Date Data</h2>

              <p>
                This building did not report full data in {{ LatestDataYear }},
                so
                <span class="bold">top-level stats are from {{ dataYear }}</span
                >, the latest full year reported.
              </p>
            </div>

            <div v-if="reportingStatus === 'Not Covered 2024'">
              <h2><span class="emoji">🗒️</span> Reporting not required in 2024</h2>
              <p>
                This building did not require report full data in 2024,
                so
                <span class="bold">top-level stats are from {{ dataYear }}</span
                >, the latest full year reported.
              </p>
            </div>
          </div>

          <div class="info-and-report-card">
            <div class="building-top-info">
              <h2>Building Info</h2>

              <!-- NOTE: We hide some less essential building info when printing -->
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
                  class="no-print"
                >
                  <dt>Building Count</dt>
                  <dd>{{ $page.building.NumberOfBuildings }}</dd>
                </div>

                <div class="no-print">
                  <dt>Community Area</dt>
                  <dd>{{ $page.building.CommunityArea | titlecase }}</dd>
                </div>

                <div>
                  <dt>Ward</dt>
                  <dd v-if="parseInt(building.Ward) !== -1">
                    <g-link class="nav-link" :to="`/ward/${building.Ward}`">
                      {{ building.Ward }}
                    </g-link>
                  </dd>
                  <dd v-else>Not found</dd>
                </div>

                <!-- Show energy rating if it's a float value (not blank or NaN) -->
                <div
                  v-if="!isNaN(parseFloat($page.building.ChicagoEnergyRating))"
                  class="no-print"
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
                      href="https://www.energystar.gov/buildings/benchmark/understand-metrics/how-score-calculated"
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

            <ReportCard :building="building" :data-year="dataYear" />
          </div>

          <details class="hidden">
            <summary>Debug Full Grade Data</summary>

            <ul>
              <li>
                <strong>AvgPercentileLetterGrade:</strong>
                <LetterGrade :grade="building.AvgPercentileLetterGrade" />
              </li>
              <li>
                <strong>AvgPercentileGrade:</strong>
                {{ building.AvgPercentileGrade }}
              </li>
              <li>
                <strong>GHGIntensityLetterGrade:</strong>
                <LetterGrade :grade="building.GHGIntensityLetterGrade" />
              </li>
              <li>
                <strong>GHGIntensityPercentileGrade:</strong>
                {{ building.GHGIntensityPercentileGrade }}
              </li>
              <li>
                <strong>EnergyMixLetterGrade:</strong>
                <LetterGrade :grade="building.EnergyMixLetterGrade" />
              </li>
              <li>
                <strong>EnergyMixWeightedPctSum:</strong>
                {{ building.EnergyMixWeightedPctSum }}
              </li>
              <li>
                <strong>EnergyMixPercentileGrade:</strong>
                {{ building.EnergyMixPercentileGrade }}
              </li>
              <li>
                <strong>SubmittedRecordsLetterGrade:</strong>
                <LetterGrade :grade="building.SubmittedRecordsLetterGrade" />
              </li>
              <li>
                <strong>MissingRecordsCount:</strong>
                {{ building.MissingRecordsCount }}
              </li>
              <li>
                <strong>SubmittedRecordsPercentileGrade:</strong>
                {{ building.SubmittedRecordsPercentileGrade }}
              </li>
            </ul>
          </details>
        </div>
      </div>

      <div class="main-cols">
        <div class="stat-tiles-col">
          <h2>Emissions & Energy Information for {{ dataYear }}</h2>

          <dl class="stat-tiles">
            <div>
              <dt
                id="emissions-intensity"
                class="label-and-grade targetable"
                tabindex="-1"
              >
                Greenhouse Gas Intensity
                <LetterGrade
                  :grade="building.GHGIntensityLetterGrade"
                  class="-large -spaced"
                />
              </dt>
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
              <dt class="label-and-grade">Total Greenhouse Gas Emissions</dt>
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
            <ReportingTile
              :historic-data="historicData"
              :grade="building.SubmittedRecordsLetterGrade"
            />
          </div>

          <div class="stat-tiles-col -energy-breakdown">
            <h2>
              Energy Breakdown
              <span class="print-only">for {{ propertyName }}</span>
            </h2>

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

        <div class="chart-col">
          <h3
            id="energy-mix"
            class="label-and-grade -energy-mix targetable"
            tabindex="-1"
          >
            Energy Mix
            <LetterGrade
              :grade="building.EnergyMixLetterGrade"
              class="-large -spaced"
            />
          </h3>
          <div class="energy-mix-cont">
            <p>
              <strong>Total Energy Use:</strong>
              {{ Math.round(totalEnergyUsekBTU).toLocaleString() }} kBTU
            </p>

            <PieChart
              :id-prefix="'energy-mix'"
              :graph-data="energyBreakdownData"
            />

            <img
              v-tooltip.bottom="{
                content: tooltipMessage,
                trigger: 'click hover',
              }"
              class="tooltip"
              src="/help.svg"
              alt="Help icon"
              tabindex="0"
            />
          </div>

          <!-- QR Code Container, for printing -->
          <div class="qr-cont print-only">
            <h2>Scan To Learn More</h2>

            <div :id="QRCodeElementId" class="qr-code">
              <!-- Gets qrcode when printing-->
            </div>

            <p class="url">
              {{ prodBuildingUrl }}
            </p>
          </div>
        </div>
      </div>

      <details class="extra-info">
        <summary class="bold">View Extra Technical & Historic Info</summary>

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

          <h2>Full Historical Data Table for {{ propertyName }}</h2>

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

      <div class="no-print">
        <h2>What Should We Do About This?</h2>

        <a href="/take-action-tips"> Own this Building? Take Action. </a>
      </div>

      <email-modal
        v-if="isEmailModalOpen"
        title="Email This Building"
        subject="What Is Our Building's Plan For Saving Energy & Reducing Emissions?"
        @close="isEmailModalOpen = false"
      >
        <p>Dear sir or madam,</p>
        <p>
          My name is <span class="to-replace">_NAME_</span>, and I am an
          <span class="to-replace">_OWNER/OCCUPANT/OTHER_</span> of
          {{ $page.building.PropertyName }}.
        </p>
        <p>
          I've been reading about {{ $page.building.PropertyName }}'s emissions
          and energy use, and I wanted to learn more about your plans to improve
          our energy efficiency, electrify the building, and reduce our
          emissions. Well insulated all-electric buildings have lower energy
          bills, cleaner air, and are more comfortable for their occupants, and
          I want to make sure there is a concrete plan to make
          {{ $page.building.PropertyName }} one of those buildings!
        </p>
        <p>
          You can see more at
          <strong>https://electrifychicago.net{{ $page.building.path }}</strong>
        </p>
      </email-modal>
    </div>
  </DefaultLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import qrcode from 'qrcode-generator';

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
  calculateEnergyBreakdown,
  DataAnomalies,
  fullyGasFree,
  IBuilding,
  IBuildingBenchmarkStats,
  IHistoricData,
  isNewBuilding,
  parseAnomalies,
  UtilityCosts,
} from '../common-functions.vue';
import { IGraphPoint } from '../components/graphs/BarGraph.vue';
import PieChart, { IPieSlice } from '../components/graphs/PieChart.vue';
import {
  getBuildingCustomInfo,
  ILink,
} from '../constants/buildings-custom-info.constant.vue';
import EmailModal from '../components/EmailModal.vue';
import LetterGrade from '../components/LetterGrade.vue';
import ShareButton from '../components/ShareButton.vue';

import vToolTip from 'v-tooltip';
import ReportCard from '../components/ReportCard.vue';

Vue.use(vToolTip);

@Component<any>({
  metaInfo() {
    const propertyName =
      this.$page.building.PropertyName || this.$page.building.Address;
    const grade = this.$page.building.AvgPercentileLetterGrade || 'N/A';
    const emissions = Math.round(
      this.$page.building.TotalGHGEmissions || 0,
    ).toLocaleString();
    const description =
      `Is ${propertyName} doing its part for Chicago's climate goals? ` +
      `We gave it an ${grade} grade, and it emits ${emissions} tons of CO₂. ` +
      `See how it stacks up and what can be done about it!`;
    const socialImageUrl = `/social-images/building-${this.$page.building.ID}.webp`;

    return {
      title: propertyName,
      meta: [
        { name: 'description', content: description },
        { property: 'og:title', content: propertyName },
        { property: 'og:description', content: description },
        { property: 'og:image', content: socialImageUrl, key: 'og:image' },
        { property: 'og:image:width', content: '1200' },
        { property: 'og:image:height', content: '630' },
        { property: 'og:type', content: 'website' },
      ],
    };
  },
  components: {
    BarGraph,
    BuildingImage,
    DataSourceFootnote,
    EmailModal,
    HistoricalBuildingDataTable,
    LetterGrade,
    NewTabIcon,
    OverallRankEmoji,
    OwnerLogo,
    PieChart,
    ReportCard,
    ReportingTile,
    ShareButton,
    StatTile,
  },
  filters: {
    titlecase(value: string) {
      return value
        .toLowerCase()
        .replace(/(?:^|\s|-)\S/g, (x) => x.toUpperCase());
    },
    lowercase(value: string) {
      return value.toLowerCase();
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

  /** QR code element ID */
  private readonly QRCodeElementId = 'qrcode';

  tooltipMessage = `
    <p class="title">Why does this matter?</p>
    <p>
      Although reducing energy use overall is important, not all energy is created equal -
      electricity can be created without emissions (via solar, wind, nuclear, etc.) but burning
      fossil gas (aka natural gas) always creates emissions.
    </p>
  `;

  /** Expose stats to template */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats =
    BuildingBenchmarkStats;

  readonly DataAnomalies = DataAnomalies;

  /** Expose UtilityCosts to template */
  readonly UtilityCosts: typeof UtilityCosts = UtilityCosts;

  /**
   * The year most/the latest buildings data is from - if this building's year is older than this,
   *  we show a warning that the data is old
   */
  readonly LatestDataYear: number = LatestDataYear;

  /** Set by Gridsome to results of GraphQL query */
  $page!: {
    building: IBuilding;
    allBenchmark: { edges: Array<{ node: IHistoricData }> };
  };

  energyBreakdownData!: Array<IPieSlice>;

  /** All benchmarks (reported and not) for this building */
  historicData!: Array<IHistoricData>;

  /** The data we are currently rendering in the historic data graph */
  currGraphData?: Array<IGraphPoint> = [];
  currGraphTitle?: string = '';

  /** The key from the historical data we are graphing */
  colToGraph = 'TotalGHGEmissions';

  totalEnergyUsekBTU!: number;

  isEmailModalOpen = false;

  /** A helper to get the current building, but with proper typing */
  get building(): IBuilding {
    return this.$page.building;
  }

  get fullyGasFree(): boolean {
    return fullyGasFree(this.building);
  }

  get isNew(): boolean {
    return isNewBuilding(this.building, this.historicData);
  }

  /** Helper for property name with address fallback */
  get propertyName(): string {
    return this.building.PropertyName || this.building.Address;
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

  get prodBuildingUrl(): string {
    if (typeof window !== 'undefined' && window.location?.pathname) {
      return `https://electrifychicago.net${window.location.pathname}`;
    }

    return `https://electrifychicago.net/building/${this.building.ID}`;
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

  get buildingAnomalies(): Array<DataAnomalies> {
    return parseAnomalies(this.building.DataAnomalies);
  }

  get shareText(): string {
    const grade = this.building.AvgPercentileLetterGrade || 'N/A';
    const emissions = Math.round(
      this.building.TotalGHGEmissions || 0,
    ).toLocaleString();
    return (
      `Check out ${this.propertyName} on Electrify Chicago! ` +
      `It got a ${grade} grade and emits ${emissions} tons of CO₂.`
    );
  }

  /** The reporting status of the current building as it shows in the data */
  get reportingStatus(): string {
    const status = this.building.ReportingStatus ? String(this.building.ReportingStatus).trim() :'';
    return status;
  }

  created(): void {
    this.historicData =
      this.$page.allBenchmark.edges.map((nodeObj) => nodeObj.node) || [];

    const breakdownWithTotal = calculateEnergyBreakdown(this.building);
    this.energyBreakdownData = breakdownWithTotal.energyBreakdown;
    this.totalEnergyUsekBTU = breakdownWithTotal.totalEnergyUse;
    this.updateGraph();

    if (typeof window !== 'undefined') {
      window.addEventListener('beforeprint', () => {
        // Render the QR code before printing, we don't need it otherwise
        this.renderQrCode();
      });
    }
  }

  mounted(): void {
    // this.renderQrCode();
  }

  /**
   * Render a QR code pointing to the current page
   */
  renderQrCode(): void {
    if (typeof window === 'undefined' || typeof document === 'undefined') {
      return;
    }

    const qr = qrcode(0, 'M');

    // Always make the QR code point to prod
    qr.addData(this.prodBuildingUrl);
    qr.make();

    const qrCodeElement = document.getElementById(this.QRCodeElementId);

    if (qrCodeElement) {
      qrCodeElement.innerHTML = qr.createSvgTag({
        cellSize: 4,
        margin: 2,
        scalable: true,
      });
    }
  }

  updateGraph(event?: Event): void {
    event?.preventDefault();

    this.currGraphData = this.historicData.map((datum: IHistoricData) => ({
      x: datum.DataYear,
      // TODO: Investigate typing
      // eslint-disable-next-line
      y: parseFloat((datum as any)[this.colToGraph] as string),
    }));

    // TODO: Investigate typing
    // eslint-disable-next-line
    this.currGraphTitle = (this.graphTitles as any)[this.colToGraph];
  }

  printPage(): void {
    if (typeof window !== 'undefined') {
      window.print();
    }
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

    // Align buttons to right underneath the image
    .cta-btns {
      justify-content: flex-end;
    }
  }

  .building-header-text {
    margin-bottom: 1rem;
  }

  .info-and-report-card {
    display: flex;
    gap: 1rem;
    align-items: flex-start;

    .report-card-cont {
      flex-basis: 18rem;
    }
  }

  h1 {
    margin: 0;
    line-height: 1.25;
  }

  h2 {
    margin: 2rem 0 0.5rem 0;
    font-size: 1.25rem;
  }

  .cta-btns {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;

    .action-btn.-print {
      aspect-ratio: 1;
      padding: 0;

      img {
        height: 2rem;
      }
    }
  }

  .stat-tiles dt,
  .label-and-grade {
    margin-bottom: 0.5rem;
    margin-left: 1rem;
  }

  .label-and-grade {
    height: 2.5rem;
    display: flex;
    align-items: center;
    margin-top: 0.5rem;

    &.-energy-mix {
      margin-top: 3.8rem;
      font-size: 1.5rem;
    }

    .letter-grade {
      line-height: 0.8;
    }
  }

  .building-banner {
    padding: 0.5rem 0.75rem;
    background-color: $warning-background;
    border: dashed 0.125rem $warning-border;
    border-radius: $brd-rad-small;
    margin-bottom: 1rem;
    justify-self: flex-start;
    max-width: 36rem;

    h2 {
      margin: 0 0 0.25rem 0;
      font-size: 1rem;
    }
    span.emoji {
      margin-right: 0.5rem;
    }
    p {
      font-size: 0.75rem;
    }

    > div + div {
      margin-top: 0.5rem;
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

  .pills-cont {
    margin-top: 0.5rem;
  }

  .building-top-info {
    background: $off-white;
    border-radius: $brd-rad-medium;
    padding: 1rem 1.5rem;

    h2 {
      margin: 0 0 0.5rem 0;
    }
  }

  .main-cols {
    display: flex;
    gap: 2rem;

    .stat-tiles-col {
      flex-basis: 70%;
    }

    .chart-col {
      flex-basis: 30%;
      flex-shrink: 0;
      margin-top: 1rem;
      max-width: 24rem;

      .energy-mix-cont {
        display: flex;
        flex-direction: column;
        padding: 1rem;
        background-color: $off-white;
        border-radius: $brd-rad-medium;

        .tooltip {
          align-self: flex-end;
          width: fit-content;
          margin-bottom: 1rem;
          margin-right: 1rem;
        }
      }
    }
  }

  .qr-cont {
    background-color: $off-white;
    border-radius: $brd-rad-medium;
    text-align: center;
    margin-top: 3rem;
    overflow: hidden;

    h2 {
      font-size: 1.75rem;
      margin: 0 0 1rem 0;
      padding: 0.75rem;
      background-color: $blue-very-dark;
      color: $white;
    }

    .qr-code {
      display: inline-block;
      width: 50%;
      aspect-ratio: 1;
      background: $white;
      padding: 0.5rem;
      margin: 1rem 0;
      border: solid 0.25rem $grey-dark;
      border-radius: 1rem;

      > * {
        display: block;
      }
    }

    p.url {
      font-size: 0.75rem;
      max-width: 80%;
      margin: 0 auto 1rem auto;
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
      flex-shrink: 0;
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
    margin-top: 1.5rem;
    margin-bottom: 2rem;
  }

  details.extra-info {
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

    // Move report card to its own column
    .info-and-report-card {
      flex-direction: column-reverse;
      align-items: stretch;

      .report-card-cont {
        flex-basis: initial;
      }
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

      .building-header-text {
        position: relative;

        .address {
          font-size: 1rem;
        }
      }

      .details-cont {
        margin-top: 1rem;
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

        // Constrain tall images on mobile so they don't take up the whole view height
        .building-img-cont.-tall {
          width: 75%;

          img {
            max-height: 25rem;
            width: min-content;
          }
        }
      }

      .building-top-info dl {
        gap: 1rem;
      }
    }

    .cta-btns {
      justify-content: flex-start;
      gap: 0.5rem;
    }

    .main-cols .chart-col {
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

  @media not print {
    // Hide print only content, like duplicate title text
    .print-only {
      display: none;
    }
  }

  /** Print Styling - hides interactive elements and simplifies layout */
  @media print {
    // Prevent removing backgrounds from warning panels and top info
    // when printing
    .building-banner,
    .building-top-info,
    .energy-mix-cont,
    .qr-cont {
      print-color-adjust: exact;
    }

    // Hide interactive elements - action buttons and extra info section
    .action-btn,
    .extra-info,
    img.tooltip {
      display: none !important;
    }

    // Undo mobile layout
    .building-header.-has-img {
      grid-template-areas:
        'img title'
        'img details' !important;
      grid-template-columns: 1fr 60%;
    }

    // Scale up title and address
    h1 {
      font-size: 3rem;
    }
    .address {
      font-size: 1.25rem !important;
      line-height: 1;
    }

    .report-card-cont {
      flex-basis: 20rem !important;
    }

    .stat-tiles-col h2 {
      font-size: 1.75rem !important;
    }

    // Lock the height of the stat tiles and the energy mix chart
    .energy-mix-cont,
    .stat-tiles dd {
      height: 21.5rem !important;
    }

    // Drop left margin from section titles
    .stat-tiles dt,
    .label-and-grade,
    .reporting-tile .headline {
      margin-left: 0;
    }

    .label-and-grade.-energy-mix {
      margin-top: 5.75rem;
    }

    // The print page is mobile (~670px) but we want it to render more desktop style,
    // since a print page ends up being 8.5" wide and so can be denser
    .building-img-cont {
      width: 100% !important;
    }

    .main-cols {
      flex-direction: row;
    }

    .info-and-report-card {
      flex-direction: row;

      // Remove any link styling, like for Energy Star Score
      a {
        color: inherit;
        text-decoration: none;
      }
      .new-tab-icon {
        display: none;
      }
    }

    // Make stat tiles two columns again
    .stat-tiles {
      margin: 0;

      > div {
        flex-basis: 48%;
      }
    }

    .reporting-tile {
      margin-top: 1rem;
    }

    // Break the Energy Breakdown to page 2
    .stat-tiles-col.-energy-breakdown {
      page-break-before: always;

      h2 {
        font-size: 2rem;
      }
    }
  }
}
</style>
