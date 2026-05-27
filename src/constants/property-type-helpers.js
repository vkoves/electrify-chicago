/* eslint-env node */
/**
 * Slugify a property type name for URL use
 * Converts "Office" -> "office", "K-12 School" -> "k-12-school"
 * "Hospital (General Medical & Surgical)" -> "hospital-general-medical-and-surgical"
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
    .replace(/&/g, 'and')
    .replace(/[()]/g, '')
    .replace(/\//g, '-')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

// eslint-disable-next-line no-undef
module.exports = { slugifyPropertyType };
