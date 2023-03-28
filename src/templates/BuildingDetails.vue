<page-query>
query ($id: ID!) {
  building(id: $id) {
    slugSource
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
          '-img-tall': Boolean(buildingImg?.isTall)
        }"
      >
        <div class="building-header-text">
          <div>
            <h1
              id="main-content"
              tabindex="-1"
            >
              {{ $page.building.PropertyName || $page.building.Address }}&nbsp;<OverallRankEmoji
                :building="$page.building"
                :stats="BuildingBenchmarkStats"
                :large-view="true"
              />
            </h1>
          </div>

          <div class="address">
            {{ $page.building.Address }}, Chicago IL, {{ $page.building.ZIPCode }}
            <a
              :href="'https://www.google.com/maps/search/' + encodedAddress"
              class="google-maps-link"
              target="_blank"
              rel="noopener noreferrer"
            >
              Find on Google Maps <NewTabIcon />
            </a>
          </div>
        </div>

        <BuildingImage :building="$page.building" />

        <div class="building-details">
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
              <dd>{{ $page.building.YearBuilt }}</dd>
            </div>

            <div>
              <dt>Primary Property Type</dt>
              <dd>{{ $page.building.PrimaryPropertyType }}</dd>
            </div>

            <!-- Only show building count if set and > 1, most are 1 -->
            <div v-if="$page.building.NumberOfBuildings && $page.building.NumberOfBuildings > 1">
              <dt>Building Count</dt>
              <dd>{{ $page.building.NumberOfBuildings }}</dd>
            </div>

            <div>
              <dt>Community Area</dt>
              <dd>{{ $page.building.CommunityArea | titlecase }}</dd>
            </div>

            <!-- Show energy rating if it's a float value (not blank or NaN) -->
            <div v-if="!isNaN(parseFloat($page.building.ChicagoEnergyRating))">
              <dt>
                <a
                  href="https://www.chicago.gov/city/en/progs/env/ChicagoEnergyRating.html"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Chicago Energy Rating
                  <NewTabIcon />
                </a>
              </dt>
              <dd>
                {{ $page.building.ChicagoEnergyRating }} / 4
              </dd>
            </div>

            <div v-if="$page.building.ENERGYSTARScore">
              <dt>
                <a
                  href="https://www.energystar.gov/buildings/benchmark/understand_metrics/how_score_calculated"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Energy Star Score
                  <NewTabIcon />
                </a>
              </dt>
              <dd>
                {{ $page.building.ENERGYSTARScore }} / 100
              </dd>
            </div>

            <div>
              <dt>Owner</dt>
              <OwnerLogo :building="$page.building" />
            </div>
          </dl>
        </div>
      </div>

      <h2>Emissions & Energy Information</h2>

      <dl class="emission-stats">
        <div>
          <dt>Greenhouse Gas Intensity</dt>
          <dd>
            <StatTile
              :building="$page.building"
              :stat-key="'GHGIntensity'"
              :stats="BuildingBenchmarkStats"
              :unit="'kg CO<sub>2</sub> / sqft'"
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
              :unit="'metric tons CO<sub>2</sub>'"
            />
          </dd>
        </div>

        <div>
          <dt>Source Energy Usage Intensity</dt>
          <dd>
            <StatTile
              :building="$page.building"
              :stat-key="'SourceEUI'"
              :stats="BuildingBenchmarkStats"
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

        <div>
          <dt>Natural Gas Use</dt>
          <dd>
            <StatTile
              :building="$page.building"
              :stat-key="'NaturalGasUse'"
              :stats="BuildingBenchmarkStats"
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
              :unit="'kBtu'"
            />
          </dd>
        </div>

        <div v-if="$page.building.DistrictSteamUse">
          <dt>District Steam Use</dt>
          <dd>
            <StatTile
              :building="$page.building"
              :stat-key="'DistrictSteamUse'"
              :stats="BuildingBenchmarkStats"
              :unit="'kBtu'"
            />
          </dd>
        </div>

        <div v-if="$page.building.DistrictChilledWaterUse">
          <dt>District Chilled Water Use</dt>
          <dd>
            <StatTile
              :building="$page.building"
              :stat-key="'DistrictChilledWaterUse'"
              :stats="BuildingBenchmarkStats"
              :unit="'kBtu'"
            />
          </dd>
        </div>
      </dl>

      <p class="constrained">
        <strong>* Important Note:</strong> Rankings and medians are among <em>included</em>
        buildings, which are those who reported under the Chicago Energy Benchmarking Ordinance for
        the year 2020 with emissions greater than 1,000 metric tons.
      </p>

      <p class="footnote">
        Data Source:
        <!-- eslint-disable-next-line max-len -->
        <a
          href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
          target="_blank"
          rel="noopener noreferrer"
        >
          Chicago Energy Benchmarking Data Covered Buildings <NewTabIcon />
        </a>
      </p>

      <p>
        Additional Resources:

        <ul>
          <li>
            <a
              href="https://www.chicago.gov/city/en/depts/mayor/supp_info/chicago-energy-benchmarking/Chicago_Energy_Benchmarking_Beyond_Benchmarking.html"
              target="_blank"
              rel="noopener noreferrer"
            >
              Chicago Energy Benchmarking: Taking Action to Improve Energy Efficiency
              | City of Chicago <NewTabIcon />
            </a>
          </li>

          <li>
            <a
              href="https://www.chicago.gov/content/dam/city/progs/env/EnergyBenchmark/2018_Chicago_Energy_Benchmarking_Results_By_Sector.pdf"
              target="_blank"
              rel="noopener noreferrer"
            >
              Chicago Average EUIs and ENERGY STAR scores by property type [PDF] <NewTabIcon />
            </a>
          </li>

          <li>
            <a
              href="https://portfoliomanager.energystar.gov/pdf/reference/US%20National%20Median%20Table.pdf"
              target="_blank"
              rel="noopener noreferrer"
            >
              U.S. Energy Use Intensity by Property Type | ENERGY STAR [PDF] <NewTabIcon />
            </a>
          </li>
        </ul>
      </p>
    </div>
  </DefaultLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';
import StatTile from '~/components/StatTile.vue';
import OwnerLogo from '~/components/OwnerLogo.vue';
import OverallRankEmoji from '~/components/OverallRankEmoji.vue';
import BuildingImage from '~/components/BuildingImage.vue';
import { IBuildingBenchmarkStats } from '~/common-functions.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import { getBuildingImage, IBuildingImage } from '../constants/building-images.constant.vue';

@Component<any>({
  metaInfo() {
    return {
      title: this.$page.building.PropertyName,
    };
  },
  components: {
    BuildingImage,
    NewTabIcon,
    OverallRankEmoji,
    OwnerLogo,
    StatTile,
  },
  filters: {
    titlecase(value: string) {
      return value.toLowerCase().replace(/(?:^|\s|-)\S/g, (x) => x.toUpperCase());
    },
  },
})
export default class BuildingDetails  extends Vue {
  /** Expose stats to readme */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats = BuildingBenchmarkStats;

   /** Set by Gridsome to results of GraphQL query */
  $page: any;

  get encodedAddress(): string {
    const propertyName = this.$page.building.PropertyName;
    const propertyAddr = this.$page.building.Address + ' , Chicago IL';

    // If we know the property name, providing it in our Google Maps search may improve accuracy
    if (propertyName) {
      // Slashes break the URL, so just swap them for spaces
      const propertyNameCleaned = propertyName.replaceAll('/', ' ');

      return encodeURI(`${propertyNameCleaned} ${propertyAddr}`);
    } else {
      return encodeURI(propertyAddr);
    }
  }

  get buildingImg(): IBuildingImage | null {
    return getBuildingImage(this.$page.building);
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
        "title img"
        "details img";

      .building-header-text {
        grid-area: title;
        align-self: end;
      }
      .building-details {
        grid-area: details;
        align-self: start;
      }
      .building-img-cont { grid-area: img; }
    }

    &:not(.-img-tall) {
      display: grid;
      grid-template-areas:
        "img"
        "details";

      .building-header-text {
        grid-area: img;
      }
      .building-img-cont {
        grid-area: img;
        width: 80%;
      }
      .building-details {
        grid-area: details;
        align-self: start;
      }

      .building-header-text {
        position: absolute;
        z-index: 10;
        backdrop-filter: blur(0.0625rem);
        background: rgb(255 255 255 / 75%);
        bottom: 4rem;
        width: 60%;
        padding: 0.5rem 1rem;
        border-top-right-radius: 0.5rem;
        border-bottom-right-radius: 0.5rem;

        h1, .address { margin: 0; }
      }
    }
  }


  h1 { margin: 0; }

  .address {
    font-size: 1.25rem;
    margin-bottom: 1rem;

    .google-maps-link {
      font-size: 0.825rem;
      margin-left: 0.5rem;
    }
  }

  .building-details {
    background: #ededed;
    border-radius: 0.5rem;
    padding: 1rem 1.5rem;

    h2 { margin-top: 0; }

    dt { font-size: 0.825rem; }
  }

  dl {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
  }

  .emission-stats {
    margin-bottom: 1rem;

    > div {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      flex-basis: 30%;
      flex-grow: 1;
      max-width: 25rem;
    }

    dt {
      font-weight: normal;
      font-size: 1.25rem;
      margin-bottom: 0.5rem;
    }

    dd, .stat-tile { height: 100%; }

    .stat-tile { min-width: 18rem; }

  }

  ul {
    margin-top: 0.5rem;

    li + li { margin-top: 0.25rem; }
  }

  @media (max-width: $mobile-max-width) {
    .building-header {
      .building-img-cont, .building-header-text { width: 100%; }

      .building-header-text { position: relative; }

      &.-has-img {
        &:not(.-img-tall), &.-img-tall {
          grid-template-areas:
            "title"
            "img"
            "details";
        }

        &:not(.-img-tall) .building-header-text {
          grid-area: title;
          position: relative;
          bottom: 0;
          width: 100%;
          background: none;
          padding: 0 0 1rem 0;
        }
      }
    }

    // Break GMaps link to new line
    .address .google-maps-link {
      display: block;
      margin-left: 0;
    }

    .building-details {
      padding: 1rem;
    }
  }
}
</style>
