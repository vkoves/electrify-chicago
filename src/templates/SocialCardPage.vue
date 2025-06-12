<page-query>
query ($id: ID!) {
  building(id: $id) {
    ID
    Address
    PropertyName
    GHGIntensity
    TotalGHGEmissions
    GrossFloorArea
    AvgPercentileLetterGrade
    ElectricityUse
    NaturalGasUse
    DistrictSteamUse
    DistrictChilledWaterUse
    EnergyMixLetterGrade
    GHGIntensityLetterGrade
    SubmittedRecordsLetterGrade
  }
}
</page-query>

<template>
  <SocialCard />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import SocialCard from '../components/SocialCard.vue';

/**
 * The page for building's social cards, found at `/social-card/:buildingId`
 */
@Component({
  components: {
    SocialCard,
  },
})
export default class SocialCardPage extends Vue {}
</script>

<style>
/* Remove default body margins for clean screenshots */
body {
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}
</style>
