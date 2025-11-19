<template>
  <!-- Make sure the banner doesn't show in printed pages, e.g. buildings -->
  <div class="global-banner no-print">
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
 * Global banner for site-wide announcements and calls to action
 *
 * Currently displays a call-to-action encouraging users to contact their alderperson
 * for our /act page.
 *
 * Note: Banner visibility is controlled by the parent layout via v-if.
 * Pages can hide the banner by passing :skip-banner="true" to DefaultLayout.
 */
@Component({})
export default class GlobalBanner extends Vue {}
</script>
