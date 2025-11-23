<template>
  <div class="us-electricity-consumption">
    <div v-if="loading" class="loading-message">
      Loading electricity consumption data...
    </div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else class="graphs-container">
      <ScatterGraph
        :data="totalData"
        y-axis-label="Consumption (trillion kWh)"
        stroke-color="chart-stroke-purple"
        fill-color="chart-fill-purple"
        container-id="electricity-total"
        title="Total U.S. Electricity Consumption"
        :show-grid="true"
        :show-trend-line="true"
      />
      <ScatterGraph
        :data="residentialData"
        y-axis-label="Consumption (trillion kWh)"
        stroke-color="chart-stroke-blue"
        fill-color="chart-fill-blue"
        container-id="electricity-residential"
        title="Residential Electricity Consumption"
        :show-grid="true"
        :show-trend-line="true"
      />
      <ScatterGraph
        :data="commercialData"
        y-axis-label="Consumption (trillion kWh)"
        stroke-color="chart-stroke-green"
        fill-color="chart-fill-green"
        container-id="electricity-commercial"
        title="Commercial Electricity Consumption"
        :show-grid="true"
        :show-trend-line="true"
      />
      <ScatterGraph
        :data="industrialData"
        y-axis-label="Consumption (trillion kWh)"
        stroke-color="chart-stroke-orange"
        fill-color="chart-fill-orange"
        container-id="electricity-industrial"
        title="Industrial Electricity Consumption"
        :show-grid="true"
        :show-trend-line="true"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import * as d3 from 'd3';

import ScatterGraph from '~/components/graphs/ScatterGraph.vue';
import { DataPoint } from '~/common-functions.vue';

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

  get totalData(): DataPoint[] {
    return this.electricityData.map((d) => ({
      year: d.year,
      value: d.total,
    }));
  }

  get residentialData(): DataPoint[] {
    return this.electricityData.map((d) => ({
      year: d.year,
      value: d.residential,
    }));
  }

  get commercialData(): DataPoint[] {
    return this.electricityData.map((d) => ({
      year: d.year,
      value: d.commercial,
    }));
  }

  get industrialData(): DataPoint[] {
    return this.electricityData.map((d) => ({
      year: d.year,
      value: d.industrial,
    }));
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

.graphs-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;

  @media (max-width: $mobile-max-width) {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
