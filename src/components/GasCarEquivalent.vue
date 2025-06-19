<template>
  <div class="gas-car-equivalent">
    <div class="gas-car-visual">
      <div class="car-rows-container">
        <div 
          v-for="row in carRowsToShow" 
          :key="row.rowIndex"
          class="car-row"
          :class="{ '-faded': row.rowIndex > 0 }"
        >
          <div 
            v-for="(car, carIndex) in row.cars" 
            :key="carIndex"
            class="car-icon"
            :class="{ '-partial': car.isPartial }"
          >
            <img 
              src="/icons/car.svg" 
              alt="Car icon"
              :style="
                car.isPartial && car.percentage 
                  ? `clip-path: inset(0 ${100 - car.percentage}% 0 0)` 
                  : ''
              "
            />
          </div>
        </div>
      </div>
      <div class="car-count-text">
        <span class="gas-car-number">{{ gasCarThousands.toFixed(1) }}k</span>
        cars worth of emissions annually*
      </div>
    </div>
    <p class="footnote gas-car-footnote">
      *Based on EPA estimate of 4.6 metric tons CO₂ per year for a 
      <a 
        href="https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle" 
        target="_blank" 
        rel="noopener"
      >
        typical passenger vehicle <NewTabIcon />
      </a>
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { calculateGasCarEquivalent } from '../common-functions.vue';
import NewTabIcon from './NewTabIcon.vue';

interface ICarIcon {
  isPartial: boolean;
  percentage?: number;
}

interface ICarRow {
  cars: Array<ICarIcon>;
  rowIndex: number;
}

@Component({
  components: {
    NewTabIcon,
  },
})
export default class GasCarEquivalent extends Vue {
  @Prop({ required: true }) totalGHGEmissions!: number;

  /** Calculate how many gas cars worth of emissions this building produces annually */
  get gasCarEquivalent(): number {
    return calculateGasCarEquivalent(this.totalGHGEmissions);
  }

  /** Calculate how many thousands of cars for visual display */
  get gasCarThousands(): number {
    return this.gasCarEquivalent / 1000;
  }

  /** Get rows of car icons to display (up to 10 cars per row) */
  get carRowsToShow(): Array<ICarRow> {
    const thousands = this.gasCarThousands;
    const totalCars = Math.floor(thousands);
    const remainder = thousands - totalCars;
    
    const CARS_PER_ROW = 10;
    const MAX_ROWS = 5; // Limit to prevent excessive visual clutter
    const rows = [];
    
    let carsProcessed = 0;
    let rowIndex = 0;
    
    // Create rows of cars
    while (carsProcessed < totalCars && rowIndex < MAX_ROWS) {
      const carsInThisRow = Math.min(CARS_PER_ROW, totalCars - carsProcessed);
      const cars: Array<ICarIcon> = [];
      
      // Add whole cars for this row
      for (let i = 0; i < carsInThisRow; i++) {
        cars.push({ isPartial: false });
      }
      
      rows.push({ cars, rowIndex });
      carsProcessed += carsInThisRow;
      rowIndex++;
    }
    
    // Add partial car to the last row if there's a remainder and space
    if (remainder > 0.1 && rows.length > 0) {
      const lastRow = rows[rows.length - 1];
      if (lastRow.cars.length < CARS_PER_ROW) {
        lastRow.cars.push({ isPartial: true, percentage: remainder * 100 });
      }
    }
    
    return rows;
  }
}
</script>

<style lang="scss" scoped>
.gas-car-equivalent {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background-color: $grey-light;
  border-radius: $brd-rad-small;
  font-size: 0.875rem;

  .gas-car-visual {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }

  .car-rows-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.125rem; // Tight spacing between rows
  }

  .car-row {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    justify-content: center;
    opacity: 1;
    transition: opacity 0.2s ease;

    &.-faded {
      opacity: 0.4; // Fade non-top rows
    }
  }

  .car-icon {
    height: 1.5rem;
    width: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;

    img {
      height: 100%;
      width: auto;
      filter: brightness(0.7); // Darken the car icons slightly
    }

    &.-partial img {
      opacity: 0.6;
    }
  }

  .car-count-text {
    text-align: center;
    line-height: 1.3;
    margin-top: 0.25rem;
  }

  .gas-car-number {
    font-weight: bold;
    color: $blue-dark;
    font-size: 1.125rem;
  }

  .gas-car-footnote {
    margin-top: 0.5rem;
    margin-bottom: 0;
  }
}
</style>