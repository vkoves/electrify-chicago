<script lang="ts">
export default { }

/**
 * A file containing supplementary building info based on their slug. This can be used
 * for things like adding custom images, notes, or building owners to very important buildings
 * (e.g. the top 10 worst or best).
 */

export interface IBuildingOwner {
  key: string;
  name: string;
  nameShort: string; // Name for table view
  logoSmall?: string; // A square logo for table view
  logoLarge?: string; // Any size logo for building details
}

/**
 * An object containing the name and logos of custom flagged building owners
 *
 *
 * Type
 */
export const BuildingOwners: { [key: string]: IBuildingOwner } = {
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

export interface IBuildingCustomInfo {
  owner?: string; // key from BuildingOwners
}

/**
 * An object containing our custom details about buildings. These are hand coded based on the
 * building slug
 *
 */
export const BuildingsCustomInfo: { [buildingSlug: string]: IBuildingCustomInfo } = {
  // Depaul Buildings
  // Helpful source: https://www.depaul.edu/campus-maps/Pages/default.aspx
  'mc-gowan-north': {owner: BuildingOwners.depaul.key},
  'mc-gowan-south': {owner: BuildingOwners.depaul.key},
  'de-paul-center': {owner: BuildingOwners.depaul.key},
  'depaul-university-holtschneider-performance-center': {owner: BuildingOwners.depaul.key},
  'student-center': {owner: BuildingOwners.depaul.key},

  // IIT buildings
  // Helpful source: https://en.wikipedia.org/wiki/List_of_Illinois_Institute_of_Technology_buildings
  'keating-hall': {owner: BuildingOwners.iit.key},
  'life-science-research-building': {owner: BuildingOwners.iit.key},
  'tech-business-center': {owner: BuildingOwners.iit.key},
  'herman-hall': {owner: BuildingOwners.iit.key},
  'iit-tower': {owner: BuildingOwners.iit.key},
  'iit-stuart-school-of-business': {owner: BuildingOwners.iit.key},
  'john-t-rettaliata-engineering-center': {owner: BuildingOwners.iit.key},
  'mc-cormick-tribune-campus-center': {owner: BuildingOwners.iit.key},
};
</script>
