<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NewTabIcon from '~/components/NewTabIcon.vue';
import ShareButton from '~/components/ShareButton.vue';
import WardLookup from '~/components/WardLookup.vue';
import EmailModal from '~/components/EmailModal.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';
import { AlderEmailContent } from '../constants/alder-email-content.constant.vue';

/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    EmailModal,
    NewTabIcon,
    ShareButton,
    WardLookup,
  },
  metaInfo() {
    return generatePageMeta(
      'act',
      'Take Action to Get Chicago Buildings Reporting Their Energy Use',
      "Support enforcement of Chicago's Building Energy Benchmarking Ordinance by contacting " +
        'your alderperson about funding an inspector position.',
    );
  },
})
export default class Act extends Vue {
  public alderFound = false;
  public initialWard: string | null = null;
  public isEmailModalOpen = false;
  public alderEmail = '';
  public alderLastName = '';

  // Expose constants for template
  readonly emailSubject = AlderEmailContent.subject;
  readonly emailBodyParagraphs = AlderEmailContent.bodyParagraphs;

  get emailGreeting(): string {
    return AlderEmailContent.getGreeting(this.alderLastName);
  }

  get emailClosing(): string {
    return AlderEmailContent.getClosing();
  }

  mounted(): void {
    // Check for ward query parameter on mount
    const urlParams = new URLSearchParams(window.location.search);
    const wardParam = urlParams.get('ward');

    if (wardParam) {
      this.initialWard = wardParam;
    }
  }

  /**
   * Get the current page URL without the ward query param for sharing (we don't want to assume
   * the recipient is the same ward)
   */
  get shareUrl(): string {
    if (typeof window === 'undefined') return '';

    return window.location.href.split('?')[0];
  }

  handleWardFound(wardInfo: { district: string }): void {
    this.alderFound = true;

    // Extract ward number from district (e.g., "Ward 6" -> "6")
    const wardMatch = wardInfo.district.match(/\d+/);
    if (wardMatch) {
      const wardNumber = wardMatch[0];
      // Update URL with ward query parameter
      const url = new URL(window.location.href);
      url.searchParams.set('ward', wardNumber);
      window.history.replaceState({}, '', url);
    }
  }

  handleEmailAlder(data: { email: string; lastName: string }): void {
    this.alderEmail = data.email;
    this.alderLastName = data.lastName;
    this.isEmailModalOpen = true;
  }
}
</script>

<template>
  <DefaultLayout :skip-banner="true">
    <div class="act-page content-constrained">
      <div class="page-grid">
        <div class="main-col">
          <div class="act-hero">
            <img
              srcset="
                /blog/contact-your-alder-2025/hunter-uc-still-500p.webp  500w,
                /blog/contact-your-alder-2025/hunter-uc-still.webp      1920w
              "
              sizes="(max-width: 768px) 500px, 1920px"
              src="/blog/contact-your-alder-2025/hunter-uc-still.webp"
              alt="Hunter at United Center"
            />
            <div class="hero-overlay">
              <h1 id="main-content" tabindex="-1">
                <span class="large">Email Your Alder</span> <br />
                To Get Chicago Buildings To Report Their Energy Use
              </h1>
            </div>
          </div>

          <p class="subtitle">
            Many of Chicago's largest buildings are ignoring a 2013 city law
            that requires them to report their energy usage,
            <em>with no accountability</em>. So far the city has missed out on
            <strong>$35 million in unrealized fines</strong>.
          </p>

          <p class="subtitle">
            Contact your alder and tell them enough is enough - let's collect
            those fines, and get buildings reporting!
          </p>
        </div>

        <section class="actions-col">
          <h3>Contact Your Alderperson</h3>
          <p>
            Enter your address to find your alderperson's contact information
          </p>

          <WardLookup
            :show-email-cta="true"
            :initial-ward="initialWard"
            @ward-found="handleWardFound"
            @email-alder="handleEmailAlder"
          />

          <transition name="slide-fade" mode="out-in">
            <div v-if="alderFound" class="additional-steps">
              <h2>Reached Out To Your Alder? Tell Your Friends!</h2>

              <ShareButton
                title="Take Action - Contact Your Alderperson"
                text="Support enforcement of Chicago's Building Energy Benchmarking Ordinance
                  by contacting your alderperson about funding an inspector position."
                :url="shareUrl"
                :show-text="true"
              />
            </div>
          </transition>
        </section>

        <section class="supp-details">
          <h2>
            The Issue: The City Has Failed to Collect $35 Million in Fines
          </h2>

          <p class="constrained">
            About 70% of Chicago's greenhouse gas emissions come from buildings.
            Since 2013, Chicago has had a Building Energy Use Benchmarking
            Ordinance requiring buildings over 50,000 ft² to report energy usage
            annually.
            <strong
              >However, the city has never enforced this ordinance.</strong
            >
          </p>

          <p class="constrained">
            Over a 6-year period starting in 2018, Chicago failed to collect
            over
            <strong>$35 million in fines</strong> (<g-link to="/fines-breakdown"
              >source</g-link
            >) from non-compliant buildings—an average of over $5.5 million in
            uncollected fines every year. And compliance is decreasing.
          </p>

          <h2>The Solution: Hire an Inspector to Enforce Fines!</h2>

          <p class="constrained">
            Starting January 1, 2025, authority over the ordinance shifted to
            the Department of Environment. But they cannot legally enforce it
            without a staff member in the position of "Inspector".
          </p>

          <p class="constrained">
            <strong>
              We need the 2026 city budget to include funding for an inspector
              to enforce the benchmarking ordinance.
            </strong>
            Since an inspector's salary would be only a small fraction of the
            several million dollars in potential fines they could collect
            annually, this would be a net revenue-generating expenditure which
            would also increase accountability and support climate action.
          </p>

          <h2>Learn More</h2>

          <p>
            For more information, see our
            <g-link to="/blog/millions-in-missed-fines">
              analysis of missed fines
            </g-link>
            and the
            <g-link to="/fines-breakdown">year by year fines breakdown</g-link>.
          </p>

          <p class="constrained">
            This advocacy effort is led in partnership with the
            <a
              ref="noopener"
              href="https://climaterealitychicago.com"
              target="_blank"
              >Climate Reality Project's Chicago Metro Chapter</a
            >.

            <a
              ref="noopener"
              href="https://climaterealitychicago.com"
              target="_blank"
              class="climate-reality-logo"
            >
              <img
                src="/partner-logos/climate-reality-dark.webp"
                alt="Climate Reality Chicago"
              />
            </a>
          </p>
        </section>
      </div>

      <email-modal
        v-if="isEmailModalOpen"
        title="Email Your Alderperson"
        :recipient-email="alderEmail"
        :subject="emailSubject"
        @close="isEmailModalOpen = false"
      >
        <p>{{ emailGreeting }}</p>
        <p v-for="(paragraph, index) in emailBodyParagraphs" :key="index">
          {{ paragraph }}
        </p>
        <p>{{ emailClosing }}</p>
      </email-modal>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.act-page {
  .page-grid {
    display: grid;
    grid-template-columns: 1fr 35rem;
    gap: 1rem;
    align-items: start;

    .main-col {
      grid-column: 1;
      grid-row: 1;
    }

    .actions-col {
      grid-column: 2;
      grid-row: 1 / span 2;
    }

    .supp-details {
      grid-column: 1;
      grid-row: 2;
    }
  }

  .act-hero {
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
    border-radius: $brd-rad-medium;

    img {
      width: 100%;
      height: auto;
      display: block;
      filter: brightness(75%);
    }

    .hero-overlay {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(
        to top,
        rgba(0, 0, 0, 0.85) 0%,
        rgba(0, 0, 0, 0.4) 50%,
        transparent 100%
      );
      padding: 3rem 3rem 1rem 3rem;
      color: white;

      h1 {
        margin: 0 0 0.5rem 0;
        font-weight: 500;
        font-size: 1.75rem;
        text-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.5);

        .large {
          font-size: 1.25em;
          font-weight: bold;
        }
      }
    }
  }

  .subtitle {
    font-size: 1.25rem;
    margin: 0;

    + .subtitle {
      margin-top: 1rem;
    }
  }

  .supp-details {
    h2 {
      margin-top: 0;
    }

    .climate-reality-logo {
      display: block;
      width: 20rem;
      margin-top: 1rem;
      padding: 0.5rem;
      border-radius: $brd-rad-medium;
      border: solid $border-thick transparent;
      transition:
        background-color 0.3s,
        border-color 0.3s;

      &:hover,
      &:focus {
        background-color: $off-white;
        border-color: $chicago-blue;
      }
    }
  }

  .actions-col {
    background: $blue-dark;
    border-radius: $brd-rad-medium;
    padding: 2rem;
    box-shadow: 0 0.25rem 0.5rem $box-shadow-main;
    color: $white;

    > h3 {
      margin: 0;
      color: $white;
      font-size: 2rem;
      font-weight: bold;
    }

    > p {
      margin-bottom: 1.5rem;
      font-size: 1.125rem;
    }

    // Override text color for ward lookup results
    .ward-lookup {
      // Override WardLookup focus color for dark background
      input {
        outline-color: $white;
      }

      .ward-result {
        color: $text-main;

        h3 {
          color: $blue-very-dark;
        }
      }

      .panel {
        color: $text-main;
      }
    }

    .additional-steps {
      h3 {
        margin-bottom: 1rem;
        font-size: 1.5rem;
      }

      .share-button-container button {
        border: solid $border-medium $white;
        outline-color: $white;
      }
    }
  }

  .share-button-container {
    text-align: center;
    margin-top: 1rem;
  }

  .announce-panel {
    margin: 1.5rem 0;
  }

  h2 {
    margin-top: 2rem;
  }

  /**
   * Tablet and Mobile Styling - switch to one column layout under 1200px
   */
  @media (max-width: $large-desktop-min-width) {
    .page-grid {
      grid-template-columns: 1fr;
      max-width: 50rem;
      margin: auto;

      .main-col {
        grid-column: 1;
        grid-row: 1;

        .act-hero {
          max-height: 20rem;
        }
      }

      .actions-col {
        grid-column: 1;
        grid-row: 2;
        margin: 1rem 0;
      }

      .supp-details {
        grid-column: 1;
        grid-row: 3;
      }
    }
  }

  /**
  * Mobile Styling
   */
  @media (max-width: $mobile-max-width) {
    .act-hero {
      margin: -1rem -1rem 1rem -1rem;
      border-radius: 0;

      .hero-overlay {
        padding: 1.5rem 1rem 1rem;

        h1 {
          font-size: 1.125rem;
        }
      }
    }

    .subtitle {
      font-size: 1rem;
    }

    .actions-col {
      padding: 1.5rem;

      > h3 {
        font-size: 1.5rem;
      }

      .additional-steps {
        h3 {
          font-size: 1.25rem;
        }
      }
    }

    .share-button-container {
      justify-content: center;
      margin-bottom: 1.5rem;
    }
  }
}
</style>
