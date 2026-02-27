<page-query>
query {
  # Get all buildings - we'll filter by property type in component
  allBuilding(sortBy: "GrossFloorArea", order: DESC) {
    edges {
      node {
        ID
        Address
        PropertyName
        PrimaryPropertyType
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
  <PropertyTypeSocialCard />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import PropertyTypeSocialCard from '../../components/social-cards/PropertyTypeSocialCard.vue';

/**
 * The template for property type social cards, found at `/property-type-social-card/:propertyType`
 */
@Component({
  components: {
    PropertyTypeSocialCard,
  },
})
export default class PropertyTypeSocialCardTemplate extends Vue {
  /** Context passed from gridsome.server.js */
  readonly $context!: { propertyType: string };

  /** Get property type from context (passed from gridsome.server.js) */
  get propertyType(): string {
    return this.$context.propertyType || '';
  }
}
</script>
