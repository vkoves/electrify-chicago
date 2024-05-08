<template>
  <div class="historical-table-cont">
    <table class="historical-data">
      <thead>
        <tr>
          <th scope="col">
            Year
          </th>
          <th
            v-if="renderedColumns.includes('GrossFloorArea')"
            scope="col"
          >
            Floor Area <span class="unit">sqft</span>
          </th>
          <th
            v-if="renderedColumns.includes('ChicagoEnergyRating')"
            scope="col"
          >
            Chicago Energy<br> Rating
          </th>
          <th
            v-if="renderedColumns.includes('ENERGYSTARScore')"
            scope="col"
          >
            Energy Star<br> Score
          </th>
          <th scope="col">
            GHG Intensity <span class="unit">kg CO<sub>2</sub>e / sqft</span>
          </th>
          <th scope="col">
            Source EUI <span class="unit">kBtu / sqft</span>
          </th>

          <th scope="col">
            Electricity Use <span class="unit">kBtu</span>
          </th>
          <th scope="col">
            Natural Gas Use <span class="unit">kBtu</span>
          </th>
          <th
            v-if="renderedColumns.includes('DistrictSteamUse')"
            scope="col"
          >
            District Steam Use <span class="unit">kBtu</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="benchmark in historicBenchmarks"
          :key="benchmark.DataYear"
        >
          <td>{{ benchmark.DataYear }}</td>
          <td v-if="renderedColumns.includes('GrossFloorArea')">
            {{ benchmark.GrossFloorArea | optionalInt }}
          </td>
          <td v-if="renderedColumns.includes('ChicagoEnergyRating')">
            {{ benchmark.ChicagoEnergyRating || '-' }}
          </td>
          <td v-if="renderedColumns.includes('ENERGYSTARScore')">
            {{ benchmark.ENERGYSTARScore || '-' }}
          </td>
          <td>{{ benchmark.GHGIntensity }}</td>
          <td>{{ benchmark.SourceEUI }}</td>

          <!-- Round big numbers -->
          <td>{{ benchmark.ElectricityUse | optionalInt }}</td>
          <td>{{ benchmark.NaturalGasUse | optionalInt }}</td>
          <td v-if="renderedColumns.includes('DistrictSteamUse')">
            {{ benchmark.DistrictSteamUse | optionalInt }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import {IHistoricData} from '../common-functions.vue';

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
     optionalInt(value: string) {
      if (!value) {
        return '-';
      }

      return parseInt(value).toLocaleString();
    },
  },
})
export default class BuildingImage extends Vue {
  @Prop({required: true}) historicBenchmarks!: Array<IHistoricData>;

  renderedColumns: Array<string> = [];

  getRenderedColumns(): Array<string> {
    if (this.historicBenchmarks.length === 0) {
      return [];
    }

    const allColKeys: Array<string> = Object.keys(this.historicBenchmarks[0]);
    const emptyColKeys = allColKeys.filter((colKey: string) => {
      // A column is empty if it's all empty string or '0', so skip it if so. Some columns switch
      // between both, like Natural Gas Use on Merch Mart, which we also want to ignore
      return !this.historicBenchmarks.every((datum) => {
        return (datum as any)[colKey] === '' || (datum as any)[colKey] === '0.0';
      });
    });

    return emptyColKeys;
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
  min-width: 62.5rem; // 1000px

  .unit {
    display: block;
    font-size: 0.75rem;
    font-weight: normal;
  }

  th, td {
    padding: 0.5rem 0.75rem;
    text-align: left;
  }

  thead {
    tr { background-color: $grey; }

    th {
      line-height: 1.25;
      font-size: 0.825rem;
    }
  }

  tbody tr:nth-of-type(even) { background-color: $grey-light; }
}
</style>
