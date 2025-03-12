<static-query>
  query {
    metadata {
      siteName
    }
  }
</static-query>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import AppFooter from '../components/layout/AppFooter.vue';
import AppHeader from '../components/layout/AppHeader.vue';

/**
 * The default layout
 *
 * Accepts a `mainClass` - pass `layout -full-width` to not have a normal width page
 */
@Component<any>({
  components: {
    AppFooter,
    AppHeader,
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
}
</script>

<template>
  <div>
    <div :class="mainClass || 'layout'">
      <AppHeader />

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
