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
  }
}
</page-query>

<template>
  <SocialCard />
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import SocialCard from '../components/SocialCard.vue';

@Component({
  components: {
    SocialCard,
  },
})
export default class SocialCardTemplate extends Vue {}
</script>

<style>
/* Remove default body margins for clean screenshots */
body {
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}
</style>