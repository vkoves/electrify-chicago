<template>
  <details class="data-disclaimer">
    <summary>Note: Data From Large Buildings in {{ LatestDataYear }}</summary>

    <div class="details-content">
      <p class="constrained">
        <strong>Note:</strong> This data only includes buildings whose emissions
        are reported under the
        <a
          href="https://www.chicago.gov/city/en/progs/env/building-energy-benchmarking---transparency.html"
          target="_blank"
          rel="noopener"
        >
          Chicago Energy Benchmarking Ordinance<NewTabIcon /> </a
        >. According to the City &ldquo;As of 2016, this list includes all
        commercial, institutional, and residential buildings larger than 50,000
        square feet.&rdquo;
      </p>

      <p class="constrained">
        The latest year of data is from {{ LatestDataYear }}, but we update the
        site regularly when new data is available, and some buildings may have
        failed to report that year, and only have older data available.
      </p>

      <p>
        Additionally, note that all tons specified are <em>metric tons</em>.
      </p>
    </div>
  </details>
</template>

<script lang="ts">
import NewTabIcon from './NewTabIcon.vue';
import { LatestDataYear } from '../constants/globals.vue';
import { Component, Vue } from 'vue-property-decorator';

/**
 * A  tile that can show the stats for a building, including whether it's
 * doing better or worse than average, it's rank and percentile rank
 */

@Component({
  name: 'DataDisclaimer',
  components: { NewTabIcon },
})
export default class DataDisclaimer extends Vue {
  readonly LatestDataYear: number = LatestDataYear;
}
</script>

<style lang="scss">
.data-disclaimer {
  margin-top: 1rem;
  margin-bottom: 1rem;
  font-size: 0.825rem;

  summary,
  .details-content {
    padding: 0.5rem 1rem;
  }

  summary {
    font-weight: bold;
  }

  p {
    margin-top: 0.5em;
  }
}
</style>
