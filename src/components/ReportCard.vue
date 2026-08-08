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
        <h2>Warning - Data Discrepancies Detected</h2>

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
  // Single sizing knob: every internal font-size and padding scales linearly
  // with this. Parents (e.g. the social-share square) can override it to
  // resize the whole card without rewriting individual rules. Defaults to
  // 1rem so existing call sites render unchanged.
  --rc-base-font-size: 1rem;

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
      padding: calc(1 * var(--rc-base-font-size));
      border-radius: $brd-rad-small;
      background: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(0.25rem);

      h2 {
        margin-top: 0;
        font-size: calc(1 * var(--rc-base-font-size));
      }
      p {
        font-size: calc(0.8125 * var(--rc-base-font-size));
      }
    }

    button {
      border-bottom: none;
      margin-top: calc(1 * var(--rc-base-font-size));
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
    // Anchor for em-based inheritance — h2/strong/etc. scale via their
    // em-based defaults relative to this size.
    font-size: var(--rc-base-font-size);

    &.-anomalous {
      filter: blur(0.125rem);
    }

    h2,
    .grades-cont {
      padding-left: calc(1 * var(--rc-base-font-size));
      padding-right: calc(1 * var(--rc-base-font-size));
    }

    h2.title {
      margin: 0;
      background-color: $chicago-red;
      color: $white;
      padding-left: calc(1.5 * var(--rc-base-font-size));
      padding-top: calc(0.5 * var(--rc-base-font-size));
      padding-bottom: calc(0.25 * var(--rc-base-font-size));
    }

    hr {
      border: solid $border-medium $grey-dark;
    }

    .grades-cont {
      background-color: $white;
      padding-top: calc(0.5 * var(--rc-base-font-size));
      padding-bottom: calc(1 * var(--rc-base-font-size));
      border: solid $border-thick $grey-dark;
      border-top: none;
      border-bottom-right-radius: $brd-rad-medium;
      border-bottom-left-radius: $brd-rad-medium;

      .letter-grade {
        font-size: calc(1.5 * var(--rc-base-font-size));
        width: calc(2 * var(--rc-base-font-size));
        text-align: center;

        &.-overall {
          font-size: calc(3 * var(--rc-base-font-size));
        }
      }
    }

    .grade-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: calc(0.5 * var(--rc-base-font-size))
        calc(0.5 * var(--rc-base-font-size))
        calc(0.5 * var(--rc-base-font-size))
        calc(0.25 * var(--rc-base-font-size));

      &.-overall {
        padding-top: calc(0.25 * var(--rc-base-font-size));
        padding-bottom: 0;
        font-size: calc(1.5 * var(--rc-base-font-size));
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
      margin-top: calc(1 * var(--rc-base-font-size));

      a {
        font-weight: 500;
        font-size: calc(0.8125 * var(--rc-base-font-size));
      }
    }
  }

  /**
   * Print Styling - Hide Learn More link and drop underlines from sub-sections
   */
  @media print {
    // Hide the anomaly warning when printing to not cover grades - there's already a top level
    // banner warning
    .anomaly-warning {
      display: none !important;
    }

    .report-card {
      filter: none !important;
    }

    h2.title {
      font-size: 1.5rem;
    }

    .grade-row {
      font-size: 1.2rem;

      .letter-grade {
        font-size: 2rem !important;

        &.-overall {
          font-size: 4rem !important;
        }
      }
    }

    .report-card a.grade-row strong {
      text-decoration: none;
    }

    .learn-more-cont {
      display: none;
    }
  }
}
</style>
