<template>
  <div class="share-button-container">
    <button
      class="action-btn -share"
      :class="{ '-with-text': showText }"
      @click="handleShare"
    >
      <span v-if="showText">Share</span>
      <img src="/icons/share.svg" alt="Share" />
    </button>
    <div
      v-show="showCopyAlert"
      class="copy-alert"
      :class="{ show: copyAlertVisible }"
    >
      Link copied to clipboard!
    </div>
    <div
      v-show="showShareDropdown"
      class="share-dropdown"
      :class="{ show: shareDropdownVisible }"
    >
      <ul class="share-list">
        <li>
          <button
            class="share-link"
            :class="{ '-with-text': showText }"
            @click="dropdownShareUrl()"
          >
          <img src="/icons/link.svg" alt="Link" />
          Copy Link
          </button>
        </li>
        <li>
          <a class="share-link" :href="redditShareUrl()" target="_blank" rel="noopener noreferrer">
            <img src="/icons/reddit.svg" alt="Reddit" />
            Share on Reddit
          </a>
        </li>
        <li>
          <a class="share-link" :href="blueskyShareUrl()" target="_blank" rel="noopener noreferrer">
            <img src="/icons/bluesky.svg" alt="Bluesky" />
            Share on Bluesky
          </a>
        </li>
        <li>
          <a class="share-link" :href="linkedinShareUrl()" target="_blank" rel="noopener noreferrer">
            <img src="/icons/linkedin.svg" alt="LinkedIn" />
            Share on LinkedIn
          </a>
        </li>
        <li>
          <a class="share-link" :href="facebookShareUrl()" target="_blank" rel="noopener noreferrer">
            <img src="/icons/facebook.svg" alt="Facebook" />
            Share on Facebook
          </a>
        </li>
        <li>
          <a class="share-link" :href="twitterShareUrl()" target="_blank" rel="noopener noreferrer">
            <img src="/icons/x.svg" alt="X" />
            Share on X
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
/**
 * Reusable share button that uses the native Web Share API when available,
 * with clipboard fallback. Shows a fade-in alert when link is copied.
 */
@Component
export default class ShareButton extends Vue {
  @Prop({ type: String, default: '' })
  title!: string;

  @Prop({ type: String, default: '' })
  text!: string;

  @Prop({ type: String, default: '' })
  url!: string;

  /** Whether to show the word "Share" or (by default) just an icon */
  @Prop({ type: Boolean, default: false })
  showText!: boolean;

  showCopyAlert = false;
  copyAlertVisible = false;

  showShareDropdown = false;
  shareDropdownVisible = false;

  // Animation timing constants
  private readonly AlertFadeDurationMs = 300;
  private readonly AlertDisplayDurationMs = 2500;

  //Share endpoint constants
  private readonly TwitterShareEndpoint = 'https://twitter.com/intent/tweet';
  private readonly FacebookShareEndpoint = 'https://www.facebook.com/sharer/sharer.php';
  private readonly LinkedInShareEndpoint = 'https://www.linkedin.com/feed/'
  private readonly BlueskyShareEndpoint = 'https://bsky.app/intent/compose';
  private readonly RedditShareEndpoint = 'http://www.reddit.com/submit';

  dropdownShareUrl(): void {
    const shareUrl =
    this.url || (typeof window !== 'undefined' ? window.location.href : '');
    return this.copyToClipboard(shareUrl);
  }

  getShareUrl(): string {
    const shareUrl =
    this.url || (typeof window !== 'undefined' ? window.location.href : '');
    return shareUrl;
  }

  linkedinShareUrl(): string {
    return `${this.LinkedInShareEndpoint}?shareActive=true&shareUrl=${encodeURIComponent(this.getShareUrl())}`;
  }

  twitterShareUrl(): string {
    return `${this.TwitterShareEndpoint}?url=${encodeURIComponent(this.getShareUrl())}`;
  }

  blueskyShareUrl(): string {
    return `${this.BlueskyShareEndpoint}?text=${this.text}%0A${encodeURIComponent(this.getShareUrl())}`;
  }

  facebookShareUrl(): string {
    return `${this.FacebookShareEndpoint}?u=${encodeURIComponent(this.getShareUrl())}`;
  }

  redditShareUrl(): string {
    return `${this.RedditShareEndpoint}?url=${encodeURIComponent(this.getShareUrl())}&title=${encodeURI(this.text)}`;
  }

  handleShare(): void {
    const shareUrl =
      this.url || (typeof window !== 'undefined' ? window.location.href : '');

    if (typeof window !== 'undefined' && window.navigator?.share) {
      // Use the Web Share API - a native browser API that allows websites to share content
      // using the device's native sharing mechanisms (e.g., share sheet on mobile devices)
      // Supported on most modern mobile browsers and some desktop browsers
      window.navigator
        .share({
          title: this.title,
          text: this.text,
          url: shareUrl,
        })
        .catch(() => {
          // Fallback: copy to clipboard
          this.copyToClipboard(shareUrl);
        });
    } else {
      // Fallback for browsers without Web Share API
      this.enableDropdown();
    }
  }

  private copyToClipboard(url: string): void {
    if (typeof window !== 'undefined') {
      navigator.clipboard
        .writeText(url)
        .then(() => {
          this.showCopiedAlert();
        })
        .catch(() => {
          // Final fallback - show URL in prompt
          prompt('Copy this link to share:', url);
        });
    }
  }

  private showCopiedAlert(): void {
    this.showCopyAlert = true;
    this.copyAlertVisible = false;

    // Small delay to ensure DOM element is rendered, then trigger fade in
    setTimeout(() => {
      this.copyAlertVisible = true;
    }, 10);

    // Start fade out after display duration, then hide completely
    setTimeout(() => {
      this.copyAlertVisible = false;
      // Hide element after animation completes
      setTimeout(() => {
        this.showCopyAlert = false;
      }, this.AlertFadeDurationMs);
    }, this.AlertDisplayDurationMs);
  }

  private enableDropdown(): void {

    if (this.showShareDropdown) {
      this.shareDropdownVisible = false;

      // Hide element after fade-out animation completes
      setTimeout(() => {
        this.showShareDropdown = false;
      }, this.AlertFadeDurationMs);

      return;
    }

    this.showShareDropdown = true;
    this.shareDropdownVisible = false;

    // Small delay to ensure DOM element is rendered, then trigger fade in
    setTimeout(() => {
      this.shareDropdownVisible = true;
    }, 10);
  }
}

</script>

<style lang="scss">
.share-button-container {
  position: relative;
  display: inline-block;

  .action-btn.-share {
    aspect-ratio: 1;
    padding: 0 0 0.2rem 0.4rem;

    img {
      height: 2rem;
    }

    &.-with-text {
      aspect-ratio: auto;
      padding: 0.5rem 1rem;
      gap: 0.5rem;

      img {
        height: 1.5rem;
      }
    }
  }

  .copy-alert {
    position: absolute;
    top: 100%;
    right: 0;
    margin-top: 0.5rem;
    background-color: $off-black;
    color: $white;
    padding: 0.5rem 0.75rem;
    border-radius: $brd-rad-small;
    font-size: 0.75rem;
    white-space: nowrap;
    z-index: 1000;
    box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.2);
    opacity: 0;
    transform: translateY(-0.5rem);
    transition: all 0.3s ease-in-out;

    &.show {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .share-dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    margin-top: 0.5rem;
    background-color: $blue-very-dark;
    padding: 1.25rem 0;
    border-radius: $brd-rad-small;
    font-size: 1.25rem;
    white-space: nowrap;
    z-index: 999;
    opacity: 0;
    list-style: none;
    transform: translateY(-0.5rem);
    transition: all 0.3s ease-in-out;

    &.show {
      opacity: 1;
      transform: translateY(0);
    }

    .share-list {
      list-style: none;
      padding: 0;
      display: grid;
      margin: 0;
      width: max-content;

      li {
        display: flex;
        align-items: center;
        padding: .5rem 1rem;

        &:hover {
          background: $link-blue;
        }
      }

      .share-link {
        align-items: center;
        color: $white;
        column-gap: 1rem;
        display: flex;
        font-weight: normal;
        outline-color: $white;
        text-decoration: none;
        background: none;
        border-bottom: none;
        font-size: 1rem;
        padding: 0;
      }

      img {
        border-radius: 0;
        width: 1.25rem;
        height: 1.25rem;
      }
    }
  }

  .share-dropdown::before {
    content: '';
    position: absolute;
    bottom: 100%;
    inset-inline-end: 14px;
    border-width: 7px;
    border-style: solid;
    border-color: transparent transparent $blue-very-dark transparent;
  }
}
</style>
