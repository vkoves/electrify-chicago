<template>
  <DefaultLayout>
    <div v-if="isDevelopment" class="constrained -wide">
      <h1 id="main-content" tabindex="-1">🖼️ Building Image Uploader</h1>

      <p>
        Upload and process building images with automatic resizing and WebP
        conversion.
      </p>

      <div class="panel -warning text-center">
        <strong>⚠️ Development Only:</strong> Images are saved to
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

          <div class="form-group">
            <label for="address">
              Address <span class="required">*</span>
            </label>
            <input
              id="address"
              v-model="form.address"
              type="text"
              placeholder="e.g. 10 W 31st Street"
              required
            />
            <small class="help-text">
              Street address only (no Chicago IL needed)
            </small>
          </div>

          <div class="form-group">
            <label for="subfolder">Subfolder</label>
            <div class="subfolder-input">
              <select
                id="subfolderSelect"
                v-model="selectedExistingFolder"
                @change="onExistingFolderChange"
              >
                <option value="">Select existing folder...</option>
                <option
                  v-for="folder in existingFolders"
                  :key="folder"
                  :value="folder"
                >
                  {{ folder }}
                </option>
              </select>
              <span class="or-text">or</span>
              <input
                id="subfolder"
                v-model="form.subfolder"
                type="text"
                placeholder="new-folder-name"
                @input="onCustomFolderInput"
              />
            </div>
            <small class="help-text">
              Leave empty to save directly in /manual/
            </small>
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
              <h4>Add to building-images.constant.vue:</h4>
              <pre><code>{{ result.codeSnippet }}</code></pre>
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

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

interface UploadForm {
  buildingId: string;
  address: string;
  subfolder: string;
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
    address: '',
    subfolder: '',
  };

  preview: PreviewData = {
    url: '',
    width: 0,
    height: 0,
    size: 0,
  };

  processing = false;
  results: UploadResult[] = [];
  selectedExistingFolder = '';

  // Known existing subfolders from auto-streetview
  existingFolders = [
    'new-buildings-2023',
    'biggest',
    'cleanest',
    'depaul',
    'iit',
    'uchicago',
  ];

  get isDevelopment(): boolean {
    return (
      process.env.NODE_ENV === 'development' ||
      process.env.GRIDSOME_MODE === 'development' ||
      (typeof window !== 'undefined' &&
        (window.location.hostname === 'localhost' ||
          window.location.hostname === '127.0.0.1'))
    );
  }

  get canSubmit(): boolean {
    return (
      this.form.buildingId.trim() !== '' &&
      this.form.address.trim() !== '' &&
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
    if (!this.form.buildingId || !this.form.address) return '';

    // Create filename: ID-address.webp (e.g. 256419-10_W_31st_Street.webp)
    const cleanAddress = this.form.address
      .replace(/[^\w\s]/g, '') // Remove special characters
      .replace(/\s+/g, '_') // Replace spaces with underscores
      .trim();

    return `${this.form.buildingId}-${cleanAddress}.webp`;
  }

  onExistingFolderChange(): void {
    if (this.selectedExistingFolder) {
      this.form.subfolder = this.selectedExistingFolder;
    }
  }

  onCustomFolderInput(): void {
    // Clear the dropdown selection when typing custom folder
    this.selectedExistingFolder = '';
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
      const subfolder = this.form.subfolder.trim();
      const filename = this.generatedFilename;
      const relativePath = subfolder
        ? `manual/${subfolder}/${filename}`
        : `manual/${filename}`;

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
  fromGoogleMaps: false,
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
    this.form = { buildingId: '', address: '', subfolder: '' };
    this.selectedExistingFolder = '';
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

.subfolder-input {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;

  select,
  input {
    flex: 1;
    min-width: 150px;
  }

  .or-text {
    color: $text-mid-light;
    font-weight: 600;
    white-space: nowrap;
  }

  @media (max-width: $mobile-max-width) {
    flex-direction: column;
    align-items: stretch;

    .or-text {
      text-align: center;
      margin: 0.5rem 0;
    }
  }
}

.required {
  color: $chicago-red;
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
