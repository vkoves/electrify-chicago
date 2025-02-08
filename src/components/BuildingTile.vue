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
  <g-link :to="path" class="tile-link">
    <div class="building-tile">
      <g-link :to="path">
        <div class="img-cont">
          <!-- TODO: Figure out how to do alt text for these images - skipping for now -->
          <img v-if="buildingImg" :src="buildingImg.imgUrl" alt="" />
        </div>
      </g-link>

      <div class="text">
        <div class="title">
          <g-link :to="path">{{ building.PropertyName }}</g-link>
        </div>
        <div class="prop-type">{{ building.PrimaryPropertyType }}</div>

        <dl>
          <div>
            <dt>GHG Intensity</dt>
            <dd>
              <div class="value">{{ building.GHGIntensity }}</div>
              <div class="unit">kg CO<sub>2</sub> / sqft</div>
            </dd>
          </div>
          <div>
            <dt>Total Emissions</dt>
            <dd>
              <div class="value">{{ building.TotalGHGEmissions }}</div>
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
  width: 21.875rem; // 350px
  background-color: $grey-light;
  border-radius: $brd-rad-medium;
  overflow: hidden;
  box-shadow: 0 0 0.625rem 0.1875rem $box-shadow-main;
  height: 100%;
  transition: outline 0.3s;
  outline: solid $border-v-thick transparent;
  text-decoration: none;
  color: $text-main;
  margin: 0 0.25rem; // add margin for outline

  &:hover, &:focus-within { outline: solid $border-v-thick $chicago-blue; }

  .img-cont {
    background: radial-gradient(circle, rgba(238,174,202,1) 0%, rgba(148,187,233,1) 100%);;
    height: 16.875rem; // 270px

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

    .title {
      font-weight: bold;
      font-size: 1.25rem;
      line-height: 1.25;

      a {
        color: inherit;
        text-decoration: none;

        &:hover, &:focus {
          text-decoration: underline;
        }
      }
    }

    .prop-type, .unit {
      font-size: 0.75rem;
      color: $text-light;
      font-weight: bold;
    }

    dl {
      display: flex;
      gap: 2rem;
      margin-bottom: 0;

      dt { font-size: 0.75rem; }
      .value {
        font-weight: bold;
      }
      .unit { line-height: 1; }
    }
  }
}
</style>
