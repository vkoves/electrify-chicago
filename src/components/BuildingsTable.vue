<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import RankText from '~/components/RankText.vue';
import OverallRankEmoji from './OverallRankEmoji.vue';
import OwnerLogo from './OwnerLogo.vue';
import { IBuilding } from '~/common-functions.vue';


// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import { IBuildingBenchmarkStats } from '~/common-functions.vue';

@Component({
  components: {
    RankText,
    OverallRankEmoji,
    OwnerLogo,
  },
})
export default class BuildingsTable extends Vue {
  /** Expose stats to template */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats = BuildingBenchmarkStats;

  @Prop({required:true}) buildings!: Array<{ node: IBuilding }>;

  @Prop({default: false}) showSquareFootage!: boolean;

  @Prop({default: false}) showGasUse!: boolean;

  @Prop({default: false}) showElectricityUse!: boolean;
}
</script>

<template>
  <div class="table-cont">
    <table :class="{ '-wide': showSquareFootage || showGasUse || showElectricityUse }">
      <thead>
        <tr>
          <th scope="col">
            Property Name / address
          </th>
          <th
            scope="col"
            class="prop-type"
          >
            Primary Property Type
          </th>
          <th v-if="showSquareFootage">
            Square Footage
          </th>
          <th
            v-if="showGasUse"
            scope="col"
            class="numeric wide-col"
          >
            Natural Gas Use<br>
            <span class="unit">(kBtu)</span>
          </th>
          <th
            v-if="showElectricityUse"
            scope="col"
            class="numeric wide-col"
          >
            Electricity Use<br>
            <span class="unit">(kBtu)</span>
          </th>
          <th
            scope="col"
            class="numeric wide-col"
          >
            Greenhouse Gas Intensity<br>
            <span class="unit">(kg CO<sub>2</sub> eq./sqft)</span>
          </th>
          <th
            scope="col"
            class="numeric wide-col"
          >
            Total Greenhouse Emissions<br>
            <span class="unit">(metric tons CO<sub>2</sub> eq.)</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="edge in buildings"
          :key="edge.node.id"
        >
          <td class="property-name">
            <g-link :to="edge.node.path">
              {{ edge.node.PropertyName || edge.node.Address }}
            </g-link>
            <OverallRankEmoji
              :building="edge.node"
              :stats="BuildingBenchmarkStats"
            />
            <OwnerLogo
              :building="edge.node"
              :is-small="true"
            />

            <div class="prop-address">
              {{ edge.node.Address }}
            </div>
          </td>
          <td>{{ edge.node.PrimaryPropertyType }}</td>

          <!-- Square footage is optional, only shown on BiggestBuildings -->
          <td
            v-if="showSquareFootage"
            class="numeric"
          >
            <template v-if="edge.node.GrossFloorArea">
              <RankText
                :building="edge.node"
                :should-round="true"
                :stats="BuildingBenchmarkStats"
                :unit="'sqft'"
                stat-key="GrossFloorArea"
              />
            </template>
            <template v-else>
              -
            </template>
          </td>

          <td
            v-if="showGasUse"
            class="numeric"
          >
            <template v-if="edge.node.NaturalGasUse">
              <RankText
                :building="edge.node"
                :should-round="true"
                :stats="BuildingBenchmarkStats"
                :unit="'kBtu'"
                stat-key="NaturalGasUse"
              />
            </template>
            <template v-else>
              -
            </template>
          </td>
          <td
            v-if="showElectricityUse"
            class="numeric"
          >
            <template v-if="edge.node.ElectricityUse">
              <RankText
                :building="edge.node"
                :should-round="true"
                :stats="BuildingBenchmarkStats"
                :unit="'kBtu'"
                stat-key="ElectricityUse"
              />
            </template>
            <template v-else>
              -
            </template>
          </td>

          <!-- GHG Intensity is shown on all tables -->
          <td class="numeric">
            <template v-if="edge.node.GHGIntensity">
              <RankText
                :building="edge.node"
                :stats="BuildingBenchmarkStats"
                stat-key="GHGIntensity"
                :unit="'kg/sqft'"
              />
            </template>
            <template v-else>
              -
            </template>
          </td>
          <td class="numeric">
            <template v-if="edge.node.TotalGHGEmissions">
              <RankText
                :building="edge.node"
                :should-round="true"
                :stats="BuildingBenchmarkStats"
                stat-key="TotalGHGEmissions"
                :unit="'tons'"
              />
            </template>
            <template v-else>
              -
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style lang="scss">
// Make the whole table scroll in a constrained container so we can have a sticky header - CSS makes
// that impossible otherwise
.table-cont {
  width: 100%;
  max-height: 80vh;
  overflow: auto;
  border: solid $border-thin $grey-dark;
  box-sizing: border-box;

  table {
    width: 100%;
    // Scroll if we get below desktop size table
    min-width: 60rem;
    border-collapse: collapse;

    // Increase width if showing extra columns on specific pages
    &.-wide {
      min-width: 88rem;

      // Wide columns shouldn't be as wide if we have more of them
      .wide-col { width: 17%; }
    }

    a {
      font-weight: bold;
      font-size: 1.125em;
      text-decoration: none;
      white-space: nowrap;
    }

    thead {
      position: sticky;
      top: 0;

      tr { background-color: $grey-dark; }

      th {
        text-align: left;
        font-weight: 500;
        line-height: 1.25;
        padding-top: 0.75rem;
        padding-bottom: 0.75rem;

        .unit {
          font-size: smaller;
          font-weight: normal;
        }
      }
    }

    th, td {
      padding: 0.75rem;
      line-height: 1.25;

      &:first-of-type { padding-left: 1rem; }
      &:last-of-type { padding-right: 1rem; }
      &.numeric { text-align: right; }
      &.wide-col { width: 20%; }
      &.prop-type { width: 12rem; }
    }

    tr:nth-of-type(2n + 2) { background-color: $grey; }

    .prop-address {
      font-size: 0.75em;
      margin-top: 0.25em;
    }
  }

  @media (max-width: $mobile-max-width) {
    // Make table screen full width on mobile
    width: calc(100% + 2rem);
    margin: 0 -1rem;

    table {
      width: 60rem;

      td.property-name, td.property-address { width: 10rem; }
    }
  }

  // On very short screens < 640px, disable vertical scrolling on the table, since it's view
  // height based and makes it very annoying at high zoom
  @media (max-height: 40rem) {
    max-height: none;
  }
}
</style>
