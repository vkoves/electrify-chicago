<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NewTabIcon from '~/components/NewTabIcon.vue';
import WardLookup from '~/components/WardLookup.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
    WardLookup,
    BuildingsHero,
  },
  metaInfo() {
    return generatePageMeta(
      'Buildings By Ward',
      'Browse Chicago buildings organized by ward - find energy performance ' +
        'data for your neighborhood!',
    );
  },
})
export default class Wards extends Vue {
  /** The ward numbers, 1 - 50 */
  wards = [
    ...Array(50)
      .fill(0)
      .map((e, i) => i + 1),
  ];
}
</script>

<!-- If this query is updated, make sure to update PageSocialCard as well -->
<template>
  <DefaultLayout main-class="layout -full-width">
    <div class="wards-page">
      <BuildingsHero :buildings="[]">
        <div class="layout-constrained">
          <h1 id="main-content" tabindex="-1">Buildings By Ward</h1>

          <p class="subtitle">
            Looking for the buildings in a specific Chicago aldermanic ward?
            Just find your ward in the list below!
          </p>
        </div>
      </BuildingsHero>

      <div class="layout-constrained -padded">
        <section class="ward-lookup-section">
          <h2>Don't Know Your Ward?</h2>
          <p>Enter your address to find your ward and alder</p>
          <WardLookup :show-contact-info="false" />
        </section>

        <ol>
          <li v-for="ward in wards" :key="ward">
            <g-link class="grey-link" :to="`/ward/${ward}`">
              Ward {{ ward }}
            </g-link>
          </li>
        </ol>
      </div>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.wards-page {
  h1 {
    margin-bottom: 0;
  }

  .subtitle {
    margin-top: 0;
  }

  .ward-lookup-section {
    margin: 2rem 0;
    padding: 2rem;
    background: $off-white;
    border: solid $border-medium $chicago-blue;
    border-radius: $brd-rad-medium;

    h2 {
      margin-top: 0;
      color: $blue-very-dark;
    }

    p {
      margin-bottom: 1rem;
    }
  }

  ol {
    display: grid;
    gap: 1.5rem 1rem;
    grid-template-columns: repeat(auto-fit, minmax(8rem, 1fr));
    list-style: none;
    margin-top: 2rem;
    padding: 0;

    li {
      text-align: center;
      font-weight: 500;

      a {
        padding: 0.5rem 1rem;
      }
    }
  }

  @media (max-width: $mobile-max-width) {
    .ward-lookup-section {
      padding: 1rem;
    }
  }
}
</style>
