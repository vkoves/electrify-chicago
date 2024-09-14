<template>
  <div class="reporting-tile">
    <p class="headline">
      Years Reported
      <span class="score">{{ reportedYearsCount }}/{{ reportingHistory.length }}</span>
      <span
        class="grade-letter"
        :class="`-${grade}` | lowercase"
      >
        {{ grade }}
      </span>
    </p>
    <ul>
      <li
        v-for="item in reportingHistory"
        :key="item.year"
        class="reporting-tile-item"
      >
        <div
          class="marker"
          :class="{ '-reported': item.isReported }"
        >
          <img
            v-if="item.isReported"
            src="/checkmark.svg"
            :alt="`${item.year} data reported`"
            class="reported"
          >
          <img
            v-else
            src="/cross.svg"
            :alt="`${item.year} data not reported`"
          >
        </div>
        <p>{{ item.year }}</p>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { IHistoricData } from "../common-functions.vue";

import { LatestDataYear } from "../constants/globals.vue";

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

  readonly LatestDataYear: number = LatestDataYear;

  get grade(): string {
    const gradeRanges = [
      { min: 0.9, grade: "A" },
      { min: 0.8, grade: "B" },
      { min: 0.7, grade: "C" },
      { min: 0.6, grade: "D" },
      { min: 0, grade: "F" },
    ];

    const score = this.reportedYearsCount / this.reportingHistory.length;
    return gradeRanges.find((range) => score >= range.min)!.grade;
  }

  get reportedYearsCount(): number {
    return this.reportingHistory.filter((entry) => entry.isReported).length;
  }

  get reportingHistory(): { year: number; isReported: boolean }[] {
    if (!this.historicData || this.historicData.length === 0) return [];

    const reportingHistory = [];
    const reportedYears = this.historicData.map((entry) =>
      parseInt(entry.DataYear),
    );

    let currentYear = reportedYears[0];
    for (let reportedYear of reportedYears) {
      // take care of missing years that lie in between reported years
      while (currentYear !== reportedYear) {
        reportingHistory.push({ year: currentYear, isReported: false });
        currentYear++;
      }
      // if year is reported (standard case)
      reportingHistory.push({ year: currentYear, isReported: true });
      currentYear++;
    }

    /**
     * if a building stopped reporting before the latest year that we have data for,
     * add the missing years to history and mark them as not reported
     */
    while (currentYear <= LatestDataYear) {
      reportingHistory.push({ year: currentYear, isReported: false });
      currentYear++;
    }

    return reportingHistory;
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
      content: "";
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
