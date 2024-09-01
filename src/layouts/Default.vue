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
  max-width: 87.5rem; // 1400px
  margin: 0 auto;
  // Account for <footer> for mobile
  padding-bottom: 5rem;

  .main-content {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>
