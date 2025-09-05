<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component<any>({
  metaInfo: {
    title: 'Page Not Found',
  },
})
export default class NotFound extends Vue {}
</script>

<template>
  <DefaultLayout>
    <div class="layout-constrained not-found-page">
      <div class="error-code">404</div>

      <h1 id="main-content" tabindex="-1">Ope, We Can't Find That Page!</h1>

      <p class="large-text">
        Sorry, the page you're looking for doesn't exist! <br />
      </p>
      <p>You may have followed an outdated link or have mistyped the URL.</p>

      <g-link to="/" class="blue-link"> Go Back to Our Homepage </g-link>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.not-found-page {
  text-align: center;

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

  .blue-link {
    display: inline-block;
    margin-top: 1rem;
    font-size: 1.125rem;
  }
}
</style>
