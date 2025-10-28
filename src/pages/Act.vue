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
        'your alderman about funding an inspector position.',
    );
  },
})
export default class Act extends Vue {}
</script>

<template>
  <DefaultLayout>
    <div class="act-page layout-constrained">
      <div class="header-with-share">
        <div>
          <h1 id="main-content" tabindex="-1">
            Take Action to Get Chicago Buildings Reporting Their Energy Use
          </h1>
          <p class="subtitle">
            Large Chicago buildings are using tons of energy, and a 2014 law
            requires them to submit data to the city, but many haven't been
            complying, and haven't gotten the fines they're supposed to.
          </p>
        </div>
        <ShareButton
          title="Take Action - Contact Your Alderman"
          text="Support enforcement of Chicago's Building Energy Benchmarking Ordinance
            by contacting your alderman about funding an inspector position."
          :show-text="true"
        />
      </div>

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
        Department of Environment. But they cannot enforce it without a staff
        member in the position of "Inspector."
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

      <h2>How You Can Help - Contact Your Alderman</h2>

      <ol class="action-steps">
        <li>
          <strong>Find your alderman</strong> by entering your address below:

          <WardLookup />
        </li>

        <li>
          <strong>Contact them</strong> via email, phone, or in person at a ward
          meeting
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
            title="Take Action - Contact Your Alderman"
            text="Support enforcement of Chicago's Building Energy Benchmarking Ordinance
              by contacting your alderman about funding an inspector position."
            :show-text="true"
          />
        </li>
      </ol>

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
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.act-page {
  .header-with-share {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;

    .share-button-container {
      flex-shrink: 0;
    }
  }

  h1 {
    margin-bottom: 0;
  }

  .subtitle {
    font-size: 1.25rem;
    font-weight: 500;
    margin-top: 0;
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

  @media (max-width: $mobile-max-width) {
    .header-with-share {
      flex-direction: column;
      align-items: flex-start;
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
