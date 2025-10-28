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
        <div class="ward-info">
          <p class="ward-number">{{ wardInfo.district }}</p>
          <p class="alderman-name">{{ wardInfo.council_member }}</p>
        </div>
        <a
          :href="`https://chicago.councilmatic.org${wardInfo.detail_link}`"
          target="_blank"
          rel="noopener"
          class="blue-link"
        >
          View Profile & Contact Info
        </a>
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

// Chicago city boundaries for biasing Google Places autocomplete results
const CHICAGO_BOUNDS = {
  north: 42.023131,
  south: 41.644286,
  east: -87.523661,
  west: -87.940267,
};

@Component
export default class WardLookup extends Vue {
  loading = false;
  error = '';
  wardInfo: WardProperties | null = null;

  private autocomplete: any = null;
  private wardsData: WardsGeoJSON | null = null;

  async mounted(): Promise<void> {
    await this.loadGoogleMaps();
    await this.loadWardsData();
  }

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

  private async loadWardsData(): Promise<void> {
    try {
      const response = await fetch('/chicago-wards-2025.geojson');
      this.wardsData = (await response.json()) as WardsGeoJSON;
    } catch (err) {
      console.error('Failed to load ward boundaries:', err);
    }
  }

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

  private findWard(lat: number, lng: number): void {
    this.loading = true;
    this.error = '';
    this.wardInfo = null;

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
      }
    }

    .blue-link {
      flex-shrink: 0;
    }
  }
}
</style>
