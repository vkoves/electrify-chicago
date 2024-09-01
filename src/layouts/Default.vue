<static-query>
  query {
    metadata {
      siteName
    }
  }
</static-query>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import AppFooter from '../components/layout/AppFooter.vue';
import AppHeader from '../components/layout/AppHeader.vue';

@Component({
  components: {
    AppFooter,
    AppHeader,
  },
})
export default class Default extends Vue {

}
</script>

<template>
  <div>
    <div class="layout">
      <AppHeader />

      <!-- The main content -->
      <slot />
    </div>

    <AppFooter />
  </div>
</template>

<style lang="scss">
.layout {
  // Make sure footer is always at the bottom
  min-height: calc(100vh - 10rem);
  max-width: 87.5rem; // 1400px
  margin: 0 auto;
  padding-left: 1rem;
  padding-right: 1rem;
  // Account for <footer> for mobile
  padding-bottom: 5rem;
}

header.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: solid $border-thin $grey;
  padding: 1rem 0;
  gap: 2rem;

  // An off screen anchor link that goes on screen when focused
  .nav-link.skip-to-main {
    position: absolute;
    background: $chicago-blue;
    color: $white;
    border-top: none;
    border-radius: 0 0 $brd-rad-medium $brd-rad-medium;
    padding: 1rem;
    top: -10rem;
    outline-offset: 0.1rem;
    padding: 0.5rem 2rem;

    &:focus { top: 0; }
  }

  .logo-link {
    display: inline-flex;
    flex-shrink: 0;

    .site-logo {
      height: 3rem;
      width: auto;
    }
  }


  .top-nav {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    flex-wrap: wrap;
    padding: 0.5rem 0;
  }

  .nav-link {
    font-weight: bold;
    color: $black;
    text-decoration: none;
    padding: 0.1rem 0.2rem;
    // Increase outline offset to prevent outline from intersecting the blue shadow
    outline-offset: 0.5rem;

    // Style current page link
    &.active--exact {
      box-shadow: 0 0.35rem $chicago-blue;
      text-decoration: none;
    }
  }

  @media (max-width: $mobile-max-width) {
    flex-wrap: wrap;
    margin-top: 0.5rem;
    height: auto;
    gap: 0;

    .logo-link {
      flex-shrink: initial;
      max-width: 22rem;

      .site-logo {
        display: block;
        width: 100%;
        height: auto;
      }
    }

    // Tighten vertical gap
    .top-nav { gap: 1.25rem 1.5rem; }

    form.search-form { width: 100%; }

    nav { margin: 1rem 0; }
  }
}
</style>
