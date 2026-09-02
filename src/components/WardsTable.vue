<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import ExportButton from '../components/ExportButton.vue';

interface IWardStats {
  Ward: number;
  CompliantBuildings: number;
  TotalBuildings: number;
  TotalGHGEmissions: number;
  AvgGHGIntensity: number;
  TotalSquareFootage: number;
  AvgBuildingAge: number | null;
}

@Component({ components: { ExportButton } })
export default class WardsTable extends Vue {
  @Prop({ required: true }) wardStats!: Array<{ node: IWardStats }>;

  @Prop({ default: false }) showBuildingAge!: boolean;

  /** Props from Search component to store field (column) being sorted and direction */
  @Prop({ default: 'Ward' }) sortedField!: keyof IWardStats;
  @Prop({ default: 'asc' }) sortedDirection!: string;

  /**
   * Prop to handle whether the sorting buttons should be shown
   * (ex. with Search component). We then emit the sorting request and the parent handles
   * actually sorting the data and passing it back in.
   */
  @Prop({ default: false }) showSort!: boolean;

  get sortedStats(): IWardStats[] {
    return this.sortStats(this.wardStats.map(({ node }) => node));
  }

  get exportRows(): (string | number | null)[][] {
    const header = [
      'Ward',
      'Compliance Rate',
      'Compliant Buildings',
      'Total Buildings',
      'Total GHG Emissions (tons CO2 eq.)',
      'Avg GHG Intensity (kg CO2 eq./sqft)',
      'Total Square Footage (sqft)',
    ];
    const rows = this.sortedStats.map((s) => [
      s.Ward,
      this.complianceRate(s),
      s.CompliantBuildings,
      s.TotalBuildings,
      s.TotalGHGEmissions,
      s.AvgGHGIntensity,
      s.TotalSquareFootage,
    ]);
    return [header, ...rows];
  }

  // TODO: Move compliance rate to a BE process for wards.json
  complianceRate(s: IWardStats): number {
    return s.TotalBuildings > 0
      ? (s.CompliantBuildings / s.TotalBuildings) * 100
      : 0;
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
    <!-- Export button -->
    <ExportButton
      filename="ward-summary"
      :rows="exportRows"
      :show-text="true"
    />

    <div class="wards-table">
      <table>
        <thead>
          <tr>
            <th scope="col">Ward</th>
            <!-- TODO: Add Click handlers on numeric columns for sorting -->
            <th scope="col">Compliance Rate</th>
            <th scope="col">Total Compliant Buildings</th>
            <th scope="col">
              Total GHG Emissions<br />
              <span class="unit">(tons CO<sub>2</sub> eq.)</span>
            </th>
            <th scope="col">
              Avg GHG Intensity<br />
              <span class="unit">(kg CO<sub>2</sub> eq./sqft)</span>
            </th>
            <th scope="col">
              Total Square Footage<br />
              <span class="unit">(sqft)</span>
            </th>
            <th v-if="showBuildingAge" scope="col">
              Avg Building Age<br />
              <span class="unit">(years)</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="stats in sortedStats" :key="stats.Ward">
            <td class="ward-col">
              <g-link :to="`/ward/${stats.Ward}`">Ward {{ stats.Ward }}</g-link>
            </td>
            <td class="numeric">{{ formatNumber(complianceRate(stats), 1) }}%</td>
            <td class="numeric">
              {{ stats.CompliantBuildings }}/{{ stats.TotalBuildings }}
            </td>
            <td class="numeric">{{ formatNumber(stats.TotalGHGEmissions) }}</td>
            <td class="numeric">{{ formatNumber(stats.AvgGHGIntensity, 2) }}</td>
            <td class="numeric">{{ formatNumber(stats.TotalSquareFootage) }}</td>
            <td v-if="showBuildingAge" class="numeric">
              {{ formatNumber(stats.AvgBuildingAge, 1) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style lang="scss">
.wards-table-cont {
  .action-btn { margin: 1rem 0; }
}

.wards-table {
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
