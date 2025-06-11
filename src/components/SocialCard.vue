<template>
  <div class="social-card">
    <div class="social-card-content">
      <div class="header">
        <div class="logo">
          <img src="/electrify-chicago-logo.svg" alt="Electrify Chicago" />
        </div>
      </div>

      <div class="main-section">
        <div class="text-content">
          <div class="building-info">
            <div class="building-title-row">
              <div class="overall-grade-section">
                <div class="overall-grade-label">Overall Grade</div>
                <LetterGrade :grade="building.AvgPercentileLetterGrade" class="-large" />
              </div>
              <div class="title-content">
                <h1 class="building-name">{{ propertyName }}</h1>
                <p class="building-address">{{ building.Address }}</p>
              </div>
            </div>
          </div>

          <div class="sub-grades">
            <div class="sub-grade-item">
              <span class="sub-grade-label">Emissions Intensity</span>
              <LetterGrade :grade="building.GHGIntensityLetterGrade" />
            </div>
            <div class="sub-grade-item">
              <span class="sub-grade-label">Energy Mix</span>
              <LetterGrade :grade="building.EnergyMixLetterGrade" />
            </div>
            <div class="sub-grade-item">
              <span class="sub-grade-label">Consistent Reporting</span>
              <LetterGrade :grade="building.SubmittedRecordsLetterGrade" />
            </div>
          </div>

          <div class="stats-grid">
            <div class="stat-item -no-background">
              <div class="stat-label">GHG Intensity</div>
              <div class="stat-value">{{ formatGHGIntensity(building.GHGIntensity) }}</div>
              <div class="stat-unit">kg CO₂e/sqft</div>
            </div>

            <div class="stat-item -no-background">
              <div class="stat-label">Total Emissions</div>
              <div class="stat-value">{{ formatNumber(building.TotalGHGEmissions) }}</div>
              <div class="stat-unit">tons CO₂e</div>
            </div>

            <div class="stat-item -no-background">
              <div class="stat-label text-center">Energy Mix</div>
              <div class="pie-chart-cont-inline">
                <PieChart
                  :id-prefix="'social-energy-mix'"
                  :graph-data="energyBreakdownData"
                />
              </div>
            </div>
          </div>
        </div>

        <div v-if="buildingImg" class="image-section">
          <img :src="buildingImg.imgUrl" :alt="propertyName" class="building-image" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IBuilding, calculateEnergyBreakdown } from '../common-functions.vue';
import { getBuildingImage, IBuildingImage } from '../constants/building-images.constant.vue';
import LetterGrade from './LetterGrade.vue';
import PieChart, { IPieSlice } from './graphs/PieChart.vue';

@Component({
  components: {
    LetterGrade,
    PieChart,
  },
})
export default class SocialCard extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  $page!: {
    building: IBuilding;
  };

  energyBreakdownData!: Array<IPieSlice>;

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

  created(): void {
    const breakdownWithTotal = calculateEnergyBreakdown(this.building);
    this.energyBreakdownData = breakdownWithTotal.energyBreakdown;
  }
}
</script>

<!--
 TODO:
   - Move to SCSS variables from colors.scss
   - Use border values from spacing.scss
   - Use rem instead of px
-->
<style lang="scss" scoped>
.social-card {
  width: 1200px;
  height: 630px;
  background: white;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
  border: 2px solid #e5e7eb;
}

.social-card-content {
  width: 100%;
  height: 100%;
  padding: 40px 60px 60px 60px;
  display: flex;
  flex-direction: column;
}

.header {
  margin-bottom: 20px;
}

.logo img {
  height: 32px;
}

.main-section {
  display: flex;
  gap: 40px;
  flex: 1;
  align-items: flex-start;
}

.text-content {
  flex: 1;
}

.image-section {
  flex: 0 0 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.building-image {
  max-width: 100%;
  max-height: 400px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.building-title-row {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.overall-grade-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  min-width: 120px;
}

.overall-grade-label {
  font-size: 14px;
  font-weight: 600;
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
  margin-top: 10px;

  // Override PieChart default sizing for inline display
  :deep(svg) {
    width: 15rem;
  }
}

.building-name {
  font-size: 42px;
  font-weight: bold;
  margin: 0 0 8px 0;
  line-height: 1.1;
  color: #1a1a1a;
}

.building-address {
  font-size: 20px;
  margin: 0;
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 30px;
  margin-bottom: 25px;
}

.stat-item {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  border: 1px solid #e5e7eb;

  &.-no-background {
    background: none;
    border: none;
    padding: 0;
  }
}

.stat-label {
  font-size: 16px;
  color: #666;
  margin-bottom: 6px;
  font-weight: 500;

  &.text-center {
    text-align: center;
  }
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 2px;
  color: #1a1a1a;
}

.stat-unit {
  font-size: 13px;
  color: #888;
}

.sub-grades {
  display: flex;
  gap: 20px;
  margin-bottom: 25px;
  padding: 15px 0;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
}

.sub-grade-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.sub-grade-label {
  color: #666;
  font-weight: 500;
  text-align: center;
  line-height: 1.3;
}

.letter-grade {
  font-size: 2.5rem;

  &.-large { font-size: 4rem; }
}
</style>