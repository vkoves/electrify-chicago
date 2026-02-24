<script lang="ts">
export default {};

/** Utility class for formatting numbers for display */
export class NumberFormatter {
  /**
   * Formats a raw kBtu value, automatically selecting billions or millions
   * so small values don't display as "0.0 billion".
   *
   * Examples:
   *   1_234_567_890 → "1.2 billion"
   *   456_789_000   → "456.8 million"
   */
  static formatKbtu(kbtu: number): string {
    if (kbtu >= 1_000_000_000) {
      return parseFloat((kbtu / 1_000_000_000).toFixed(1)) + ' billion';
    }
    return parseFloat((kbtu / 1_000_000).toFixed(1)) + ' million';
  }
}
</script>
