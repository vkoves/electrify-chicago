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
    <div class="page-constrained footer-inner">
      <div class="full-width">
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
          target="_blank"
          rel="noopener"
        >
          <img alt="" src="/github-mark.svg" height="16" />
          Contribute on GitHub
        </a>
      </div>

      <div>
        <a href="https://bsky.app/profile/electrifychicago.net"
          class="bluesky"
          target="_blank"
          rel="noopener">
          <img alt="" src="/bluesky.svg" height="16" />
          Follow Us On Bluesky
        </a>
      </div>

      <div>
        <g-link to="/release-notes/" class="smaller"> Release Notes </g-link>
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

  > .footer-inner {
    display: flex;
    flex-wrap: wrap;
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

  a.github-link, a.bluesky {
    text-decoration: none;
    padding: 0.3125rem 1rem;
    border-radius: $brd-rad-full;
    font-size: 0.825rem;
    line-height: 1;
  }

  a.github-link {
    background-color: $off-white;
    border: none;

    &:hover,
    &:focus {
      background-color: $white;
    }
  }

  a.bluesky {
    background-color: #0886FE; // Bluesky blue
    color: $white;

    &:hover, &:focus {
      background-color: #016cd0;
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
    padding: 1.25rem;

    > .footer-inner {
      gap: 0.8125rem;
    }
  }
}
</style>
