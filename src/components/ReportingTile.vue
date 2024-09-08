<template>
  <div class="reporting-tile">
    <p>
      Years Reported
      <span class="score"
        >{{ reportedYears }}/{{ reportingHistory.length }}</span
      >
      <span>{{ grade }}</span>
    </p>
    <ul>
      <li v-for="item in reportingHistory" :key="item.year">
        {{ item.year }} - {{ item.isReported }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { IHistoricData } from "../common-functions.vue";

import { LatestDataYear } from "../constants/globals.vue";

@Component
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

    const score = this.reportedYears / this.reportingHistory.length;
    return gradeRanges.find((range) => score >= range.min)!.grade;
  }

  get reportedYears(): number {
    return this.reportingHistory.filter((entry) => entry.isReported).length;
  }

  get reportingHistory(): { year: number; isReported: boolean }[] {
    if (!this.historicData || this.historicData.length === 0) return [];

    const reportingHistory = [];
    const reportedYears = this.historicData.map((entry) =>
      parseInt(entry.DataYear)
    );

    let currentYear = reportedYears[0];
    for (let reportedYear of reportedYears) {
      // adds missing years to reportHistory in between reported years
      while (currentYear !== reportedYear) {
        reportingHistory.push({ year: currentYear, isReported: false });
        currentYear++;
      }
      // if year is reported
      reportingHistory.push({ year: currentYear, isReported: true });
      currentYear++;
    }

    // if a building stopped reporting before the latest year, add missing years to history
    while (currentYear <= LatestDataYear) {
      reportingHistory.push({ year: currentYear, isReported: false });
      currentYear++;
    }

    return reportingHistory;
  }
}
</script>

<style lang="scss"></style>
