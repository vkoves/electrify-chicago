<static-query>
  query {
    metadata {
      siteName
    }
  }
</static-query>

<script lang="ts">
/* global process */
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppFooter from '../components/layout/AppFooter.vue';
import AppHeader from '../components/layout/AppHeader.vue';
import MetaInfoPanel from '../components/MetaInfoPanel.vue';
import TakeActionBanner from '../components/TakeActionBanner.vue';

/**
 * The default layout
 *
 * Accepts a `mainClass` - pass `layout -full-width` to not have a normal width page
 */
@Component<any>({
  components: {
    AppFooter,
    AppHeader,
    MetaInfoPanel,
    TakeActionBanner,
  },
  metaInfo() {
    return {
      meta: [
        {
          // Default side wide meta description
          key: 'description',
          name: 'description',
          content:
            "Learn about Chicago's most polluting buildings, and why we need to electrify!",
        },
      ],
    };
  },
})
export default class Default extends Vue {
  @Prop() mainClass?: string;

  get isDevelopment(): boolean {
    return process.env.NODE_ENV === 'development';
  }

  /** Show the Take Action banner on all pages except /act */
  get showTakeActionBanner(): boolean {
    // Check if we're in the browser (not SSR) and not on the /act page
    if (typeof window === 'undefined') return true;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return (this as any).$route?.path !== '/act';
  }
}
</script>

<template>
  <div>
    <MetaInfoPanel v-if="isDevelopment" />

    <div :class="mainClass || 'layout'">
      <AppHeader />

      <!-- Take Action Banner - Show on all pages except /act -->
      <TakeActionBanner v-if="showTakeActionBanner" />

      <div class="main-content">
        <!-- The main content -->
        <slot />
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<style lang="scss">
.layout {
  // Make sure footer is always at the bottom
  min-height: calc(100vh - 10rem);
  // Account for <footer> for mobile
  padding-bottom: 5rem;

  &:not(.-full-width) {
    max-width: $desktop-max-width;
    margin: 0 auto;

    .main-content {
      padding-left: 1rem;
      padding-right: 1rem;
    }
  }

  // On full width pages, have no margin and apply max-width to the header
  &.-full-width header {
    max-width: $desktop-max-width;
    margin: 0 auto;
  }
}
</style>
