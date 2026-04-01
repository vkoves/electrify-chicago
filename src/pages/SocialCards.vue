<template>
  <DefaultLayout>
    <div class="social-cards-debug page-constrained">
      <h1>Social Cards Debug Page</h1>
      <p>This page is for testing and debugging social card generation.</p>

      <div class="test-cards">
        <h2>Test Buildings</h2>

        <div class="card-grid">
          <div class="test-card">
            <h3>Crown Hall (Has Image)</h3>
            <p><strong>ID:</strong> 256419</p>
            <p>
              Illinois Institute of Technology building with architectural image
            </p>
            <div class="links">
              <a
                :href="`/social-card/256419`"
                target="_blank"
                class="grey-link"
              >
                View Social Card
              </a>
              <a
                :href="`/building-id/256419`"
                target="_blank"
                class="grey-link -secondary"
              >
                View Building Page
              </a>
            </div>
          </div>

          <div class="test-card">
            <h3>Marina Towers (Long Title & Vert. Image)</h3>
            <p><strong>ID:</strong> 239096</p>
            <p>
              Iconic Chicago residential towers with distinctive architecture
            </p>
            <div class="links">
              <a
                :href="`/social-card/239096`"
                target="_blank"
                class="grey-link"
              >
                View Social Card
              </a>
              <a
                :href="`/building-id/239096`"
                target="_blank"
                class="grey-link -secondary"
              >
                View Building Page
              </a>
            </div>
          </div>

          <div class="test-card">
            <h3>445 W Erie (No Image)</h3>
            <p><strong>ID:</strong> 257000</p>
            <p>Building without image to test text-only layout</p>
            <div class="links">
              <a
                :href="`/social-card/257000`"
                target="_blank"
                class="grey-link"
              >
                View Social Card
              </a>
              <a
                :href="`/building-id/257000`"
                target="_blank"
                class="grey-link -secondary"
              >
                View Building Page
              </a>
            </div>
          </div>

          <div class="test-card">
            <h3>Merchandise Mart (good energy mix graph)</h3>
            <p><strong>ID:</strong> 103656</p>
            <p>Has a pretty three slice energy mix</p>
            <div class="links">
              <a
                :href="`/social-card/103656`"
                target="_blank"
                class="grey-link"
              >
                View Social Card
              </a>
              <a
                :href="`/building-id/103656`"
                target="_blank"
                class="grey-link -secondary"
              >
                View Building Page
              </a>
            </div>
          </div>
        </div>
      </div>

      <div class="test-pages">
        <h2>Test Page Social Cards</h2>

        <div class="card-grid">
          <div
            v-for="pageConfig in pageConfigs"
            :key="pageConfig.id"
            class="test-card"
          >
            <h3>{{ pageConfig.title }}</h3>
            <p><strong>ID:</strong> {{ pageConfig.id }}</p>
            <p>{{ pageConfig.description }}</p>
            <div class="links">
              <a
                :href="`/page-social-card/${pageConfig.id}`"
                target="_blank"
                class="grey-link"
              >
                View Social Card
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import {
  pageSocialConfigs,
  type IPageSocialConfig,
} from '../constants/page-social-images/page-social-configs.vue';

/**
 * TODO: Add this to footer in local dev
 */
/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  metaInfo() {
    return {
      title: 'Social Cards Debug',
      meta: [
        { name: 'robots', content: 'noindex, nofollow' }, // Don't index debug page
      ],
    };
  },
})
export default class SocialCards extends Vue {
  /** Get all page social configurations for the template */
  get pageConfigs(): IPageSocialConfig[] {
    return Object.values(pageSocialConfigs);
  }
}
</script>

<style lang="scss" scoped>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.test-card {
  background: $off-white;
  border: $border-thin solid $grey-dark;
  border-radius: 1rem;
  padding: 1.5rem;

  h3 {
    margin-top: 0;
  }
}

.links {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;

  .grey-link {
    font-weight: bold;

    &:not(.-secondary) {
      color: $white;
      background-color: $blue-dark;

      &:focus,
      &:hover {
        background-color: $blue-very-dark;
      }
    }
  }
}
</style>
