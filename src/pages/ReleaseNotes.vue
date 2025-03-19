<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return { title: 'About Us' };
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
