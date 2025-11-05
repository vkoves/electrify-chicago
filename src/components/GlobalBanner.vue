<template>
  <div v-show="shouldShow" class="global-banner">
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
import { Component, Prop, Vue } from 'vue-property-decorator';

/**
 * Global banner for site-wide announcements and calls to action
 *
 * Currently displays a call-to-action encouraging users to contact their alderperson
 * for our /act page
 */
@Component({})
export default class GlobalBanner extends Vue {
  /** Array of paths where the banner should be hidden */
  @Prop({ default: () => [] })
  hideOnPaths!: string[];

  /** Whether to show the banner on the current page */
  get shouldShow(): boolean {
    // During SSR or before mount, check if we're on a Gridsome static page
    if (typeof window === 'undefined') {
      // During SSR, default to showing (will be handled client-side)
      return true;
    }

    // In the browser, use the actual current path
    const currentPath = window.location.pathname;
    return !this.hideOnPaths.includes(currentPath);
  }
}
</script>
