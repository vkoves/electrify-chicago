<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IBuildingOwner } from '../constants/buildings-custom-info.constant.vue';
import { IOwnerStats } from '../constants/owner-helpers.vue';

/**
 * A component that renders a tile for a building owner with key stats
 */
@Component
export default class OwnerTile extends Vue {
  @Prop({ required: true }) owner!: IBuildingOwner;
  @Prop({ required: true }) stats!: IOwnerStats;
}
</script>

<template>
  <div>
    <g-link :to="'/owner/' + owner.key + '/'" class="tile-link" tabindex="-1">
      <div class="owner-tile">
        <div class="logo-cont">
          <img :src="owner.logoLarge" :alt="owner.name" />
        </div>

        <div class="main-text">
          <g-link :to="'/owner/' + owner.key + '/'">
            <div class="title">
              {{ owner.name }}
            </div>
          </g-link>

          <div class="stats">
            <dl>
              <div>
                <dt>Buildings</dt>
                <dd>
                  <div class="value">
                    {{ stats.buildingCount }}
                  </div>
                </dd>
              </div>
              <div>
                <dt>Total Emissions</dt>
                <dd>
                  <div class="value">
                    {{ Math.round(stats.totalGHGEmissions).toLocaleString() }}
                  </div>
                  <div class="unit">tons CO<sub>2</sub>e</div>
                </dd>
              </div>
              <div>
                <dt>Avg GHG Intensity</dt>
                <dd>
                  <div class="value">
                    {{ stats.avgGHGIntensity.toFixed(1) }}
                  </div>
                  <div class="unit">kg CO<sub>2</sub> / sqft</div>
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </g-link>
  </div>
</template>

<style lang="scss">
.owner-tile {
  width: 20rem; // 320px - same as BuildingTile
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

  .logo-cont {
    display: flex;
    align-items: center;
    justify-content: center;
    background: $white;
    height: 10rem; // 160px - shorter than BuildingTile
    padding: 1.5rem;

    img {
      max-height: 100%;
      max-width: 100%;
      object-fit: contain;
    }
  }

  .main-text {
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
      line-height: 1.5;
      margin-bottom: 0.5rem;
    }

    .stats {
      margin-top: 0.5rem;
    }

    dl {
      display: flex;
      gap: 1rem;
      margin-bottom: 0;

      dt {
        font-size: 0.75rem;
        color: $text-mid-light;
        font-weight: bold;
      }

      dd {
        margin: 0;
      }

      .value {
        font-weight: bold;
        font-size: 1rem;
      }

      .unit {
        font-size: 0.75rem;
        color: $text-mid-light;
        font-weight: bold;
        line-height: 1;
      }
    }
  }
}
</style>
