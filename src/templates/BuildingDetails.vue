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
      <div>
        <h1>
          {{ $page.building.PropertyName || $page.building.Address }}
          <OverallRankEmoji
            :building="$page.building"
            :stats="BuildingBenchmarkStats"
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

          <!--
            Hidden for now because it's wrong in the source data
            <div>
              <dt>Ward</dt>
              <dd>{{ $page.building.Wards }}</dd>
            </div>
          -->

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
import { IBuildingBenchmarkStats } from '~/common-functions.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
import * as BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';

@Component<any>({
  metaInfo() {
    return {
      title: this.$page.building.PropertyName,
    };
  },
  components: {
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
      return encodeURI(`${propertyName} ${propertyAddr}`);
    } else {
      return encodeURI(propertyAddr);
    }
  }
}
</script>

<style lang="scss">
.building-details-page {

  h1 { margin-bottom: 0; }

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
