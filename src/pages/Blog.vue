<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';
import { LatestDataYear } from '../constants/globals.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return { title:  'Blog' };
  },
})
export default class About extends Vue {
  readonly LatestDataYear: number = LatestDataYear;
}
</script>
<template>
  <DefaultLayout>
    <div class="layout-constrained blog-page">
      <h1
        id="main-content"
        tabindex="-1"
      >
        Electrify Chicago Blog
      </h1>

      <ul>
        <li>
          <h2>
            <g-link to="/blog/millions-in-missed-fines">
              City Of Chicago Failed to Collect $30 Million In Potential Fines from Building
              Benchmarking Ordinance
            </g-link>
          </h2>

          <p>
            The City of Chicago didn't fully enforce the benchmarking ordinance that requires the
            owners of large building to report their emissions - and based on the fine amounts laid
            out in the ordinance, we calculated the city missed out on millions and harmed
            transparency and accountability.
          </p>
        </li>
      </ul>

      <ul>
        <li>
          <h2>
            <g-link to="/blog/GHG-Intensity-Predict-Compliance">
              Do High Emitting Buildings Report Emissions Less Often?
            </g-link>
          </h2>

          <p>
            Qualitatively, some readers have reported that buildings who report high levels of emissions
            seem to stop reporting. This blog post looks at the data to determine if there is a pattern in the data
            that links high emitting buildings to non-reporting. We find that despite anecdotal observations, 
            there seems to be no pattern for buildings that have higher GHG intensities in the prior year or 
            upwardly trending GHG intensities to stop reporting the following year. 
          </p>
        </li>
      </ul>

    </div>
  </DefaultLayout>
</template>
<style lang="scss">
.blog-page {
  ul {
    list-style: none;
    padding: 0;
  }

  h2 a {
    text-decoration: none;

    &:hover, &:focus { text-decoration: underline; }
  }
}
</style>
