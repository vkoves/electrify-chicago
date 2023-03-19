<page-query>
query ($id: ID!) {
  building(id: $id) {
    Address
    PropertyName
    GHGIntensity
    GrossFloorArea
    TotalGHGEmissions
    YearBuilt
    ElectricityUse
    NaturalGasUse
  }
}
</page-query>

<template>
  <Layout>
    <div>
      <h1 v-html="$page.building.PropertyName" />

      Address
      {{ $page.building.Address }}

      GHG Intensity
      <template v-if="$page.building.GHGIntensity">
        {{ $page.building.GHGIntensity }}
      </template>
      <template v-else>?</template>

      Total GHG Emissions
      <template v-if="$page.building.TotalGHGEmissions">
        {{ $page.building.TotalGHGEmissions }}
      </template>
      <template v-else>?</template>

      Natural Gas Use

      <template v-if="$page.building.NaturalGasUse">
        {{ $page.building.NaturalGasUse }}
      </template>
      <template v-else>?</template>

      Electricity Use
      <template v-if="$page.building.ElectricityUse">
        {{ $page.building.ElectricityUse }}
      </template>
      <template v-else>?</template>
    </div>
  </Layout>
</template>

<script>
export default {
  metaInfo() {
    return {
      title: this.$page.building.PropertyName
    }
  }
}
</script>