<template>
  <div class="building-social-square" :data-slide="slideNumber">
    <div class="brand soc-panel">
      <img src="/electrify-chicago-logo.svg" alt="Electrify Chicago" />
    </div>

    <!--
      Building photo floats outside the dark overlay and panel so it isn't
      darkened; positioned flush with the left edge of the square.
    -->
    <img
      v-if="slideNumber === 1 && buildingImage"
      class="building-photo"
      :src="buildingImage.imgUrl"
      :alt="propertyName"
    />

    <!-- Slide 1: Title / building intro -->
    <div v-if="slideNumber === 1" class="slide -title">
      <div class="soc-panel" :class="{ '-with-photo': buildingImage }">
        <h1>{{ propertyName }}</h1>
        <p class="address">
          {{ building.Address }}, Chicago IL {{ building.ZIPCode }}
        </p>

        <dl class="info-stats">
          <div>
            <dt>Square Footage</dt>
            <dd>{{ formattedSquareFootage }} sqft</dd>
          </div>
          <div v-if="yearBuilt">
            <dt>Built</dt>
            <dd>{{ yearBuilt }}</dd>
          </div>
        </dl>

        <div class="grade-block">
          <span class="grade-label">Overall Grade</span>
          <span class="grade-value">{{
            building.AvgPercentileLetterGrade || 'N/A'
          }}</span>
        </div>
      </div>
    </div>

    <!-- Slide 2: Report card -->
    <div v-else-if="slideNumber === 2" class="slide -report">
      <div class="soc-panel">
        <h2>{{ propertyName }}</h2>
        <p class="caption">{{ dataYear }} Report Card</p>
        <div class="report-card-wrapper">
          <ReportCard :building="building" :data-year="dataYear" />
        </div>
      </div>
    </div>

    <!-- Slide 3: Energy mix pie chart -->
    <div v-else-if="slideNumber === 3" class="slide -energy">
      <div class="soc-panel">
        <h2>Energy Mix</h2>
        <p class="caption">{{ propertyName }} &middot; {{ dataYear }}</p>
        <div class="pie-wrapper">
          <PieChart
            id-prefix="social-square-energy-mix"
            :graph-data="energyBreakdown"
            :sort-by-largest="false"
            :light-text="true"
          />
        </div>
      </div>
    </div>

    <!-- Slide 4: Call to action -->
    <div v-else-if="slideNumber === 4" class="slide -cta">
      <div class="soc-panel">
        <h2>See the full report</h2>
        <p class="url">electrifychicago.net{{ building.path }}</p>
      </div>
    </div>

    <!-- Fallback for unknown slide numbers -->
    <div v-else class="slide -fallback">
      <div class="soc-panel">
        <p>Slide {{ slideNumber }} not yet defined</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {
  calculateEnergyBreakdown,
  IBuilding,
  IBuildingBenchmarkStats,
} from '../common-functions.vue';
import {
  getBuildingImage,
  IBuildingImage,
} from '../constants/building-images.constant.vue';
import PieChart, { IPieSlice } from './graphs/PieChart.vue';
import ReportCard from './ReportCard.vue';

/**
 * A 1080x1080 square rendering of a building's stats, intended for export
 * as an Instagram-ready image. Different slides are rendered based on the
 * `slideNumber` prop so the parent can step through the deck.
 */
@Component({
  components: {
    PieChart,
    ReportCard,
  },
})
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

  get formattedSquareFootage(): string {
    return Math.round(this.building.GrossFloorArea || 0).toLocaleString();
  }

  get yearBuilt(): number | null {
    const year = this.building.YearBuilt;
    if (!year || Number.isNaN(year)) {
      return null;
    }
    return Math.round(year);
  }

  get buildingImage(): IBuildingImage | null {
    return getBuildingImage(this.building);
  }

  get dataYear(): number {
    return this.building.DataYear as number;
  }

  get energyBreakdown(): Array<IPieSlice> {
    return calculateEnergyBreakdown(this.building).energyBreakdown;
  }
}
</script>

<style lang="scss">
.building-social-square {
  // Render at Instagram square resolution (1080x1080). Consumers can scale
  // with CSS transforms for preview.
  width: 1080px;
  height: 1080px;
  color: $white;
  position: relative;
  overflow: hidden;
  font-family: inherit;
  // Centered crop of the Chicago skyline as the backdrop on every slide
  background-image: url('/chicago-skyline.jpg');
  background-size: cover;
  background-position: center;

  // 50% darken overlay so foreground text/panels stay readable
  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1;
  }

  // Semi-transparent black panel for readable text content. A real
  // backdrop-filter blur isn't reliably captured by html-to-image during
  // export, so we use a solid translucent fill instead.
  .soc-panel {
    background-color: rgba(0, 0, 0, 0.6);
    border-radius: 0.5rem;
    padding: 2rem 2.5rem;
    color: $white;
    border: none;

    // When the building photo is overlaid on the left of the panel, push
    // panel content to the right so it doesn't sit behind the image.
    &.-with-photo {
      padding-left: 33rem;
    }
  }

  .slide {
    position: relative;
    z-index: 2;
    width: 100%;
    height: 100%;
    padding: 4rem;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 2rem;
  }

  // Logo chip overrides the shared .soc-panel styling: pinned to the top-left
  // corner of the square with a white background and only the bottom-right
  // corner rounded so it visually anchors into the corner.
  .brand.soc-panel {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 2;
    padding: 1.25rem 1.75rem;
    background-color: $white;
    border-radius: 0 0 0.5rem 0;
    display: inline-flex;
    align-items: center;

    img {
      display: block;
      height: 3rem;
      width: auto;
    }
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
    color: $white;
    opacity: 0.85;
  }

  // Building photo: pinned to the left edge of the square, sitting on top
  // of (but not darkened by) the overlay and panel. Only the right-side
  // corners are rounded so the left side stays flush with the slide edge.
  .building-photo {
    position: absolute;
    top: 18rem;
    left: 0;
    width: 34rem;
    height: 24rem;
    object-fit: cover;
    border-radius: 0 0.5rem 0.5rem 0;
    z-index: 3;
  }

  .info-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem 3rem;
    margin: 1.5rem 0 0 0;
    padding: 0;

    > div {
      margin: 0;
    }

    dt {
      font-size: 1.5rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      opacity: 0.85;
    }

    dd {
      font-size: 2.25rem;
      font-weight: 700;
      margin: 0.25rem 0 0 0;
    }
  }

  // Centered wrapper for the embedded ReportCard on slide 2. The card is
  // designed for ~18rem desktop columns, so we scale it up here for the
  // larger square canvas and center it horizontally.
  .report-card-wrapper {
    margin-top: 1.5rem;
    display: flex;
    justify-content: center;

    .report-card-cont {
      width: 32rem;
      max-width: 100%;
      font-size: 1.5rem;
    }

    // ReportCard normally inherits its background from the page; on the
    // dark social-square panel we need to supply one.
    .report-card {
      background-color: $white;
      color: $text-main;
    }

    // The "Learn About Our Grading" link is page UI, not relevant in the
    // exported share image.
    .learn-more-cont {
      display: none;
    }
  }

  // Centered wrapper for the embedded PieChart on slide 3. The chart renders
  // its own SVG with fixed internal dimensions; we just give it room.
  .pie-wrapper {
    margin-top: 1.5rem;
    display: flex;
    justify-content: center;
    align-items: center;

    .pie-chart-cont {
      width: 100%;
      max-width: 36rem;
    }
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
      opacity: 0.85;
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
      opacity: 0.85;
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
    margin: 0;
  }

  .slide.-fallback {
    align-items: center;

    .soc-panel {
      opacity: 0.75;
    }
  }
}
</style>
