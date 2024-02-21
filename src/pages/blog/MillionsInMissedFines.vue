<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';
import { LatestDataYear } from '~/constants/globals.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return { title:  'City Missed 27 Million in Fines' };
  },
})
export default class About extends Vue {
  readonly LatestDataYear: number = LatestDataYear;
}
</script>
<template>
  <DefaultLayout>
    <div class="layout-constrained">
      <h1
        id="main-content"
        tabindex="-1"
      >
        City Of Chicago Didn't Collect $26.7 Million In Fines
      </h1>
      <p class="constrained bold">
        Hasn't Enforced The Benchmarking Ordinance Fines for 2,905 Non Enforcements In Past 5 Years
        (2019 - 2023)
      </p>

      <g-link to="/blog/millions-in-missed-fines">
        Back to Blog
      </g-link>

      <p class="constrained">
        Electrify Chicago has analyzed the last five years of city benchmark data, and found
        2,905 instances of buildings not submitting data. Based on the
        <a href="https://www.chicago.gov/content/dam/city/progs/env/EnergyBenchmark/sample_notification_letter.pdf">
          latest (2024) official notification letter <NewTabIcon/>
        </a> fines for non-compliance could total up to $9,200.
      </p>

      <p>
        <strong>With $9,200 of fines X 2,905 instances of non-compliance, that's a whopping $26.7 million dollars of not-collected fines</strong>
      </p>
      </ul>
    </div>
  </DefaultLayout>
</template>
