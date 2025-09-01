<template>
  <div class="meta-cont">
    <details class="meta-info-panel page-constrained">
      <summary class="meta-toggle-btn">
        Meta Info (Developer Only)
        <span
          v-if="hasWarning"
          class="warning-icon"
          title="Using default description"
          >⚠️</span
        >
        <span
          v-if="hasCustomImage"
          class="photo-icon"
          title="Custom social image"
          >📷</span
        >
      </summary>

      <div class="meta-info-content">
        <div class="meta-section">
          <h2>Page Meta</h2>
          <div class="meta-item">
            <strong>Title</strong><br />
            {{ pageTitle }}
          </div>
          <div class="meta-item">
            <strong>Description</strong><br />
            {{ pageDescription }}
          </div>
        </div>

        <div v-if="socialImageUrl" class="meta-section">
          <h4>Social Image</h4>
          <img
            :src="socialImageUrl"
            :alt="pageTitle"
            class="social-image-preview"
            @error="onImageError"
          />
          <div class="meta-item">
            <strong>URL:</strong> {{ socialImageUrl }}
          </div>
        </div>

        <div class="meta-section -row">
          <div class="meta-item">
            <g-link to="/social-cards" class="grey-link">
              All Social Cards Debug Page
            </g-link>
          </div>
          <div v-if="specificSocialCardUrl" class="meta-item">
            <a :href="specificSocialCardUrl" class="grey-link" target="_blank">
              This Page's Social Card Page
            </a>
          </div>
        </div>
      </div>
    </details>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

/**
 * Development-only meta information panel component
 *
 * Displays page metadata (title, description, social image) in a collapsible panel
 * at the top of the page during development. Shows visual indicators:
 * - ⚠️ Warning icon for pages using default descriptions (except homepage)
 * - 📷 Photo icon for pages with custom social images
 *
 * Only rendered in development mode via conditional rendering in Default.vue layout.
 * Automatically updates meta info on page navigation with a delay to allow vue-meta
 * to update the DOM.
 */
@Component
export default class MetaInfoPanel extends Vue {
  pageTitle = 'Loading...';
  pageDescription = 'Loading...';
  socialImageUrl: string | null = null;

  mounted(): void {
    // Wait for Vue metadata to update, then re-fetch it
    setTimeout(() => {
      this.updateMetaInfo();
    }, 300);
  }

  get hasWarning(): boolean {
    // Don't show warning on homepage where default description is appropriate
    const isHomepage =
      window.location.pathname === '/' || window.location.pathname === '/index';

    if (isHomepage) {
      return false;
    }

    return (
      this.pageDescription ===
        "Learn about Chicago's most polluting buildings, and why we need to electrify!" ||
      this.pageDescription === 'No description'
    );
  }

  get hasCustomImage(): boolean {
    return (
      this.socialImageUrl !== null &&
      !this.socialImageUrl.includes('social-image.png')
    );
  }

  get specificSocialCardUrl(): string | null {
    const currentPath = window.location.pathname;

    // Building detail pages: /building-id/123456 -> /social-card/123456
    if (currentPath.startsWith('/building/') && this.socialImageUrl) {
      // Grab the ID from the social image, e.g. `/social-images/building-101185.webp` -> `101185`
      const buildingId = this.socialImageUrl.split('building-')[1].split('.webp')[0];

      return `/social-card/${buildingId}`;
    }

    // Owner pages: /owner/depaul -> /owner-social-card/depaul
    if (currentPath.startsWith('/owner/')) {
      const ownerId = currentPath.replace('/owner/', '');
      return `/owner-social-card/${ownerId}`;
    }

    // Page social cards: check if this page has a custom social image
    if (
      this.socialImageUrl &&
      this.socialImageUrl.includes('/social-images/page-')
    ) {
      const match = this.socialImageUrl.match(
        /\/social-images\/page-(.+)\.webp/,
      );
      if (match) {
        const pageId = match[1];
        return `/page-social-card/${pageId}`;
      }
    }

    return null;
  }

  updateMetaInfo(): void {
    this.pageTitle = document?.title || 'No title';

    const descMeta = document?.querySelector(
      'meta[property="description"]',
    ) as HTMLMetaElement;
    const ogDescMeta = document?.querySelector(
      'meta[property="og:description"]',
    ) as HTMLMetaElement;

    this.pageDescription =
      ogDescMeta?.content || descMeta?.content || 'No description';

    const ogImageMeta = document?.querySelector(
      'meta[property="og:image"]',
    ) as HTMLMetaElement;

    this.socialImageUrl = ogImageMeta?.content || null;
  }

  onImageError(): void {
    // eslint-disable-next-line no-console -- Development debugging only
    console.warn('Social image failed to load:', this.socialImageUrl);
  }
}
</script>

<style lang="scss" scoped>
div.meta-cont {
  border-bottom: solid $border-medium $grey-dark;
}

.meta-info-panel {
  background: $white;
}

.meta-toggle-btn {
  width: 100%;
  padding: 0.5rem 0;
  font-size: 0.875rem;
  font-weight: bold;
  background: none;
}

.meta-info-content {
  max-height: 50vh;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.meta-section {
  &.-row {
    display: flex;
    gap: 1rem;
  }

  + .meta-section {
    margin-top: 0.5rem;
  }

  h2 {
    margin: 0;
    font-size: 1.25rem;
  }

  h4 {
    margin: 0 0 0.25rem 0;
    font-size: 1rem;
    color: $blue-dark;
  }
}

.meta-item {
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  word-break: break-word;

  strong {
    color: $off-black;
    margin-right: 0.5rem;
  }
}

.social-image-preview {
  margin-top: 0.5rem;
  max-width: 300px;
  max-height: 150px;
  border: 1px solid $grey-light;
  border-radius: 0.25rem;
  object-fit: contain;
  background: $white;
}

// Add top margin to layout when panel is visible
.meta-info-panel + * {
  margin-top: 0 !important;
}
</style>
