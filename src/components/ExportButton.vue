<template>
  <div class="export-button-container">
    <button
      class="action-btn -export"
      :class="{ '-with-text': showText }"
      @click="handleExport"
    >
      <span v-if="showText">Export</span>
      <img src="/icons/export.svg" alt="Export"/>
    </button>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

/**
 * Reusable Export button that exports building stats to .CSV
 *
 * Source - https://stackoverflow.com/a/24922761
 * Posted by Xavier John, modified by community. See post 'Timeline' for change history
 * Retrieved 2026-03-25, License - CC BY-SA 4.0
 */
@Component
export default class ExportButton extends Vue {
  @Prop({ type: String, required: true })
  filename!: string;

  @Prop({ type: Array, required: true })
  rows!: (string | number | Date | null)[][];

  /** Whether to show the word "Export" or (by default) just an icon */
  @Prop({ type: Boolean, default: false })
  showText!: boolean;

  handleExport(): void {
    const processRow = (row: (string | number | Date | null)[]): string => {
      let finalVal = '';
      for (let j = 0; j < row.length; j++) {
        let innerValue = row[j] === null ? '' : row[j]!.toString();
        if (row[j] instanceof Date) {
          innerValue = (row[j] as Date).toLocaleString();
        }
        let result = innerValue.replace(/"/g, '""');
        if (result.search(/("|,|\n)/g) >= 0) {
          result = '"' + result + '"';
        }
        if (j > 0) finalVal += ',';
        finalVal += result;
      }
      return finalVal + '\n';
    };

    let csvFile = '';
    for (let i = 0; i < this.rows.length; i++) {
      csvFile += processRow(this.rows[i]);
    }

    const blob = new Blob([csvFile], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      const filename = this.filename.endsWith('.csv') ? this.filename : `${this.filename}.csv`;
      link.setAttribute('download', filename);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
}
</script>

<style lang="scss">
.export-button-container {
  position: relative;
  display: inline-block;

  .action-btn.-export {
    aspect-ratio: 1;
    padding: 0 0 0.2rem 0.2rem;

    img {
      height: 2rem;
    }

    &.-with-text {
      aspect-ratio: auto;
      padding: 0.5rem 1rem;
      gap: 0.5rem;

      img {
        height: 1.5rem;
      }
    }
  }
}
</style>