<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IBuilding } from '../common-functions.vue';
import LetterGrade from './LetterGrade.vue';

/**
 * A component that shows a building's overall report card
 */
@Component({
  components: {
    LetterGrade,
  },
})
export default class ReportCard extends Vue {
  @Prop({ required: true }) building!: IBuilding;

  @Prop({ required: true }) dataYear!: number;

  /** Whether we're currently blurring the report card and showing an anomaly warning */
  showingWarning = false;

  get hasAnomalies(): boolean {
    return this.building.DataAnomalies.length > 0;
  }

  /** Focus a given element, which allows us to apply CSS when it's focused */
  focusElem(targetId: string): void {
    const targetElem = document.getElementById(targetId);

    if (targetElem) {
      targetElem.focus();
    } else {
      throw new Error(`No element found matching selector '#${targetId}'!`);
    }
  }

  mounted(): void {
    this.showingWarning = this.hasAnomalies;
  }

  hideWarning(): void {
    this.showingWarning = false;
  }
}
</script>
<template>
  <div class="report-card-cont">
    <div
      v-if="hasAnomalies"
      class="anomaly-warning fadeable"
      :class="{ '-faded': !showingWarning }"
    >
      <div class="warning-inner">
        <h2>Warning - Data Discrepencies Detected</h2>

        <p>
          We detected some issues with this building's data, so these grades may
          not be reflective of the building's true performance.
        </p>

        <button @click="hideWarning()">Dismiss</button>
      </div>
    </div>
    <div class="report-card" :class="{ '-anomalous': showingWarning }">
      <h2 class="title">{{ dataYear }} Report Card</h2>

      <div class="grades-cont">
        <div class="grade-row -overall">
          <div>
            <strong>Overall Grade</strong>
          </div>
          <LetterGrade
            :grade="building.AvgPercentileLetterGrade"
            class="-overall"
          />
        </div>

        <hr />

        <a
          href="#emissions-intensity"
          class="grade-row"
          @click="focusElem('emissions-intensity')"
        >
          <div><strong>Emissions Intensity</strong> - 50%</div>
          <LetterGrade :grade="building.GHGIntensityLetterGrade" />
        </a>

        <a
          href="#energy-mix"
          class="grade-row"
          @click="focusElem('energy-mix')"
        >
          <div><strong>Energy Mix</strong> - 40%</div>
          <LetterGrade :grade="building.EnergyMixLetterGrade" />
        </a>

        <a
          href="#years-reported"
          class="grade-row"
          @click="focusElem('years-reported')"
        >
          <div><strong>Consistent Reporting</strong> - 10%</div>
          <LetterGrade :grade="building.SubmittedRecordsLetterGrade" />
        </a>

        <div class="learn-more-cont">
          <a href="/blog/how-we-grade-buildings"> Learn About Our Grading </a>
        </div>
      </div>
    </div>
  </div>
</template>
<style lang="scss">
.report-card-cont {
  position: relative;
  border-radius: $brd-rad-medium;
  overflow: hidden;
  flex-shrink: 0;
  // When printing, don't remove colors or backgrounds
  print-color-adjust: exact;

  .anomaly-warning {
    position: absolute;
    background: rgba(0, 0, 0, 0.25);
    width: 100%;
    height: 100%;
    z-index: 1;
    color: white;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;

    .warning-inner {
      width: 80%;
      max-width: 30rem;
      padding: 1rem;
      border-radius: $brd-rad-small;
      background: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(0.25rem);

      h2 {
        margin-top: 0;
        font-size: 1rem;
      }
      p {
        font-size: 0.8125rem;
      }
    }

    button {
      border-bottom: none;
      margin-top: 1rem;
    }
  }

  .fadeable {
    transition: opacity 0.3s;

    &.-faded {
      opacity: 0;
      visibility: hidden;
    }
  }

  .report-card {
    &.-anomalous {
      filter: blur(0.125rem);
    }

    h2,
    .grades-cont {
      padding-left: 1rem;
      padding-right: 1rem;
    }

    h2.title {
      margin: 0;
      background-color: $chicago-red;
      color: $white;
      padding-left: 1.5rem;
      padding-top: 0.5rem;
      padding-bottom: 0.25rem;
    }

    hr {
      border: solid $border-medium $grey-dark;
    }

    .grades-cont {
      padding-top: 0.5rem;
      padding-bottom: 1rem;
      border: solid $border-thick $grey-dark;
      border-top: none;
      border-bottom-right-radius: $brd-rad-medium;
      border-bottom-left-radius: $brd-rad-medium;

      .letter-grade {
        font-size: 1.5rem;
        width: 2rem;
        text-align: center;

        &.-overall {
          font-size: 3rem;
        }
      }
    }

    .grade-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 0.5rem 0.5rem 0.25rem;

      &.-overall {
        padding-top: 0.25rem;
        padding-bottom: 0;
        font-size: 1.5rem;
      }
    }

    // Style linked grade rows
    a.grade-row {
      text-decoration: none;
      color: $text-main;

      &:hover {
        background-color: $off-white;
      }

      // For a more subtle link effect, use a dotted underline
      strong {
        text-decoration: underline;
        text-decoration-style: dotted;
      }
    }

    .learn-more-cont {
      margin-top: 1rem;

      a {
        font-weight: 500;
        font-size: 0.8125rem;
      }
    }
  }
}
</style>
