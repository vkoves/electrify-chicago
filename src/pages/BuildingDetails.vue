<page-query>
query ($id: ID!) {
  building(id: $id) {
    Address
    ElectricityUse
    GHGIntensity
    GrossFloorArea
    NaturalGasUse
    NumberOfBuildings
    PrimaryPropertyType
    PropertyName
    TotalGHGEmissions
    YearBuilt
    ZIPCode
  }
}
</page-query>

<template>
  <DefaultLayout>
    <div>
      <h1 v-html="$page.building.PropertyName" />

      <dl>
        <dt>Full Address</dt>
        <dd>{{ $page.building.Address }}, Chicago IL, {{ $page.building.ZIPCode }}</dd>

        <dt>Square Footage</dt>
        <dd>{{ $page.building.GrossFloorArea }} sq. feet</dd>

        <dt>Year Built</dt>
        <dd>{{ $page.building.YearBuilt }}</dd>

        <dt>Primary Property Type</dt>
        <dd>{{ $page.building.PrimaryPropertyType }}</dd>

        <dt>Number of Buildings</dt>
        <dd>{{ $page.building.NumberOfBuildings }}</dd>

        <dt>GHG Intensity</dt>
        <dd>
          <template v-if="$page.building.GHGIntensity">
            {{ $page.building.GHGIntensity }} kg CO<sub>2</sub>/sqft
          </template>
          <template v-else>?</template>
        </dd>

        <dt>Total GHG Emissions</dt>
        <dd>
          <template v-if="$page.building.TotalGHGEmissions">
            {{ $page.building.TotalGHGEmissions }} metric tons CO<sub>2</sub>
          </template>
          <template v-else>?</template>
        </dd>

        <dt>Natural Gas Use</dt>
        <dd>
          <template v-if="$page.building.NaturalGasUse">
            {{ $page.building.NaturalGasUse }} kBtu
          </template>
          <template v-else>?</template>
        </dd>

        <dt>Electricity Use</dt>
        <dd>
          <template v-if="$page.building.ElectricityUse">
            {{ $page.building.ElectricityUse }} kBtu
          </template>
          <template v-else>?</template>
        </dd>
      </dl>

    </div>
  </DefaultLayout>
</template>

<script>
export default {
  metaInfo() {
    return {
      title: this.$page.building.PropertyName,
    };
  },
};
</script>
