<template>
  <div class="ward-lookup">
    <div class="search-container">
      <input
        ref="addressInput"
        type="text"
        placeholder="Enter your Chicago address..."
        class="address-input"
      />
    </div>

    <div v-if="loading" class="loading">
      Searching...
    </div>

    <div v-if="error" class="panel -warning">
      {{ error }}
    </div>

    <div v-if="wardInfo" class="ward-result">
      <h3>Your Alderman</h3>
      <div class="result-content">
        <img
          v-if="alderImagePath"
          :src="alderImagePath"
          :alt="wardInfo.council_member"
          class="alder-photo"
        />
        <div class="ward-info">
          <p class="ward-number">{{ wardInfo.district }}</p>
          <p class="alderman-name">{{ wardInfo.council_member }}</p>

          <div v-if="alderInfo" class="contact-info">
            <p v-if="alderInfo.email" class="email">
              <strong>Email:</strong>
              <a :href="`mailto:${alderInfo.email}`">{{ alderInfo.email }}</a>
            </p>
            <p v-if="alderInfo.officePhone" class="phone">
              <strong>Phone:</strong> {{ alderInfo.officePhone }}
            </p>
          </div>
        </div>
        <div class="actions">
          <g-link v-if="wardPagePath" :to="wardPagePath" class="blue-link">
            View Ward Buildings
          </g-link>
          <a
            :href="`https://chicago.councilmatic.org${wardInfo.detail_link}`"
            target="_blank"
            rel="noopener"
            class="blue-link"
          >
            View Full Profile
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
/* eslint-disable @typescript-eslint/no-explicit-any */
import { Component, Vue } from 'vue-property-decorator';
import booleanPointInPolygon from '@turf/boolean-point-in-polygon';
import { point } from '@turf/helpers';
import { loadGoogleMaps } from '~/google-maps-loader';
import { AlderImages } from '~/components/alder-images.constant.vue';

interface WardProperties {
  district: string;
  council_member: string;
  detail_link: string;
  select_id: string;
}

interface WardFeature {
  type: 'Feature';
  properties: WardProperties;
  geometry: any;
}

interface WardsGeoJSON {
  type: 'FeatureCollection';
  features: WardFeature[];
}

interface AlderInfo {
  name: string;
  office: string;
  officePhone: string;
  email: string;
  website: string;
}

// Chicago city boundaries for biasing Google Places autocomplete results
const CHICAGO_BOUNDS = {
  north: 42.023131,
  south: 41.644286,
  east: -87.523661,
  west: -87.940267,
};

@Component
export default class WardLookup extends Vue {
  public loading = false;
  public error = '';
  public wardInfo: WardProperties | null = null;
  public alderInfo: AlderInfo | null = null;

  private autocomplete: any = null;
  private wardsData: WardsGeoJSON | null = null;
  private aldersData: Map<string, AlderInfo> = new Map();

  /** Get the image path for the current alderman based on ward number */
  get alderImagePath(): string | null {
    if (!this.wardInfo) return null;

    // Extract ward number from district (e.g., "Ward 6" -> "6")
    const wardMatch = this.wardInfo.district.match(/\d+/);
    if (!wardMatch) return null;

    const wardNumber = wardMatch[0];
    const filename = AlderImages[wardNumber];
    return filename ? `/alders/${filename}` : null;
  }

  /** Get the ward page path for the current ward */
  get wardPagePath(): string | null {
    if (!this.wardInfo) return null;

    // Extract ward number from district (e.g., "Ward 6" -> "6")
    const wardMatch = this.wardInfo.district.match(/\d+/);
    if (!wardMatch) return null;

    return `/ward/${wardMatch[0]}`;
  }

  /** Initialize the component by loading all required data */
  async mounted(): Promise<void> {
    await Promise.all([
      this.loadGoogleMaps(),
      this.loadWardsData(),
      this.loadAldersData(),
    ]);
  }

  /** Load Google Maps API and initialize autocomplete */
  private async loadGoogleMaps(): Promise<void> {
    // In Gridsome, client-side env vars must be prefixed with GRIDSOME_
    // Access via process.env which gets compiled at build time
    const apiKey = process.env.GRIDSOME_GOOGLE_MAPS_API_KEY || '';

    if (!apiKey) {
      this.error =
        'Google Maps API key not configured. Please add GRIDSOME_GOOGLE_MAPS_API_KEY ' +
        'to your .env file and restart the dev server.';
      return;
    }

    try {
      // Load Google Maps API
      await loadGoogleMaps(apiKey);

      // Import the places library
      const google = (window as any).google;
      await google.maps.importLibrary('places');

      // Initialize autocomplete on the input
      const input = this.$refs.addressInput as HTMLInputElement;

      this.autocomplete = new google.maps.places.Autocomplete(input, {
        types: ['address'],
        componentRestrictions: { country: 'us' },
        bounds: CHICAGO_BOUNDS,
      });

      // Listen for place selection
      this.autocomplete.addListener('place_changed', () => {
        this.handlePlaceSelected();
      });
    } catch (err) {
      this.error = 'Failed to load Google Maps. Please try again later.';
      console.error('Google Maps loading error:', err);
    }
  }

  /** Load ward boundary GeoJSON data */
  private async loadWardsData(): Promise<void> {
    try {
      const response = await fetch('/chicago-wards-2025.geojson');
      this.wardsData = (await response.json()) as WardsGeoJSON;
    } catch (err) {
      console.error('Failed to load ward boundaries:', err);
    }
  }

  /** Load alderman contact information from CSV */
  private async loadAldersData(): Promise<void> {
    try {
      const response = await fetch('/alders-info.csv');
      const csvText = await response.text();

      // Parse CSV and build a map of ward number -> alder info
      const lines = csvText.split('\n');
      for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        // Simple CSV parsing (handles quoted fields)
        const values = this.parseCSVLine(line);
        if (values.length < 5) continue;

        const office = values[1].trim();
        // Skip non-ward entries (like "Mayor", "Clerk")
        if (!office.match(/^\d+$/)) continue;

        this.aldersData.set(office, {
          name: values[0].replace(/"/g, '').trim(),
          office,
          officePhone: values[2].trim(),
          email: values[4].trim(),
          website: values[5].trim(),
        });
      }
    } catch (err) {
      console.error('Failed to load alderman info:', err);
    }
  }

  /** Parse a CSV line handling quoted fields */
  private parseCSVLine(line: string): string[] {
    const result: string[] = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const char = line[i];

      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        result.push(current);
        current = '';
      } else {
        current += char;
      }
    }
    result.push(current);

    return result;
  }

  /** Handle Google Places autocomplete selection */
  private handlePlaceSelected(): void {
    if (!this.autocomplete) return;

    const place = this.autocomplete.getPlace();

    if (!place.geometry || !place.geometry.location) {
      this.error = 'Please select an address from the dropdown.';
      return;
    }

    const lat = place.geometry.location.lat();
    const lng = place.geometry.location.lng();

    this.findWard(lat, lng);
  }

  /** Find which ward contains the given coordinates */
  private findWard(lat: number, lng: number): void {
    this.loading = true;
    this.error = '';
    this.wardInfo = null;
    this.alderInfo = null;

    if (!this.wardsData) {
      this.error = 'Ward boundary data not loaded. Please refresh the page.';
      this.loading = false;
      return;
    }

    try {
      const searchPoint = point([lng, lat]);

      // Find which ward contains this point
      for (const feature of this.wardsData.features) {
        if (booleanPointInPolygon(searchPoint, feature.geometry)) {
          this.wardInfo = feature.properties;

          // Extract ward number from district (e.g., "Ward 6" -> "6")
          const wardMatch = feature.properties.district.match(/\d+/);
          if (wardMatch) {
            const wardNumber = wardMatch[0];
            // Look up alderman info
            this.alderInfo = this.aldersData.get(wardNumber) || null;
          }

          this.loading = false;
          return;
        }
      }

      // If we get here, the point wasn't in any ward
      this.error =
        'This address does not appear to be in Chicago. Please enter a Chicago address.';
      this.loading = false;
    } catch (err) {
      console.error('Error finding ward:', err);
      this.error = 'An error occurred while finding your ward. Please try again.';
      this.loading = false;
    }
  }
}
</script>

<style lang="scss">
.ward-lookup {
  margin: 2rem 0;

  .search-container {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;

    @media (max-width: $mobile-max-width) {
      flex-direction: column;
    }
  }

  .address-input {
    flex: 1;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border: solid $border-medium $grey;
    border-radius: $brd-rad-small;

    &:focus {
      outline: 0.25rem dashed $blue-very-dark;
      outline-offset: 0.125rem;
      border-color: $blue-dark;
    }
  }

  .search-button {
    padding: 0.75rem 1.5rem;
    background-color: $blue-dark;
    color: $white;
    border: none;
    border-radius: $brd-rad-small;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    white-space: nowrap;

    &:hover,
    &:focus {
      background-color: $blue-very-dark;
    }
  }

  .loading {
    padding: 1rem;
    text-align: center;
    color: $text-mid-light;
    font-style: italic;
  }

  .ward-result {
    margin-top: 1.5rem;
    padding: 1.5rem;
    background: $off-white;
    border: solid $border-medium $chicago-blue;
    border-radius: $brd-rad-medium;

    h3 {
      margin-top: 0;
      margin-bottom: 1rem;
      color: $blue-very-dark;
    }

    .result-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;

      @media (max-width: $mobile-max-width) {
        flex-direction: column;
        align-items: flex-start;
      }
    }

    .alder-photo {
      width: 120px;
      height: 120px;
      border-radius: 50%;
      object-fit: cover;
      border: solid $border-medium $chicago-blue;
      flex-shrink: 0;

      @media (max-width: $mobile-max-width) {
        width: 100px;
        height: 100px;
      }
    }

    .ward-info {
      flex: 1;

      p {
        margin: 0.25rem 0;
      }

      .ward-number {
        font-size: 1.125rem;
        font-weight: bold;
        color: $blue-very-dark;
      }

      .alderman-name {
        font-size: 1rem;
        color: $text-main;
        margin-bottom: 0.75rem;
      }

      .contact-info {
        margin-top: 0.75rem;
        font-size: 0.9rem;

        p {
          margin: 0.5rem 0;
        }

        a {
          color: $link-blue;
          text-decoration: none;

          &:hover,
          &:focus {
            text-decoration: underline;
          }
        }

        .email,
        .phone {
          strong {
            display: inline-block;
            min-width: 4rem;
          }
        }
      }
    }

    .actions {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
      align-items: flex-end;
      flex-shrink: 0;

      @media (max-width: $mobile-max-width) {
        align-items: flex-start;
        width: 100%;
      }

      .blue-link {
        white-space: nowrap;
      }
    }
  }
}
</style>
