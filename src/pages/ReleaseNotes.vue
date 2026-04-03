<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';

/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return { title: 'Release Notes' };
  },
})
export default class About extends Vue {}
</script>
<template>
  <DefaultLayout>
    <div class="release-notes-page">
      <div class="layout-constrained">
        <h1 id="main-content" tabindex="-1">Release Notes</h1>
      </div>
      
      <div class="layout-constrained">
        <h2>April 3rd, 2026 - Update to Map Geocoding</h2>

        <p>
          We've introduced changes to our data pipeline to correct the geocodes for buildings in our dataset.
          Previously, our <g-link to="/map">Map</g-link> component had been relying on incorrect coordinates being reported from the city's raw data.
          With this update, <b>21029</b> / 28,329 buildings are now visible on the map in their proper locations!
        </p>

      <div class="two-cols">
        <div>
          <a href="/release-notes/2026/geocoding-before.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2026/geocoding-before.webp"
              alt="Map component showing pin of building in incorrect location"
            />
          </a>

          <p class="bold">IIT Map Pins Before</p>
        </div>
        <div>
          <a href="/release-notes/2026/geocoding-after.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2026/geocoding-after.webp"
              alt="Map component showing pin in correct location after data update"
            />
          </a>

          <p class="bold">IIT Map Pins After</p>
        </div>
      </div>
      </div>

      <div class="layout-constrained">
        <h2>March 3rd, 2026 - New Property Type Pages</h2>

        <p>
          We added new property type pages (like
          <g-link to="/property-type/data-center">Data Centers</g-link> or
          <g-link to="/property-type/museums">Museums</g-link>), to make it easy
          to learn more about all properties marked as a certain type!
          Previously, clicking a property type on a building page just took you
          to a filtered search, but now each property type has its own dedicated
          page with critical stats and graphs and images of a sample of those
          buildings.
        </p>

        <p>
          Each property type page now includes a stats panel with total
          emissions, average GHG intensity, total square footage, grade
          distribution, and total energy mix. You can also expand a
          <strong>Trends</strong> section to see graphs of how the buildings in
          that property type have changed over time.
        </p>
      </div>

      <div class="layout-constrained -wide">
        <a href="/release-notes/2026/new-prop-type-page.webp" target="_blank">
          <img
            class="-shadowed"
            src="/release-notes/2026/new-prop-type-page.webp"
            alt="The new Data Centers property type page showing a hero with building photos, a
              stats panel with 7 buildings, 273,034 metric tons total emissions, 83.6 kg CO2e/sqft
              average GHG intensity, 2.6M total square footage, a grade distribution pie chart,
              and a total energy mix pie chart showing 99% electricity"
          />
        </a>
      </div>

      <div class="layout-constrained">
        <h2>
          September 22nd, 2025 - Enhanced Building Owner Pages & Hero Imagery
        </h2>

        <p>
          We made significant improvements to building owner pages to make them
          more compelling and informative. Each owner page now features a hero
          that showcases images of the buildings they own, showing a quick
          preview of some of their properties. We've added this hero imagery to
          other pages, like our <g-link to="/all-electric">all electric</g-link>
          page!
        </p>

        <p>
          Building owner pages now also include additional statistics and graphs
          to help you better understand each owner's environmental impact,
          including total square footage, total emissions, average greenhouse
          gas intensity, and a breakdown of their buildings' grades.
        </p>

        <p>
          Additionally, we've improved meta imagery across the site - pages now
          have proper social media preview images, making them look better when
          shared on social platforms!
        </p>

        <p>
          <strong>Update Oct. 2025:</strong> We've now added these same stats
          and graphs to the ward pages as well!
        </p>
      </div>

      <div class="two-cols">
        <div>
          <a href="/release-notes/2025/biggest-before.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2025/biggest-before.webp"
              alt="Building owner page showing basic layout without hero images"
            />
          </a>

          <p class="bold">Before</p>
        </div>
        <div>
          <a href="/release-notes/2025/biggest-after.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2025/biggest-after.webp"
              alt="Enhanced building owner page with building hero images and improved stats"
            />
          </a>

          <p class="bold">After</p>
        </div>
      </div>

      <div class="two-cols">
        <div>
          <a href="/release-notes/2025/iit-before.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2025/iit-before.webp"
              alt="IIT owner page before improvements"
            />
          </a>

          <p class="bold">IIT Before</p>
        </div>
        <div>
          <a href="/release-notes/2025/iit-after.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2025/iit-after.webp"
              alt="IIT owner page with new building hero and enhanced statistics"
            />
          </a>

          <p class="bold">IIT After</p>
        </div>
      </div>

      <div class="layout-constrained">
        <h2>August 22nd, 2025 - Data Update to 2023 & Citywide Stats</h2>

        <p>
          We updated the source data to the year 2023, bringing in the latest
          building emissions and energy data. This update includes
          <strong>61 new buildings</strong> that submitted data for the first
          time and <strong>288 buildings that stopped reporting</strong> from
          the previous year.
        </p>

        <p>
          You can
          <strong>
            track building participation with our new
            <g-link to="/latest-updates">Latest Updates Page</g-link>!</strong
          >
          discover which buildings joined or dropped out of Chicago's energy
          benchmarking program between data years.
        </p>

        <p>
          <strong
            >Want to see the bigger picture? Check out our new
            <g-link to="/citywide-stats">Citywide Stats Page</g-link>!</strong
          >
          We've got a variety of graphs that reveal citywide trends over time,
          so you can see if Chicago buildings are getting cleaner or dirtier
          year over year.
        </p>

        <h2>August 5th, 2025 - Improved Printing for Buildings</h2>

        <p>
          We added a new print button that makes it easy to print our building
          pages, so you can print off a building that you're interested in. Our
          print mode removes navigation elements to focus on the building data
          and make pages more suitable for printing or saving as PDFs, including
          a QR code so folks who see the printed page can see the full data.
        </p>
      </div>

      <div class="two-cols">
        <div>
          <a href="/release-notes/2025/print-mode-btn.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2025/print-mode-btn.webp"
              alt="Building page showing the new print mode button in the top right corner"
            />
          </a>

          <p class="bold">New Print Button</p>
        </div>
        <div>
          <a href="/release-notes/2025/print-mode-preview.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2025/print-mode-preview.webp"
              alt="Building page in print mode showing clean layout without navigation or footer"
            />
          </a>

          <p class="bold">Print Preview</p>
        </div>
      </div>

      <div class="layout-constrained">
        <h2>June 6th, 2025 - Added Ward Info & Pages</h2>

        <p>
          Buildings now have their ward shown on the building details page, and
          there are pages for all of Chicago's 50 wards. These are linked from
          an individual building, our <g-link to="/wards">Wards Page</g-link>,
          or can be found directly at
          <code>electrifychicago.net/ward/WardNumber</code> (e.g.
          <a href="https://electrifychicago.net/ward/1/"
            >https://electrifychicago.net/ward/1</a
          >).
        </p>

        <h2>March 14th, 2025 - Building Grades v1</h2>

        <p>
          We wanted to make buildings more easy to understand at a glance, so
          you can quickly see if a building is a top performer or highly
          polluting. After months of hard work, we released our first version of
          building grades, based off of emissions intensity, energy mix, and
          consistent reporting.
        </p>

        <p>
          Want to learn more?
          <a href="/blog/how-we-grade-buildings">Read About Our Grading</a>!
        </p>
      </div>

      <div class="two-cols">
        <div>
          <a href="/release-notes/2025/gradesv1-homepage.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2025/gradesv1-homepage.webp"
              alt="The Electrify Chicago homepage showing Chicago's most emissions intense
                buildings and some featured Chicago buildings, with Crown Hall getting an F,
                Digital Lakeside getting a C, and more."
            />
          </a>

          <p class="bold">Our Homepage With Grades (as of March 2025)</p>
        </div>
        <div>
          <a
            href="/release-notes/2025/gradesv1-marina-towers.webp"
            target="_blank"
          >
            <img
              class="-shadowed"
              src="/release-notes/2025/gradesv1-marina-towers.webp"
              alt="Electrify Chicago's Marina Towers page, showing it has an overall A, a B under
                emissions intensity, an A under electricity mix, and an A for consistent reporting."
            />
          </a>

          <p class="bold">
            A Sample Building With Its Report Card (as of March 2025)
          </p>
        </div>
      </div>

      <div class="layout-constrained">
        <h2>February 14th, 2025 - Homepage Redesign</h2>

        <p>
          We redesigned the homepage to make it more visually appealing and
          prompt people to our two most common features - our search and our map
          page. We also added some featured buildings, like museums, to
          encourage people to explore the site for buildings they know about!
        </p>
      </div>

      <div class="two-cols">
        <div>
          <a href="/release-notes/2025/homepage-before.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2025/homepage-before.webp"
              alt="Electrify Chicago Homepage showing a lot of introductory text and a table of
                buildings"
            />
          </a>

          <p class="bold">Before</p>
        </div>
        <div>
          <a href="/release-notes/2025/homepage-after.webp" target="_blank">
            <img
              class="-shadowed"
              src="/release-notes/2025/homepage-after.webp"
              alt="Electrify Chicago Homepage with a large skyline hero section at the top with a
                prominent search bar and a blue map links, and tiles of buildings below with images
                for each building and their overall emissions and GHG intensity"
            />
          </a>

          <p class="bold">After</p>
        </div>
      </div>

      <div class="layout-constrained">
        <h2>
          August 30th, 2024 - New Visualizations for Historic Changes & Energy
          Mix
        </h2>

        <p>
          We added new graphs to help visualize how buildings have changed in
          their emissions, emissions intensity, and energy use over time, and a
          new pie chart that shows the mix of types of energy a building
          consumes, making it easy to see at a glance if a building is mostly
          using electricity, fossil gas, or something else!
        </p>
      </div>

      <div class="two-cols">
        <div>
          <a
            href="/release-notes/2024/merch-mart-pre-graphs.webp"
            target="_blank"
          >
            <img
              class="-shadowed"
              src="/release-notes/2024/merch-mart-pre-graphs.webp"
              alt="Electrify Chicago Merchandise Mart Page showing just stat tiles with no graphs."
            />
          </a>

          <p class="bold">Before</p>
        </div>
        <div>
          <a
            href="/release-notes/2024/merch-mart-post-graphs.webp"
            target="_blank"
          >
            <img
              class="-shadowed"
              src="/release-notes/2024/merch-mart-post-graphs.webp"
              alt="Electrify Chicago Merchandise Mart Page showing just stat tiles with graphs
              showing greenhouse gas intensity and total emissions have improved over time, and
              that Merch Mart's energy use is 44% electricity, 40% fossil gas, and 16% district
              chilling"
            />
          </a>

          <p class="bold">After</p>
        </div>
      </div>

      <div class="layout-constrained">
        <h2>April 2nd, 2024 - Data Update to 2022</h2>

        <p>
          Updated the source data to the year 2022, and dropped the filter
          limiting buildings to the latest year on most pages, so that dirty
          buildings that didn't report in 2022 still show up on our largest
          emitter lists.

          <strong
            >Buildings shown that have old data now use a mantel clock emoji
            (🕰️)</strong
          >.
        </p>

        <h2>August 30th, 2023 - Data Update to 2021</h2>

        <p>
          Updated the source data to the year 2021, which prevents being able to
          access 2020 data (for now) but also adds all reported buildings,
          removing the filter for emissions > 1,000 tons. Additionally,
          buildings that did <em>not</em> report in 2020 will have their latest
          year of data shown, so only buildings with data in 2020 and 2021 have
          data loss.
        </p>

        <p>
          We will be working on showing historical data, including comparisons,
          in a future update.
        </p>

        <hr />

        <p>
          Found a bug or have a feature request?
          <a href="https://github.com/vkoves/electrify-chicago/issues/new">
            File an issue on the Electrify Chicago GitHub </a
          >!
        </p>
      </div>
    </div>
  </DefaultLayout>
</template>
<style lang="scss">
.release-notes-page {
  .layout-constrained img.-shadowed {
    width: 100%;
  }

  .two-cols {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2%;

    > * {
      width: 49%;
    }
  }

  @media (max-width: $mobile-max-width) {
    .two-cols {
      flex-direction: column;
      gap: 1rem;

      > * {
        width: 100%;
      }
    }
  }
}
</style>
