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

      <div class="table-cont">
        <table>
          <caption>
            Buildings Out Of Compliance Per Year & Predicted Fines
          </caption>
          <thead>
            <tr>
              <th class="year">Year</th>
              <th class="count">
                Non-Reporting <br />
                Buildings
              </th>
              <th class="fine">
                Predicted <br />
                Fines
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="[year, fineData] in fineData"
              :key="year"
              :class="{ '-total': year === 'total' }"
            >
              <td class="year">{{ year }}</td>
              <td class="count">
                {{ fineData.count.toLocaleString()
                }}<span v-if="year === 'total'" class="asterisk">*</span>
              </td>
              <td class="fine">${{ fineData.fines.toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>

        <p class="footnote">
          <strong>*</strong> The total is a number of incidents of
          non-compliance, not a count of buildings, since several buildings
          don't report for several years.
        </p>
      </div>

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
  .table-cont {
    width: 24rem;
    margin: auto;

    .footnote {
      margin-top: 0.5rem;
    }

    @media (max-width: $mobile-max-width) {
      width: 100%;
    }
  }

  table {
    border-collapse: collapse;
    border: solid $border-thin $grey-dark;
    width: 100%;

    caption {
      font-weight: 600;
      margin-bottom: 0.5rem;
      font-size: 1.125rem;
    }

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
      &.fine,
      &.count {
        text-align: right;
      }
      &.year {
        text-align: center;
      }

      span.asterisk {
        position: relative;
        margin-left: 0.125em;
        top: -0.25rem;
      }
    }
  }
}
</style>
