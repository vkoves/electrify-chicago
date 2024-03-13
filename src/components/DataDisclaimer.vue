<template>
  <details class="data-disclaimer">
    <summary>
      Note: Data only includes large Chicago buildings from {{ LatestDataYear }},
      unless explicitly stated otherwise.
    </summary>

    <p class="constrained">
      <strong>Note:</strong> This data only includes buildings whose emissions are reported
      under the
      <a
        href="https://www.chicago.gov/city/en/progs/env/building-energy-benchmarking---transparency.html"
        target="_blank"
        rel="noopener"
      >
        Chicago Energy Benchmarking Ordinance<NewTabIcon />
      </a>. According to the City &ldquo;As of 2016,
      this list includes all commercial, institutional, and residential buildings larger than
      50,000 square feet.&rdquo; This dataset is also then filtered to only buildings with
      reported emissions > 1,000 metric tons CO<sub>2</sub> equivalent.
    </p>

    <p class="constrained">
      This data is also from {{ LatestDataYear }}, but when new benchmark data
      is available, we'll update the site.
    </p>
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
  components: {NewTabIcon},
})
export default class DataDisclaimer extends Vue {
  readonly LatestDataYear: number = LatestDataYear;
}
</script>

<style lang="scss">
.data-disclaimer {
  background: $grey;
  border-radius: $brd-rad-medium;
  margin-bottom: 1rem;

  summary, p { padding: 0.5rem 1rem; }

  summary {
    font-weight: bold;
    font-size: 0.825rem;
  }

  p {
    margin-top: 0.5rem;
  }
}
</style>
