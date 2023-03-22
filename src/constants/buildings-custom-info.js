/**
 * A file containing supplementary building info based on their slug. This can be used
 * for things like adding custom images, notes, or building owners to very important buildings
 * (e.g. the top 10 worst or best).
 */


/**
 * An object containing the name and logos of custom flagged building owners
 *
 * IBuildingOwner {
 *   key: string;
 *   name: string;
 *   logoSmall?: string; // A square logo for table view
 *   logoLarge?: string; // Any size logo for building details
 * }
 *
 * Type { [key: string]: IBuildingOwner}
 */
export const BuildingOwners = {
  depaul: {
    key: 'depaul',
    name: 'DePaul University',
    nameShort: 'DePaul',
    logoSmall: '/building-owners/depaul/logo-small.jpg',
    logoLarge: '/building-owners/depaul/logo-large.png',
  },
  iit: {
    key: 'iit',
    name: 'Illinois Institute of Technology (Illinois Tech)',
    nameShort: 'Illinois Tech',
    logoSmall: '/building-owners/iit/logo-small.png',
    logoLarge: '/building-owners/iit/logo-large.svg',
  },
};

/**
 * An object containing our custom details about buildings. These are hand coded based on the
 * building slug
 *
 * export interface IBuildingCustomInfo {
 *   owner?: string; // key from BuildingOwners
 * }
 */
export const BuildingsCustomInfo = {
  // Depaul Buildings
  'mc-gowan-north': {owner: BuildingOwners.depaul.key},
  'mc-gowan-south': {owner: BuildingOwners.depaul.key},
  'de-paul-center': {owner: BuildingOwners.depaul.key},
  'depaul-university-holtschneider-performance-center': {owner: BuildingOwners.depaul.key},

  // IIT buildings
  'keating-hall': {owner: BuildingOwners.iit.key},
  'life-science-research-building': {owner: BuildingOwners.iit.key},
  'tech-business-center': {owner: BuildingOwners.iit.key},
  'herman-hall': {owner: BuildingOwners.iit.key},
};
