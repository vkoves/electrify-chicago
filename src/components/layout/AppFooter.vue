<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

/**
 * Site Wide Footer
 */
@Component({
  name: 'AppFooter',
})
export default class AppFooter extends Vue {}
</script>

<template>
  <footer>
    <div class="constrained">
      <div>
        Created with <span class="heart">&#x2764;</span> by
        <a
          href="https://github.com/vkoves/electrify-chicago/graphs/contributors"
          >volunteers</a
        >
        in Chicago
      </div>

      <div>
        <a
          href="https://github.com/vkoves/electrify-chicago"
          class="github-link"
        >
          <img alt="" src="/github-mark.svg" width="16" />
          Contribute to Electrify Chicago on GitHub
        </a>
      </div>
    </div>
  </footer>
</template>

<style lang="scss">
footer {
  width: 100%;
  text-align: center;
  padding: 2rem 0;
  background-color: $grey;

  > .constrained {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: auto;
    gap: 2rem;
  }

  a {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: $text-main;
    font-weight: 600;
  }

  a.github-link {
    text-decoration: none;
    padding: 0.25rem 0.5rem;
    border-radius: 1rem;
    background-color: $off-white;
    border: none;
    font-size: 0.825rem;

    &:hover,
    &:focus {
      background-color: $white;
    }
  }

  .heart {
    font-size: 1.5rem;
    vertical-align: -0.1rem;
    color: $chicago-red;
    line-height: 0;
    margin: 0 0.125rem;
  }

  @media (max-width: $mobile-max-width) {
    position: static;
  }
}
</style>
