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
    return { title:  'About Us' };
  },
})
export default class About extends Vue {
}
</script>
<template>
  <DefaultLayout>
    <div class="layout-constrained">
      <h1
        id="main-content"
        tabindex="-1"
      >
        Release Notes
      </h1>

      <!-- TODO: Finalize this date before merge -->
      <h2>March ???, 2024 - Data Update to 2022</h2>

      <p>
        Updated the source data to the year 2022, and dropped the filter limiting buildings to the
        latest year on most pages, so that dirty buildings that didn't report in 2022 still show up
        on our largest emitter lists.
      </p>

      <h2>August 30th, 2023 - Data Update to 2021</h2>

      <p>
        Updated the source data to the year 2021, which prevents being able to access 2020 data
        (for now) but also adds all reported buildings, removing the filter for emissions > 1,000
        tons. Additionally, buildings that did <em>not</em> report in 2020 will have their latest
        year of data shown, so only buildings with data in 2020 and 2021 have data loss.
      </p>

      <p>
        We will be working on showing historical data, including comparisons, in a future update.
      </p>

      <hr>

      <p>
        Found a bug or have a feature request?
        <a href="https://github.com/vkoves/electrify-chicago/issues/new">
          File an issue on the Electrify Chicago GitHub</a>!
      </p>
    </div>
  </DefaultLayout>
</template>
