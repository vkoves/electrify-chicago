<script lang="ts">
export default {};

/**
 * Email content for contacting alderpersons about enforcing the
 * Building Energy Benchmarking Ordinance.
 */
export const AlderEmailContent = {
  subject: 'Supporting An Inspector to Enforce Energy Benchmarking',

  /**
   * Email body paragraphs for alderperson advocacy email.
   * Each item in the array represents one paragraph.
   */
  bodyParagraphs: [
    "I'm writing to ask you to support an inspector position to enforce " +
      "Chicago's Building Energy Use Benchmarking Ordinance.",

    'In 2013, Chicago passed the first-in-the-nation Building Energy Use ' +
      'Benchmarking Ordinance. It requires buildings over 50,000 square feet to ' +
      'annually report energy usage data. But the city has never enforced that ordinance.',

    'According to Electrify Chicago (https://electrifychicago.net/fines-breakdown), ' +
      'Chicago has failed to collect over $35 million in fines for buildings that ' +
      "didn't comply with the reporting requirement over just the past six years. That " +
      'averages to nearly $6 million in uncollected fines every year, and compliance is ' +
      'decreasing.',

    'Starting January 1, 2025, authority over the ordinance shifted to the Department ' +
      'of Environment. But they cannot enforce it without a staff member in the position ' +
      'of "Inspector."',

    "Climate Reality Project's Chicago Metro Chapter & Electrify Chicago advocate for " +
      "including funding in the city's 2026 budget to hire an inspector who can enforce " +
      'the benchmarking ordinance. Enforcing the ordinance could bring in millions of dollars of ' +
      "revenue, increase accountability, and support voluntary climate action in Chicago's big " +
      'buildings.',

    'Thank you for your attention to this important matter.',
  ],

  /**
   * Generate the email greeting with the alderperson's last name
   */
  getGreeting(alderLastName: string): string {
    return `Alderperson ${alderLastName},`;
  },

  /**
   * Generate the email closing
   */
  getClosing(): string {
    return 'Your constituent,';
  },

  /**
   * Generate the full email body as a plain text string for mailto links
   */
  getBodyPlainText(alderLastName: string): string {
    const greeting = this.getGreeting(alderLastName);
    const closing = this.getClosing();

    return `${greeting}\n\n${this.bodyParagraphs.join('\n\n')}\n\n${closing}\n\n`;
  },
};
</script>
