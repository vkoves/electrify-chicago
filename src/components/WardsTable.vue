<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { IBuilding } from '../common-functions.vue';

/** Aggregated statistics for a single ward */
interface IWardStats {
  ward: number;
  buildingCount: number;
  totalGHGEmissions: number;
  avgGHGIntensity: number;
  totalSquareFootage: number;
  avgBuildingAge: number | null;
}

@Component({})
export default class WardsTable extends Vue {
  @Prop({ required: true }) buildings!: Array<{ node: IBuilding }>;

  @Prop({ default: false }) showBuildingAge!: boolean;

  /** Props from Search component to store field (column) being sorted and direction */
  @Prop({ default: 'ward' }) sortedField!: keyof IWardStats;
  @Prop({ default: 'asc' }) sortedDirection!: string;

  /**
   * Prop to handle whether the sorting buttons should be shown
   * (ex. with Search component). We then emit the sorting reuqest and the parent handles
   * actually sorting the data and passing it back in.
   */
  @Prop({ default: false }) showSort!: boolean;

  readonly CurrentYear = new Date().getFullYear();

  get wardStats(): IWardStats[] {
    const wardMap: Record<number, IBuilding[]> = {};

    for (const { node } of this.buildings) {
      const ward = Number(node.Ward);
      //TODO: Fix missing ward data
      //Filter out buildings with no ward data available.
      if (!ward || ward == -1) continue;

      if (!wardMap[ward]) wardMap[ward] = [];
      wardMap[ward].push(node);
    }

    const stats: IWardStats[] = Object.entries(wardMap).map(
      ([wardStr, buildings]) => {
        const ward = Number(wardStr);

        const totalGHGEmissions = buildings.reduce(
          (sum, b) => sum + (b.TotalGHGEmissions || 0),
          0,
        );

        const ghgBuildings = buildings.filter((b) => b.GHGIntensity > 0);
        const avgGHGIntensity =
          ghgBuildings.length > 0
            ? ghgBuildings.reduce((sum, b) => sum + b.GHGIntensity, 0) /
              ghgBuildings.length
            : 0;

        const totalSquareFootage = buildings.reduce(
          (sum, b) => sum + (b.GrossFloorArea || 0),
          0,
        );

        const builtBuildings = buildings.filter(
          (b) => b.YearBuilt && b.YearBuilt > 1800,
        );
        const avgBuildingAge =
          builtBuildings.length > 0
            ? this.CurrentYear -
              builtBuildings.reduce((sum, b) => sum + b.YearBuilt, 0) /
                builtBuildings.length
            : null;

        return {
          ward,
          buildingCount: buildings.length,
          totalGHGEmissions,
          avgGHGIntensity,
          totalSquareFootage,
          avgBuildingAge,
        };
      },
    );

    return this.sortStats(stats);
  }

  sortStats(stats: IWardStats[]): IWardStats[] {
    return [...stats].sort((a, b) => {
      const aVal = a[this.sortedField];
      const bVal = b[this.sortedField];

      if (aVal === null && bVal === null) return 0;
      if (aVal === null) return 1;
      if (bVal === null) return -1;

      const diff = (aVal as number) - (bVal as number);
      return this.sortedDirection === 'asc' ? diff : -diff;
    });
  }

  formatNumber(value: number, decimals = 0): string {
    return value.toLocaleString('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });
  }
}
</script>

<template>
  <div class="wards-table-cont">
    <table
        :class="{
        '-wide':
          showSquareFootage ||
          showGasUse ||
          showElectricityUse ||
          showBuildingAge,
      }"
    >
      <thead>
        <tr>
          <th scope="col">Ward</th>
          <!-- TODO: Add Click handlers on numeric columns for sorting -->
          <th scope="col">Buildings</th>
          <th scope="col"> Total GHG Emissions<br />
            <span class="unit">(tons CO<sub>2</sub> eq.)</span>
          </th>
          <th scope="col">Avg GHG Intensity<br />
            <span class="unit">(kg CO<sub>2</sub> eq./sqft)</span>
          </th>
          <th scope="col">Total Square Footage<br />
            <span class="unit">(sqft)</span>
          </th>
          <!-- TODO: Need to add method to handle invalid or null YearBuilt value-->
          <th v-if="showBuildingAge" scope="col">Avg Building Age<br />
            <span class="unit">(years)</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stats in wardStats" :key="stats.ward">
          <td class="ward-col">
            <g-link :to="`/ward/${stats.ward}`">Ward {{ stats.ward }}</g-link>
          </td>
          <td class="numeric">{{ formatNumber(stats.buildingCount) }}</td>
          <td class="numeric">{{ formatNumber(stats.totalGHGEmissions) }}</td>
          <td class="numeric">{{ formatNumber(stats.avgGHGIntensity, 2) }}</td>
          <td class="numeric">{{ formatNumber(stats.totalSquareFootage) }}</td>
          <td class="numeric">
            <template v-if="showBuildingAge">
              {{ formatNumber(stats.avgBuildingAge, 1) }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style lang="scss">
.wards-table-cont {
  width: 100%;
  max-height: 80vh;
  overflow: auto;
  border: solid $border-thin $grey-dark;
  box-sizing: border-box;
  print-color-adjust: exact;

  table {
    width: 100%;
    min-width: 50rem;
    border-collapse: collapse;

    a {
      font-weight: bold;
      text-decoration: none;
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

        &.-sortable {
          cursor: pointer;

          &:hover .sort.deselected,
          .sort.selected {
            color: $black;
          }
          .sort.deselected {
            color: rgba(0, 0, 0, 0.5);
          }

          .sort {
            margin-left: 0.2rem;
            font-size: 0.7rem;
            padding: 0;
            background-color: transparent;
            border-bottom: none;
            transition: color 0.3s;
          }
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
        text-align: left;
      }
      &.ward-col {
        width: 7rem;
      }
    }

    tr:nth-of-type(2n + 2) {
      background-color: $grey;
    }
  }

  @media (max-width: $mobile-max-width) {
    width: calc(100% + 2rem);
    margin: 0 -1rem;
    max-height: none;

    table {
      min-width: 40rem;

      thead th {
        font-size: 0.825rem;
        padding: 0.5rem 0.25rem;
      }
    }
  }

  @media print {
    margin: 0 !important;
  }
}
</style>
