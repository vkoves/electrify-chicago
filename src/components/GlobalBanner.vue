<template>
  <div v-if="shouldShow" class="global-banner">
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

  /** Track whether to show the banner (reactive) */
  private isVisible = true;

  /** Whether to show the banner on the current page */
  get shouldShow(): boolean {
    return this.isVisible;
  }

  mounted(): void {
    // Check path after mount to ensure we're in the browser
    if (typeof window !== 'undefined') {
      const currentPath = window.location.pathname;
      this.isVisible = !this.hideOnPaths.includes(currentPath);
    }
  }
}
</script>
