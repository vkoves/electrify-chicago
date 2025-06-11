<template>
  <div class="social-card">
    <div class="social-card-content">
      <div class="main-section">
        <div class="text-content">
          <div class="building-info">
            <h1 class="building-name">{{ propertyName }}</h1>
            <p class="building-address">{{ building.Address }}</p>
          </div>
          
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-label">Overall Grade</div>
              <div class="stat-value">
                <LetterGrade :grade="building.AvgPercentileLetterGrade" class="-large" />
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-label">GHG Intensity</div>
              <div class="stat-value">{{ formatGHGIntensity(building.GHGIntensity) }}</div>
              <div class="stat-unit">kg CO₂e/sqft</div>
            </div>
            
            <div class="stat-item">
              <div class="stat-label">Total Emissions</div>
              <div class="stat-value">{{ formatNumber(building.TotalGHGEmissions) }}</div>
              <div class="stat-unit">tons CO₂e</div>
            </div>
          </div>
        </div>
        
        <div v-if="buildingImg" class="image-section">
          <img :src="buildingImg.imgUrl" :alt="propertyName" class="building-image" />
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
import { getBuildingImage, IBuildingImage } from '../constants/building-images.constant.vue';
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
      maximumFractionDigits: 1 
    });
  }
}
</script>

<style lang="scss" scoped>
.social-card {
  width: 1200px;
  height: 630px;
  background: white;
  color: #1a1a1a;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.main-section {
  display: flex;
  gap: 40px;
  flex: 1;
  align-items: center;
}

.text-content {
  flex: 1;
}

.image-section {
  flex: 0 0 300px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.building-image {
  max-width: 100%;
  max-height: 400px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.building-info {
  margin-bottom: 30px;
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
  gap: 20px;
}

.stat-item {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  border: 1px solid #e5e7eb;
}

.stat-label {
  font-size: 16px;
  color: #666;
  margin-bottom: 6px;
  font-weight: 500;
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

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.logo img {
  height: 36px;
}

.url {
  font-size: 18px;
  font-weight: 500;
  color: #1a472a;
}

// Use global letter-grade styling with -large modifier for bigger size
</style>