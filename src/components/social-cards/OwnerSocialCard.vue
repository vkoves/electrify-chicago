<template>
  <BaseSocialCard :buildings="buildings">
    <template #hero-content>
      <div class="owner-info">
        <div class="top-title">Emissions for Buildings Owned By</div>
        <img
          v-if="owner.logoLarge"
          :src="owner.logoLarge"
          :alt="owner.name + ' logo'"
          class="owner-logo"
        />
        <h1 class="owner-name">{{ owner.name }}</h1>
      </div>
    </template>
  </BaseSocialCard>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IBuilding } from '../../common-functions.vue';
import {
  IBuildingOwner,
  BuildingsCustomInfo,
  IBuildingCustomInfo,
} from '../../constants/buildings-custom-info.constant.vue';
import BaseSocialCard from './BaseSocialCard.vue';

/**
 * Our social card page for generating meta imagery for building owners, showing the images for the
 * some of the buildings they own plus their logo
 */
@Component({
  components: {
    BaseSocialCard,
  },
})
export default class OwnerSocialCard extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  $page!: {
    allBuilding: {
      edges: Array<{ node: IBuilding }>;
    };
  };

  /** Get the current owner from parent context */
  get owner(): IBuildingOwner {
    return (
      (this.$parent as any).owner || {
        key: 'default',
        name: 'Building Owner',
        nameShort: 'Owner',
        logoLarge: '',
      }
    );
  }

  /** Get buildings for the hero section */
  get buildings(): Array<IBuilding> {
    const allBuildings = this.$page.allBuilding.edges.map((edge) => edge.node);
    const ownerId = this.owner.key;

    // Filter buildings by owner ID using BuildingsCustomInfo
    const ownerBuildingIds = Object.entries(BuildingsCustomInfo)
      .filter(([, buildingInfo]: [string, IBuildingCustomInfo]) => {
        return buildingInfo.owner === ownerId;
      })
      .map(([buildingId]: [string, IBuildingCustomInfo]) => buildingId);

    const ownerBuildings = allBuildings.filter((building) => {
      return ownerBuildingIds.includes(String(building.ID));
    });

    // Return top 50 buildings for this owner, sorted by floor area
    return ownerBuildings
      .sort((a, b) => (b.GrossFloorArea || 0) - (a.GrossFloorArea || 0))
      .slice(0, 50);
  }
}
</script>

<style lang="scss" scoped>
.owner-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;

  .top-title {
    font-size: 2.5rem;
    font-weight: bold;
    margin: 0;
  }

  :deep(.buildings-hero) {
    // Make the overlay full height
    .hero-overlay {
      top: 0;
      display: flex;
      align-items: center;
    }
  }

  .owner-logo {
    max-height: 10rem;
    max-width: 50rem;
    object-fit: contain;
    padding: 0.5rem 1rem;
    border-radius: 1rem;
    background-color: $white;
  }

  h1.owner-name {
    font-size: 3rem;
    font-weight: bold;
    line-height: 1;
    margin-top: 1rem;
    margin-bottom: 5rem;
  }
}
</style>
