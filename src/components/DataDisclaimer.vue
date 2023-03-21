<template>
  <details class="data-disclaimer">
    <summary>Note: Data only includes large Chicago buildings</summary>

    <p class="constrained">
        <strong>Note:</strong> This data only includes buildings whose emissions are reported
        under the Chicago Energy Benchmarking Ordinance. According to the City &ldquo;As of 2016,
        this list includes all commercial, institutional, and residential buildings larger than
        50,000 square feet.&rdquo; This dataset is also then filtered to only buildings with
        reported emissions > 1,000 metric tons.
    </p>
  </details>
</template>

<script>
/**
 * A  tile that can show the stats for a building, including whether it's
 * doing better or worse than average, it's rank and percentile rank
 */
export default {
  name: 'DataDisclaimer',
};
</script>

<style lang="scss">
.data-disclaimer {
  background: $grey;
  border-radius: 0.5rem;
  margin-bottom: 1rem;

  summary, p { padding: 1rem; }

  summary {
    font-weight: bold;
    font-size: 0.825rem;
  }

  p {
    margin: 0;
    padding-top: 0;
  }
}
</style>
