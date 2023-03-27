<template>
  <!-- On large views we'll say the owner is unknown, in a table we output nothing -->
  <div
    v-if="owner || !isSmall"
    class="owner-cont"
    :class="{
      '-small': isSmall,
      '-unknown': !owner
    }"
  >
    <template v-if="owner">
      <img
        v-if="!isSmall"
        :src="ownerLogoSrc"
        :alt="owner.name"
      >
      <div
        v-if="!isSmall"
        class="owner-label"
      >
        <strong>Note:</strong> Owner manually tagged
      </div>

      <!-- If small view should short building name -->
      <span v-if="isSmall">({{ owner.nameShort }})</span>
    </template>

    <div v-if="!isSmall && !owner">
      Not Tagged
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import {IBuilding} from '~/common-functions.vue';
import {
  BuildingsCustomInfo,
  IBuildingOwner,
  BuildingOwners,
} from '~/constants/buildings-custom-info.constant.vue';
import { getBuildingCustomInfo } from '../constants/buildings-custom-info.constant.vue';

/**
 * A component that given a building shows the logo of its owner if one is set in
 * BuildingsCustomInfo
 */
@Component
export default class OwnerLogo extends Vue {
  @Prop({required: true}) building!: IBuilding;
  @Prop({ default: false }) isSmall!: boolean;

  /**
   * Returns the BuildingOwners object associated with the passed building so we can get the logo
   * and name, if one was set.
   */
  get owner(): IBuildingOwner | null {
    const buildingCustomInfo = getBuildingCustomInfo(this.building);

    if (buildingCustomInfo?.owner) {
      return BuildingOwners[buildingCustomInfo.owner];
    }

    return null;
  }

  /**
   * Returns a path to the owner logo, if the owner is known
   */
  get ownerLogoSrc(): string | null {
    const logo = this.isSmall ? this.owner?.logoSmall : this.owner?.logoLarge;

    return logo ?? null;
  }
}
</script>

<style lang="scss">
.owner-cont {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;

  &.-small, &.-unknown { margin: 0; }

  &.-small {
    display: inline-block;
    font-size: small;
    margin: 0;
  }

  .owner-label {
    margin-bottom: 0.5rem;
    font-size: smaller;
  }

  img { width: 20rem; }
}
</style>
