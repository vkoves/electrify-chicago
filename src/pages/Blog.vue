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
    return { title:  'About Us' };
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
        Blog
      </h1>

      <ul>
        <li>
          <g-link to="/blog/millions-in-missed-fines">
            Millions In Missed Fines
          </g-link>
        </li>
      </ul>
    </div>
  </DefaultLayout>
</template>
