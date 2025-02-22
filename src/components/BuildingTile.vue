<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import { IBuilding } from '../common-functions.vue';
import {
  getBuildingImage,
  IBuildingImage,
} from '../constants/building-images.constant.vue';
import OwnerLogo from './OwnerLogo.vue';
import LetterGrade from './LetterGrade.vue';

/**
 * A component that renders a tile for a building
 */
@Component({
  components: {
    OwnerLogo,
    LetterGrade,
  },
})
export default class BuildingTile extends Vue {
  @Prop({ required: true }) building!: IBuilding;

  /** The URL going to this building */
  @Prop({ required: true }) path!: string;

  /**
   * Returns the image object associated with this image
   */
  get buildingImg(): IBuildingImage | null {
    return getBuildingImage(this.building);
  }

  /**
   * Whether a building is _fully_ gas free, meaning no gas burned on-site or to heat it
   * through a district heating system.
   */
  get fullyGasFree(): boolean {
    return (
      parseFloat(this.building.NaturalGasUse) === 0 &&
      parseFloat(this.building.DistrictSteamUse) === 0
    );
  }
}
</script>

<template>
  <div>
    <g-link :to="path" class="tile-link" tabindex="-1">
      <div class="building-tile">
        <div class="img-cont">
          <div class="pills-cont">
            <div v-if="fullyGasFree" class="pill -all-electric">
              <span>⚡</span> All Electric
            </div>
          </div>

          <OwnerLogo :building="building" :is-small="true" />

          <!-- TODO: Figure out how to do alt text for these images - skipping for now -->
          <img v-if="buildingImg" :src="buildingImg.imgUrl" alt="" />
        </div>

        <div class="text">
          <g-link :to="path">
            <div class="title">
              {{ building.PropertyName }}
            </div>
          </g-link>
          <div class="prop-type">{{ building.PrimaryPropertyType }}</div>

          <div class="stats">
            <dl>
              <div>
                <dt>GHG Intensity</dt>
                <dd>
                  <div class="value">
                    {{
                      parseFloat(
                        building.GHGIntensity.toString(),
                      ).toLocaleString()
                    }}
                  </div>
                  <div class="unit">kg CO<sub>2</sub> / sqft</div>
                </dd>
              </div>
              <div>
                <dt>Total Emissions</dt>
                <dd>
                  <div class="value">
                    {{
                      parseInt(
                        building.TotalGHGEmissions.toString(),
                      ).toLocaleString()
                    }}
                  </div>
                  <div class="unit">tons CO<sub>2</sub>e</div>
                </dd>
              </div>
            </dl>

            <div class="grade-cont">
              <LetterGrade :grade="building.AvgPercentileLetterGrade" />

              <div>Overall Grade</div>
            </div>
          </div>
        </div>
      </div>
    </g-link>
  </div>
</template>

<style lang="scss">
.tile-link {
  text-decoration: none;
}

.building-tile {
  width: 20rem; // 320px
  background-color: $grey-light;
  border-radius: $brd-rad-medium;
  overflow: hidden;
  box-shadow: 0.125rem 0.125rem 0.75rem $box-shadow-main;
  height: 100%;
  transition: outline 0.3s;
  outline: solid $border-v-thick transparent;
  text-decoration: none;
  color: $text-main;

  &:hover,
  &:focus-within {
    outline: solid $border-v-thick $chicago-blue;
  }

  .img-cont {
    position: relative;
    background: radial-gradient(
      circle,
      rgba(238, 174, 202, 1) 0%,
      rgba(148, 187, 233, 1) 100%
    );
    height: 15rem; // 240px

    .owner-cont {
      position: absolute;
      top: 0;
      left: 0;
      background: $white;
      top: 0;
      margin: 0;
      border-bottom-right-radius: $brd-rad-medium;

      &:hover,
      &:focus-within {
        background-color: $grey-light;
      }

      a {
        padding: 0.5rem 1rem;
      }

      img {
        display: block;
        height: 1.5rem;
        width: auto;
      }
    }

    .pills-cont {
      position: absolute;
      top: 0.5rem;
      right: 0.5rem;

      .pill {
        font-weight: bold;
        padding: 0.125rem 1rem;
        border-radius: 1rem;
        font-size: 0.875rem;

        &.-all-electric {
          background: #fff6aa;
          color: #9e5e00;
        }

        span {
          text-shadow: 0.0625rem 0 0.0625rem $black;
        }
      }
    }

    img {
      height: 100%;
      width: 100%;
      object-fit: cover;
      // show near the top of the image
      object-position: 50% 10%;
    }
  }

  .text {
    padding: 0.75rem 1rem;

    a {
      display: block;
      color: inherit;
      text-decoration: none;

      &:focus {
        text-decoration: underline;
      }
    }

    .title {
      font-weight: bold;
      font-size: 1.125rem;
      line-height: 1.25;
      // Truncate with ellipsis, don't wrap
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }

    .prop-type,
    .unit {
      color: $text-mid-light;
      font-weight: bold;
    }

    .prop-type {
      font-size: 0.875rem;
    }

    .unit {
      font-size: 0.75rem;
    }

    .stats {
      display: flex;
      justify-content: space-between;
    }

    dl {
      display: flex;
      gap: 2rem;
      margin-bottom: 0;

      dt {
        font-size: 0.75rem;
      }
      .value {
        font-weight: bold;
      }
      .unit {
        line-height: 1;
      }
    }

    .grade-cont {
      font-size: 0.6125rem;
      color: $text-mid-light;
      margin-top: 0.25rem;
      margin-right: 1.25rem;
      text-align: center;

      .letter-grade {
        font-size: 2.5rem;
        line-height: 1.25;
      }
    }
  }
}
</style>
