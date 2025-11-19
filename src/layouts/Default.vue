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
import GlobalBanner from '../components/GlobalBanner.vue';

/**
 * The default layout
 *
 * Props:
 * - `mainClass` - pass `layout -full-width` to not have a normal width page
 * - `skipBanner` - pass `true` to hide the global banner (e.g., on the Act page)
 */
@Component<any>({
  components: {
    AppFooter,
    AppHeader,
    MetaInfoPanel,
    GlobalBanner,
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
  @Prop({ default: false }) skipBanner?: boolean;

  get isDevelopment(): boolean {
    return process.env.NODE_ENV === 'development';
  }
}
</script>

<template>
  <div>
    <MetaInfoPanel v-if="isDevelopment" />

    <div :class="mainClass || 'layout'">
      <AppHeader />

      <!-- Global Banner - Can be skipped with skipBanner prop -->
      <GlobalBanner v-if="!skipBanner" />

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
