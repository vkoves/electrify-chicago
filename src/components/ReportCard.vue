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
}
</script>
<template>
  <div class="report-card">
    <h2 class="title">{{ dataYear }} Report Card</h2>

    <div class="grades-cont">
      <div class="grade-row -overall">
        <div><strong>Overall Grade</strong></div>
        <LetterGrade
          :grade="building.AvgPercentileLetterGrade"
          class="-overall"
        />
      </div>

      <hr />

      <div class="grade-row">
        <div><strong>Emissions Intensity</strong> - 50%</div>
        <LetterGrade :grade="building.GHGIntensityLetterGrade" />
      </div>

      <div class="grade-row">
        <div><strong>Energy Mix</strong> - 40%</div>
        <LetterGrade :grade="building.EnergyMixWeightedPctSumLetterGrade" />
      </div>

      <div class="grade-row">
        <div><strong>Consistent Reporting</strong> - 10%</div>
        <LetterGrade :grade="building.SubmittedRecordsGrade" />
      </div>
    </div>
  </div>
</template>
<style lang="scss">
.report-card {
  border-radius: $brd-rad-medium;
  flex-shrink: 0;
  overflow: hidden;

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
}
</style>
