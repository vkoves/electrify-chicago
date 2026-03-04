<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import PieChart, { IPieSlice } from '~/components/graphs/PieChart.vue';
import SparkLine, { INumGraphPoint } from '~/components/graphs/SparkLine.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import {
  EnergyBreakdownColors,
  GradeColors,
  IBuildingNode,
  PropertyTypeStats,
  YearData,
  getMedianMultipleMsg,
  kBtuToKwh,
  kBtuToKwhTooltip,
  pluralizePropertyType,
} from '../common-functions.vue';
import { NumberFormatter } from '../utils/number-formatter.vue';
import vToolTip from 'v-tooltip';

import { slugifyPropertyType } from '../constants/property-type-helpers.vue';
import { generatePropertyTypeMeta } from '../constants/meta-helpers.vue';
import BuildingStatsByPropertyType from '../data/dist/building-statistics-by-property-type.json';
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import HistoricStatsByPropertyType from '../data/dist/historic-stats-by-property-type.json';

Vue.use(vToolTip);

/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    BuildingsTable,
    BuildingsHero,
    PieChart,
    SparkLine,
    DataDisclaimer,
    DataSourceFootnote,
  },
  metaInfo() {
    const propertyType: string = this.$context.propertyType;
    const propertyTypePlural = pluralizePropertyType(propertyType);
    const slug = slugifyPropertyType(propertyType);

    return generatePropertyTypeMeta(slug, propertyTypePlural, propertyType);
  },
})
export default class PropertyType extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  readonly $page!: { allBuilding: { edges: Array<IBuildingNode> } };
  readonly $context!: { propertyType: string };

  buildingsFiltered: Array<IBuildingNode> = [];

  avgGHGIntensity?: string;
  totalGHGEmissions?: string;
  totalSquareFootage?: string;
  gradeDistributionPie: Array<IPieSlice> = [];

  totalElectricityUseKbtu?: number;
  medianElectricityUseKbtu?: number;
  totalNaturalGasUse?: string;
  medianNaturalGasUse?: string;

  showTrends = false;

  created(): void {
    // Buildings are pre-filtered by GraphQL query using PrimaryPropertyType field
    this.buildingsFiltered = this.$page.allBuilding.edges;
    this.loadPropertyTypeStats();
  }

  loadPropertyTypeStats(): void {
    const stats = this.propertyTypeStats;

    if (!stats) return;

    this.totalGHGEmissions = Math.round(
      stats.TotalGHGEmissions?.total ?? 0,
    ).toLocaleString();
    this.avgGHGIntensity = (stats.GHGIntensity?.mean ?? 0).toFixed(1);
    this.totalSquareFootage = (
      (stats.GrossFloorArea?.total ?? 0) / 1000000
    ).toFixed(1);

    if (stats.ElectricityUse?.total) {
      this.totalElectricityUseKbtu = stats.ElectricityUse.total;
      this.medianElectricityUseKbtu = stats.ElectricityUse.median;
    }

    if (stats.NaturalGasUse?.total) {
      this.totalNaturalGasUse = NumberFormatter.formatKbtu(
        stats.NaturalGasUse.total,
      );
      this.medianNaturalGasUse = NumberFormatter.formatKbtu(
        stats.NaturalGasUse.median ?? 0,
      );
    }

    // Build data for Pie Chart
    this.gradeDistributionPie = Object.entries(stats.gradeDistribution ?? {})
      .sort(([a], [b]) => {
        const gradeOrder = ['A', 'B', 'C', 'D', 'F'];
        return gradeOrder.indexOf(a) - gradeOrder.indexOf(b);
      })
      .map(([grade, count]) => ({
        label: `Grade ${grade}`,
        value: count,
        color: GradeColors[grade] || '#999999',
      }));
  }

  get propertyType(): string {
    return this.$context.propertyType;
  }

  get propertyTypePlural(): string {
    return pluralizePropertyType(this.$context.propertyType);
  }

  get buildingCount(): number {
    return this.buildingsFiltered.length;
  }

  get totalElectricityUse(): string | undefined {
    if (this.totalElectricityUseKbtu == null) return undefined;
    return NumberFormatter.formatBigNumber(
      kBtuToKwh(this.totalElectricityUseKbtu),
    );
  }

  get totalElectricityUseTooltip(): string {
    if (this.totalElectricityUseKbtu == null) return '';
    return kBtuToKwhTooltip(this.totalElectricityUseKbtu);
  }

  get medianElectricityUse(): string | undefined {
    if (this.medianElectricityUseKbtu == null) return undefined;
    return NumberFormatter.formatBigNumber(
      kBtuToKwh(this.medianElectricityUseKbtu),
    );
  }

  get medianElectricityUseTooltip(): string {
    if (this.medianElectricityUseKbtu == null) return '';
    return kBtuToKwhTooltip(this.medianElectricityUseKbtu);
  }

  get citywideMedianElectricityUse(): string {
    return NumberFormatter.formatBigNumber(
      kBtuToKwh(BuildingBenchmarkStats.ElectricityUse.median),
    );
  }

  get citywideMedianElectricityUseTooltip(): string {
    return kBtuToKwhTooltip(BuildingBenchmarkStats.ElectricityUse.median);
  }

  get citywideMedianNaturalGasUse(): string {
    return NumberFormatter.formatKbtu(
      BuildingBenchmarkStats.NaturalGasUse.median,
    );
  }

  get electricityTotalVsCitywideMultiple(): string | null {
    const total = this.propertyTypeStats?.ElectricityUse?.total;
    if (!total) return null;
    return getMedianMultipleMsg(
      BuildingBenchmarkStats.ElectricityUse.median,
      total,
    );
  }

  get electricityMedianMultiple(): string | null {
    const median = this.propertyTypeStats?.ElectricityUse?.median;
    if (!median) return null;
    return getMedianMultipleMsg(
      BuildingBenchmarkStats.ElectricityUse.median,
      median,
    );
  }

  get gasTotalVsCitywideMultiple(): string | null {
    const total = this.propertyTypeStats?.NaturalGasUse?.total;
    if (!total) return null;
    return getMedianMultipleMsg(
      BuildingBenchmarkStats.NaturalGasUse.median,
      total,
    );
  }

  get gasMedianMultiple(): string | null {
    const median = this.propertyTypeStats?.NaturalGasUse?.median;
    if (!median) return null;
    return getMedianMultipleMsg(
      BuildingBenchmarkStats.NaturalGasUse.median,
      median,
    );
  }

  get propertyTypeStats(): PropertyTypeStats | null {
    return (
      (BuildingStatsByPropertyType as Record<string, PropertyTypeStats>)[
        this.propertyType
      ] ?? null
    );
  }

  get historicPropertyTypeStats(): Record<string, YearData> | null {
    return (
      (HistoricStatsByPropertyType as Record<string, Record<string, YearData>>)[
        this.propertyType
      ] ?? null
    );
  }

  /** Extracts a median value for a metric across all years for this property type. */
  private historicMedian(metric: keyof YearData): INumGraphPoint[] {
    if (!this.historicPropertyTypeStats) return [];
    return Object.entries(this.historicPropertyTypeStats)
      .map(([year, yearData]) => ({
        x: parseInt(year),
        y: yearData[metric]?.median ?? 0,
      }))
      .filter((d) => d.y > 0)
      .sort((a, b) => a.x - b.x);
  }

  /** Extracts a total (mean * count) value for a metric across all years for this property type. */
  private historicTotal(metric: keyof YearData): INumGraphPoint[] {
    if (!this.historicPropertyTypeStats) return [];
    return Object.entries(this.historicPropertyTypeStats)
      .map(([year, yearData]) => {
        const s = yearData[metric];
        return {
          x: parseInt(year),
          y: s?.count && s.mean ? Math.round(s.mean * s.count) : 0,
        };
      })
      .filter((d) => d.y > 0)
      .sort((a, b) => a.x - b.x);
  }

  get buildingCountOverTime(): INumGraphPoint[] {
    if (!this.historicPropertyTypeStats) return [];
    return Object.entries(this.historicPropertyTypeStats)
      .map(([year, yearData]) => ({
        x: parseInt(year),
        y: yearData.GHGIntensity?.count ?? 0,
      }))
      .filter((d) => d.y > 0)
      .sort((a, b) => a.x - b.x);
  }

  get totalGHGOverTime(): INumGraphPoint[] {
    return this.historicTotal('TotalGHGEmissions');
  }

  get ghgIntensityOverTime(): INumGraphPoint[] {
    return this.historicMedian('GHGIntensity');
  }

  get electricityUseOverTime(): INumGraphPoint[] {
    return this.historicTotal('ElectricityUse');
  }

  get naturalGasUseOverTime(): INumGraphPoint[] {
    return this.historicTotal('NaturalGasUse');
  }

  get weatherNormalizedSourceEUIOverTime(): INumGraphPoint[] {
    return this.historicMedian('WeatherNormalizedSourceEUI');
  }

  // TODO: Move to using calculateEnergyBreakdown
  get energyMixPie(): IPieSlice[] {
    const stats = this.propertyTypeStats;
    if (!stats) return [];

    const slices: IPieSlice[] = [];
    const electricityTotal = stats.ElectricityUse?.total;
    if (electricityTotal)
      slices.push({
        label: 'Electricity',
        value: electricityTotal,
        color: EnergyBreakdownColors.Electricity,
      });
    const naturalGasTotal = stats.NaturalGasUse?.total;
    if (naturalGasTotal)
      slices.push({
        label: 'Fossil Gas',
        value: naturalGasTotal,
        color: EnergyBreakdownColors.NaturalGas,
      });
    const districtSteamTotal = stats.DistrictSteamUse?.total;
    if (districtSteamTotal)
      slices.push({
        label: 'District Steam',
        value: districtSteamTotal,
        color: EnergyBreakdownColors.DistrictSteam,
      });
    const districtChillingTotal = stats.DistrictChilledWaterUse?.total;
    if (districtChillingTotal)
      slices.push({
        label: 'District Chilling',
        value: districtChillingTotal,
        color: EnergyBreakdownColors.DistrictChilling,
      });
    return slices;
  }
}
</script>

<!-- Buildings are filtered by property type at query time using the PrimaryPropertyType field -->
<page-query>
  query($propertyType: String!) {
    allBuilding(
      filter: { PrimaryPropertyType: { eq: $propertyType } }
      sortBy: "GrossFloorArea"
    ) {
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
          path
          PrimaryPropertyType
          GHGIntensity
          GHGIntensityRank
          GHGIntensityPercentileRank
          TotalGHGEmissions
          TotalGHGEmissionsRank
          TotalGHGEmissionsPercentileRank
          AvgPercentileLetterGrade
          NaturalGasUse
          DistrictSteamUse
          DataAnomalies
          GrossFloorArea
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
          YearBuilt
          AvgPercentileLetterGrade
        }
      }
    }
  }
</page-query>

<template>
  <DefaultLayout main-class="layout -full-width">
    <div class="property-type-page">
      <BuildingsHero :buildings="buildingsFiltered.map((edge) => edge.node)">
        <h1 id="main-content" tabindex="-1">{{ propertyTypePlural }}</h1>
        <p class="building-count">
          {{ buildingCount.toLocaleString() }} building{{
            buildingCount !== 1 ? 's' : ''
          }}
          in Chicago
        </p>
      </BuildingsHero>

      <div class="page-constrained">
        <section class="stats-panel">
          <h2 class="stats-heading">{{ propertyType }} Stats</h2>

          <div class="stats-row">
            <div class="stat-item">
              <div class="stat-number">
                {{ buildingCount.toLocaleString() }}
              </div>
              <div class="stat-label bold">Buildings</div>
            </div>

            <div class="stat-item">
              <div class="stat-number">{{ totalGHGEmissions }}</div>
              <div class="stat-label">
                <strong>Total Emissions</strong> <br />
                <span class="unit">metric tons CO<sub>2</sub>e</span>
              </div>
            </div>

            <div class="stat-item">
              <div class="stat-number">{{ avgGHGIntensity }}</div>
              <div class="stat-label">
                <strong>Avg GHG Intensity</strong> <br />
                <span class="unit">kg CO<sub>2</sub>e/sqft</span>
              </div>
            </div>

            <div class="stat-item">
              <div class="stat-number">{{ totalSquareFootage }}M</div>
              <div class="stat-label bold">Total Square Footage</div>
            </div>

            <div
              v-if="gradeDistributionPie.length > 0"
              class="stat-item grade-chart-inline"
            >
              <PieChart
                :graph-data="gradeDistributionPie"
                id-prefix="grade-distribution"
                :show-labels="true"
                :sort-by-largest="false"
                :small="true"
              />
              <div class="stat-label bold -no-min">Grade Distribution</div>
            </div>

            <div
              v-if="energyMixPie.length > 0"
              class="stat-item grade-chart-inline"
            >
              <PieChart
                :graph-data="energyMixPie"
                id-prefix="energy-mix"
                :show-labels="true"
                :small="true"
              />
              <div class="stat-label bold -no-min">Total Energy Mix</div>
            </div>
          </div>

          <div
            v-if="totalElectricityUse || totalNaturalGasUse"
            class="stats-subsection"
          >
            <div v-if="totalElectricityUse" class="stat-item">
              <img
                src="/energy-icons/electricity.svg"
                alt=""
                class="stat-icon electricity"
              />
              <div>
                <div class="stat-label -no-min bold">Total Electricity Use</div>
                <div class="stat-number">
                  {{ totalElectricityUse }} kWh
                  <img
                    v-tooltip.bottom="{
                      content: totalElectricityUseTooltip,
                      trigger: 'click hover',
                    }"
                    class="tooltip -left"
                    src="/info.svg"
                    alt="Info icon"
                    tabindex="0"
                  />
                </div>
                <div
                  v-if="electricityTotalVsCitywideMultiple"
                  class="stat-median-compare"
                >
                  <strong
                    >{{ electricityTotalVsCitywideMultiple }} Median City
                    Building</strong
                  >
                  ({{ citywideMedianElectricityUse }} kWh)
                </div>
                <div v-if="medianElectricityUse" class="stat-type-median">
                  Median {{ propertyType }}: {{ medianElectricityUse }} kWh
                  <span v-if="electricityMedianMultiple"
                    >({{ electricityMedianMultiple }} median)</span
                  >
                </div>
              </div>
            </div>

            <div v-if="totalNaturalGasUse" class="stat-item">
              <img
                src="/energy-icons/natural-gas.svg"
                alt=""
                class="stat-icon"
              />
              <div>
                <div class="stat-label -no-min bold">Total Natural Gas Use</div>
                <div class="stat-number">{{ totalNaturalGasUse }} kBtu</div>
                <div
                  v-if="gasTotalVsCitywideMultiple"
                  class="stat-median-compare"
                >
                  <strong
                    >{{ gasTotalVsCitywideMultiple }} Median City
                    Building</strong
                  >
                  ({{ citywideMedianNaturalGasUse }} kBtu)
                </div>
                <div v-if="medianNaturalGasUse" class="stat-type-median">
                  Median {{ propertyType }}: {{ medianNaturalGasUse }} kBtu
                  <span v-if="gasMedianMultiple"
                    >({{ gasMedianMultiple }} median)</span
                  >
                </div>
              </div>
            </div>
          </div>

          <button
            v-if="buildingCountOverTime.length > 1"
            class="trends-toggle"
            @click="showTrends = !showTrends"
          >
            {{ showTrends ? 'Hide' : 'Show' }} Trends
            <span class="trends-toggle-arrow" :class="{ '-open': showTrends }"
              >▼</span
            >
          </button>

          <div
            v-if="buildingCountOverTime.length > 1 && showTrends"
            class="stats-subsection -spark-lines"
          >
            <div class="spark-stat-item">
              <div class="spark-label">Buildings Reporting</div>
              <SparkLine
                :graph-data="buildingCountOverTime"
                graph-title="Buildings Reporting"
                unit="buildings"
              />
            </div>

            <div class="spark-stat-item">
              <div class="spark-label">
                Total GHG Emissions
                <span class="spark-unit">metric tons CO<sub>2</sub>e</span>
              </div>
              <SparkLine
                :graph-data="totalGHGOverTime"
                graph-title="Total GHG Emissions"
                unit="metric tons CO₂e"
              />
            </div>

            <div class="spark-stat-item">
              <div class="spark-label">
                Median GHG Intensity
                <span class="spark-unit">kg CO<sub>2</sub>e / sqft</span>
              </div>
              <SparkLine
                :graph-data="ghgIntensityOverTime"
                graph-title="Median GHG Intensity"
                unit="kg CO₂e / sqft"
              />
            </div>

            <div
              v-if="electricityUseOverTime.length > 1"
              class="spark-stat-item"
            >
              <div class="spark-label">
                Total Electricity Use
                <span class="spark-unit">kBtu</span>
              </div>
              <SparkLine
                :graph-data="electricityUseOverTime"
                graph-title="Total Electricity Use"
                unit="kBtu"
              />
            </div>

            <div
              v-if="naturalGasUseOverTime.length > 1"
              class="spark-stat-item"
            >
              <div class="spark-label">
                Total Natural Gas Use
                <span class="spark-unit">kBtu</span>
              </div>
              <SparkLine
                :graph-data="naturalGasUseOverTime"
                graph-title="Total Natural Gas Use"
                unit="kBtu"
              />
            </div>

            <div
              v-if="weatherNormalizedSourceEUIOverTime.length > 1"
              class="spark-stat-item"
            >
              <div class="spark-label">
                Median Weather Normalized Source EUI
                <span class="spark-unit">kBtu/sqft</span>
              </div>
              <SparkLine
                :graph-data="weatherNormalizedSourceEUIOverTime"
                graph-title="Median Weather Normalized Source EUI"
                unit="kBtu/sqft"
              />
            </div>
          </div>
        </section>

        <h2>All {{ propertyTypePlural }}</h2>

        <p class="constrained -wide smaller">
          Showing {{ propertyTypePlural }} buildings that reported their energy
          use and greenhouse gas emissions to the City of Chicago under energy
          benchmarking.
        </p>

        <DataDisclaimer />

        <BuildingsTable
          :buildings="buildingsFiltered"
          :show-year-built="true"
          :show-square-footage="true"
        />

        <DataSourceFootnote />
      </div>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.property-type-page {
  h1 {
    font-size: 1.5rem;
  }

  .building-count {
    font-size: 1.125rem;
    font-weight: 600;
    margin-top: 0.5rem;
    color: $white;
  }

  h2 {
    margin-bottom: 0.5rem;
  }

  .stats-heading {
    width: 100%;
    margin: 0;
    font-size: 1rem;
    padding: 1rem 1rem 0;
  }

  .stats-panel {
    display: flex;
    align-items: center;
    margin: 2rem 0;
    background: $off-white;
    border-radius: $brd-rad-medium;
    flex-wrap: wrap;

    @media (max-width: $mobile-max-width) {
      flex-direction: column;
      gap: 1rem;
    }

    .stats-row {
      display: flex;
      align-items: center;
      gap: 2rem;
      width: 100%;
      flex-wrap: wrap;
      padding: 0 1rem 1rem;
      margin-top: 0;

      @media (max-width: $mobile-max-width) {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
      }

      .stat-item {
        text-align: center;
        flex: 1;
        min-width: 0;
        padding-right: 2rem;
        border-right: $border-thin solid $grey;

        &:last-child {
          border-right: none;
          padding-right: 0;
        }

        @media (max-width: $mobile-max-width) {
          text-align: left;
          border-right: none;
          padding-right: 0;
        }

        &.grade-chart-inline {
          display: flex;
          flex-direction: column;
          align-items: center;

          @media (max-width: $mobile-max-width) {
            padding-top: 1.5rem;
            border-top: $border-thin solid $grey;
          }
        }
      }
    }

    .stat-number {
      font-size: 1.75rem;
      font-weight: bold;
      color: $off-black;
      line-height: 1.2;
    }

    .stat-label {
      font-size: 0.875rem;
      color: $text-mid-light;
      line-height: 1.25;
      margin-top: 0.25rem;

      .unit {
        font-size: 0.75rem;
      }

      &:not(.-no-min) {
        // Lock to two lines for alignment
        min-height: 3.2em;
      }
    }

    .stat-avg {
      font-size: 0.75rem;
      color: $text-mid-light;
      margin-top: 0.25rem;
    }

    .stat-median-compare {
      font-size: 0.875rem;
      color: $text-mid-light;
      margin-top: 0.25rem;
    }

    .stat-type-median {
      font-size: 0.8rem;
      color: $text-mid-light;
      margin-top: 0.15rem;
    }

    .stats-subsection {
      display: flex;
      gap: 2rem;
      width: 100%;
      padding: 1rem;
      border-top: $border-thin solid $grey;
      flex-wrap: wrap;

      @media (max-width: $mobile-max-width) {
        gap: 1.5rem;

        .divider {
          display: none;
        }
      }

      .stat-item {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 0.75rem;
        text-align: left;
        flex: 1;
        padding-right: 2rem;
        border-right: $border-thin solid $grey;

        &:last-child {
          border-right: none;
          padding-right: 0;
        }
      }

      .stat-icon {
        width: 2rem;
        height: 2rem;
        flex-shrink: 0;

        &.electricity {
          width: 3rem;
          height: 3rem;
          filter: drop-shadow(0.125rem 0.125rem rgba(0, 0, 0, 0.4));
        }
      }
    }
  }

  .trends-toggle {
    width: 100%;
    padding: 0.6rem 1rem;
    background: none;
    border: none;
    border-top: $border-thin solid $grey;
    border-radius: 0 0 $brd-rad-medium $brd-rad-medium;
    font-size: 0.8rem;
    color: $text-mid-light;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.4rem;

    &:hover {
      background: $grey-light;
      color: $off-black;
    }

    .trends-toggle-arrow {
      display: inline-block;
      transition: transform 0.2s ease;
      font-size: 0.6rem;

      &.-open {
        transform: rotate(180deg);
      }
    }
  }

  .stats-subsection.-spark-lines {
    gap: 1rem;

    .spark-stat-item {
      flex: 1;

      .spark-label {
        font-size: 0.875rem;
        color: $off-black;
        font-weight: 600;
        line-height: 1.2;
        min-height: 2.5rem;
        display: flex;
        flex-direction: column;
      }

      .spark-unit {
        font-size: 0.75rem;
        color: $text-mid-light;
        font-weight: normal;
      }

      .spark-graph-cont {
        margin-top: 0.5rem;
        width: 8rem;
      }
    }
  }
}
</style>
