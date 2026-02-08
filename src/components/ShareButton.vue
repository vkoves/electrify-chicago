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
          <img src="/icons/link.svg" alt="Link" />
          <button
            class="share-link"
            :class="{ '-with-text': showText }"
            @click="dropdownShareUrl()"
          >
          Copy Link
            <!--span v-if="showText">Share</span-->
          </button>
        </li>
        <li>
          <img src="/icons/reddit.svg" alt="Reddit" />
          <a class="share-link" :href="redditShareUrl()" target="_blank" rel="noopener noreferrer">
            Share on Reddit
          </a>
        </li>
        <li>
          <img src="/icons/bluesky.svg" alt="Bluesky" />
          <a class="share-link" :href="blueskyShareUrl()" target="_blank" rel="noopener noreferrer">
            Share on Bluesky
          </a>
        </li>
        <li>
          <img src="/icons/facebook.svg" alt="Facebook" />
          <a class="share-link" :href="facebookShareUrl()" target="_blank" rel="noopener noreferrer">
            Share on Facebook
          </a>
        </li>
        <li>
          <img src="/icons/x.svg" alt="X" />
          <a class="share-link" :href="twitterShareUrl()" target="_blank" rel="noopener noreferrer">
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
  private readonly BlueskyShareEndpoint = 'https://bsky.app/intent/compose';
  private readonly RedditShareEndpoint = 'http://www.reddit.com/submit';

  dropdownShareUrl(): void {
    const shareUrl =
    this.url || (typeof window !== 'undefined' ? window.location.href : '');
    return this.copyToClipboard(shareUrl);
  }

  //TODO: add support for &text= with current page title
  twitterShareUrl(): string {
      const shareUrl =
      this.url || (typeof window !== 'undefined' ? window.location.href : '');
      return `${this.TwitterShareEndpoint}?url=${shareUrl}`;
  }

  // TODO: Tag Electrify Chicago acct?
  blueskyShareUrl(): string {
      const shareUrl =
      this.url || (typeof window !== 'undefined' ? window.location.href : '');
      return `${this.BlueskyShareEndpoint}?text=${this.text}%0A${shareUrl}`;
  }

  facebookShareUrl(): string {
    const shareUrl =
    this.url || (typeof window !== 'undefined' ? window.location.href : '');
    return `${this.FacebookShareEndpoint}?u=${shareUrl}`;
  }

  //TODO: Add support for &title=
  redditShareUrl(): string {
    const shareUrl =
    this.url || (typeof window !== 'undefined' ? window.location.href : '');
    return `${this.RedditShareEndpoint}?url=${shareUrl}&title=${this.text}`;
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
      //this.copyToClipboard(shareUrl);
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
    this.showShareDropdown = true;
    this.shareDropdownVisible = false;

    // Small delay to ensure DOM element is rendered, then trigger fade in
    setTimeout(() => {
      this.shareDropdownVisible = true;
    }, 10);

    //TODO: Replace with function to close dropdown when user clicks
    //      elsewhere on page, or selects a link to share.

    // Start fade out after display duration, then hide completely
    /*setTimeout(() => {
      this.shareDropdownVisible = false;
      // Hide element after animation completes
      setTimeout(() => {
        this.showDropdown = false;
      }, this.AlertFadeDurationMs);
    }, this.AlertDisplayDurationMs);*/
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
    padding: 0.5rem 1.75rem .5rem .5rem;
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

      .share-list {
        list-style: none;
        padding: 0;
        display: grid;
        row-gap: .75rem;

        li {
          display: flex;
          align-items: center;
        }

        .share-link {
          color: $white;
          text-decoration: none;
          margin-inline: .5rem;
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
  }
}
</style>
