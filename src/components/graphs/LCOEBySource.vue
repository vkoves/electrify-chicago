<template>
  <div class="lcoe-by-source">
    <div v-if="loading" class="loading-message">Loading energy cost data...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else>
      <ScatterGraph
        :series="allSeries"
        y-axis-label="Cost (¢/kWh)"
        container-id="lcoe-all-sources"
        title="Levelized Cost of Energy by Source Over Time"
        :show-grid="true"
        :show-trend-line="false"
        :show-legend="true"
        :y-axis-formatter="formatAsCents"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import * as d3 from 'd3';

import ScatterGraph from '~/components/graphs/ScatterGraph.vue';
import { DataSeries } from '~/common-functions.vue';

interface LCOERecord {
  Entity: string;
  Code: string;
  Year: string;
  'Bioenergy levelized cost of energy': string;
  'Geothermal levelized cost of energy': string;
  'Offshore wind levelized cost of energy': string;
  'Solar photovoltaic levelized cost of energy': string;
  'Concentrated solar power levelized cost of energy': string;
  'Hydropower levelized cost of energy': string;
  'Onshore wind levelized cost of energy': string;
}

interface LCOEData {
  year: number;
  solarPV: number;
  onshoreWind: number;
  bioenergy: number;
  hydropower: number;
}

@Component({
  components: {
    ScatterGraph,
  },
})
export default class LCOEBySource extends Vue {
  private lcoeData: LCOEData[] = [];
  private loading = true;
  private error = '';

  mounted(): void {
    this.loadLCOEData();
  }

  formatAsCents(value: number): string {
    const cents = value * 100;
    return `${cents.toFixed(0)}¢`;
  }

  async loadLCOEData(): Promise<void> {
    try {
      const response = await fetch(
        '/blog/electric-bill/lcoe/levelized-cost-of-energy.csv',
      );

      if (!response.ok) {
        throw new Error('Failed to load LCOE data');
      }

      const csvText = await response.text();
      const records = d3.csvParse(csvText) as unknown as LCOERecord[];

      this.lcoeData = records.map((record) => ({
        year: parseInt(record.Year, 10),
        solarPV: parseFloat(
          record['Solar photovoltaic levelized cost of energy'],
        ),
        onshoreWind: parseFloat(
          record['Onshore wind levelized cost of energy'],
        ),
        bioenergy: parseFloat(record['Bioenergy levelized cost of energy']),
        hydropower: parseFloat(record['Hydropower levelized cost of energy']),
      }));

      this.loading = false;
    } catch (err) {
      this.error = 'Error loading energy cost data. Please try again later.';
      this.loading = false;
      console.error('Error loading LCOE data:', err);
    }
  }

  get allSeries(): DataSeries[] {
    return [
      {
        name: 'Solar PV',
        data: this.lcoeData.map((d) => ({
          year: d.year,
          value: d.solarPV,
        })),
        strokeColor: 'chart-stroke-orange',
        fillColor: 'chart-fill-orange',
      },
      {
        name: 'Onshore Wind',
        data: this.lcoeData.map((d) => ({
          year: d.year,
          value: d.onshoreWind,
        })),
        strokeColor: 'chart-stroke-teal',
        fillColor: 'chart-fill-teal',
      },
      {
        name: 'Bioenergy',
        data: this.lcoeData.map((d) => ({
          year: d.year,
          value: d.bioenergy,
        })),
        strokeColor: 'chart-stroke-green',
        fillColor: 'chart-fill-green',
      },
      {
        name: 'Hydropower',
        data: this.lcoeData.map((d) => ({
          year: d.year,
          value: d.hydropower,
        })),
        strokeColor: 'chart-stroke-blue',
        fillColor: 'chart-fill-blue',
      },
    ];
  }
}
</script>

<style lang="scss" scoped>
@import '~/scss/spacing.scss';

.lcoe-by-source {
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
