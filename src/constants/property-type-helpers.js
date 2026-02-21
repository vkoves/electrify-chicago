/* eslint-env node */
/**
 * Slugify a property type name for URL use
 * Converts "Office" -> "office", "K-12 School" -> "k-12-school", etc.
 *
 * IMPORTANT: This function is used in both:
 * - gridsome.server.js (Node.js, build time) for generating routes
 * - Vue components (browser, runtime) for creating links
 *
 * @param {string} propertyType - The property type name
 * @returns {string} - The slugified property type
 */
function slugifyPropertyType(propertyType) {
  return propertyType
    .toLowerCase()
    .replace(/\//g, '-') // Replace slashes with hyphens
    .replace(/\s+/g, '-'); // Replace spaces with hyphens
}

// eslint-disable-next-line no-undef
module.exports = { slugifyPropertyType };
