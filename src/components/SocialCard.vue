<template>
  <div class="social-card">
    <div class="social-card-content">
      <div class="building-info">
        <h1 class="building-name">{{ propertyName }}</h1>
        <p class="building-address">{{ building.Address }}</p>
      </div>
      
      <div class="stats-grid">
        <div class="stat-item primary">
          <div class="stat-label">Overall Grade</div>
          <div class="stat-value">
            <LetterGrade :grade="building.AvgPercentileLetterGrade" class="-social" />
          </div>
        </div>
        
        <div class="stat-item">
          <div class="stat-label">GHG Intensity</div>
          <div class="stat-value">{{ formatNumber(building.GHGIntensity) }}</div>
          <div class="stat-unit">kg CO₂e/sqft</div>
        </div>
        
        <div class="stat-item">
          <div class="stat-label">Total Emissions</div>
          <div class="stat-value">{{ formatNumber(building.TotalGHGEmissions) }}</div>
          <div class="stat-unit">tons CO₂e</div>
        </div>
        
        <div class="stat-item">
          <div class="stat-label">Square Footage</div>
          <div class="stat-value">{{ formatNumber(building.GrossFloorArea) }}</div>
          <div class="stat-unit">sqft</div>
        </div>
      </div>
      
      <div class="footer">
        <div class="logo">
          <img src="/electrify-chicago-logo.svg" alt="Electrify Chicago" />
        </div>
        <div class="url">electrify-chicago.com</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IBuilding } from '../common-functions.vue';
import LetterGrade from './LetterGrade.vue';

@Component({
  components: {
    LetterGrade,
  },
})
export default class SocialCard extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  $page!: {
    building: IBuilding;
  };

  /** A helper to get the current building, but with proper typing */
  get building(): IBuilding {
    return this.$page.building;
  }

  /** Helper for property name with address fallback */
  get propertyName(): string {
    return this.building.PropertyName || this.building.Address;
  }

  formatNumber(value: number): string {
    if (!value) return '—';
    return Math.round(value).toLocaleString();
  }
}
</script>

<style lang="scss" scoped>
.social-card {
  width: 1200px;
  height: 630px;
  background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 100%);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
}

.social-card-content {
  width: 100%;
  height: 100%;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.building-info {
  text-align: center;
  margin-bottom: 40px;
}

.building-name {
  font-size: 48px;
  font-weight: bold;
  margin: 0 0 12px 0;
  line-height: 1.1;
  color: white;
}

.building-address {
  font-size: 24px;
  margin: 0;
  opacity: 0.9;
  color: #e8f5e8;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin: 40px 0;
}

.stat-item {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
  
  &.primary {
    grid-column: 1 / -1;
    background: rgba(255, 255, 255, 0.15);
  }
}

.stat-label {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 4px;
  
  .primary & {
    font-size: 48px;
  }
}

.stat-unit {
  font-size: 14px;
  opacity: 0.8;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.logo img {
  height: 40px;
  filter: brightness(0) invert(1);
}

.url {
  font-size: 20px;
  font-weight: 500;
  opacity: 0.9;
}

// Letter grade styling for social cards
:deep(.letter-grade.-social) {
  font-size: 48px !important;
  width: auto !important;
  height: auto !important;
  padding: 12px 20px !important;
  border-radius: 12px !important;
  
  &.-a { background-color: #22c55e !important; }
  &.-b { background-color: #84cc16 !important; }
  &.-c { background-color: #eab308 !important; }
  &.-d { background-color: #f97316 !important; }
  &.-f { background-color: #ef4444 !important; }
}
</style>