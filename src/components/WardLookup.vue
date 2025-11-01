<template>
  <div class="ward-lookup">
    <div class="search-container">
      <label for="ward-lookup-addr">Your Chicago Address</label>
      <input
        id="ward-lookup-addr"
        ref="addressInput"
        type="text"
        placeholder="1060 W. Addison St..."
        class="address-input"
      />
    </div>

    <div v-if="loading" class="loading">Searching...</div>

    <div v-if="error" class="panel -warning">
      {{ error }}
    </div>

    <transition name="slide-fade" mode="out-in">
      <div v-if="wardInfo" :key="wardInfo.district" class="ward-result">
        <h3>Your Ward & Alderperson</h3>
        <div class="result-content">
          <img
            v-if="alderImagePath"
            :src="alderImagePath"
            :alt="alderFormattedName"
            class="alder-photo"
          />
          <div class="ward-info">
            <p class="ward-number">{{ wardInfo.district }}</p>
            <p class="alder-name">{{ alderFormattedName }}</p>

            <div v-if="alderInfo && showContactInfo" class="contact-info">
              <p v-if="alderInfo.email" class="email">
                <strong>Email:&nbsp;</strong>
                <a :href="`mailto:${alderInfo.email}`">{{ alderInfo.email }}</a>
              </p>
              <p v-if="alderInfo.officePhone" class="phone">
                <strong>Phone:&nbsp;</strong>
                <span>{{ alderInfo.officePhone }}</span>
              </p>
            </div>

            <div v-if="!showEmailCta" class="actions">
              <div class="action-links">
                <g-link
                  v-if="wardPagePath"
                  :to="wardPagePath"
                  class="blue-link"
                >
                  View Ward Buildings
                </g-link>
                <a
                  :href="`https://chicago.councilmatic.org${wardInfo.detail_link}`"
                  target="_blank"
                  rel="noopener"
                  class="grey-link"
                >
                  Full Profile On Councilmatic
                  <NewTabIcon />
                </a>
              </div>
            </div>
          </div>
        </div>

        <div v-if="showEmailCta" class="actions-full-width">
          <button
            v-if="alderInfo && alderInfo.email"
            class="email-cta"
            @click="handleEmailClick"
          >
            Email Alderperson {{ alderLastName }}
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script lang="ts">
/* eslint-disable @typescript-eslint/no-explicit-any */
import { Component, Prop, Vue } from 'vue-property-decorator';
import booleanPointInPolygon from '@turf/boolean-point-in-polygon';
import { point } from '@turf/helpers';
import { loadGoogleMaps } from '~/google-maps-loader.vue';
import { AlderImages } from '~/components/alder-images.constant.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import {
  loadAldersData,
  loadWardBoundaries,
  formatAlderName,
  AlderInfo,
  WardProperties,
  WardsGeoJSON,
} from '~/utils/alder-data.vue';

// Chicago city boundaries for biasing Google Places autocomplete results
const CHICAGO_BOUNDS = {
  north: 42.023131,
  south: 41.644286,
  east: -87.523661,
  west: -87.940267,
};

/**
 * Ward lookup component that allows users to find their ward by address
 * or displays ward info if an initial ward number is provided.
 *
 * @fires ward-found - Emitted when a ward is found (either via address
 *   lookup or initial ward prop). Passes WardProperties object containing
 *   the ward's council member name and related information.
 * @fires email-alder - Emitted when user clicks the email button.
 *   Passes the alderperson's email and last name.
 */
@Component({
  components: {
    NewTabIcon,
  },
})
export default class WardLookup extends Vue {
  /** Whether to show contact information (email/phone) */
  @Prop({ default: true })
  showContactInfo!: boolean;

  /** Whether to show a large "Email Your Alder" CTA button */
  @Prop({ default: false })
  showEmailCta!: boolean;

  /** Optional initial ward number to display on load */
  @Prop({ default: null })
  initialWard!: string | null;

  public loading = false;
  public error = '';
  public wardInfo: WardProperties | null = null;
  public alderInfo: AlderInfo | null = null;

  private autocomplete: any = null;
  private wardsData: WardsGeoJSON | null = null;
  private aldersData: Map<string, AlderInfo> = new Map();

  /** Get the image path for the current alder based on ward number */
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

  /** Format alder name from "Last, First" to "First Last" */
  get alderFormattedName(): string | null {
    if (!this.wardInfo) return null;
    return formatAlderName(this.wardInfo.council_member);
  }

  /** Get just the alder's last name */
  get alderLastName(): string | null {
    if (!this.wardInfo) return null;

    const name = this.wardInfo.council_member;
    // Extract last name (first part before comma)
    const parts = name.split(',').map((part) => part.trim());
    if (parts.length >= 1) {
      return parts[0];
    }
    return name; // Return as-is if format is unexpected
  }

  /** Check if the user is on a mobile device */
  get isMobile(): boolean {
    if (typeof window === 'undefined') return false;
    return window.innerWidth <= 768;
  }

  /** Handle email button click - emit event for desktop, open mailto for mobile */
  handleEmailClick(): void {
    if (!this.alderInfo) return;

    if (this.isMobile) {
      // On mobile, use mailto link to open email app with prefilled content
      const subject = encodeURIComponent(
        'Supporting An Inspector to Enforce Energy Benchmarking',
      );
      const body = encodeURIComponent(
        `Alderperson ${this.alderLastName},\n\n` +
          `I'm writing to ask you to support an inspector position to enforce Chicago's Building Energy Use Benchmarking Ordinance.\n\n` +
          `In 2013, Chicago passed the first-in-the-nation Building Energy Use Benchmarking Ordinance. It requires buildings over 50,000 square feet to annually report energy usage data.\n\n` +
          `But the city has never enforced that ordinance.\n\n` +
          `According to Electrify Chicago (https://electrifychicago.net/fines-breakdown), over a 6-year period starting in 2018, Chicago failed to collect over $35 million in fines for buildings that didn't comply with the reporting requirement. That is, on average, nearly $6 million in uncollected fines every year. And compliance is decreasing.\n\n` +
          `Starting January 1, 2025, authority over the ordinance shifted from the Department of Business Affairs and Consumer Protection to the Department of Environment. But they cannot enforce it without a staff member in the position of "Inspector."\n\n` +
          `Climate Reality Project's Chicago Metro Chapter advocates including funding in the city's 2026 budget to hire an inspector who can enforce the benchmarking ordinance.\n\n` +
          `Since an inspector's salary would be only a small fraction of the nearly $6 million in potential fines they could collect annually, we expect it to be a cost-neutral or, more likely, net revenue-generating expenditure in coming years. Enforcing the ordinance would also increase accountability and support voluntary climate action in buildings.\n\n` +
          `Your constituent,\n\n`,
      );
      window.location.href = `mailto:${this.alderInfo.email}?subject=${subject}&body=${body}`;
    } else {
      // On desktop, emit event for parent to show modal
      this.$emit('email-alder', {
        email: this.alderInfo.email,
        lastName: this.alderLastName,
      });
    }
  }

  /** Initialize the component by loading all required data */
  async mounted(): Promise<void> {
    await Promise.all([
      this.loadGoogleMaps(),
      this.loadWardBoundaries(),
      this.loadAldersData(),
    ]);

    // If initial ward is provided, look it up
    if (this.initialWard) {
      this.loadWardByNumber(this.initialWard);
    }
  }

  /** Load Google Maps API and initialize autocomplete */
  private async loadGoogleMaps(): Promise<void> {
    // In Gridsome, client-side env vars must be prefixed with GRIDSOME_
    // Access via process.env which gets compiled at build time
    // eslint-disable-next-line no-undef
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

  /** Load ward boundary GeoJSON data using shared utility */
  private async loadWardBoundaries(): Promise<void> {
    this.wardsData = await loadWardBoundaries();
  }

  /** Load alder contact information from CSV using shared utility */
  private async loadAldersData(): Promise<void> {
    this.aldersData = await loadAldersData();
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

  /** Load ward information by ward number */
  private loadWardByNumber(wardNumber: string): void {
    if (!this.wardsData) {
      this.error = 'Ward boundary data not loaded. Please refresh the page.';
      return;
    }

    // Find the ward with the matching number
    for (const feature of this.wardsData.features) {
      const wardMatch = feature.properties.district.match(/\d+/);
      if (wardMatch && wardMatch[0] === wardNumber) {
        this.wardInfo = feature.properties;
        this.alderInfo = this.aldersData.get(wardNumber) || null;
        // Emit event when ward is found
        this.$emit('ward-found', this.wardInfo);
        return;
      }
    }

    // Ward not found
    this.error = `Ward ${wardNumber} not found.`;
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
            // Look up alder info
            this.alderInfo = this.aldersData.get(wardNumber) || null;
          }

          this.loading = false;
          // Emit event when ward is found
          this.$emit('ward-found', this.wardInfo);
          return;
        }
      }

      // If we get here, the point wasn't in any ward
      this.error =
        'This address does not appear to be in Chicago. Please enter a Chicago address.';
      this.loading = false;
    } catch (err) {
      console.error('Error finding ward:', err);
      this.error =
        'An error occurred while finding your ward. Please try again.';
      this.loading = false;
    }
  }
}
</script>

<style lang="scss">
.ward-lookup {
  .search-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1rem;

    label {
      font-size: 0.8125rem;
    }
    label,
    input {
      font-weight: 500;
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
        margin: 0;
      }

      .ward-number {
        font-size: 1.125rem;
        font-weight: bold;
        color: $blue-very-dark;
      }

      .alder-name {
        font-size: 1.25rem;
        color: $text-main;
        font-weight: bold;
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
          font-weight: 500;

          strong {
            display: inline-block;
            min-width: 3.5rem;
          }
        }
      }

      .actions {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-top: 1.5rem;

        .action-links {
          display: flex;
          gap: 1rem;
          flex-wrap: wrap;

          @media (max-width: $mobile-max-width) {
            flex-direction: column;
          }

          .blue-link,
          .grey-link {
            white-space: nowrap;
          }

          .blue-link {
            flex: 1;
          }

          .grey-link {
            display: inline-flex;
            align-items: center;
            color: $link-blue;
            gap: 0.5rem;
            font-weight: bold;
          }
        }
      }
    }

    .actions-full-width {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      margin-top: 1.5rem;

      .email-cta {
        display: block;
        padding: 0.5rem;
        max-width: 20rem;
        background: $blue-dark;
        color: $white;
        text-align: center;
        text-decoration: none;
        font-size: 1.25rem;
        font-weight: bold;
        border: none;
        border-radius: $brd-rad-small;
        transition: background 0.2s ease;
        cursor: pointer;

        &:hover,
        &:focus {
          background: $blue-very-dark;
          color: $white;
        }
      }

      .secondary-links {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;

        .grey-link {
          display: inline-flex;
          align-items: center;
          color: $text-light;
          gap: 0.25rem;
          text-decoration: none;
          font-weight: normal;

          &:hover,
          &:focus {
            text-decoration: underline;
            color: $link-blue;
          }
        }
      }
    }
  }
}
</style>
