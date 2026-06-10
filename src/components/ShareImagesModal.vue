<template>
  <Popup class="share-images-modal" @close="close()">
    <div class="header">
      <img src="/icons/share.svg" alt="" />
      <h1 autofocus>Share Images</h1>
    </div>

    <div class="modal-body">
      <p class="intro">
        Preview the social images for {{ propertyName }}. Use the arrows to step
        through each slide.
      </p>

      <div ref="previewFrame" class="preview-frame">
        <div
          class="preview-scaler"
          :style="{ transform: `scale(${previewScale})` }"
        >
          <BuildingSocialSquare
            :building="building"
            :stats="stats"
            :slide-number="currentSlide"
          />
        </div>
      </div>

      <div class="slide-nav">
        <button
          class="nav-btn"
          :disabled="currentSlide <= 1 || isDownloading"
          @click="prevSlide"
        >
          <img src="/icons/arrow-back.svg" alt="" />
          Prev
        </button>
        <span class="slide-counter"
          >Slide {{ currentSlide }} of {{ SlideCount }}</span
        >
        <button
          class="nav-btn"
          :disabled="currentSlide >= SlideCount || isDownloading"
          @click="nextSlide"
        >
          Next
          <img src="/icons/arrow-next.svg" alt="" />
        </button>
      </div>

      <div class="download-actions">
        <button
          class="download-btn"
          :disabled="isDownloading"
          @click="downloadCurrentSlide"
        >
          {{
            isDownloading && downloadMode === 'single'
              ? 'Downloading…'
              : `Download Slide ${currentSlide}`
          }}
        </button>
        <button
          class="download-btn -all"
          :disabled="isDownloading"
          @click="downloadAllSlides"
        >
          {{
            isDownloading && downloadMode === 'all'
              ? `Downloading ${downloadProgress} / ${SlideCount}…`
              : 'Download All'
          }}
        </button>
      </div>
    </div>

    <!--
      Hidden, off-screen render of the social square at native 1080px used
      to capture clean export images regardless of the visible preview's
      scaled-down size. Slide number is set right before each capture.
    -->
    <div ref="captureContainer" class="capture-container" aria-hidden="true">
      <BuildingSocialSquare
        ref="captureSquare"
        :building="building"
        :stats="stats"
        :slide-number="captureSlide"
      />
    </div>
  </Popup>
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue } from 'vue-property-decorator';
import Popup from './layout/Popup.vue';
import BuildingSocialSquare from './BuildingSocialSquare.vue';
import { IBuilding, IBuildingBenchmarkStats } from '../common-functions.vue';
import { downloadBlob, elementToPngBlob } from '../download-helpers.vue';

type DownloadMode = 'idle' | 'single' | 'all';

/**
 * Modal that previews a deck of Instagram-ready square images for a building,
 * with controls to step through the slides.
 */
@Component({
  components: {
    BuildingSocialSquare,
    Popup,
  },
})
export default class ShareImagesModal extends Vue {
  @Prop({ required: true }) building!: IBuilding;
  @Prop({ required: true }) stats!: IBuildingBenchmarkStats;

  readonly SlideCount: number = BuildingSocialSquare.SlideCount;

  /** Native pixel size of the social square (matches Instagram square spec) */
  private readonly SourceSizePx = 1080;

  currentSlide = 1;

  /** Which slide the hidden capture container is currently rendering */
  captureSlide = 1;

  /** Scale factor from source 1080px square down to preview frame width */
  previewScale = 1;

  /** Tracks which download flow (if any) is in flight */
  downloadMode: DownloadMode = 'idle';

  /** When in 'all' mode, how many slides have completed downloading */
  downloadProgress = 0;

  private resizeObserver?: ResizeObserver;

  get isDownloading(): boolean {
    return this.downloadMode !== 'idle';
  }

  get propertyName(): string {
    return this.building.PropertyName || this.building.Address;
  }

  mounted(): void {
    const frame = this.$refs.previewFrame as HTMLElement | undefined;
    if (!frame || typeof ResizeObserver === 'undefined') {
      return;
    }

    const updateScale = (): void => {
      this.previewScale = frame.clientWidth / this.SourceSizePx;
    };

    updateScale();
    this.resizeObserver = new ResizeObserver(updateScale);
    this.resizeObserver.observe(frame);
  }

  beforeDestroy(): void {
    this.resizeObserver?.disconnect();
  }

  prevSlide(): void {
    if (this.currentSlide > 1) {
      this.currentSlide -= 1;
    }
  }

  nextSlide(): void {
    if (this.currentSlide < this.SlideCount) {
      this.currentSlide += 1;
    }
  }

  /** Filename-safe slug derived from the building's name/address */
  private get buildingSlug(): string {
    const raw =
      this.building.PropertyName || this.building.Address || 'building';
    return (
      raw
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '') || 'building'
    );
  }

  private slideFilename(slideNumber: number): string {
    return `electrify-chicago-${this.buildingSlug}-slide-${slideNumber}.png`;
  }

  /**
   * Render the hidden capture square at the given slide and return a PNG blob.
   * Slide changes are awaited via $nextTick so Vue has flushed the new content
   * before html-to-image reads the DOM.
   */
  private async renderSlideToBlob(slideNumber: number): Promise<Blob> {
    this.captureSlide = slideNumber;
    await this.$nextTick();

    const captureComp = this.$refs.captureSquare as Vue | undefined;
    const el = captureComp?.$el as HTMLElement | undefined;
    if (!el) {
      throw new Error('Capture element not found');
    }
    return elementToPngBlob(el);
  }

  async downloadCurrentSlide(): Promise<void> {
    if (this.isDownloading) return;
    this.downloadMode = 'single';
    try {
      const blob = await this.renderSlideToBlob(this.currentSlide);
      downloadBlob(blob, this.slideFilename(this.currentSlide));
    } catch (error) {
      console.error('Failed to download slide', error);
    } finally {
      this.downloadMode = 'idle';
    }
  }

  async downloadAllSlides(): Promise<void> {
    if (this.isDownloading) return;
    this.downloadMode = 'all';
    this.downloadProgress = 0;
    try {
      for (let n = 1; n <= this.SlideCount; n += 1) {
        const blob = await this.renderSlideToBlob(n);
        downloadBlob(blob, this.slideFilename(n));
        this.downloadProgress = n;
        // Small pause so browsers don't drop rapid successive downloads
        await new Promise((resolve) => setTimeout(resolve, 150));
      }
    } catch (error) {
      console.error('Failed to download all slides', error);
    } finally {
      this.downloadMode = 'idle';
      this.downloadProgress = 0;
    }
  }

  @Emit()
  close(): boolean {
    return true;
  }
}
</script>

<style lang="scss">
dialog.share-images-modal {
  .popup-inner {
    max-width: 40rem;
    margin: auto auto;
  }

  .header {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    background-color: $blue-very-dark;
    color: $white;
    padding: 1.25rem 1.5rem;

    h1 {
      margin: 0;
      font-size: 1.5rem;
    }

    img {
      height: 1.75rem;
    }
  }

  .modal-body {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .intro {
    margin: 0;
    font-size: 0.9rem;
    color: $text-light;
  }

  .preview-frame {
    // Square frame at a reasonable preview size; the inner social square
    // is rendered at 1080px and scaled down to fit.
    width: 100%;
    aspect-ratio: 1;
    max-width: 32rem;
    background-color: $off-white;
    border: solid $border-thin $grey;
    border-radius: $brd-rad-small;
    margin: 0 auto;
    overflow: hidden;
    position: relative;
  }

  .preview-scaler {
    // The inner square renders at native 1080px and is scaled down via an
    // inline transform driven by ResizeObserver so it stays pixel-accurate
    // for later export.
    position: absolute;
    inset: 0;
    transform-origin: top left;
    width: 1080px;
    height: 1080px;
  }

  .slide-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;

    .nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background-color: $blue-dark;
      color: $white;
      border: none;
      border-radius: $brd-rad-small;
      padding: 0.5rem 1rem;
      font-weight: bold;
      cursor: pointer;

      img {
        height: 0.875rem;
        width: auto;
        // Arrow icons ship as black fill; invert to render white on the
        // blue button background.
        filter: invert(1);
      }

      &:hover:not(:disabled),
      &:focus:not(:disabled) {
        background-color: $blue-very-dark;
      }

      &:disabled {
        background-color: $grey;
        color: $text-mid-light;
        cursor: not-allowed;

        img {
          // Drop the white invert so the arrow matches the dark disabled text
          filter: none;
          opacity: 0.6;
        }
      }
    }

    .slide-counter {
      font-size: 0.9rem;
      color: $text-mid-light;
    }
  }

  .download-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-top: 0.5rem;
    justify-content: space-between;

    .download-btn {
      flex: 1 1 12rem;
      background-color: $blue-dark;
      color: $white;
      border: none;
      border-radius: $brd-rad-small;
      padding: 0.625rem 1rem;
      font-weight: bold;
      cursor: pointer;

      &:hover:not(:disabled),
      &:focus:not(:disabled) {
        background-color: $blue-very-dark;
      }

      &:disabled {
        background-color: $grey;
        color: $text-mid-light;
        cursor: not-allowed;
      }

      &.-all {
        background-color: $blue-very-dark;

        &:hover:not(:disabled),
        &:focus:not(:disabled) {
          background-color: $link-blue;
        }
      }
    }
  }

  // Off-screen render target for full-resolution image capture. Kept in the
  // DOM (rather than visibility:hidden) so html-to-image can read it.
  .capture-container {
    position: fixed;
    top: 0;
    left: -100000px;
    width: 1080px;
    height: 1080px;
    pointer-events: none;
  }
}
</style>
