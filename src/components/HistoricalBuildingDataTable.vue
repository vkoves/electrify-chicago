<template>
  <div class="historical-table-cont">
    <table class="historical-data">
      <thead>
        <tr>
          <th scope="col">Year</th>

          <th class="text-center grade-header -overall">
            Overall <br />
            Grade
          </th>
          <th class="text-center grade-header small-col-header">
            Emissions <br />
            Intensity <br />
            Sub-Grade
          </th>
          <th class="text-center grade-header small-col-header">
            Energy Mix <br />
            Sub-Grade
          </th>
          <th class="text-center grade-header small-col-header">
            Reporting Mix <br />
            Sub-Grade
          </th>

          <th scope="col">
            GHG Intensity <span class="unit">kg CO<sub>2</sub>e / sqft</span>
          </th>
          <th scope="col">
            GHG Emissions <span class="unit">metric tons CO<sub>2</sub>e</span>
          </th>

          <!-- Energy Mix & Values -->
          <th class="text-center">Energy Mix</th>
          <th scope="col">Electricity Use <span class="unit">kBTU</span></th>
          <th scope="col">Fossil Gas Use <span class="unit">kBTU</span></th>
          <th v-if="renderedColumns.includes('DistrictSteamUse')" scope="col">
            District <br />
            Steam Use <span class="unit">kBTU</span>
          </th>
          <th
            v-if="renderedColumns.includes('DistrictChilledWaterUse')"
            scope="col"
          >
            District Chilled <br />
            Water Use <span class="unit">kBTU</span>
          </th>

          <th scope="col">Source EUI <span class="unit">kBTU / sqft</span></th>
          <th v-if="renderedColumns.includes('GrossFloorArea')" scope="col">
            Floor Area <span class="unit">sqft</span>
          </th>

          <th
            v-if="renderedColumns.includes('ChicagoEnergyRating')"
            scope="col"
          >
            Chicago Energy<br />
            Rating
          </th>
          <th v-if="renderedColumns.includes('ENERGYSTARScore')" scope="col">
            Energy Star<br />
            Score
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="benchmark in historicBenchmarks" :key="benchmark.DataYear">
          <td class="bold">{{ benchmark.DataYear }}</td>

          <!-- Only show any grades if the average exists for that year, otherwise it's
            incomplete data-->
          <td class="text-center">
            <LetterGrade
              v-if="benchmark.AvgPercentileLetterGrade"
              class="-overall"
              :grade="benchmark.AvgPercentileLetterGrade"
            />
          </td>
          <td class="text-center">
            <LetterGrade
              v-if="benchmark.AvgPercentileLetterGrade"
              :grade="benchmark.GHGIntensityLetterGrade"
            />
          </td>
          <td class="text-center">
            <LetterGrade
              v-if="benchmark.AvgPercentileLetterGrade"
              :grade="benchmark.EnergyMixLetterGrade"
            />
          </td>
          <td class="text-center">
            <LetterGrade
              v-if="benchmark.AvgPercentileLetterGrade"
              :grade="benchmark.SubmittedRecordsLetterGrade"
            />
          </td>

          <td>{{ benchmark.GHGIntensity }}</td>
          <td>{{ benchmark.TotalGHGEmissions | optionalFloat }}</td>

          <!-- Energy Mix & Energy (rounded because they are big numbers) -->
          <td class="energy-mix">
            <!-- Only show energy mix data if it's a reported year -->
            <div v-if="benchmark.GHGIntensity" class="mix-text">
              <div>
                <span class="prcnt"
                  >{{ calcEnergyMix(benchmark).elecPrcnt }}%</span
                >
                <span class="label">Electricity</span>
              </div>
              <div>
                <span class="prcnt"
                  >{{ calcEnergyMix(benchmark).natGasPrcnt }}%</span
                >
                <span class="label">Fossil Gas</span>
              </div>
              <div>
                <span class="prcnt"
                  >{{ calcEnergyMix(benchmark).otherPrcnt }}%</span
                >
                <span class="label">Other</span>
              </div>
            </div>

            <PieChart
              v-if="benchmark.GHGIntensity"
              :id-prefix="'y' + benchmark.DataYear"
              :graph-data="getBreakdown(benchmark)"
              :show-labels="false"
            />
          </td>
          <td>{{ benchmark.ElectricityUse | optionalInt }}</td>
          <td>{{ benchmark.NaturalGasUse | optionalInt }}</td>
          <td v-if="renderedColumns.includes('DistrictSteamUse')">
            {{ benchmark.DistrictSteamUse | optionalInt }}
          </td>
          <td v-if="renderedColumns.includes('DistrictChilledWaterUse')">
            {{ benchmark.DistrictChilledWaterUse | optionalInt }}
          </td>

          <td>{{ benchmark.SourceEUI }}</td>
          <td v-if="renderedColumns.includes('GrossFloorArea')">
            {{ benchmark.GrossFloorArea | optionalInt }}
          </td>

          <td v-if="renderedColumns.includes('ChicagoEnergyRating')">
            {{ benchmark.ChicagoEnergyRating || '-' }}
          </td>
          <td v-if="renderedColumns.includes('ENERGYSTARScore')">
            {{ benchmark.ENERGYSTARScore || '-' }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import {
  calculateEnergyBreakdown,
  IHistoricData,
} from '../common-functions.vue';
import PieChart, { IPieSlice } from './graphs/PieChart.vue';
import LetterGrade from './LetterGrade.vue';

/**
 * A component that given an array of a building's benchmarking renders
 * a table showing columns of data with values (skipping any columns that
 * never had a value, like if a building never had an Energy star score)
 */
@Component({
  filters: {
    /**
     * Round and process an optional float to a locale string
     *
     * Ex: null -> '-', '12345.67' -> '12,345'
     */
    optionalInt(value: number | null) {
      if (!value) {
        return '-';
      }
      return Math.round(value).toLocaleString();
    },

    optionalFloat(value: number | null) {
      if (!value) {
        return '-';
      }
      if(value >= 1000) {
        return Math.floor(value).toLocaleString();
      } 
      return value.toLocaleString();
    },
  },
  components: {
    LetterGrade,
    PieChart,
  },
})
export default class HistoricalBuildingTable extends Vue {
  @Prop({ required: true }) historicBenchmarks!: Array<IHistoricData>;

  renderedColumns: Array<string> = [];

  /** Expose calculateEnergyBreakdown to template */
  getBreakdown(benchmark: IHistoricData): Array<IPieSlice> {
    return calculateEnergyBreakdown(benchmark).energyBreakdown;
  }

  getRenderedColumns(): Array<string> {
    if (this.historicBenchmarks.length === 0) {
      return [];
    }

    const allColKeys: Array<string> = Object.keys(this.historicBenchmarks[0]);
    const emptyColKeys = allColKeys.filter((colKey: string) => {
      // A column is empty if it's all empty string or '0', so skip it if so. Some columns switch
      // between both, like Natural Gas Use on Merch Mart, which we also want to ignore
      return !this.historicBenchmarks.every((datum) => {
        return (
          (datum as any)[colKey] === '' || (datum as any)[colKey] === '0.0'
        );
      });
    });

    return emptyColKeys;
  }

  calcEnergyMix(benchmarkRow: IHistoricData): {
    elecPrcnt: number;
    natGasPrcnt: number;
    otherPrcnt: number;
  } {
    const totalUse =
      benchmarkRow.ElectricityUse +
      benchmarkRow.NaturalGasUse +
      benchmarkRow.DistrictSteamUse +
      benchmarkRow.DistrictChilledWaterUse;

    const elecPrcnt = Math.round(
      100 * (benchmarkRow.ElectricityUse / totalUse),
    );
    const natGasPrcnt = Math.round(
      100 * (benchmarkRow.NaturalGasUse / totalUse),
    );
    const otherUse =
      benchmarkRow.DistrictSteamUse ||
      0 + benchmarkRow.DistrictChilledWaterUse ||
      0;
    const otherPrcnt = Math.round((100 * otherUse) / totalUse);

    return { elecPrcnt, otherPrcnt, natGasPrcnt };
  }

  created(): void {
    this.renderedColumns = this.getRenderedColumns();
  }
}
</script>

<style lang="scss">
.historical-table-cont {
  max-width: 100%;
  overflow-x: auto;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

table.historical-data {
  border: solid 0.125rem $grey;
  border-radius: $brd-rad-small;
  border-collapse: collapse;
  width: 100%;
  min-width: 80rem;

  .unit {
    display: block;
    font-size: 0.75rem;
    font-weight: normal;
  }

  .energy-mix {
    display: flex;
    font-size: 0.8125rem;
    align-items: center;
    justify-content: space-around;
    gap: 1rem;

    .mix-text {
      flex-basis: 6rem;

      div {
        display: flex;
        justify-content: space-between;
        gap: 0.5rem;

        .prcnt {
          width: 40%;
          text-align: right;
        }
        .label {
          width: 100%;
        }
      }
    }

    .pie-chart-cont {
      width: 4rem;
    }
  }

  th,
  td {
    padding: 0.5rem 0.5rem;
    // Numbers should be right aligned, and most columns are numbers
    text-align: right;

    &:first-of-type {
      padding-left: 0.75rem;
    }
    &.text-center {
      text-align: center;
    }
  }

  thead {
    tr {
      background-color: $grey;
    }

    th {
      line-height: 1.25;
      font-size: 0.825rem;
      white-space: nowrap;

      &.grade-header {
        width: 3rem;

        &.-overall {
          padding-left: 1rem;
        }
      }

      &.small-col-header {
        font-weight: normal;
        font-size: 0.7rem;
      }
    }
  }

  tbody tr:nth-of-type(even) {
    background-color: $grey-light;
  }

  .letter-grade {
    font-size: 1.25rem;

    &.-overall {
      font-size: 1.75rem;
    }
    &:not(.-overall) {
      vertical-align: bottom;
    }
  }
}
</style>
