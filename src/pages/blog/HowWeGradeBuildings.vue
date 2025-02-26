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
    return {
      title: 'How We Grade Buildings, And Why',
    };
  },
})
export default class HowWeGradeBuildings extends Vue {}
</script>
<template>
  <DefaultLayout>
    <div class="layout-constrained how-we-grade-page">
      <g-link to="/blog" class="back-link grey-link"> Back to Blog </g-link>

      <h1 id="main-content" tabindex="-1">How We Grade Buildings, And Why</h1>

      <p>
        We've been working towards grading buildings at Electrify Chicago for a
        long-time, and in March 2025 we rolled out our first version. Let's walk
        through how it works, and why!
      </p>

      <h2>Why Grade Buildings?</h2>

      <p>
        <strong
          >We want to make it easy for folks to see, at-a-glance, whether a
          building is &ldquo;good&rdquo; or &ldquo;bad&rdquo; compared to other
          city buildings</strong
        >. But good and bad are relative, so let's explain what our team means
        with that.
      </p>

      <h2>Our North Stars - Energy Use & Energy Mix</h2>

      <p>
        At Electrify Chicago, we're focused on the impact of buildings on
        climate change, and on encouraging buildings to reduce their emissions,
        so we have two primary criteria for what makes a building good:
      </p>

      <ol>
        <li>It Uses As Little Energy As Possible Per Square Foot</li>
        <li>
          It Uses Primarily (Or Only) Electricity, Rather Than Burning Fuels For
          Energy
        </li>
      </ol>

      <p>
        The first point is easy to explain - the less energy a building users
        per square foot, the lower emissions it has, and it's a metric that's
        agnostic to building size. We considered grading by total emissions, but
        that would mean that incredibly efficient large buildings could never
        get an A grade.
      </p>

      <p>
        For the second point - electricity <em>can</em> be made without creating
        emissions. In Illinois, we have a large fleet of nuclear plants that
        create low-carbon electricity, and a growing numbers of solar and wind
        plants joining our grid. That means that two buildings with the same
        energy use, but one using electricity and one using fossil gas, are very
        different - in 10 years, without any internal changes, the all-electric
        building will have reduced its emissions as the grid gets cleaner
        year-by-year.
      </p>

      <h2>
        The Biggest Challenge: We Don't Know What Goes On <em>Inside</em> A
        Building
      </h2>

      <p>
        One of the biggest limitations of the city benchmarking data is that,
        compared to a formal energy auditing process, no information is
        collected on how a building is used. The same energy use and emissions
        intensity is very different if a building:
      </p>

      <ul>
        <li>Is open 24/7 to the public</li>
        <li>Runs refrigerators and freezers to keep food safe</li>
        <li>
          Heats, cools, and filters millions of gallons of water for aquarium
          exhibits
        </li>
      </ul>

      <p>
        We can't consistently get such information for each building, so we
        grade all buildings compared to all other city buildings. This means
        that some buildings are marked as average that should be expected to
        perform better (say because they are an office building) while high
        energy intensity uses will be penalized.
      </p>

      <h2>Some Examples</h2>

      Some example buildings:

      <ul>
        <li>Merchandise Mart - B</li>

        <li>Core Site - C</li>

        <li>Art Institute of Chicago - D</li>
      </ul>

      <h2>Better Alternatives</h2>

      <p>Energy Star! We can't do that because of data</p>
    </div>
  </DefaultLayout>
</template>
<style lang="scss">
.how-we-grade-page {
}
</style>
