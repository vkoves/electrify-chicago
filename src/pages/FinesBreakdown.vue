<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';

import FinesData from '../data/dist/fines-by-year.json';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return { title: 'Fines Breakdown' };
  },
})
export default class FinesBreakdown extends Vue {
  // Expose fines data to template
  fineData = Object.entries(FinesData);
}
</script>
<template>
  <DefaultLayout>
    <div class="fines-breakdown-page layout-constrained">
      <h1 id="main-content" tabindex="-1">Breakdown of Predicted Fines</h1>

      <p>
        The City of Chicago energy benchmarking ordinance stipulates fines for
        non compliance, which top out at $9,200 per year. As we reported in our
        <g-link to="/blog/millions-in-missed-fines">
          Feb 2024 article about missed fines</g-link
        >, <strong>these fines have never been levied</strong>, and to our
        knowledge, as of October 2025, they still have not been.
      </p>

      <p>
        This page totals the predicted fines the city could have collected from
        buildings they know are not in compliance, assuming that these buildings
        would not come into compliance after initial fines and would hit the
        annual maximum fine.
      </p>

      <table>
        <thead>
          <tr>
            <th class="year">Year</th>
            <th class="fine">Predicted Fines</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="[year, fine] in fineData"
            :key="year"
            :class="{ '-total': year === 'total' }"
          >
            <td class="year">{{ year }}</td>
            <td class="fine">${{ fine.toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>

      <p>
        To maintain accuracy, predictions are based off of simply counting the
        buildings marked "Not Submitted" and multiplying by the maximum annual
        fine. This does not account for buildings we believe did not submit full
        data (like if they are missing an emissions total or emissions
        intensity), if the city officially marks those buildings as having
        submitted and thus in compliance.
      </p>
    </div>
  </DefaultLayout>
</template>
<style lang="scss">
.fines-breakdown-page {
  table {
    width: 16rem;
    margin: auto;
    border-collapse: collapse;
    border: solid $border-thin $grey-dark;

    thead tr {
      background-color: $blue-dark;
      color: $white;
    }

    tbody tr:nth-of-type(odd) {
      background-color: $off-white;
    }

    tr.-total {
      font-size: 1.25rem;
      font-weight: bold;

      td.year {
        text-transform: capitalize;
      }
    }

    th,
    td {
      &.fine {
        text-align: right;
      }
      &.year {
        text-align: center;
      }
    }
  }
}
</style>
