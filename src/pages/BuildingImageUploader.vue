<template>
  <DefaultLayout>
    <div v-if="isDevelopment" class="constrained -wide">
      <h1 id="main-content" tabindex="-1">🖼️ Building Image Uploader</h1>

      <p>
        Upload and process building images with automatic resizing and WebP
        conversion.
      </p>

      <div class="panel -warning text-center">
        <strong>⚠️ Manual Process:</strong> Images are downloaded to your
        Downloads folder. You must manually move them to
        static/building-imgs/manual/
      </div>

      <!-- Upload Form -->
      <section>
        <h2>Upload New Building Image</h2>

        <form class="upload-form" @submit.prevent="handleUpload">
          <div class="form-group">
            <label for="buildingId">
              Building ID <span class="required">*</span>
            </label>
            <input
              id="buildingId"
              v-model="form.buildingId"
              type="text"
              placeholder="e.g. 256419"
              required
              pattern="[0-9]+"
              title="Building ID must be numeric"
            />
          </div>

          <!-- Building Info Display -->
          <div v-if="selectedBuilding" class="building-info">
            <h3>Building Found:</h3>
            <div class="building-details">
              <p>
                <strong>Name:</strong>
                {{ selectedBuilding.PropertyName || '[No Name Available]' }}
              </p>
              <p><strong>Address:</strong> {{ selectedBuilding.Address }}</p>
              <p>
                <strong>Type:</strong>
                {{ selectedBuilding.PrimaryPropertyType }}
              </p>
              <p v-if="selectedBuilding.YearBuilt">
                <strong>Year Built:</strong> {{ selectedBuilding.YearBuilt }}
              </p>
            </div>
          </div>

          <div
            v-else-if="form.buildingId && !selectedBuilding"
            class="building-not-found"
          >
            <p>⚠️ Building ID "{{ form.buildingId }}" not found in database</p>
          </div>

          <div class="form-group">
            <label for="imageFile">
              Image File <span class="required">*</span>
            </label>
            <input
              id="imageFile"
              ref="fileInput"
              type="file"
              accept="image/*"
              required
              @change="handleFileSelect"
            />
            <small class="help-text">
              Accepts PNG, JPG, WebP. Will be auto-resized and converted to
              WebP.
            </small>
          </div>

          <!-- Image Preview -->
          <div v-if="preview.url" class="preview-section">
            <h3>Preview</h3>
            <div class="preview-container">
              <img
                :src="preview.url"
                :alt="`Preview for building ${form.buildingId}`"
                class="preview-image"
              />
              <div class="preview-info">
                <p>
                  <strong>Original:</strong> {{ preview.width }}×{{
                    preview.height
                  }}px
                </p>
                <p>
                  <strong>Will resize to:</strong> {{ targetWidth }}×{{
                    targetHeight
                  }}px ({{ isPortrait ? 'Portrait' : 'Landscape' }})
                </p>
                <p>
                  <strong>File size:</strong> {{ formatFileSize(preview.size) }}
                </p>
                <p><strong>Filename:</strong> {{ generatedFilename }}</p>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button
              type="submit"
              class="button -primary"
              :disabled="processing || !canSubmit"
            >
              {{ processing ? 'Processing...' : 'Upload & Process Image' }}
            </button>
            <button type="button" class="button" @click="resetForm">
              Reset Form
            </button>
          </div>
        </form>
      </section>

      <!-- Results -->
      <section v-if="results.length > 0">
        <h2>Recent Uploads</h2>
        <div class="results-list">
          <div
            v-for="result in results"
            :key="result.timestamp"
            class="result-item"
            :class="{ '-error': result.error }"
          >
            <div class="result-info">
              <strong>Building ID:</strong> {{ result.buildingId }}<br />
              <strong>Path:</strong> {{ result.path }}<br />
              <strong>Status:</strong> {{ result.error ? 'Error' : 'Success' }}
              <div v-if="result.error" class="error-message">
                {{ result.error }}
              </div>
              <div v-if="!result.error" class="success-details">
                {{ result.dimensions }} • {{ result.fileSize }}
              </div>
            </div>
            <div
              v-if="!result.error && result.codeSnippet"
              class="code-snippet"
            >
              <h4>Next Steps:</h4>
              <ol class="next-steps">
                <li>
                  Move the downloaded file to: <code>{{ result.path }}</code>
                </li>
                <li>
                  Add this code to building-images.constant.vue:

                  <pre><code>{{ result.codeSnippet }}</code></pre>
                </li>
                <li>
                  <g-link :to="`/building-id/${result.buildingId}`"
                    >View Building Page</g-link
                  >
                  (to confirm image displays correctly)
                </li>
              </ol>
              <button
                class="button -small"
                @click="copyToClipboard(result.codeSnippet)"
              >
                Copy Code
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Quick Links -->
      <section>
        <h3>🚀 Quick Links</h3>
        <div class="quick-links">
          <g-link to="/admin" class="grey-link">← Back to Admin</g-link>
          <g-link to="/social-cards" class="grey-link"
            >Social Cards Debug</g-link
          >
          <a
            href="/static/building-imgs/manual/"
            target="_blank"
            class="grey-link"
          >
            View Manual Folder ↗
          </a>
        </div>
      </section>
    </div>

    <!-- Production warning -->
    <div v-else class="constrained text-center">
      <h1>🚫 Access Denied</h1>
      <p>Building Image Uploader is only available during local development.</p>
      <g-link to="/" class="button -primary">← Return to Home</g-link>
    </div>
  </DefaultLayout>
</template>

<static-query>
  query {
    allBuilding {
      edges {
        node {
          ID
          PropertyName
          Address
          PrimaryPropertyType
          YearBuilt
        }
      }
    }
  }
</static-query>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IBuilding } from '../common-functions.vue';

interface UploadForm {
  buildingId: string;
}

interface PreviewData {
  url: string;
  width: number;
  height: number;
  size: number;
}

interface UploadResult {
  timestamp: number;
  buildingId: string;
  path: string;
  error?: string;
  dimensions?: string;
  fileSize?: string;
  codeSnippet?: string;
}

@Component<any>({
  metaInfo() {
    return {
      title: 'Building Image Uploader',
      meta: [{ name: 'robots', content: 'noindex, nofollow' }],
    };
  },
})
export default class BuildingImageUploader extends Vue {
  form: UploadForm = {
    buildingId: '',
  };

  /** Set by Gridsome to results of GraphQL query */
  readonly $static!: {
    allBuilding: { edges: Array<{ node: IBuilding }> };
  };

  preview: PreviewData = {
    url: '',
    width: 0,
    height: 0,
    size: 0,
  };

  processing = false;
  results: UploadResult[] = [];

  get isDevelopment(): boolean {
    return (
      process.env.NODE_ENV === 'development' ||
      process.env.GRIDSOME_MODE === 'development' ||
      (typeof window !== 'undefined' &&
        (window.location.hostname === 'localhost' ||
          window.location.hostname === '127.0.0.1'))
    );
  }

  get selectedBuilding(): IBuilding | null {
    if (!this.form.buildingId.trim() || !this.$static?.allBuilding) return null;

    const building = this.$static.allBuilding.edges.find(
      (edge) => edge.node.ID.toString() === this.form.buildingId.trim(),
    );

    return building ? building.node : null;
  }

  get canSubmit(): boolean {
    return (
      this.form.buildingId.trim() !== '' &&
      this.selectedBuilding !== null &&
      this.preview.url !== ''
    );
  }

  get isPortrait(): boolean {
    return this.preview.height > this.preview.width;
  }

  get targetWidth(): number {
    return this.isPortrait ? 600 : 1000;
  }

  get targetHeight(): number {
    if (this.preview.width === 0) return 0;
    return Math.floor(
      (this.preview.height * this.targetWidth) / this.preview.width,
    );
  }

  get generatedFilename(): string {
    if (!this.form.buildingId || !this.selectedBuilding) return '';

    // Create filename: ID-address.webp (e.g. 256419-10_W_31st_Street.webp) and remove
    // characters
    const cleanAddress = this.selectedBuilding.Address.replace(/[^\w\s]/g, '')
      .replace(/\s+/g, '_') // Replace spaces with underscores
      .trim();

    return `${this.form.buildingId}-${cleanAddress}.webp`;
  }

  handleFileSelect(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file) {
      this.clearPreview();
      return;
    }

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        this.preview = {
          url: e.target?.result as string,
          width: img.width,
          height: img.height,
          size: file.size,
        };
      };
      img.src = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }

  async handleUpload(): Promise<void> {
    if (!this.canSubmit) return;

    this.processing = true;

    try {
      const fileInput = this.$refs.fileInput as HTMLInputElement;
      const file = fileInput.files?.[0];

      if (!file) {
        throw new Error('No file selected');
      }

      // Process image
      const processedBlob = await this.processImage(file);

      // Create path
      const filename = this.generatedFilename;
      const relativePath = `manual/${filename}`;

      const result: UploadResult = {
        timestamp: Date.now(),
        buildingId: this.form.buildingId,
        path: `static/building-imgs/${relativePath}`,
        dimensions: `${this.targetWidth}×${this.targetHeight}px`,
        fileSize: this.formatFileSize(processedBlob.size),
        codeSnippet: this.generateCodeSnippet(
          this.form.buildingId,
          relativePath,
        ),
      };

      // Download the processed image
      this.downloadBlob(processedBlob, filename);

      this.results.unshift(result);
      this.resetForm();
    } catch (error) {
      this.results.unshift({
        timestamp: Date.now(),
        buildingId: this.form.buildingId,
        path: '',
        error:
          error instanceof Error ? error.message : 'Unknown error occurred',
      });
    } finally {
      this.processing = false;
    }
  }

  async processImage(file: File): Promise<Blob> {
    return new Promise((resolve, reject) => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();

      img.onload = () => {
        canvas.width = this.targetWidth;
        canvas.height = this.targetHeight;

        if (ctx) {
          ctx.drawImage(img, 0, 0, this.targetWidth, this.targetHeight);

          canvas.toBlob(
            (blob) => {
              if (blob) {
                resolve(blob);
              } else {
                reject(new Error('Failed to process image'));
              }
            },
            'image/webp',
            0.7,
          );
        } else {
          reject(new Error('Could not get canvas context'));
        }
      };

      img.onerror = () => reject(new Error('Failed to load image'));
      img.src = URL.createObjectURL(file);
    });
  }

  downloadBlob(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  generateCodeSnippet(buildingId: string, relativePath: string): string {
    return `'${buildingId}': {
  imgUrl: BuildingImagesBase + '${relativePath}',
  fromGoogleMaps: true,
},`;
  }

  formatFileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes}B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
  }

  clearPreview(): void {
    this.preview = { url: '', width: 0, height: 0, size: 0 };
  }

  resetForm(): void {
    this.form = { buildingId: '' };
    this.clearPreview();
    const fileInput = this.$refs.fileInput as HTMLInputElement;
    if (fileInput) fileInput.value = '';
  }

  async copyToClipboard(text: string): Promise<void> {
    try {
      await navigator.clipboard.writeText(text);
      // Could add a toast notification here
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../scss/global';

.upload-form {
  background-color: $off-white;
  padding: 2rem;
  border-radius: $brd-rad-medium;
  margin-bottom: 2rem;
}

.panel.-warning {
  margin-top: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;

  label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: $blue-dark;
  }

  input[type='text'],
  input[type='file'],
  select {
    width: 100%;
    max-width: 400px;
    padding: 0.75rem;
    border: $border-thin solid $grey-light;
    border-radius: $brd-rad-small;
    font-size: 1rem;

    &:focus {
      outline: none;
      border-color: $blue-dark;
    }
  }

  .help-text {
    display: block;
    margin-top: 0.25rem;
    color: $text-mid-light;
    font-size: 0.9rem;
  }
}

.required {
  color: $chicago-red;
}

.building-info {
  background-color: $off-white;
  border: $border-thin solid $green;
  border-radius: $brd-rad-medium;
  padding: 1.5rem;
  margin: 1rem 0;

  h3 {
    color: $green;
    margin-bottom: 1rem;
  }

  .building-details {
    p {
      margin-bottom: 0.5rem;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

.building-not-found {
  background-color: $concern-very-bad-background;
  border: $border-thin solid $red;
  border-radius: $brd-rad-medium;
  padding: 1rem;
  margin: 1rem 0;

  p {
    color: $chicago-red;
    font-weight: 600;
    margin: 0;
  }
}

.preview-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background-color: $white;
  border-radius: $brd-rad-medium;
  border: $border-thin solid $grey-light;

  h3 {
    margin-bottom: 1rem;
  }
}

.preview-container {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 1.5rem;
  align-items: start;

  @media (max-width: $mobile-max-width) {
    grid-template-columns: 1fr;
  }
}

.preview-image {
  max-width: 200px;
  max-height: 150px;
  border-radius: $brd-rad-small;
  border: $border-thin solid $grey-light;
}

.preview-info {
  font-size: 0.9rem;
  color: $text-mid-light;

  p {
    margin-bottom: 0.25rem;
  }
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;

  @media (max-width: $mobile-max-width) {
    flex-direction: column;
  }
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.result-item {
  padding: 1.5rem;
  background-color: $off-white;
  border-radius: $brd-rad-medium;
  border: $border-thin solid $grey-light;

  &.-error {
    background-color: $concern-very-bad-background;
    border-color: $red;
  }
}

.error-message {
  color: $chicago-red;
  font-weight: 600;
  margin-top: 0.5rem;
}

.success-details {
  color: $green;
  font-weight: 600;
  margin-top: 0.5rem;
}

.code-snippet {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: $border-thin solid $grey-light;

  h4 {
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
  }

  pre {
    background-color: $grey-light;
    padding: 1rem;
    border-radius: $brd-rad-small;
    overflow-x: auto;
    font-size: 0.8rem;
    margin-bottom: 0.5rem;
  }

  .button.-small {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
  }

  .next-steps {
    margin: 1rem 0;

    li {
      margin-bottom: 0.5rem;
    }

    code {
      background-color: $grey-light;
      padding: 0.2rem 0.4rem;
      border-radius: $brd-rad-small;
      font-size: 0.8rem;
    }
  }
}

.quick-links {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;

  @media (max-width: $mobile-max-width) {
    flex-direction: column;
    align-items: center;
  }
}
</style>
