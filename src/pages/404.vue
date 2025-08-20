<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component<any>({
  metaInfo: {
    title: 'Page Not Found',
  },
})
export default class NotFound extends Vue {
}
</script>

<template>
  <DefaultLayout>
    <div class="layout-constrained not-found-page">
      <div class="error-code">404</div>

      <h1 id="main-content" tabindex="-1">Ope, We Can't Find That Page!</h1>

      <p class="large-text">
        Sorry, the page you're looking for doesn't exist. It may have been moved,
        deleted, or you may have typed the URL incorrectly.
      </p>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.not-found-page {
  text-align: center;
}

.error-code {
  font-size: 6rem;
  font-weight: bold;
  color: $blue-dark;
  margin: 3rem 0;
  line-height: 1;
  text-align: center;
  text-shadow: 0.25rem 0.25rem 0.125rem $box-shadow-main;

  @media (max-width: $mobile-max-width) {
    font-size: 4rem;
  }
}

</style>