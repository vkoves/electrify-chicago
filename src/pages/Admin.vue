<template>
  <DefaultLayout>
    <div v-if="isDevelopment" class="constrained -wide">
      <h1 id="main-content" tabindex="-1">🔧 Admin Tools</h1>

      <p>Development-only admin interface for managing Electrify Chicago.</p>

      <div class="panel -warning text-center">
        <strong>⚠️ Local Development Only:</strong> This page is not available
        in production builds.
      </div>

      <section>
        <h2>🖼️ Social Media & Images</h2>
        <div class="admin-grid">
          <div class="admin-card">
            <h3>Social Cards Debug</h3>
            <p>
              Test and debug social media card generation for building pages.
            </p>
            <g-link to="/social-cards" class="button -primary"
              >Open Social Cards</g-link
            >
          </div>

          <div class="admin-card">
            <h3>Building Image Uploader</h3>
            <p>
              Upload, review, and manage building images with auto-processing.
            </p>
            <g-link to="/building-image-uploader" class="button -primary"
              >Open Uploader</g-link
            >
          </div>
        </div>
      </section>

      <section>
        <h2>📊 Data Management</h2>
        <div class="admin-grid">
          <div class="admin-card -coming-soon">
            <h3>Data Import</h3>
            <p>
              Import new Chicago Energy Benchmarking data and process building
              information.
            </p>
            <button class="button" disabled>Coming Soon</button>
          </div>

          <div class="admin-card -coming-soon">
            <h3>Building Data Editor</h3>
            <p>Edit building names, addresses, and custom information.</p>
            <button class="button" disabled>Coming Soon</button>
          </div>
        </div>
      </section>

      <section>
        <h3>🚀 Quick Links</h3>
        <div class="quick-links">
          <g-link to="/" class="grey-link">← Back to Site</g-link>
          <g-link to="/latest-updates" class="grey-link">Latest Updates</g-link>
          <g-link to="/biggest-buildings" class="grey-link"
            >Biggest Buildings</g-link
          >
          <a
            href="http://localhost:8080/__graphql"
            target="_blank"
            class="grey-link"
          >
            GraphQL Explorer ↗
          </a>
        </div>
      </section>
    </div>

    <!-- Production warning -->
    <div v-else class="constrained text-center">
      <h1>🚫 Access Denied</h1>
      <p>Admin tools are only available during local development.</p>
      <g-link to="/" class="button -primary">← Return to Home</g-link>
    </div>
  </DefaultLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component<any>({
  metaInfo() {
    return {
      title: 'Admin Tools',
      meta: [{ name: 'robots', content: 'noindex, nofollow' }],
    };
  },
})
export default class Admin extends Vue {
  get isDevelopment(): boolean {
    return (
      process.env.NODE_ENV === 'development' ||
      process.env.GRIDSOME_MODE === 'development' ||
      (typeof window !== 'undefined' &&
        (window.location.hostname === 'localhost' ||
          window.location.hostname === '127.0.0.1'))
    );
  }
}
</script>

<style lang="scss" scoped>
@import '../scss/global';

// Removed - using existing .panel -warning class instead

.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.admin-card {
  padding: 1.5rem;
  border: $border-thin solid $grey-light;
  border-radius: $brd-rad-medium;
  background-color: $white;

  h3 {
    margin-bottom: 0.5rem;
  }

  &.-coming-soon {
    opacity: 0.7;
    background-color: $grey-light;
  }
}

.quick-links {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

@media (max-width: $mobile-max-width) {
  .admin-grid {
    grid-template-columns: 1fr;
  }

  .quick-links {
    flex-direction: column;
    align-items: center;
  }
}
</style>
