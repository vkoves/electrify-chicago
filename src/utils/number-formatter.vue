<script lang="ts">
export default {};

/** Utility class for formatting numbers for display */
export class NumberFormatter {
  /**
   * Formats a large number, automatically selecting billions, millions, or
   * falling back to a locale-formatted integer for smaller values.
   *
   * Examples:
   *   1_234_567_890 → "1.2 billion"
   *   456_789_000   → "456.8 million"
   *   12_345        → "12,345"
   */
  static formatBigNumber(value: number): string {
    if (value >= 1_000_000_000) {
      return parseFloat((value / 1_000_000_000).toFixed(1)) + ' billion';
    } else if (value >= 1_000_000) {
      return parseFloat((value / 1_000_000).toFixed(1)) + ' million';
    }
    return Math.round(value).toLocaleString();
  }

  /**
   * Formats a raw kBtu value using formatBigNumber.
   *
   * Examples:
   *   1_234_567_890 → "1.2 billion"
   *   456_789_000   → "456.8 million"
   */
  static formatKbtu(kbtu: number): string {
    return NumberFormatter.formatBigNumber(kbtu);
  }
}
</script>
