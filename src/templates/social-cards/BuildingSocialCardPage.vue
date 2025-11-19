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
  <BuildingSocialCard />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import BuildingSocialCard from '../../components/social-cards/BuildingSocialCard.vue';

/**
 * The page for building's social cards, found at `/social-card/:buildingId`
 */
@Component({
  components: {
    BuildingSocialCard,
  },
})
export default class BuildingSocialCardPage extends Vue {}
</script>

<style></style>
