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
  getMedianMultipleMsg,
  pluralizePropertyType,
} from '../common-functions.vue';
import { NumberFormatter } from '../utils/number-formatter.vue';
import { slugifyPropertyType } from '../constants/property-type-helpers.vue';
import { generatePropertyTypeMeta } from '../constants/meta-helpers.vue';
import BuildingStatsByPropertyType from '../data/dist/building-statistics-by-property-type.json';
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import HistoricStatsByPropertyType from '../data/dist/historic-stats-by-property-type.json';

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

  totalElectricityUse?: string;
  medianElectricityUse?: string;
  totalNaturalGasUse?: string;
  medianNaturalGasUse?: string;

  showTrends = false;

  created(): void {
    // Buildings are pre-filtered by GraphQL query using PrimaryPropertyType field
    this.buildingsFiltered = this.$page.allBuilding.edges;
    this.loadPropertyTypeStats();
  }

  loadPropertyTypeStats(): void {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const stats = (BuildingStatsByPropertyType as Record<string, any>)[
      this.$context.propertyType
    ];

    if (!stats) return;

    this.totalGHGEmissions = Math.round(
      stats.TotalGHGEmissions.total,
    ).toLocaleString();
    this.avgGHGIntensity = (stats.GHGIntensity.mean as number).toFixed(1);
    this.totalSquareFootage = (stats.GrossFloorArea.total / 1000000).toFixed(1);

    if (stats.ElectricityUse?.total) {
      this.totalElectricityUse = NumberFormatter.formatKbtu(
        stats.ElectricityUse.total,
      );
      this.medianElectricityUse = NumberFormatter.formatKbtu(
        stats.ElectricityUse.median,
      );
    }

    if (stats.NaturalGasUse?.total) {
      this.totalNaturalGasUse = NumberFormatter.formatKbtu(
        stats.NaturalGasUse.total,
      );
      this.medianNaturalGasUse = NumberFormatter.formatKbtu(
        stats.NaturalGasUse.median,
      );
    }

    // Build data for Pie Chart
    this.gradeDistributionPie = Object.entries(
      stats.gradeDistribution as Record<string, number>,
    )
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

  get citywideMedianElectricityUse(): string {
    return NumberFormatter.formatKbtu(
      BuildingBenchmarkStats.ElectricityUse.median,
    );
  }

  get citywideMedianNaturalGasUse(): string {
    return NumberFormatter.formatKbtu(
      BuildingBenchmarkStats.NaturalGasUse.median,
    );
  }

  get electricityTotalVsCitywideMultiple(): string | null {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const stats = (BuildingStatsByPropertyType as Record<string, any>)[
      this.propertyType
    ];
    if (!stats?.ElectricityUse?.total) return null;
    return getMedianMultipleMsg(
      BuildingBenchmarkStats.ElectricityUse.median,
      stats.ElectricityUse.total,
    );
  }

  get electricityMedianMultiple(): string | null {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const stats = (BuildingStatsByPropertyType as Record<string, any>)[
      this.propertyType
    ];
    if (!stats?.ElectricityUse?.median) return null;
    return getMedianMultipleMsg(
      BuildingBenchmarkStats.ElectricityUse.median,
      stats.ElectricityUse.median,
    );
  }

  get gasTotalVsCitywideMultiple(): string | null {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const stats = (BuildingStatsByPropertyType as Record<string, any>)[
      this.propertyType
    ];
    if (!stats?.NaturalGasUse?.total) return null;
    return getMedianMultipleMsg(
      BuildingBenchmarkStats.NaturalGasUse.median,
      stats.NaturalGasUse.total,
    );
  }

  get gasMedianMultiple(): string | null {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const stats = (BuildingStatsByPropertyType as Record<string, any>)[
      this.propertyType
    ];
    if (!stats?.NaturalGasUse?.median) return null;
    return getMedianMultipleMsg(
      BuildingBenchmarkStats.NaturalGasUse.median,
      stats.NaturalGasUse.median,
    );
  }

  /* eslint-disable @typescript-eslint/no-explicit-any */
  get historicPropertyTypeStats(): Record<string, any> | null {
    return (
      (HistoricStatsByPropertyType as Record<string, any>)[this.propertyType] ??
      null
    );
  }
  /* eslint-enable @typescript-eslint/no-explicit-any */

  get buildingCountOverTime(): INumGraphPoint[] {
    if (!this.historicPropertyTypeStats) return [];
    return Object.entries(this.historicPropertyTypeStats)
      .map(([year, stats]) => ({
        x: parseInt(year),
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        y: (stats as any).GHGIntensity?.count ?? 0,
      }))
      .filter((d) => d.y > 0)
      .sort((a, b) => a.x - b.x);
  }

  get totalGHGOverTime(): INumGraphPoint[] {
    if (!this.historicPropertyTypeStats) return [];
    return Object.entries(this.historicPropertyTypeStats)
      .map(([year, stats]) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const s = (stats as any).TotalGHGEmissions;
        return {
          x: parseInt(year),
          y: s?.count > 0 ? Math.round(s.mean * s.count) : 0,
        };
      })
      .filter((d) => d.y > 0)
      .sort((a, b) => a.x - b.x);
  }

  get ghgIntensityOverTime(): INumGraphPoint[] {
    if (!this.historicPropertyTypeStats) return [];
    return Object.entries(this.historicPropertyTypeStats)
      .map(([year, stats]) => ({
        x: parseInt(year),
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        y: (stats as any).GHGIntensity?.median ?? 0,
      }))
      .filter((d) => d.y > 0)
      .sort((a, b) => a.x - b.x);
  }

  get electricityUseOverTime(): INumGraphPoint[] {
    if (!this.historicPropertyTypeStats) return [];
    return Object.entries(this.historicPropertyTypeStats)
      .map(([year, stats]) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const s = (stats as any).ElectricityUse;
        return {
          x: parseInt(year),
          y: s?.count > 0 ? Math.round(s.mean * s.count) : 0,
        };
      })
      .filter((d) => d.y > 0)
      .sort((a, b) => a.x - b.x);
  }

  get naturalGasUseOverTime(): INumGraphPoint[] {
    if (!this.historicPropertyTypeStats) return [];
    return Object.entries(this.historicPropertyTypeStats)
      .map(([year, stats]) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const s = (stats as any).NaturalGasUse;
        return {
          x: parseInt(year),
          y: s?.count > 0 ? Math.round(s.mean * s.count) : 0,
        };
      })
      .filter((d) => d.y > 0)
      .sort((a, b) => a.x - b.x);
  }

  // TODO: Move to using calculateEnergyBreakdown
  get energyMixPie(): IPieSlice[] {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const stats = (BuildingStatsByPropertyType as Record<string, any>)[
      this.propertyType
    ];
    if (!stats) return [];

    const slices: IPieSlice[] = [];
    if (stats.ElectricityUse?.total > 0)
      slices.push({
        label: 'Electricity',
        value: stats.ElectricityUse.total,
        color: EnergyBreakdownColors.Electricity,
      });
    if (stats.NaturalGasUse?.total > 0)
      slices.push({
        label: 'Fossil Gas',
        value: stats.NaturalGasUse.total,
        color: EnergyBreakdownColors.NaturalGas,
      });
    if (stats.DistrictSteamUse?.total > 0)
      slices.push({
        label: 'District Steam',
        value: stats.DistrictSteamUse.total,
        color: EnergyBreakdownColors.DistrictSteam,
      });
    if (stats.DistrictChilledWaterUse?.total > 0)
      slices.push({
        label: 'District Chilling',
        value: stats.DistrictChilledWaterUse.total,
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
                <div class="stat-number">{{ totalElectricityUse }} kBtu</div>
                <div
                  v-if="electricityTotalVsCitywideMultiple"
                  class="stat-median-compare"
                >
                  <strong
                    >{{ electricityTotalVsCitywideMultiple }} Median City
                    Building</strong
                  >
                  ({{ citywideMedianElectricityUse }} kBtu)
                </div>
                <div v-if="medianElectricityUse" class="stat-type-median">
                  Median {{ propertyType }}: {{ medianElectricityUse }} kBtu
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
