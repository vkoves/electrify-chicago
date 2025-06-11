<template>
  <DefaultLayout>
    <h1 class="page-title" tabindex="-1">Citywide Stats</h1>
    
    <div class="graphs-container">
      <div class="graph-section">
        <h2>GHG Intensity (kg CO2e/sq ft)</h2>
        <div id="ghg-intensity-chart"></div>
      </div>
      
      <div class="graph-section">
        <h2>Total GHG Emissions (metric tons CO2e)</h2>
        <div id="total-ghg-chart"></div>
      </div>
      
      <div class="graph-section">
        <h2>Electricity Use (kWh)</h2>
        <div id="electricity-chart"></div>
      </div>
      
      <div class="graph-section">
        <h2>Natural Gas Use (therms)</h2>
        <div id="natural-gas-chart"></div>
      </div>
      
      <div class="graph-section">
        <h2>Source EUI (kBtu/sq ft)</h2>
        <div id="source-eui-chart"></div>
      </div>
      
      <div class="graph-section">
        <h2>Site EUI (kBtu/sq ft)</h2>
        <div id="site-eui-chart"></div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NewTabIcon from '~/components/NewTabIcon.vue';
import HistoricStats from '../data/dist/historic-stats.json'
import { renderScatterplot } from '../components/graphs/Scatterplot';

interface GraphConfig {
  data: DataPoint[];
  containerId: string;
  title: string;
  yAxisLabel: string;
  color: string;
}

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
  DistrictSteamUse?: MetricStats;
  DistrictChilledWaterUse?: MetricStats;
}


type MetricDetail = 'count' | 'mean' | 'std' | 'min' | 'max' | '25%' | '50%' | '75%';

@Component({
  components: {
    NewTabIcon,
  },
})
export default class ScatterplotGraph extends Vue {

  mounted() {

// Map from user-friendly keys to actual MetricStats properties
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

// Helper function to extract data for a specific metric
function extractMetricData(
  metricName: keyof YearData,
  detail: MetricDetail
): DataPoint[] {
  const historicStats = HistoricStats as Record<string, YearData>;

  return Object.entries(historicStats)
    .map(([year, yearData]: [string, YearData]) => {
      const stats = yearData[metricName];
      const value = stats ? stats[detailKeyMap[detail]] : undefined;

      return {
        year: parseInt(year),
        value: value ?? 0
      };
    })
    .filter((point: DataPoint) => point.value !== 0)
    .sort((a: DataPoint, b: DataPoint) => a.year - b.year);
}

  const allData: Record<string, Record<MetricDetail, DataPoint[]>> = {
    GHGIntensity: {
      count: extractMetricData('GHGIntensity', 'count'),
      mean: extractMetricData('GHGIntensity', 'mean'),
      std: extractMetricData('GHGIntensity', 'std'),
      min: extractMetricData('GHGIntensity', 'min'),
      max: extractMetricData('GHGIntensity', 'max'),
      '25%': extractMetricData('GHGIntensity', '25%'),
      '50%': extractMetricData('GHGIntensity', '50%'),
      '75%': extractMetricData('GHGIntensity', '75%'),
    },
    TotalGHGEmissions: {
      count: extractMetricData('TotalGHGEmissions', 'count'),
      mean: extractMetricData('TotalGHGEmissions', 'mean'),
      std: extractMetricData('TotalGHGEmissions', 'std'),
      min: extractMetricData('TotalGHGEmissions', 'min'),
      max: extractMetricData('TotalGHGEmissions', 'max'),
      '25%': extractMetricData('TotalGHGEmissions', '25%'),
      '50%': extractMetricData('TotalGHGEmissions', '50%'),
      '75%': extractMetricData('TotalGHGEmissions', '75%'),
    },
    ElectricityUse: {
      count: extractMetricData('ElectricityUse', 'count'),
      mean: extractMetricData('ElectricityUse', 'mean'),
      std: extractMetricData('ElectricityUse', 'std'),
      min: extractMetricData('ElectricityUse', 'min'),
      max: extractMetricData('ElectricityUse', 'max'),
      '25%': extractMetricData('ElectricityUse', '25%'),
      '50%': extractMetricData('ElectricityUse', '50%'),
      '75%': extractMetricData('ElectricityUse', '75%'),
    },
    NaturalGasUse: {
      count: extractMetricData('NaturalGasUse', 'count'),
      mean: extractMetricData('NaturalGasUse', 'mean'),
      std: extractMetricData('NaturalGasUse', 'std'),
      min: extractMetricData('NaturalGasUse', 'min'),
      max: extractMetricData('NaturalGasUse', 'max'),
      '25%': extractMetricData('NaturalGasUse', '25%'),
      '50%': extractMetricData('NaturalGasUse', '50%'),
      '75%': extractMetricData('NaturalGasUse', '75%'),
    },
    SourceEUI: {
      count: extractMetricData('SourceEUI', 'count'),
      mean: extractMetricData('SourceEUI', 'mean'),
      std: extractMetricData('SourceEUI', 'std'),
      min: extractMetricData('SourceEUI', 'min'),
      max: extractMetricData('SourceEUI', 'max'),
      '25%': extractMetricData('SourceEUI', '25%'),
      '50%': extractMetricData('SourceEUI', '50%'),
      '75%': extractMetricData('SourceEUI', '75%'),
    },
    SiteEUI: {
      count: extractMetricData('SiteEUI', 'count'),
      mean: extractMetricData('SiteEUI', 'mean'),
      std: extractMetricData('SiteEUI', 'std'),
      min: extractMetricData('SiteEUI', 'min'),
      max: extractMetricData('SiteEUI', 'max'),
      '25%': extractMetricData('SiteEUI', '25%'),
      '50%': extractMetricData('SiteEUI', '50%'),
      '75%': extractMetricData('SiteEUI', '75%'),
    },
  };

    const graphConfigs: GraphConfig[] = [
      {
        data: allData.GHGIntensity['mean'],
        containerId: 'ghg-intensity-chart',
        title: 'GHG Intensity',
        yAxisLabel: 'kg CO2e/sq ft',
        color: '#e74c3c'
      },
      {
        data: allData.TotalGHGEmissions['mean'],
        containerId: 'total-ghg-chart',
        title: 'Total GHG Emissions',
        yAxisLabel: 'metric tons CO2e',
        color: '#3498db'
      },
      {
        data: allData.ElectricityUse['mean'],
        containerId: 'electricity-chart',
        title: 'Electricity Use',
        yAxisLabel: 'kWh',
        color: '#f39c12'
      },
      {
        data: allData.NaturalGasUse['mean'],
        containerId: 'natural-gas-chart',
        title: 'Natural Gas Use',
        yAxisLabel: 'therms',
        color: '#27ae60'
      },
      {
        data: allData.SourceEUI['mean'],
        containerId: 'source-eui-chart',
        title: 'Source EUI',
        yAxisLabel: 'kBtu/sq ft',
        color: '#9b59b6'
      },
      {
        data: allData.SiteEUI['mean'],
        containerId: 'site-eui-chart',
        title: 'Site EUI',
        yAxisLabel: 'kBtu/sq ft',
        color: '#1abc9c'
      }
    ];

    // Create all graphs
    graphConfigs.forEach(config => {
      if (config.data.length > 0) {
        renderScatterplot(config);
      }
    });
  }

}


</script>


<style lang="scss" scoped>
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
  justify-content: center;
  align-items: center;
  
  h2 {
    margin-bottom: 1rem;
    font-size: 1.2rem;
    color: #333;
  }
  
  div[id$="-chart"] {
    position: relative;
  }
}

.tooltip {
  font-size: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>