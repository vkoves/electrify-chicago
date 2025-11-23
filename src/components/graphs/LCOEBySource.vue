<template>
  <div class="lcoe-by-source">
    <div v-if="loading" class="loading-message">Loading energy cost data...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>
    <div v-else class="graphs-container">
      <ScatterGraph
        :data="solarData"
        y-axis-label="Cost ($/kWh)"
        stroke-color="chart-stroke-orange"
        fill-color="chart-fill-orange"
        container-id="lcoe-solar"
        title="Solar Photovoltaic Cost Over Time"
        :show-grid="true"
        :show-trend-line="true"
      />
      <ScatterGraph
        :data="windData"
        y-axis-label="Cost ($/kWh)"
        stroke-color="chart-stroke-teal"
        fill-color="chart-fill-teal"
        container-id="lcoe-wind"
        title="Onshore Wind Cost Over Time"
        :show-grid="true"
        :show-trend-line="true"
      />
      <ScatterGraph
        :data="bioenergyData"
        y-axis-label="Cost ($/kWh)"
        stroke-color="chart-stroke-green"
        fill-color="chart-fill-green"
        container-id="lcoe-bioenergy"
        title="Bioenergy Cost Over Time"
        :show-grid="true"
        :show-trend-line="true"
      />
      <ScatterGraph
        :data="hydropowerData"
        y-axis-label="Cost ($/kWh)"
        stroke-color="chart-stroke-blue"
        fill-color="chart-fill-blue"
        container-id="lcoe-hydropower"
        title="Hydropower Cost Over Time"
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

  get solarData(): DataPoint[] {
    return this.lcoeData.map((d) => ({
      year: d.year,
      value: d.solarPV,
    }));
  }

  get windData(): DataPoint[] {
    return this.lcoeData.map((d) => ({
      year: d.year,
      value: d.onshoreWind,
    }));
  }

  get bioenergyData(): DataPoint[] {
    return this.lcoeData.map((d) => ({
      year: d.year,
      value: d.bioenergy,
    }));
  }

  get hydropowerData(): DataPoint[] {
    return this.lcoeData.map((d) => ({
      year: d.year,
      value: d.hydropower,
    }));
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
