<template>
  <div class="reporting-tile">
    <p class="headline">
      Years Reported
      <span class="score"
        >{{ reportedYearsCount }}/{{ reportingHistory.length }}</span
      >
      <span class="grade-letter" :class="`-${grade}` | lowercase">
        {{ grade }}
      </span>
    </p>

    <ul>
      <li
        v-for="item in reportingHistory"
        :key="item.year"
        class="reporting-tile-item"
      >
        <div class="marker" :class="{ '-reported': item.isReported }">
          <img
            v-if="item.isReported"
            src="/checkmark.svg"
            :alt="`${item.year} data reported`"
            class="reported"
          />
          <img
            v-else
            src="/cross.svg"
            :alt="`${item.year} data not reported`"
          />
        </div>
        <p>{{ item.year }}</p>
      </li>
    </ul>

    <p class="footnote">
      <strong>Note:</strong> Buildings are marked as reporting when we have
      greenhouse gas intensity values for them, but some buildings are missing
      GHG intensity values but have reported the underlying energy use data, but
      we're unsure why this is the case.
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IHistoricData } from '../common-functions.vue';

import { LatestDataYear } from '../constants/globals.vue';

/**
 * A tile that shows the reporting history of a building. For each year, it shows a
 * checkmark if there is data available and a cross if there is no data. It starts
 * from the year that the building first reported their data and goes to the last year
 * of data that the website shows. It also shows a score and a letter grade depending on
 * how many years were successfully reported.
 *
 * TODO:
 * Some examples that can be used for testing:
 * 1. United Center (reporting stops before the latest year of data -> therefore, adding the
 *    missing years)
 * 2. Digital Printer's Row (missing reports in between years that are reported)
 * 3. Searle Chemistry Laboratory (all years reported)
 * 4. Crown Hall (only 3 years reported with the latest one missing)
 */
@Component<any>({
  filters: {
    lowercase(value: string) {
      return value.toLowerCase();
    },
  },
})
export default class ReportingTile extends Vue {
  @Prop() historicData?: Array<IHistoricData>;

  @Prop({ required: true }) grade!: string; /** A - F letter grade */

  readonly LatestDataYear: number = LatestDataYear;

  get reportedYearsCount(): number {
    return this.reportingHistory.filter((entry) => entry.isReported).length;
  }

  /**
   * Based on the historic data, create a simplified mapping of whether data was reported
   */
  get reportingHistory(): { year: number; isReported: boolean }[] {
    if (!this.historicData || this.historicData.length === 0) return [];

    return this.historicData.map((datum: IHistoricData) => {
      return {
        year: parseInt(datum.DataYear),
        isReported: !isNaN(parseInt(datum.GHGIntensity)),
      };
    });
  }
}
</script>

<style lang="scss">
.reporting-tile {
  .headline {
    font-size: 1.5rem;
    font-weight: bold;
    margin-right: 0.5rem;
    margin-bottom: 1rem;

    .score {
      font-size: 1.1rem;
      font-weight: bold;
      margin-left: 0.25rem;
    }

    .grade-letter {
      font-size: 2.25rem;
      margin-left: 1rem;
    }
  }

  ul {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem 2rem;
    list-style: none;
    padding: 0;

    .reporting-tile-item {
      margin-top: 0;
      text-align: center;
      font-weight: bold;
    }
  }

  .marker {
    position: relative;
    width: 2.5rem;
    height: 2.5rem;
    margin-bottom: 0.25rem;

    &::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 85%;
      height: 85%;
      border: 0.225rem solid #767676;
      border-radius: 50%;
      z-index: -1;
    }

    img {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 100%;
      height: 100%;
    }

    &.-reported {
      img {
        top: 40%;
        left: 62%;
      }
    }
  }

  @media (max-width: $mobile-max-width) {
    .headline {
      margin-bottom: 0.5rem;
    }

    ul {
      column-gap: 1.5rem;
    }

    .marker {
      width: 1.75rem;
      height: 1.75rem;

      &::before {
        border-width: 0.175rem;
      }
    }
  }
}
</style>
