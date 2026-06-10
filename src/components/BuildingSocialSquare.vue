<template>
  <div class="building-social-square" :data-slide="slideNumber">
    <!-- Slide 1: Title / building intro -->
    <div v-if="slideNumber === 1" class="slide -title">
      <div class="brand">Electrify Chicago</div>
      <h1>{{ propertyName }}</h1>
      <p class="address">
        {{ building.Address }}, Chicago IL {{ building.ZIPCode }}
      </p>
      <div class="grade-block">
        <span class="grade-label">Overall Grade</span>
        <span class="grade-value">{{
          building.AvgPercentileLetterGrade || 'N/A'
        }}</span>
      </div>
    </div>

    <!-- Slide 2: GHG emissions -->
    <div v-else-if="slideNumber === 2" class="slide -emissions">
      <div class="brand">Electrify Chicago</div>
      <h2>Total Greenhouse Gas Emissions</h2>
      <div class="big-stat">
        {{ formattedEmissions }}
        <span class="unit">tons CO<sub>2</sub>e</span>
      </div>
      <p class="caption">{{ propertyName }}</p>
    </div>

    <!-- Slide 3: Energy mix placeholder -->
    <div v-else-if="slideNumber === 3" class="slide -energy">
      <div class="brand">Electrify Chicago</div>
      <h2>Energy Mix</h2>
      <p class="caption">Energy breakdown for {{ propertyName }} goes here.</p>
    </div>

    <!-- Slide 4: Call to action -->
    <div v-else-if="slideNumber === 4" class="slide -cta">
      <div class="brand">Electrify Chicago</div>
      <h2>See the full report</h2>
      <p class="url">electrifychicago.net{{ building.path }}</p>
    </div>

    <!-- Fallback for unknown slide numbers -->
    <div v-else class="slide -fallback">
      <p>Slide {{ slideNumber }} not yet defined</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IBuilding, IBuildingBenchmarkStats } from '../common-functions.vue';

/**
 * A 1080x1080 square rendering of a building's stats, intended for export
 * as an Instagram-ready image. Different slides are rendered based on the
 * `slideNumber` prop so the parent can step through the deck.
 */
@Component
export default class BuildingSocialSquare extends Vue {
  /** Total number of slides available in the deck */
  static readonly SlideCount = 4;

  @Prop({ required: true }) building!: IBuilding;
  @Prop({ required: true }) slideNumber!: number;
  @Prop({ required: true }) stats!: IBuildingBenchmarkStats;

  get propertyName(): string {
    return this.building.PropertyName || this.building.Address;
  }

  get formattedEmissions(): string {
    return Math.round(this.building.TotalGHGEmissions || 0).toLocaleString();
  }
}
</script>

<style lang="scss">
.building-social-square {
  // Render at Instagram square resolution (1080x1080). Consumers can scale
  // with CSS transforms for preview.
  width: 1080px;
  height: 1080px;
  background-color: $white;
  color: $text-main;
  position: relative;
  overflow: hidden;
  font-family: inherit;

  .slide {
    width: 100%;
    height: 100%;
    padding: 4rem;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 2rem;
  }

  .brand {
    position: absolute;
    top: 2.5rem;
    left: 4rem;
    font-size: 1.75rem;
    font-weight: 700;
    color: $blue-very-dark;
    letter-spacing: 0.05em;
  }

  h1 {
    font-size: 5rem;
    line-height: 1.1;
    margin: 0;
  }

  h2 {
    font-size: 3.5rem;
    margin: 0;
  }

  .address {
    font-size: 2rem;
    margin: 0;
    color: $text-light;
  }

  .grade-block {
    margin-top: 2rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    .grade-label {
      font-size: 1.75rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: $text-light;
    }

    .grade-value {
      font-size: 10rem;
      font-weight: 700;
      line-height: 1;
    }
  }

  .big-stat {
    font-size: 8rem;
    font-weight: 700;
    line-height: 1;

    .unit {
      display: block;
      font-size: 2.5rem;
      font-weight: 400;
      color: $text-light;
      margin-top: 1rem;
    }
  }

  .caption {
    font-size: 2rem;
    margin: 0;
  }

  .url {
    font-size: 2.5rem;
    font-weight: 700;
    color: $blue-very-dark;
    margin: 0;
  }

  .slide.-fallback {
    align-items: center;
    color: $text-light;
  }
}
</style>
