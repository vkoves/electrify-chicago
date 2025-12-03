<template>
  <DefaultLayout>
    <div class="citywide-stats-page">
      <h1 class="page-title" tabindex="-1">Citywide Stats</h1>
      <p>
        These charts provide an overview of energy and emissions data across all
        large buildings tracked in the city. Explore trends over time, compare
        building performance, and identify opportunities for sustainability
        improvements.
      </p>

      <p>
        <strong>Important Note!</strong> 2019 data is impacted by COVID, because
        data is reported on a delay. A large number of buildings didn't report
        their 2019 data, and so some statistics may have varied. To learn more,
        see our article:
        <g-link to="/blog/GHG-Intensity-Predict-Compliance">
          Do High Emitting Buildings Report Emissions Less Often? </g-link
        >, where we have a clear graph of the COVID reporting shifts.
      </p>

      <div
        class="graphs-container"
        aria-label="citywide data and info for all buidings we track"
      >
        <article
          v-for="graph in graphConfigs"
          :key="graph.containerId"
          :aria-label="`${graph.title} - graph and info`"
        >
          <div class="graph-info">
            <h2>{{ graph.title }} ({{ graph.yAxisLabel }})</h2>
            <p v-for="(paragraph, i) in graph.description" :key="i">
              {{ paragraph }}
            </p>
          </div>

          <ScatterGraph
            :data="graph.data"
            :y-axis-label="graph.yAxisLabel"
            :stroke-color="graph.strokeColor"
            :fill-color="graph.fillColor"
            :container-id="graph.containerId"
            :show-grid="true"
            :title="graph.title"
            :y-axis-formatter="formatSI"
            :y-axis-padding="0.5"
          />
        </article>
      </div>
      <p>
        * According to the Department of Energy,
        <a
          href="https://afdc.energy.gov/data/10310"
          target="_blank"
          aria-label="department of energy average fuel economy data - opens in a new tab"
        >
          the average car gets 24.4 MPG
        </a>
        , which requires approximately 102.5 gallons of gas to travel 2,500
        miles. Using the
        <a
          href="https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator"
          target="_blank"
          aria-label="EPA Greenhouse Gas Equivalencies Calculator - opens in a new tab"
        >
          EPA’s Greenhouse Gas Equivalencies Calculator
        </a>
        , this corresponds to about 0.911 metric tons, or roughly 2,000 pounds
        of CO₂.
      </p>
    </div>
  </DefaultLayout>
</template>

<script lang="ts">
import ScatterGraph from '@/components/graphs/ScatterGraph.vue';
import { graphConfigs } from '../constants/citywide-stats-graph-data.vue';
import { Component, Vue } from 'vue-property-decorator';
import * as d3 from 'd3';

@Component<any>({
  components: {
    ScatterGraph,
  },
  metaInfo() {
    return { title: 'Citywide Stats' };
  },
})
export default class CityWideStats extends Vue {
  data(): any {
    return {
      graphConfigs,
    };
  }

  // Format large numbers with SI notation (k, M, G, etc.)
  formatSI(value: number): string {
    return d3.format('~s')(value);
  }
}
</script>

<style scoped lang="scss">
.citywide-stats-page {
  max-width: 1000px;
  margin: 0 auto;
}
.graphs-container {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 3rem;
  article {
    display: flex;
    gap: 1rem;
    width: 100%;

    .graph-info {
      padding: 1rem;
      h2 {
        font-size: 1.2rem;
        margin: 0;
        color: #333;
      }

      p {
        max-width: 600px;
        font-size: 0.95rem;
        color: #555;
        margin-bottom: 1rem;
      }
    }
  }
}

/* Mobile breakpoint — stack vertically */
@media (max-width: $mobile-max-width) {
  .graphs-container article {
    flex-direction: column;
    align-items: center; /* Center content horizontally */
  }

  .graphs-container article .graph-info {
    max-width: 100%;
    padding: 0 1rem;
  }
}
</style>
