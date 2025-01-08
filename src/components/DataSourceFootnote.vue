<template>
  <p class="footnote">
    Data Source:
    <!-- eslint-disable-next-line max-len -->
    <a
      href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
      target="_blank"
      rel="noopener"
    >
      Chicago Energy Benchmarking Data <NewTabIcon />
    </a>
  </p>
</template>

<script lang="ts">
import NewTabIcon from './NewTabIcon.vue';

/**
 * A common footnote paragraph
 */
export default {
  name: 'DataSourceFootnote',
  components: { NewTabIcon },
};
</script>

<style lang="scss"></style>
