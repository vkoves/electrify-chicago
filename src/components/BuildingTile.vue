<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import { IBuilding } from '../common-functions.vue';
import {
  getBuildingImage,
  IBuildingImage,
} from '../constants/building-images.constant.vue';

/**
 * A component that renders a tile for a building
 */
@Component({
  components: {},
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

  get currentYear(): number {
    return new Date().getFullYear();
  }
}
</script>

<template>
  <g-link :to="path" class="tile-link" tabindex="-1">
    <div class="building-tile">
      <div class="img-cont">
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

        <dl>
          <div>
            <dt>GHG Intensity</dt>
            <dd>
              <div class="value">
                {{
                  parseFloat(building.GHGIntensity.toString()).toLocaleString()
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
      </div>
    </div>
  </g-link>
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
  box-shadow: 0 0 0.75rem $box-shadow-main;
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
    background: radial-gradient(
      circle,
      rgba(238, 174, 202, 1) 0%,
      rgba(148, 187, 233, 1) 100%
    );
    height: 15rem; // 240px

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
      width: fit-content;
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
      font-size: 0.75rem;
      color: $text-light;
      font-weight: bold;
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
  }
}
</style>
