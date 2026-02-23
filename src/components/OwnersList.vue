<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import OwnerTile from './OwnerTile.vue';
import { IBuildingNode } from '../common-functions.vue';
import {
  calculateAllOwnerStats,
  getTopOwnersByEmissions,
  IOwnerWithStats,
} from '../constants/owner-helpers.vue';

/**
 * Component that displays a list of building owners with their stats
 */
@Component({
  components: {
    OwnerTile,
  },
})
export default class OwnersList extends Vue {
  @Prop({ required: true }) buildings!: Array<IBuildingNode>;

  /** Top owners to display (sorted by total emissions) */
  topOwners: Array<IOwnerWithStats> = [];

  created(): void {
    const ownerStats = calculateAllOwnerStats(this.buildings);
    this.topOwners = getTopOwnersByEmissions(ownerStats, 6);
  }
}
</script>

<template>
  <div class="owners-list-section">
    <div class="list-title">
      <h2>Building Owners</h2>
      <g-link class="bold" to="/large-owners">View All</g-link>
    </div>
    <p class="list-desc">
      Explore major property owners in Chicago and their environmental impact
    </p>

    <div class="buildings-scroll-cont">
      <ul class="building-tiles">
        <li v-for="ownerData in topOwners" :key="ownerData.owner.key">
          <OwnerTile :owner="ownerData.owner" :stats="ownerData.stats" />
        </li>
      </ul>
    </div>
  </div>
</template>
