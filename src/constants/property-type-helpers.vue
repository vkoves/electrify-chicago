<script lang="ts">
export default {};

/**
 * Re-export property type helpers for use in Vue components
 * The actual implementation is in property-type-helpers.js so it can be
 * shared between Node.js (gridsome.server.js) and browser code (Vue components)
 */
// eslint-disable-next-line @typescript-eslint/no-require-imports
const helpers = require('./property-type-helpers.js') as {
  slugifyPropertyType: (propertyType: string) => string;
};
export const slugifyPropertyType = helpers.slugifyPropertyType;
</script>
