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
            :color="graph.color"
            :container-id="graph.containerId"
            :show-grid="true"
            :title="graph.title"
          />
        </article>
      </div>
    </div>
  </DefaultLayout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ScatterGraph from '@/components/graphs/ScatterGraph.vue';
import { graphConfigs } from '../components/citywide-stats/graph-data';

export default defineComponent({
  name: 'CitywideStatsPage',
  components: {
    ScatterGraph,
  },
  data() {
    return {
      graphConfigs: graphConfigs,
    };
  },
});
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
      max-width: 400px;
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
