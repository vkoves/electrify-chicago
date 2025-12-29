<template>
  <!-- We're not showing a global banner right now, but I'm leaving the structure here for any
   future ones-->

  <!-- Make sure the banner doesn't show in printed pages, e.g. buildings -->
  <!-- <div class="global-banner no-print">
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
  </div> -->
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

<style lang="scss">
  /**
 * Global banner - notice panel for important announcements and calls to action
 */
.global-banner {
  position: relative;
  background: $blue-very-dark;
  padding: 1rem 0;
  box-shadow: 0 0.3125rem 0.25rem $box-shadow-main;
  width: 100%;
  z-index: 1;

  // Add margin and border-radius for non-full-width layouts
  .layout:not(.-full-width) & {
    margin: 0 1rem 2rem;
    border-radius: $brd-rad-medium;
    width: calc(100% - 2rem);
  }

  .page-constrained {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 2rem;
  }

  .content-left {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex-grow: 1;
  }

  h2 {
    color: $white;
    font-size: 1.25rem;
    margin: 0;
  }

  p {
    color: $white;
    font-size: 0.875rem;
  }

  a {
    background-color: $white;
    padding: 0.5rem 1.25rem;
    border-radius: $brd-rad-small;
    text-align: center;
    text-decoration: none;
    font-weight: bold;
    font-size: 0.9rem;

    &:focus {
      outline-color: $white;
    }
    &:hover,
    &:focus {
      background-color: $off-white;
    }
  }

  /** Mobile styling */
  @media (max-width: $mobile-max-width) {
    padding: 0.75rem 0;
    text-align: center;

    .page-constrained {
      gap: 0.5rem;
      flex-direction: column;
    }

    h2 {
      font-size: 1rem;
    }

    a {
      padding: 0.3125rem 1rem;
      font-size: 0.85rem;
    }

    p {
      font-size: 0.75rem;
    }
  }
}
</style>
