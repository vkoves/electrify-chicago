<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { generatePageSocialMeta } from '../constants/page-social-meta.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return generatePageSocialMeta(
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

<template>
  <DefaultLayout>
    <div class="wards-page layout-constrained">
      <h1 id="main-content" and tabindex="-1">Buildings By Ward</h1>
      <p class="subtitle">
        Looking for the buildings in a specific Chicago aldermanic ward? Just
        find your ward in the list below!
      </p>

      <ol>
        <li v-for="ward in wards" :key="ward">
          <g-link class="grey-link" :to="`/ward/${ward}`">
            Ward {{ ward }}
          </g-link>
        </li>
      </ol>
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
}
</style>
