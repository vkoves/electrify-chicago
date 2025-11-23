<template>
  <div class="us-electricity-consumption">
    <div v-if="loading" class="loading-message">
      Loading electricity consumption data...
    </div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else>
      <ScatterGraph
        :series="allSeries"
        y-axis-label="Consumption (trillion kWh)"
        container-id="electricity-all-sectors"
        title="U.S. Electricity Consumption by Sector"
        :show-grid="true"
        :show-trend-line="false"
        :show-legend="true"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import * as d3 from 'd3';

import ScatterGraph from '~/components/graphs/ScatterGraph.vue';
import { DataSeries } from '~/common-functions.vue';

interface ElectricityRecord {
  '': string; // The CSV has an unnamed first column for year
  industrial: string;
  commercial: string;
  residential: string;
  transportation: string;
  'direct use': string;
}

interface ElectricityData {
  year: number;
  industrial: number;
  commercial: number;
  residential: number;
  transportation: number;
  directUse: number;
  total: number;
}

@Component({
  components: {
    ScatterGraph,
  },
})
export default class USElectricityConsumption extends Vue {
  private electricityData: ElectricityData[] = [];
  private loading = true;
  private error = '';

  mounted(): void {
    this.loadElectricityData();
  }

  async loadElectricityData(): Promise<void> {
    try {
      const response = await fetch(
        '/blog/electric-bill/electric-use/retail-major-sectors.csv',
      );

      if (!response.ok) {
        throw new Error('Failed to load electricity consumption data');
      }

      const csvText = await response.text();

      // Skip the first 5 header/description lines
      const lines = csvText.split('\n');
      const dataLines = lines.slice(5).join('\n');

      const records = d3.csvParse(dataLines) as unknown as ElectricityRecord[];

      this.electricityData = records
        .filter((record) => {
          const yearNum = parseInt(record[''], 10);
          return !isNaN(yearNum) && yearNum > 1900;
        })
        .map((record) => {
          const industrial = parseFloat(record.industrial);
          const commercial = parseFloat(record.commercial);
          const residential = parseFloat(record.residential);
          const transportation = parseFloat(record.transportation);
          const directUse = parseFloat(record['direct use']);

          return {
            year: parseInt(record[''], 10),
            industrial,
            commercial,
            residential,
            transportation,
            directUse,
            total:
              industrial + commercial + residential + transportation + directUse,
          };
        });

      this.loading = false;
    } catch (err) {
      this.error =
        'Error loading electricity consumption data. Please try again later.';
      this.loading = false;
      console.error('Error loading electricity data:', err);
    }
  }

  get allSeries(): DataSeries[] {
    return [
      {
        name: 'Total',
        data: this.electricityData.map((d) => ({
          year: d.year,
          value: d.total,
        })),
        strokeColor: 'chart-stroke-purple',
        fillColor: 'chart-fill-purple',
      },
      {
        name: 'Residential',
        data: this.electricityData.map((d) => ({
          year: d.year,
          value: d.residential,
        })),
        strokeColor: 'chart-stroke-blue',
        fillColor: 'chart-fill-blue',
      },
      {
        name: 'Commercial',
        data: this.electricityData.map((d) => ({
          year: d.year,
          value: d.commercial,
        })),
        strokeColor: 'chart-stroke-green',
        fillColor: 'chart-fill-green',
      },
      {
        name: 'Industrial',
        data: this.electricityData.map((d) => ({
          year: d.year,
          value: d.industrial,
        })),
        strokeColor: 'chart-stroke-orange',
        fillColor: 'chart-fill-orange',
      },
    ];
  }
}
</script>

<style lang="scss" scoped>
@import '~/scss/spacing.scss';

.us-electricity-consumption {
  margin: 2rem 0;
}

.loading-message,
.error-message {
  padding: 2rem;
  text-align: center;
  font-size: 1rem;
}

.error-message {
  color: $text-light;
}

</style>
