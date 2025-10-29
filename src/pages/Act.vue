<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NewTabIcon from '~/components/NewTabIcon.vue';
import ShareButton from '~/components/ShareButton.vue';
import WardLookup from '~/components/WardLookup.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';

@Component<any>({
  components: {
    NewTabIcon,
    ShareButton,
    WardLookup,
  },
  metaInfo() {
    return generatePageMeta(
      'Take Action to Get Chicago Buildings Reporting Their Energy Use',
      "Support enforcement of Chicago's Building Energy Benchmarking Ordinance by contacting " +
        'your alderperson about funding an inspector position.',
    );
  },
})
export default class Act extends Vue {
  public alderFound = false;

  handleWardFound(): void {
    this.alderFound = true;
  }
}
</script>

<template>
  <DefaultLayout>
    <div class="act-page content-constrained">
      <div class="two-cols">
        <div class="main-col">
          <div class="act-hero">
            <img
              srcset="
                /blog/hunter-united-center-still-500p.webp  500w,
                /blog/hunter-united-center-still.webp      1920w
              "
              sizes="(max-width: 768px) 500px, 1920px"
              src="/blog/hunter-united-center-still.webp"
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
            Many of Chicago's largest buildings are ignoring a 2014 city law
            that requires them to report their energy usage,
            <em>with no accountability</em>. So far the city has missed out on
            <strong>$35 million in unrealized fines</strong>.
          </p>

          <p class="subtitle">
            Contact your alder and tell them enough is enough - let's collect
            those fines, and get buildings reporting!
          </p>
        </div>
        <section class="actions">
          <h3>Contact Your Alderperson</h3>
          <p>Enter your address to find your alderperson's contact information</p>

          <WardLookup @ward-found="handleWardFound" />

          <div v-if="alderFound" class="additional-steps">
            <h3>Next Steps</h3>
            <ol class="action-steps">
              <li>
                <strong>Contact them</strong> via email, phone, or in person at a
                ward meeting
              </li>

              <li>
                <strong>Tell them:</strong>
                <ul>
                  <li>You support enforcing the Energy Benchmarking Ordinance</li>
                  <li>
                    To ensure the 2026 budget include funding for an inspector
                    position in the Department of Environment
                  </li>
                  <li>
                    This will help collect millions in unpaid fines and support
                    Chicago's climate goals by showing how buildings use energy
                  </li>
                </ul>
              </li>

              <li>
                <strong>Share this page</strong> with friends, neighbors, and
                community groups <br />

                <ShareButton
                  title="Take Action - Contact Your Alderperson"
                  text="Support enforcement of Chicago's Building Energy Benchmarking Ordinance
            by contacting your alderperson about funding an inspector position."
                  :show-text="true"
                />
              </li>
            </ol>
          </div>
        </section>
      </div>

      <section>
        <h2>The Issue - $35 Million in Uncollected Fines</h2>

        <p class="constrained">
          About 70% of Chicago's greenhouse gas emissions come from buildings.
          Since 2013, Chicago has had a Building Energy Use Benchmarking Ordinance
          requiring buildings over 50,000 ft² to report energy usage annually.
          <strong>However, the city has never enforced this ordinance.</strong>
        </p>

        <p class="constrained">
          Over a 5-year period starting in 2018, Chicago failed to collect over
          <strong>$35 million in fines</strong> (<g-link to="/fines-breakdown"
            >source</g-link
          >) from non-compliant buildings—an average of $6 million+ in uncollected
          fines every year. And compliance is decreasing.
        </p>

        <h2>The Solution - Hire an Inspector to Enforce Fines!</h2>

        <p class="constrained">
          Starting January 1, 2025, authority over the ordinance shifted to the
          Department of Environment. But they cannot legally enforce it without a
          staff member in the position of "Inspector".
        </p>

        <p class="constrained">
          <strong>
            We need the 2026 city budget to include funding for an inspector to
            enforce the benchmarking ordinance.
          </strong>
          Since an inspector's salary would be only a small fraction of the
          roughly $6 million in potential fines they could collect annually, this
          would likely be a net revenue-generating expenditure while increasing
          accountability and supporting climate action.
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
          This advocacy effort is led in partnership with the Climate Reality
          Project's Chicago Metro Chapter.
        </p>
      </section>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.act-page {
  .two-cols {
    display: flex;
    gap: 1rem;
    align-items: flex-start;

    .main-col {
      flex-basis: 80%;
    }

    .actions {
      flex: 0 0 35rem;
    }
  }

  .act-hero {
    position: relative;
    overflow: hidden;
    margin-bottom: 1.5rem;
    border-radius: $brd-rad-small;

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
      padding: 3rem;
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
  }

  .actions {
    background: $blue-dark;
    border-radius: $brd-rad-medium;
    padding: 2rem;
    box-shadow: 0 0.25rem 0.5rem $box-shadow-main;
    color: $white;

    h3 {
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
      margin-top: 2rem;
      padding-top: 2rem;
      border-top: solid $border-medium rgba(255, 255, 255, 0.3);

      h3 {
        margin-bottom: 1rem;
        font-size: 1.5rem;
      }
    }
  }

  .share-button-container {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
  }

  .announce-panel {
    margin: 1.5rem 0;
  }

  h2 {
    margin-top: 2rem;
  }

  .action-steps {
    font-size: 1.125rem;
    line-height: 1.6;
    padding-left: 1.5rem;

    li {
      margin-bottom: 1rem;
    }

    ul {
      font-size: 1rem;
      margin-top: 0.5rem;
    }
  }

  .iframe-container {
    position: relative;
    width: 100%;
    padding-bottom: 75%;
    margin: 1.5rem 0;
    border: solid $border-thin $grey;
    border-radius: $brd-rad-small;
    overflow: hidden;

    iframe {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border: none;
    }
  }

  /**
   * Tablet and Mobile Styling
   */
  @media (max-width: 72rem) { // 1024px
    .two-cols {
      display: block;

      .main-col,
      .actions {
        flex: none;
        width: 100%;
      }
    }
  }

  @media (max-width: $mobile-max-width) {
    .act-hero {
      margin-bottom: 1rem;

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

    .actions {
      padding: 1.5rem;

      h3 {
        font-size: 1.5rem;
      }

      .additional-steps {
        margin-top: 1.5rem;
        padding-top: 1.5rem;

        h3 {
          font-size: 1.25rem;
        }
      }
    }

    .share-button-container {
      justify-content: center;
      margin-bottom: 1.5rem;
    }

    .action-steps {
      font-size: 1rem;
      padding-left: 1.25rem;
    }

    .iframe-container {
      padding-bottom: 100%;
    }
  }
}
</style>
