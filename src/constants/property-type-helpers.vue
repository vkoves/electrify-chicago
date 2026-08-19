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

/**
 * An emoji for each property type, used to make lists of property types easier
 * to scan. Types not listed here fall back to PropertyTypeEmojiFallback.
 */
export const PropertyTypeEmoji: Record<string, string> = {
  'Adult Education': '📚',
  'Ambulatory Surgical Center': '🏥',
  'Automobile Dealership': '🚗',
  'Bank Branch': '🏦',
  'College/University': '🎓',
  'Convention Center': '🎪',
  Courthouse: '⚖️',
  'Data Center': '💾',
  'Distribution Center': '📦',
  'Enclosed Mall': '🛍️',
  'Financial Office': '🏦',
  'Fitness Center/Health Club/Gym': '🏋️',
  'Hospital (General Medical & Surgical)': '🏥',
  Hotel: '🏨',
  'Ice/Curling Rink': '⛸️',
  'Indoor Arena': '🏟️',
  'K-12 School': '🏫',
  Laboratory: '🔬',
  Library: '📖',
  'Medical Office': '🩺',
  'Mixed Use Property': '🏙️',
  'Movie Theater': '🎬',
  'Multifamily Housing': '🏢',
  Museum: '🏛️',
  Office: '🏢',
  Other: '🏗️',
  'Other - Education': '📚',
  'Other - Entertainment/Public Assembly': '🎭',
  'Other - Lodging/Residential': '🏘️',
  'Other - Mall': '🛍️',
  'Other - Public Services': '🏛️',
  'Other - Recreation': '🎡',
  'Other - Services': '🔧',
  'Other - Specialty Hospital': '🏥',
  'Outpatient Rehabilitation/Physical Therapy': '🩼',
  'Performing Arts': '🎭',
  'Pre-school/Daycare': '🧸',
  'Prison/Incarceration': '🔒',
  'Repair Services (Vehicle, Shoe, Locksmith, etc.)': '🔧',
  'Residence Hall/Dormitory': '🛏️',
  'Residential Care Facility': '🧑‍⚕️',
  'Retail Store': '🛒',
  'Senior Care Community': '👵',
  'Senior Living Community': '👵',
  'Social/Meeting Hall': '🤝',
  'Stadium (Open)': '🏟️',
  'Strip Mall': '🏬',
  'Supermarket/Grocery Store': '🥫',
  'Urgent Care/Clinic/Other Outpatient': '🚑',
  'Vehicle Dealership': '🚗',
  'Wholesale Club/Supercenter': '🏬',
  'Worship Facility': '🛐',
};

/** Emoji shown for any property type missing from PropertyTypeEmoji */
export const PropertyTypeEmojiFallback = '🏢';

/**
 * Get the emoji for a property type, falling back to a generic building emoji
 * for any type we haven't explicitly mapped
 */
export function getPropertyTypeEmoji(propertyType: string): string {
  return PropertyTypeEmoji[propertyType] ?? PropertyTypeEmojiFallback;
}
</script>
