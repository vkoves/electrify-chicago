<template>
  <div class="data-update-banner">
    <div class="page-constrained">
      <div class="content-left">
        <h2>📣 Take Action to Improve Emissions Reporting!</h2>
        <p>
          <strong>$35 million</strong> is already lost from unenforced fines,
          help Chicago not lose any more.
        </p>
      </div>
      <g-link to="/act"> Contact Your Alderperson </g-link>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

/**
 * Banner promoting the Take Action page
 * Displays a call-to-action encouraging users to contact their alderperson
 */
@Component({})
export default class TakeActionBanner extends Vue {}
</script>
