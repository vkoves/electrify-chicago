<template>
  <img class="new-tab-icon" src="/new-tab.svg" alt="(opens in a new tab)">
</template>

<script>
/**
 * A  tile that can show the stats for a building, including whether it's
 * doing better or worse than average, it's rank and percentile rank
 */
export default {
  name: 'NewTabIcon',
};
</script>

<style lang="scss">
.new-tab-icon {
  width: 1em;
  height: 1em;
}
</style>
