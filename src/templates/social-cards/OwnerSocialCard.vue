<page-query>
query {
  # Get all buildings - we'll filter by owner in component
  allBuilding(sortBy: "GrossFloorArea", order: DESC) {
    edges {
      node {
        ID
        Address
        PropertyName
        GrossFloorArea
        AvgPercentileLetterGrade
        GHGIntensityLetterGrade
        EnergyMixLetterGrade
        SubmittedRecordsLetterGrade
        GHGIntensity
        TotalGHGEmissions
        ElectricityUse
        NaturalGasUse
        DistrictSteamUse
        DistrictChilledWaterUse
      }
    }
  }
}
</page-query>

<template>
  <OwnerSocialCard />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import OwnerSocialCard from '../../components/social-cards/OwnerSocialCard.vue';
import { BuildingOwners, IBuildingOwner } from '../../constants/buildings-custom-info.constant.vue';

/**
 * The template for owner social cards, found at `/owner-social-card/:ownerId`
 */
@Component({
  components: {
    OwnerSocialCard,
  },
})
export default class OwnerSocialCardTemplate extends Vue {
  /** Get owner info from context (passed from gridsome.server.js) */
  get owner(): IBuildingOwner {
    // ownerId is available from GraphQL context
    const ownerId = (this as any).$context.ownerId;

    return (
      BuildingOwners[ownerId] || {
        key: 'default',
        name: 'Building Owner',
        nameShort: 'Owner',
        logoLarge: '',
      }
    );
  }
}
</script>