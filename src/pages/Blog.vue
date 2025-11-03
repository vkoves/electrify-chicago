<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';
import { LatestDataYear } from '../constants/globals.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return generatePageMeta(
      'Blog',
      'Read our latest insights on building decarbonization, energy policy, ' +
        'and climate action in Chicago/',
    );
  },
})
export default class About extends Vue {
  readonly LatestDataYear: number = LatestDataYear;
}
</script>
<template>
  <DefaultLayout>
    <div class="layout-constrained blog-page">
      <h1 id="main-content" tabindex="-1">Electrify Chicago Blog</h1>

      <ul class="blogs-list">
        <li>
          <h2>
            <g-link to="/blog/what-just-happened-to-my-electric-bill">
              What Just Happened to My Electric Bill?
            </g-link>
          </h2>
          <p class="publish-time">
            Published <time datetime="2025-11-03">Nov. 3rd, 2025</time>
          </p>

          <p>
            ComEd bills have shot up dramatically in the last few months. Learn
            the surprising story behind the price increases, why PJM (the
            regional grid operator) is the real cause, and what you can do to
            help fix it and lower your bills.
          </p>
        </li>

        <li>
          <h2>
            <g-link to="/blog/how-we-grade-buildings">
              How We Grade Buildings, And Why
            </g-link>
          </h2>
          <p class="publish-time">
            Published <time datetime="2025-03-11">Mar. 11th, 2025</time>
          </p>

          <p>
            Electrify Chicago gives buildings letter grades from A to F based on
            their environmental performance. Learn how we calculate these
            grades, what they mean, and why we think grading buildings helps
            drive transparency and improvement in Chicago's building emissions.
          </p>
        </li>

        <li>
          <h2>
            <g-link to="/blog/GHG-Intensity-Predict-Compliance">
              Do High Emitting Buildings Report Emissions Less Often?
            </g-link>
          </h2>
          <p class="publish-time">
            <!-- TODO: Update publish time when PR is about to get merged -->
            Published <time datetime="2025-3-06">Mar. 6th, 2025</time>
          </p>

          <p>
            Qualitatively, some readers have reported that buildings who report
            high levels of emissions seem to stop reporting. This blog post
            looks at the data to determine if there is a pattern in the data
            that links high emitting buildings to non-reporting. We find that
            despite anecdotal observations, there seems to be no pattern for
            buildings that have higher GHG intensities in the prior year or
            upwardly trending GHG intensities to stop reporting the following
            year.
          </p>
        </li>

        <li>
          <h2>
            <g-link to="/blog/millions-in-missed-fines">
              City Of Chicago Failed to Collect $30 Million In Potential Fines
              from Building Benchmarking Ordinance
            </g-link>
          </h2>
          <p class="publish-time">
            Published <time datetime="2024-02-02">Feb. 2nd, 2024</time>
          </p>

          <p>
            The City of Chicago didn't fully enforce the benchmarking ordinance
            that requires the owners of large building to report their emissions
            - and based on the fine amounts laid out in the ordinance, we
            calculated the city missed out on millions and harmed transparency
            and accountability.
          </p>
        </li>
      </ul>
    </div>
  </DefaultLayout>
</template>
<style lang="scss">
.blog-page {
  ul.blogs-list {
    list-style: none;
    padding: 0;

    h2 {
      margin-bottom: 0;
    }

    li + li {
      margin-top: 2rem;
    }
  }

  h2 a {
    text-decoration: none;

    &:hover,
    &:focus {
      text-decoration: underline;
    }
  }
}
</style>
