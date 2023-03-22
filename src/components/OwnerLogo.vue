<template>
    <!-- On large views we'll say the owner is unknown, in a table we output nothing -->
    <div v-if="owner || !isSmall" class="owner-cont" :class="{
        '-small': isSmall,
        '-unknown': !owner
    }">
        <template v-if="owner">
            <img v-if="!isSmall" :src="ownerLogoSrc" :alt="owner.name"/>
            <div v-if="!isSmall" class="owner-label">
                <strong>Note:</strong> Owner manually tagged
            </div>

            <!-- If small view should short building name -->
            <span v-if="isSmall">({{ owner.nameShort }})</span>
        </template>

        <div v-if="!isSmall && !owner">Unknown</div>
    </div>
</template>

<script>
// The function Gridsome uses to make slugs, so it should match
import slugify from '@sindresorhus/slugify';
import {BuildingsCustomInfo, BuildingOwners} from '../constants/buildings-custom-info';

/**
 * A component that given a building shows the logo of its owner if one is set in
 * BuildingsCustomInfo
 */
export default {
  name: 'OwnerLogo',
  props: {
    building: Object,
    isSmall: Boolean,
  },
  computed: {
    /**
     * Returns the BuildingOwners object associated with the passed building so we can get the logo
     * and name, if one was set.
     *
     * @return {IBuildingOwner | null}
     */
    owner() {
      const buildingSlug = slugify(this.building.slugSource);
      const buildingCustomInfo = BuildingsCustomInfo[buildingSlug];

      if (buildingCustomInfo) {
        return BuildingOwners[buildingCustomInfo.owner];
      }

      return null;
    },

    /**
     * Returns a path to the owner logo, if the owner is known
     *
     * @return {string|null}
     */
    ownerLogoSrc() {
      if (!this.owner) {
        return null;
      }

      return this.isSmall ? this.owner.logoSmall : this.owner.logoLarge;
    },
  },
};
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
