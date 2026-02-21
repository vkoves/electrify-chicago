<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import BarGraph, {
  IGraphPoint,
} from '../components/graphs/BarGraph.vue';
import SparkLine, {
  INumGraphPoint,
} from '../components/graphs/SparkLine.vue';
import PieChart, { IPieSlice } from '../components/graphs/PieChart.vue';
import ScatterGraph from '../components/graphs/ScatterGraph.vue';
import { DataPoint, DataSeries } from '../common-functions.vue';

/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    BarGraph,
    SparkLine,
    PieChart,
    ScatterGraph,
  },
  metaInfo() {
    return { title: 'Graph Component Demos' };
  },
})
export default class GraphDemos extends Vue {
  // BarGraph sample data
  barGraphData: Array<IGraphPoint> = [
    { x: '2018', y: 450 },
    { x: '2019', y: 520 },
    { x: '2020', y: 380 },
    { x: '2021', y: 610 },
    { x: '2022', y: 580 },
    { x: '2023', y: 650 },
  ];

  // SparkLine sample data
  sparkLineData: Array<INumGraphPoint> = [
    { x: 2018, y: 1200 },
    { x: 2019, y: 1350 },
    { x: 2020, y: 1100 },
    { x: 2021, y: 1500 },
    { x: 2022, y: 1450 },
    { x: 2023, y: 1600 },
  ];

  // PieChart sample data
  pieChartData: Array<IPieSlice> = [
    { label: 'Electricity', value: 45, color: '#F0E100' },
    { label: 'Natural Gas', value: 35, color: '#993300' },
    { label: 'District Steam', value: 15, color: '#ABABAB' },
    { label: 'District Chilling', value: 5, color: '#01295F' },
  ];

  // ScatterGraph single series sample data
  scatterSingleData: Array<DataPoint> = [
    { year: 2018, value: 25.4 },
    { year: 2019, value: 27.2 },
    { year: 2020, value: 24.1 },
    { year: 2021, value: 28.5 },
    { year: 2022, value: 29.3 },
    { year: 2023, value: 30.1 },
  ];

  // ScatterGraph multi-series sample data
  scatterMultiData: Array<DataSeries> = [
    {
      name: 'Residential',
      data: [
        { year: 2018, value: 15.2 },
        { year: 2019, value: 16.1 },
        { year: 2020, value: 14.8 },
        { year: 2021, value: 17.3 },
        { year: 2022, value: 18.0 },
        { year: 2023, value: 19.1 },
      ],
      strokeColor: 'chart-stroke-blue',
      fillColor: 'chart-fill-blue',
    },
    {
      name: 'Commercial',
      data: [
        { year: 2018, value: 28.5 },
        { year: 2019, value: 30.2 },
        { year: 2020, value: 27.1 },
        { year: 2021, value: 31.8 },
        { year: 2022, value: 32.5 },
        { year: 2023, value: 33.9 },
      ],
      strokeColor: 'chart-stroke-orange',
      fillColor: 'chart-fill-orange',
    },
  ];
}
</script>

<template>
  <DefaultLayout>
    <div class="graph-demos constrained -wide">
      <h1 id="main-content" tabindex="-1">Graph Component Demos</h1>

      <p>
        This page showcases the available graph components in our codebase.
        Each example includes sample data and common configurations.
      </p>

      <!-- BarGraph Demo -->
      <section class="demo-section">
        <h2>BarGraph</h2>
        <p>
          A bar chart component for displaying categorical data with numeric
          values. Supports both string and numeric x-axis values.
        </p>

        <div class="demo-container">
          <BarGraph
            graph-title="Annual Emissions Over Time"
            :graph-data="barGraphData"
          />
        </div>

        <div class="code-example">
          <h3>Usage Example:</h3>
          <pre>
<code>&lt;BarGraph
  graph-title="Annual Emissions Over Time"
  :graph-data="barGraphData"
/&gt;

// Data format:
const barGraphData: Array&lt;IGraphPoint&gt; = [
  { x: '2018', y: 450 },
  { x: '2019', y: 520 },
  // ...
];</code>
</pre>
        </div>
      </section>

      <!-- SparkLine Demo -->
      <section class="demo-section">
        <h2>SparkLine</h2>
        <p>
          A compact line graph component ideal for showing trends in small
          spaces. Displays min and max values with interactive tooltips.
        </p>

        <div class="demo-container -small">
          <SparkLine
            graph-title="GHG Intensity Trend"
            :graph-data="sparkLineData"
            unit="tons CO<sub>2</sub>e"
          />
        </div>

        <div class="code-example">
          <h3>Usage Example:</h3>
          <pre>
<code>&lt;SparkLine
  graph-title="GHG Intensity Trend"
  :graph-data="sparkLineData"
  unit="tons CO&lt;sub&gt;2&lt;/sub&gt;e"
/&gt;

// Data format:
const sparkLineData: Array&lt;INumGraphPoint&gt; = [
  { x: 2018, y: 1200 },
  { x: 2019, y: 1350 },
  // ...
];</code>
</pre>
        </div>
      </section>

      <!-- PieChart Demo -->
      <section class="demo-section">
        <h2>PieChart</h2>
        <p>
          A pie chart component for displaying proportional data. Supports
          custom colors and optional labels.
        </p>

        <div class="demo-container -medium">
          <PieChart
            :graph-data="pieChartData"
            id-prefix="energy-breakdown"
            :show-labels="true"
            :sort-by-largest="true"
          />
        </div>

        <div class="code-example">
          <h3>Usage Example:</h3>
          <pre>
<code>&lt;PieChart
  :graph-data="pieChartData"
  id-prefix="energy-breakdown"
  :show-labels="true"
  :sort-by-largest="true"
/&gt;

// Data format:
const pieChartData: Array&lt;IPieSlice&gt; = [
  { label: 'Electricity', value: 45, color: '#F0E100' },
  { label: 'Natural Gas', value: 35, color: '#993300' },
  // ...
];</code>
</pre>
        </div>
      </section>

      <!-- ScatterGraph Single Series Demo -->
      <section class="demo-section">
        <h2>ScatterGraph (Single Series)</h2>
        <p>
          A scatter plot component with line connections. Supports trend lines,
          grid display, and interactive tooltips. Single series mode is ideal
          for simple time series data.
        </p>

        <div class="demo-container">
          <ScatterGraph
            container-id="scatter-single-demo"
            title="Average GHG Intensity"
            y-axis-label="GHG Intensity (kg CO₂/sqft)"
            :data="scatterSingleData"
            stroke-color="chart-stroke-blue"
            fill-color="chart-fill-blue"
            :show-grid="true"
            :show-trend-line="true"
            :show-legend="false"
          />
        </div>

        <div class="code-example">
          <h3>Usage Example:</h3>
          <pre>
<code>&lt;ScatterGraph
  container-id="scatter-single-demo"
  title="Average GHG Intensity"
  y-axis-label="GHG Intensity (kg CO₂/sqft)"
  :data="scatterSingleData"
  stroke-color="chart-stroke-blue"
  fill-color="chart-fill-blue"
  :show-grid="true"
  :show-trend-line="true"
/&gt;

// Data format:
const scatterSingleData: Array&lt;DataPoint&gt; = [
  { year: 2018, value: 25.4 },
  { year: 2019, value: 27.2 },
  // ...
];</code>
</pre>
        </div>
      </section>

      <!-- ScatterGraph Multi-Series Demo -->
      <section class="demo-section">
        <h2>ScatterGraph (Multi-Series)</h2>
        <p>
          ScatterGraph also supports multiple data series with a legend,
          allowing comparison of different datasets on the same chart.
        </p>

        <div class="demo-container">
          <ScatterGraph
            container-id="scatter-multi-demo"
            title="Emissions by Building Type"
            y-axis-label="GHG Intensity (kg CO₂/sqft)"
            :series="scatterMultiData"
            :show-grid="true"
            :show-trend-line="true"
            :show-legend="true"
          />
        </div>

        <div class="code-example">
          <h3>Usage Example:</h3>
          <pre>
<code>&lt;ScatterGraph
  container-id="scatter-multi-demo"
  title="Emissions by Building Type"
  y-axis-label="GHG Intensity (kg CO₂/sqft)"
  :series="scatterMultiData"
  :show-grid="true"
  :show-trend-line="true"
  :show-legend="true"
/&gt;

// Data format:
const scatterMultiData: Array&lt;DataSeries&gt; = [
  {
    name: 'Residential',
    data: [{ year: 2018, value: 15.2 }, ...],
    strokeColor: 'chart-stroke-blue',
    fillColor: 'chart-fill-blue',
  },
  {
    name: 'Commercial',
    data: [{ year: 2018, value: 28.5 }, ...],
    strokeColor: 'chart-stroke-orange',
    fillColor: 'chart-fill-orange',
  },
];</code>
</pre>
        </div>
      </section>

      <!-- Props Reference -->
      <section class="demo-section">
        <h2>Common Props Reference</h2>

        <h3>ScatterGraph Props</h3>
        <ul>
          <li>
            <code>showGrid</code> (boolean, default: true) - Display horizontal
            and vertical grid lines
          </li>
          <li>
            <code>showTrendLine</code> (boolean, default: true) - Display
            linear regression trend line
          </li>
          <li>
            <code>showLegend</code> (boolean, default: false) - Display
            color-coded legend (useful for multi-series)
          </li>
          <li>
            <code>hidePoints</code> (boolean, default: false) - Hide data point
            circles, showing only lines
          </li>
          <li>
            <code>yAxisPadding</code> (number, default: 0.1) - Y-axis padding
            as fraction of max value (0.1 = 10%)
          </li>
          <li>
            <code>animationDuration</code> (number, default: 800) - Animation
            duration in milliseconds
          </li>
          <li>
            <code>yAxisFormatter</code> (function) - Custom formatter for y-axis
            tick values
          </li>
        </ul>

        <h3>PieChart Props</h3>
        <ul>
          <li>
            <code>showLabels</code> (boolean, default: true) - Display labels
            for each slice
          </li>
          <li>
            <code>sortByLargest</code> (boolean, default: true) - Sort slices by
            size (largest first)
          </li>
        </ul>
      </section>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.graph-demos {
  .demo-section {
    margin-bottom: 4rem;
    padding-bottom: 2rem;
    border-bottom: solid $border-thin $grey;

    &:last-child {
      border-bottom: none;
    }
  }

  .demo-container {
    background: $white;
    padding: 2rem;
    border-radius: $brd-rad-medium;
    border: solid $border-thin $grey;
    margin-top: 1rem;
    margin-bottom: 1.5rem;

    &.-small {
      max-width: 25rem;
    }

    &.-medium {
      max-width: 35rem;
    }
  }

  .code-example {
    background: $grey-light;
    padding: 1.5rem;
    border-radius: $brd-rad-medium;

    h3 {
      margin-top: 0;
    }

    pre {
      margin: 0;
      overflow-x: auto;

      code {
        display: block;
        background-color: $white;
      }
    }
  }

  ul li {
    margin-bottom: 0.75rem;
    line-height: 1.5;
  }
}
</style>
