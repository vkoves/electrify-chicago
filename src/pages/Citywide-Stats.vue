<template>
  <DefaultLayout>
    <h1 class="page-title" tabindex="-1">Citywide Stats</h1>

    <div class="graphs-container">
      <div
        v-for="graph in graphConfigs"
        :key="graph.containerId"
        class="graph-section"
      >
        <h2>{{ graph.title }} ({{ graph.yAxisLabel }})</h2>
        <ScatterGraph
          :data="graph.data"
          :y-axis-label="graph.yAxisLabel"
          :color="graph.color"
          :container-id="graph.containerId"
          :show-grid="true"
        />
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
