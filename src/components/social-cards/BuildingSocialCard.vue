<template>
  <div class="social-card">
    <div class="social-card-content">
      <div class="main-section" :class="{ '-no-img': !buildingImg }">
        <div class="text-content">
          <div class="building-info">
            <div class="building-title-row">
              <div class="overall-grade-section">
                <div class="overall-grade-label">Overall Grade</div>
                <LetterGrade
                  :grade="building.AvgPercentileLetterGrade"
                  class="-large"
                />
              </div>
              <div class="title-content">
                <h1 class="building-name">{{ propertyName }}</h1>
                <p class="building-address">{{ building.Address }}</p>
              </div>
              <!-- If no building image, put the logo in the top right -->
              <div v-if="!buildingImg" class="logo -no-img">
                <img
                  src="/electrify-chicago-logo.svg"
                  alt="Electrify Chicago"
                />
              </div>
            </div>
          </div>

          <div class="sub-grades">
            <div class="sub-grade-item">
              <span class="sub-grade-label">GHG Intensity</span>
              <LetterGrade :grade="building.GHGIntensityLetterGrade" />
            </div>
            <div class="sub-grade-item">
              <span class="sub-grade-label">Energy Mix</span>
              <LetterGrade :grade="building.EnergyMixLetterGrade" />
            </div>
            <div class="sub-grade-item">
              <span class="sub-grade-label">Reporting</span>
              <LetterGrade :grade="building.SubmittedRecordsLetterGrade" />
            </div>
          </div>

          <div class="stats-grid">
            <div
              class="stat-item"
              :class="getConcernLevelClasses(ghgIntensityConcernLevel)"
            >
              <div class="stat-label">GHG Intensity</div>
              <div class="stat-value">
                {{ formatGHGIntensity(building.GHGIntensity) }}
              </div>
              <div class="stat-unit">kg CO₂e/sqft</div>
              <div v-if="ghgIntensityMedianMsg" class="median-comparison">
                <span class="median-mult"
                  >{{ ghgIntensityMedianMsg }} median</span
                >
                <div class="median-val">
                  {{ stats.GHGIntensity.median.toLocaleString() }} kg CO₂e/sqft
                </div>
              </div>
            </div>

            <div
              class="stat-item"
              :class="getConcernLevelClasses(energyMixConcernLevel)"
            >
              <div class="stat-label text-center">Energy Mix</div>
              <div class="pie-chart-cont-inline">
                <PieChart
                  :id-prefix="'social-energy-mix'"
                  :graph-data="energyBreakdownData"
                />
              </div>
            </div>

            <div
              class="stat-item"
              :class="getConcernLevelClasses(totalEmissionsConcernLevel)"
            >
              <div class="stat-label">Total Emissions</div>
              <div class="stat-value">
                {{ formatNumber(building.TotalGHGEmissions) }}
              </div>
              <div class="stat-unit">tons CO₂e</div>
              <div v-if="totalEmissionsMedianMsg" class="median-comparison">
                <span class="median-mult"
                  >{{ totalEmissionsMedianMsg }} median</span
                >
                <div class="median-val">
                  {{
                    Math.round(stats.TotalGHGEmissions.median).toLocaleString()
                  }}
                  tons CO₂e
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Second column, if there's images -->
        <div v-if="buildingImg" class="image-section">
          <img
            :src="buildingImg.imgUrl"
            :alt="propertyName"
            class="building-image"
          />

          <div class="logo">
            <img src="/electrify-chicago-logo.svg" alt="Electrify Chicago" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  IBuilding,
  calculateEnergyBreakdown,
  IBuildingBenchmarkStats,
  getConcernLevel,
  getMedianMultipleMsg,
} from '../../common-functions.vue';
import {
  getBuildingImage,
  IBuildingImage,
} from '../../constants/building-images.constant.vue';
import buildingBenchmarkStats from '../../data/dist/building-benchmark-stats.json';
import LetterGrade from '../LetterGrade.vue';
import PieChart, { IPieSlice } from '../graphs/PieChart.vue';

@Component({
  components: {
    LetterGrade,
    PieChart,
  },
})
export default class BuildingSocialCard extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  $page!: {
    building: IBuilding;
  };

  energyBreakdownData!: Array<IPieSlice>;

  readonly stats: IBuildingBenchmarkStats = buildingBenchmarkStats;

  /** A helper to get the current building, but with proper typing */
  get building(): IBuilding {
    return this.$page.building;
  }

  /** Helper for property name with address fallback */
  get propertyName(): string {
    return this.building.PropertyName || this.building.Address;
  }

  /** Get building image if available */
  get buildingImg(): IBuildingImage | null {
    return getBuildingImage(this.building);
  }

  /** Get concern level for GHG Intensity */
  get ghgIntensityConcernLevel(): number | null {
    return getConcernLevel(this.building, 'GHGIntensity', this.stats);
  }

  /** Get concern level for Total Emissions */
  get totalEmissionsConcernLevel(): number | null {
    return getConcernLevel(this.building, 'TotalGHGEmissions', this.stats);
  }

  /** Get concern level for Energy Mix based on letter grade */
  get energyMixConcernLevel(): number | null {
    const grade = this.building.EnergyMixLetterGrade;
    if (!grade) return null;

    // Convert letter grade to concern level
    switch (grade) {
      case 'A':
        return 0; // great
      case 'B':
        return 1; // good
      case 'C':
        return 2; // medium
      case 'D':
        return 3; // bad
      case 'F':
        return 4; // very bad
      default:
        return null;
    }
  }

  /** Get median multiple message for GHG Intensity */
  get ghgIntensityMedianMsg(): string | null {
    return this.getMedianMessage('GHGIntensity');
  }

  /** Get median multiple message for Total Emissions */
  get totalEmissionsMedianMsg(): string | null {
    return this.getMedianMessage('TotalGHGEmissions');
  }

  formatNumber(value: number): string {
    if (!value) return '—';
    return Math.round(value).toLocaleString();
  }

  formatGHGIntensity(value: number): string {
    if (!value) return '—';
    return value.toLocaleString(undefined, {
      minimumFractionDigits: 1,
      maximumFractionDigits: 1,
    });
  }

  /** Returns concern level class bindings for a given concern level */
  getConcernLevelClasses(concernLevel: number | null): Record<string, boolean> {
    return {
      'concern-level-very-bad': concernLevel === 4,
      'concern-level-bad': concernLevel === 3,
      'concern-level-medium': concernLevel === 2,
      'concern-level-good': concernLevel === 1,
      'concern-level-great': concernLevel === 0,
    };
  }

  /** Returns median multiple message for a given stat key */
  getMedianMessage(statKey: string): string | null {
    const median = this.stats[statKey]?.median;
    const statValue = this.building[statKey] as number;
    return getMedianMultipleMsg(median, statValue);
  }

  created(): void {
    const breakdownWithTotal = calculateEnergyBreakdown(this.building);
    this.energyBreakdownData = breakdownWithTotal.energyBreakdown;
  }
}
</script>

<style lang="scss" scoped>
.social-card {
  position: relative;
  width: 75rem;
  height: 39.375rem;
  background: $white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
  border: $border-medium solid $grey-dark;
}

.social-card-content {
  width: 100%;
  height: 100%;
  padding: 1rem;
  display: flex;
  flex-direction: column;

  .main-section {
    display: flex;
    height: 100%;
    gap: 2.5rem;
    flex: 1;
    align-items: center;

    &.-no-img .stats-grid {
      // If there's no image, we don't need to save space, so lock each column
      grid-template-columns: 1fr 1fr 1fr;
    }

    .text-content {
      flex: 1;
    }

    .image-section {
      display: flex;
      flex: 0 0 24rem;
      height: 100%;
      flex-direction: column;
      align-items: flex-end;
      justify-content: center;
    }
  }

  .logo {
    text-align: right;
    margin-top: auto;
    align-self: flex-end;

    // If at the top, align to top
    &.-no-img {
      align-self: flex-start;
      margin-top: 0;
    }

    img {
      height: 2.25rem;
    }
  }
}

.building-image {
  max-width: 100%;
  max-height: 80%;
  border-radius: $brd-rad-medium;
  object-fit: cover;
  box-shadow: 0 0.5rem 1.25rem rgba(0, 0, 0, 0.15);
  margin-top: auto;
}

.building-title-row {
  display: flex;
  align-items: center;
  gap: 3rem;
  margin-bottom: 1.5rem;
  margin-left: 1rem;
}

.overall-grade-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  background: $off-white;
  border-radius: $brd-rad-medium;
  padding: 1rem;
  min-width: 7.5rem;
}

.overall-grade-label {
  font-size: 1.25rem;
  font-weight: bold;
  text-align: center;
  line-height: 1.2;
}

.title-content {
  flex: 1;
}

.pie-chart-cont-inline {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1rem;

  // Override PieChart default sizing for inline display and hide labels, since
  // you acn't read them at that size anyway
  :deep(svg) {
    width: 10rem;
    transform: scale(1.6) translate(0, 0.15rem);

    // Hide any external labels - allow internal labels like 100% electric
    text:not(.-only-slice) tspan {
      display: none;
    }
    tspan.percent {
      font-size: 2.5rem;
    }
    tspan.label {
      font-size: 1.5rem;
    }
  }
}

.building-name {
  font-size: 2.625rem;
  font-weight: bold;
  margin: 0 0 0.5rem 0;
  line-height: 1.1;
}

.building-address {
  line-height: 1;
  font-size: 1.5rem;
  margin: 0;
  color: $text-mid-light;
}

.stats-grid {
  display: grid;
  // Lock the two stat tiles to the same width, allow energy mix to be smaller
  grid-template-columns: 1fr 1fr auto;
  gap: 1.5rem;
  align-items: center;
}

.stat-item {
  border-radius: $brd-rad-medium;
  padding: 1.25rem 1.25rem 1rem 1.25rem;
  text-align: center;
  border-bottom-width: 0.625rem;
  border-bottom-style: solid;
  height: 100%;

  &.-no-background {
    background: none;
    padding: 0;
    border: none;

    .stat-label {
      color: $text-mid-light;
    }
  }

  .median-mult {
    font-size: 1.5rem;
  }

  // Hiding the median value for now, it's too much info
  .median-val {
    display: none;
  }
}

.sub-grade-label,
.stat-label {
  font-weight: bold;
  font-size: 1.65rem;
  text-align: center;
  line-height: 1.3;
  margin-bottom: 0.25rem;

  &.text-center {
    text-align: center;
  }
}

.sub-grade-label,
.stat-item.-no-background .stat-label {
  color: $text-mid-light;
}

.stat-value {
  font-size: 3rem;
  font-weight: bold;
  line-height: 1;
  margin-top: 1rem;
}

.stat-unit {
  font-size: 1.5rem;
}

.sub-grades {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 1.5625rem;
  padding: 0.9375rem 0;
  border-top: $border-thick solid $grey-light;
  border-bottom: $border-thick solid $grey-light;
}

.sub-grade-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.letter-grade {
  font-size: 4rem;

  &.-large {
    font-size: 6rem;
  }
}
</style>
