<page-query>
query ($id: ID!) {
  building(id: $id) {
    Address
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
      <h1 v-html="$page.building.PropertyName" />

      <div class="building-details">
        <h2>Building Info</h2>

        <dl>
          <div>
            <dt>Full Address</dt>
            <dd>{{ $page.building.Address }}, Chicago IL, {{ $page.building.ZIPCode }}</dd>
          </div>

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
            <dt>Ward</dt>
            <dd>{{ $page.building.Wards }}</dd>
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
              :unit="'kBtu / sq ft'"
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
              :unit="'kBtu / sq ft'"
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

// Log out stats for debugging
console.log('BuildingBenchmarkStats', BuildingBenchmarkStats);

export default {
  metaInfo() {
    return {
      title: this.$page.building.PropertyName,
    };
  },
  components: {
    StatTile,
  },
  data() {
    return {BuildingBenchmarkStats};
  },
};
</script>

<style lang="scss">
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

  dt {
    font-weight: normal;
    margin-bottom: 0.25rem;
  }
}
</style>
