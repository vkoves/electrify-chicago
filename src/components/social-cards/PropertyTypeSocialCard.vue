<template>
  <BaseSocialCard :buildings="buildings">
    <template #hero-content>
      <div class="property-type-info">
        <div class="property-type-name">{{ propertyTypePlural }}</div>
        <div class="property-type-count">
          {{ buildingCount }} building{{ buildingCount !== 1 ? 's' : '' }}
        </div>
      </div>
    </template>
  </BaseSocialCard>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { IBuilding, pluralizePropertyType } from '../../common-functions.vue';
import BaseSocialCard from './BaseSocialCard.vue';

/**
 * Social card for property type pages, showing buildings of that type
 */
@Component({
  components: {
    BaseSocialCard,
  },
})
export default class PropertyTypeSocialCard extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  $page!: {
    allBuilding: {
      edges: Array<{ node: IBuilding }>;
    };
  };

  /** Get the current property type from parent context */
  get propertyType(): string {
    return (this.$parent as { propertyType?: string }).propertyType || '';
  }

  /** Get the pluralized property type name */
  get propertyTypePlural(): string {
    return pluralizePropertyType(this.propertyType);
  }

  /** Get buildings for the hero section */
  get buildings(): Array<IBuilding> {
    const allBuildings = this.$page.allBuilding.edges.map((edge) => edge.node);

    // Filter buildings by property type
    const typeBuildings = allBuildings.filter(
      (building) => building.PrimaryPropertyType === this.propertyType,
    );

    // Get all buildings of this type, since we show a count
    return typeBuildings
      .sort((a, b) => (b.GrossFloorArea || 0) - (a.GrossFloorArea || 0));
  }

  get buildingCount(): number {
    return this.buildings.length;
  }
}
</script>

<style lang="scss" scoped>
.property-type-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;

  .property-type-name {
    font-size: 6rem;
    font-weight: bold;
    line-height: 1;
    margin: 0;
  }

  .property-type-count {
    font-size: 2.5rem;
    margin: 0;
    line-height: 1;
  }
}
</style>
