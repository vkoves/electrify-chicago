<page-query>
query ($id: ID!) {
  building(id: $id) {
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
    <div>
      <h1>
        {{ $page.building.PropertyName || $page.building.Address }}
      </h1>

      <div class="address">
        {{ $page.building.Address }}, Chicago IL, {{ Math.round($page.building.ZIPCode) }}
      </div>

      <div class="building-details">
        <h2>Building Info</h2>

        <dl>
          <div>
            <dt>Square Footage</dt>
            <dd>
              <StatTile
              :building="$page.building"
              :statKey="'GrossFloorArea'"
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

          <div>
            <dt>Ward</dt>
            <dd>{{ Math.round($page.building.Wards) }}</dd>
          </div>

          <div v-if="$page.building.ChicagoEnergyRating">
            <dt>
              <a href="https://www.chicago.gov/city/en/progs/env/ChicagoEnergyRating.html">
                Chicago Energy Rating
              </a>
            </dt>
            <dd>
              {{ Math.round($page.building.ChicagoEnergyRating) }} / 4
            </dd>
          </div>

          <div v-if="$page.building.ENERGYSTARScore">
            <dt>
              <a href="https://www.energystar.gov/buildings/benchmark/understand_metrics/how_score_calculated">
                Energy Star Score
              </a>
            </dt>
            <dd>
              {{ Math.round($page.building.ENERGYSTARScore) }} / 100
            </dd>
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
              :statKey="'GHGIntensity'"
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
              :statKey="'TotalGHGEmissions'"
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
              :statKey="'SourceEUI'"
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
              :statKey="'SiteEUI'"
              :stats="BuildingBenchmarkStats"
              :unit="'kBtu / sqft'"
              />

            {{  $page.buildingSiteEUIRank }}
          </dd>
        </div>

        <div>
          <dt>Natural Gas Use</dt>
          <dd>
            <StatTile
              :building="$page.building"
              :statKey="'NaturalGasUse'"
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
              :statKey="'ElectricityUse'"
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
              :statKey="'DistrictSteamUse'"
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
              :statKey="'DistrictChilledWaterUse'"
              :stats="BuildingBenchmarkStats"
              :unit="'kBtu'"
              />
          </dd>
        </div>
      </dl>

      <p class="footnote">
        Data Source:
        <!-- eslint-disable-next-line max-len -->
        <a href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking-Covered-Buildings/g5i5-yz37"
          target="_blank" rel="noopener noreferrer">
          Chicago Energy Benchmarking - Covered Buildings (opens in a new tab)
        </a>
      </p>
    </div>
  </DefaultLayout>
</template>

<script>
import StatTile from '~/components/StatTile.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
const BuildingBenchmarkStats = require('../data/dist/building-benchmark-stats.json');

export default {
  metaInfo() {
    return {
      title: this.$page.building.PropertyName,
    };
  },
  components: {
    StatTile,
  },
  filters: {
    titlecase(value) {
      return value.toLowerCase().replace(/(?:^|\s|-)\S/g, (x) => x.toUpperCase());
    },
  },
  data() {
    return {
      BuildingBenchmarkStats,
    };
  },
};
</script>

<style lang="scss">
h1 { margin-bottom: 0; }

.address {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.building-details {
  background: #ededed;
  border-radius: 0.5rem;
  padding: 0.25rem 2rem 0.5rem;
}

dl {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.emission-stats {
  margin-bottom: 5rem;

  > div {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  dt {
    font-weight: normal;
    margin-bottom: 0.25rem;
  }

  dd, .stat-tile { height: 100%; }

  .stat-tile { min-width: 18rem; }
}
</style>
