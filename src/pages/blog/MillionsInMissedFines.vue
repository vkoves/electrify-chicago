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
        The City Of Chicago Hasn't Enforced The Benchmarking Ordinance, Didn't Collect $26.7 Million
        In Fines for 2,905 Non Enforcements
      </h1>

      <p class="constrained">
        Electrify Chicago is an independent open-source project looking to shed light onto one of
        the biggest sources of Chicago's CO<sub>2</sub> emissions - buildings. By providing more
        information about some of the city's largest and most polluting buildings, we hope t
        encourage these buildings to electrify, particularly by mobilizing people related to the
        building - whether that be students and faculty for a college building or employees and
        patients at a hospital.
      </p>
      </ul>
    </div>
  </DefaultLayout>
</template>
