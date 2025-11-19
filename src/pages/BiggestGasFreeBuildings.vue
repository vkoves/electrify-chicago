<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

/**
 * Redirect page for backwards compatibility
 *
 * This page was renamed to "All Electric Buildings" on Aug. 27th, 2025.
 * This redirect ensures old bookmarks and links continue to work.
 */
@Component<any>({
  metaInfo() {
    return {
      title: 'Redirecting to All Electric Buildings',
      meta: [{ 'http-equiv': 'refresh', content: '0; URL=/all-electric' }],
      link: [{ rel: 'canonical', href: '/all-electric' }],
    };
  },
})
export default class BiggestGasFreeBuildings extends Vue {}
</script>

<template>
  <DefaultLayout>
    <div class="redirect-page">
      <h1>Redirecting to All Electric Buildings...</h1>
      <p>
        This page has moved to
        <g-link to="/all-electric">All Electric Buildings</g-link>. You will be
        redirected automatically.
      </p>
    </div>
  </DefaultLayout>
</template>

<style lang="scss" scoped>
.redirect-page {
  text-align: center;
  padding: 4rem 1rem;

  h1 {
    margin-bottom: 1rem;
  }

  p {
    margin-bottom: 0.5rem;
  }
}
</style>
