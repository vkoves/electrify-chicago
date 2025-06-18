<template>
  <DefaultLayout>
    <h1 class="page-title" tabindex="-1">Citywide Stats</h1>

    <div class="graphs-container">
      <div v-for="graph in graphConfigs" :key="graph.containerId" class="graph-section">
        <h2>{{ graph.title }} ({{ graph.yAxisLabel }})</h2>
        <ScatterGraph
          :data="graph.data"
          :y-axis-label="graph.yAxisLabel"
          :color="graph.color"
          :container-id="graph.containerId"
        />
      </div>
    </div>
  </DefaultLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HistoricStats from '../data/dist/historic-stats.json'
import ScatterGraph from '@/components/graphs/ScatterGraph.vue'


interface DataPoint {
  year: number;
  value: number;
}

interface MetricStats {
  count: number;
  mean: number;
  std: number;
  min: number;
  max: number;
  twentyFifthPercentile: number;
  median: number;
  seventyFifthPercentile: number;
}

interface YearData {
  GHGIntensity?: MetricStats;
  TotalGHGEmissions?: MetricStats;
  ElectricityUse?: MetricStats;
  NaturalGasUse?: MetricStats;
  SourceEUI?: MetricStats;
  SiteEUI?: MetricStats;
}

type MetricDetail = 'count' | 'mean' | 'std' | 'min' | 'max' | '25%' | '50%' | '75%';

const detailKeyMap: Record<MetricDetail, keyof MetricStats> = {
  count: 'count',
  mean: 'mean',
  std: 'std',
  min: 'min',
  max: 'max',
  '25%': 'twentyFifthPercentile',
  '50%': 'median',
  '75%': 'seventyFifthPercentile'
};

function extractMetricData(
  metricName: keyof YearData,
  detail: MetricDetail
): DataPoint[] {
  const historicStats = HistoricStats as Record<string, YearData>;
  return Object.entries(historicStats)
    .map(([year, yearData]) => {
      const stats = yearData[metricName];
      const value = stats ? stats[detailKeyMap[detail]] : undefined;
      return {
        year: parseInt(year),
        value: value ?? 0
      };
    })
    .filter(d => d.value !== 0)
    .sort((a, b) => a.year - b.year);
}

export default defineComponent({
  name: 'CitywideStatsPage',
  components: {
    ScatterGraph
  },
  data() {
    return {
      graphConfigs: [
        {
          data: extractMetricData('GHGIntensity', 'mean'),
          containerId: 'ghg-intensity-chart',
          title: 'GHG Intensity',
          yAxisLabel: 'kg CO2e/sq ft',
          color: '#e74c3c'
        },
        {
          data: extractMetricData('TotalGHGEmissions', 'mean'),
          containerId: 'total-ghg-chart',
          title: 'Total GHG Emissions',
          yAxisLabel: 'metric tons CO2e',
          color: '#3498db'
        },
        {
          data: extractMetricData('ElectricityUse', 'mean'),
          containerId: 'electricity-chart',
          title: 'Electricity Use',
          yAxisLabel: 'kWh',
          color: '#f39c12'
        },
        {
          data: extractMetricData('NaturalGasUse', 'mean'),
          containerId: 'natural-gas-chart',
          title: 'Natural Gas Use',
          yAxisLabel: 'therms',
          color: '#27ae60'
        },
        {
          data: extractMetricData('SourceEUI', 'mean'),
          containerId: 'source-eui-chart',
          title: 'Source EUI',
          yAxisLabel: 'kBtu/sq ft',
          color: '#9b59b6'
        },
        {
          data: extractMetricData('SiteEUI', 'mean'),
          containerId: 'site-eui-chart',
          title: 'Site EUI',
          yAxisLabel: 'kBtu/sq ft',
          color: '#1abc9c'
        }
      ]
    }
  }
})
</script>

<style scoped lang="scss">
.graphs-container {
  margin-top: 2rem;
}
.page-title {
  text-align: center;
}
.graph-section {
  margin-bottom: 3rem;
  display: flex;
  flex-direction: column;
  align-items: center;

  h2 {
    margin-bottom: 1rem;
    font-size: 1.2rem;
    color: #333;
  }
}
</style>
