<template>
  <DefaultLayout>
    <div class="social-cards-debug">
      <h1>Social Cards Debug Page</h1>
      <p>This page is for testing and debugging social card generation.</p>

      <div class="test-cards">
        <h2>Test Buildings</h2>

        <div class="card-grid">
          <div class="test-card">
            <h3>Crown Hall (Has Image)</h3>
            <p><strong>ID:</strong> 256419</p>
            <p>Illinois Institute of Technology building with architectural image</p>
            <div class="links">
              <a :href="`/social-card/256419`" target="_blank" class="btn">
                View Social Card
              </a>
              <a :href="`/building-id/256419`" target="_blank" class="btn -secondary">
                View Building Page
              </a>
            </div>
          </div>

          <div class="test-card">
            <h3>Marina Towers (Long Title & Vert. Image)</h3>
            <p><strong>ID:</strong> 239096</p>
            <p>Iconic Chicago residential towers with distinctive architecture</p>
            <div class="links">
              <a :href="`/social-card/239096`" target="_blank" class="btn">
                View Social Card
              </a>
              <a :href="`/building-id/239096`" target="_blank" class="btn -secondary">
                View Building Page
              </a>
            </div>
          </div>

          <div class="test-card">
            <h3>445 W Erie (No Image)</h3>
            <p><strong>ID:</strong> 257000</p>
            <p>Building without image to test text-only layout</p>
            <div class="links">
              <a :href="`/social-card/257000`" target="_blank" class="btn">
                View Social Card
              </a>
              <a :href="`/building-id/257000`" target="_blank" class="btn -secondary">
                View Building Page
              </a>
            </div>
          </div>

          <div class="test-card">
            <h3>Merchandise Mart (good energy mix graph)</h3>
            <p><strong>ID:</strong> 103656</p>
            <p>Has a pretty three slice energy mix</p>
            <div class="links">
              <a :href="`/social-card/103656`" target="_blank" class="btn">
                View Social Card
              </a>
              <a :href="`/building-id/103656`" target="_blank" class="btn -secondary">
                View Building Page
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

/**
 * TODO: Add this to footer in local dev
 */
@Component<any>({
  metaInfo() {
    return {
      title: 'Social Cards Debug',
      meta: [
        { name: 'robots', content: 'noindex, nofollow' }, // Don't index debug page
      ],
    }
  },
})
export default class SocialCards extends Vue {}
</script>

<style lang="scss" scoped>
.social-cards-debug {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  color: #1a472a;
  margin-bottom: 1rem;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.test-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;

  h3 {
    margin: 0 0 1rem 0;
    color: #1a472a;
  }

  p {
    margin: 0.5rem 0;
    color: #666;
  }
}

.links {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #1a472a;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.2s;

  &:hover {
    background: #2d5a3d;
  }

  &.-secondary {
    background: #6b7280;

    &:hover {
      background: #4b5563;
    }
  }
}

.instructions {
  margin-top: 3rem;
  padding: 2rem;
  background: #f0f9ff;
  border: 1px solid #0ea5e9;
  border-radius: 12px;

  h2, h3 {
    color: #0c4a6e;
  }

  code {
    background: #e0e7ff;
    padding: 0.125rem 0.375rem;
    border-radius: 4px;
    font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
    font-size: 0.875rem;
  }

  ol, ul {
    margin: 1rem 0;
    padding-left: 1.5rem;
  }

  li {
    margin: 0.5rem 0;
  }
}
</style>