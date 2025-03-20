<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import RankText from '~/components/RankText.vue';
import OverallRankEmoji from './OverallRankEmoji.vue';
import OwnerLogo from './OwnerLogo.vue';
import { IBuilding, IBuildingBenchmarkStats } from '../common-functions.vue';

// This simple JSON is a lot easier to just use directly than going through GraphQL and it's
// tiny
import BuildingBenchmarkStats from '../data/dist/building-benchmark-stats.json';
import LetterGrade from './LetterGrade.vue';

@Component({
  components: {
    LetterGrade,
    OverallRankEmoji,
    OwnerLogo,
    RankText,
  },
})
export default class BuildingsTable extends Vue {
  /** Expose stats to template */
  readonly BuildingBenchmarkStats: IBuildingBenchmarkStats =
    BuildingBenchmarkStats;

  @Prop({ required: true }) buildings!: Array<{ node: IBuilding }>;

  @Prop({ default: false }) showSquareFootage!: boolean;

  @Prop({ default: false }) showGasUse!: boolean;

  @Prop({ default: false }) showElectricityUse!: boolean;

  /** Props from Search component to store field (column) being sorted and direction */
  @Prop({ default: 'GHGIntensity' }) sortedField!: string;
  @Prop({ default: 'desc' }) sortedDirection!: string;

  // declares the property emit for TS
  $emit: any;

  /** Method to return the relevant aria-label value
   * based on whether the column is selected and sorted */
  getAriaLabelForSort(fieldname: string): string {
    if (fieldname === this.sortedField) {
      return `Currently sorted by ${this.sortedField} in 
      ${this.sortedDirection === 'asc' ? 'ascending' : 'descending'} order.`;
    } else {
      return `Sort by this column, ${this.sortedField}`;
    }
  }
}
</script>

<template>
  <div class="buildings-table-cont">
    <table
      :class="{
        '-wide': showSquareFootage || showGasUse || showElectricityUse,
      }"
    >
      <thead>
        <tr>
          <th scope="col">Name / Address</th>
          <th scope="col" class="prop-type">Primary Property Type</th>
          <th v-if="showSquareFootage">Square Footage</th>
          <!-- Click handlers on numeric columns for sorting -->
          <th
            v-if="showGasUse"
            scope="col"
            class="numeric wide-col"
            @click="$emit('sort', 'NaturalGasUse')"
          >
            Fossil Gas Use<br />
            <span class="unit">(kBtu)</span>
            <button
              :class="
                sortedField === 'NaturalGasUse'
                  ? 'sort selected'
                  : 'sort deselected'
              "
              :aria-label="getAriaLabelForSort('NaturalGasUse')"
            >
              {{
                sortedField === 'NaturalGasUse'
                  ? sortedDirection === 'asc'
                    ? '▲'
                    : '▼'
                  : '▼'
              }}
            </button>
          </th>
          <th
            v-if="showElectricityUse"
            scope="col"
            class="numeric wide-col"
            @click="$emit('sort', 'ElectricityUse')"
          >
            Electricity Use<br />
            <span class="unit">(kBtu)</span>
            <button
              :class="
                sortedField === 'ElectricityUse'
                  ? 'sort selected'
                  : 'sort deselected'
              "
              :aria-label="getAriaLabelForSort('ElectricityUse')"
            >
              {{
                sortedField === 'ElectricityUse'
                  ? sortedDirection === 'asc'
                    ? '▲'
                    : '▼'
                  : '▼'
              }}
            </button>
          </th>

          <th
            scope="col"
            class="numeric wide-col"
            @click="$emit('sort', 'GHGIntensity')"
          >
            GHG Intensity<br />
            <span class="unit">(kg CO<sub>2</sub> eq./sqft)</span>
            <button
              :class="
                sortedField === 'GHGIntensity'
                  ? 'sort selected'
                  : 'sort deselected'
              "
              :aria-label="getAriaLabelForSort('GHGIntensity')"
            >
              {{
                sortedField === 'GHGIntensity'
                  ? sortedDirection === 'asc'
                    ? '▲'
                    : '▼'
                  : '▼'
              }}
            </button>
          </th>
          <th
            scope="col"
            class="numeric wide-col"
            @click="$emit('sort', 'TotalGHGEmissions')"
          >
            Total GHG Emissions<br />
            <span class="unit">(tons CO<sub>2</sub> eq.)</span>
            <button
              :class="
                sortedField === 'TotalGHGEmissions'
                  ? 'sort selected'
                  : 'sort deselected'
              "
              :aria-label="getAriaLabelForSort('TotalGHGEmissions')"
            >
              {{
                sortedField === 'TotalGHGEmissions'
                  ? sortedDirection === 'asc'
                    ? '▲'
                    : '▼'
                  : '▼'
              }}
            </button>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="edge in buildings" :key="edge.node.id">
          <td class="property-name">
            <g-link :to="edge.node.path">
              {{ edge.node.PropertyName || edge.node.Address }}
            </g-link>
            <OverallRankEmoji
              :building="edge.node"
              :stats="BuildingBenchmarkStats"
            />

            <OwnerLogo :building="edge.node" :is-text="true" />
            <LetterGrade
              v-if="edge.node.AvgPercentileLetterGrade"
              :grade="edge.node.AvgPercentileLetterGrade"
              class="-circled"
            />

            <div class="prop-address">
              {{ edge.node.Address }}
            </div>
          </td>
          <td>{{ edge.node.PrimaryPropertyType }}</td>

          <!-- Square footage is optional, only shown on BiggestBuildings -->
          <td v-if="showSquareFootage" class="numeric">
            <template v-if="edge.node.GrossFloorArea">
              <RankText
                :building="edge.node"
                :should-round="true"
                :stats="BuildingBenchmarkStats"
                :unit="'sqft'"
                stat-key="GrossFloorArea"
              />
            </template>
            <template v-else> - </template>
          </td>

          <td v-if="showGasUse" class="numeric">
            <template v-if="edge.node.NaturalGasUse">
              <RankText
                :building="edge.node"
                :should-round="true"
                :stats="BuildingBenchmarkStats"
                :unit="'kBtu'"
                stat-key="NaturalGasUse"
              />
            </template>
            <template v-else> - </template>
          </td>
          <td v-if="showElectricityUse" class="numeric">
            <template v-if="edge.node.ElectricityUse">
              <RankText
                :building="edge.node"
                :should-round="true"
                :stats="BuildingBenchmarkStats"
                :unit="'kBtu'"
                stat-key="ElectricityUse"
              />
            </template>
            <template v-else> - </template>
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
            <template v-else> - </template>
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
            <template v-else> - </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style lang="scss">
// Make the whole table scroll in a constrained container so we can have a sticky header - CSS makes
// that impossible otherwise
.buildings-table-cont {
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
      .wide-col {
        width: 17%;
      }
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

      tr {
        background-color: $grey-dark;
      }

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

    th,
    td {
      padding: 0.75rem;
      line-height: 1.25;

      &:first-of-type {
        padding-left: 1rem;
      }
      &:last-of-type {
        padding-right: 1rem;
      }
      &.numeric {
        text-align: right;
        cursor: pointer;

        .sort {
          margin-left: 0.2rem;
          font-size: 0.7rem;
          padding: 0;
          background-color: transparent;
          border-bottom: none;
        }
        .sort.selected {
          color: black;
        }
        .sort.deselected {
          color: gray;
        }
      }
      &.wide-col {
        width: 20%;
      }
      &.prop-type {
        width: 12rem;
      }
    }

    tr:nth-of-type(2n + 2) {
      background-color: $grey;
    }

    .prop-address {
      font-size: 0.75em;
      margin-top: 0.25em;
    }
  }

  @media (max-width: $mobile-max-width) {
    // Make table screen full width on mobile
    width: calc(100% + 2rem);
    margin: 0 -1rem;
    // Disable max-height lots of scrolling is fine on mobile
    max-height: none;

    table {
      width: 70rem;

      thead th {
        font-size: 0.825rem;
        padding: 0.5rem 0.25rem;
      }
      td.property-name,
      td.property-address {
        width: 10rem;
      }
    }
  }
}
</style>
