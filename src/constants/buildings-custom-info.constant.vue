<script lang="ts">
// The function Gridsome uses to make slugs, so it should match
import slugify from '@sindresorhus/slugify';
import { IBuilding } from '../common-functions.vue';

export default { };

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

export interface IBuildingOwners {
  [ownerKey: string]: IBuildingOwner;
}

/**
 * An object containing the name and logos of custom flagged building owners
 */
export const BuildingOwners: IBuildingOwners = {
  depaul: {
    key: 'depaul',
    name: 'DePaul University',
    nameShort: 'DePaul',
    logoSmall: '/building-owners/depaul/logo-small.jpg',
    logoLarge: '/building-owners/depaul/logo-large.png',
  },

  iit: {
    key: 'iit',
    name: 'Illinois Institute of Technology',
    nameShort: 'Illinois Tech',
    logoSmall: '/building-owners/iit/logo-small.png',
    logoLarge: '/building-owners/iit/logo-large.svg',
  },

  uchicago: {
    key: 'uchicago',
    name: 'University of Chicago',
    nameShort: 'UChicago',
    logoSmall: '/building-owners/uchicago/uchicago-small.jpg',
    logoLarge: '/building-owners/uchicago/uchicago-large.png',
  },

  northwestern: {
    key: 'northwestern',
    name: 'Northwestern University',
    nameShort: 'Northwestern',
    logoSmall: '/building-owners/northwestern/northwestern-large.png',
    logoLarge: '/building-owners/northwestern/northwestern-large.png',
  },

  /**
   * IMPORTANT! If you add a new building owner, make sure to add it to the gridsome.server.js to
   * register the owner page, since it cannot import this file.
   */
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
  /**
   * Depaul Buildings
   * Helpful source: https://www.depaul.edu/campus-maps/Pages/default.aspx
   */
  'mc-gowan-north': {owner: BuildingOwners.depaul.key},
  'mc-gowan-south': {owner: BuildingOwners.depaul.key},
  'de-paul-center': {owner: BuildingOwners.depaul.key},
  'depaul-university-holtschneider-performance-center': {owner: BuildingOwners.depaul.key},
  'student-center': {owner: BuildingOwners.depaul.key},

  /**
   * IIT buildings
   * Helpful source: https://en.wikipedia.org/wiki/List_of_Illinois_Institute_of_Technology_buildings
   */
  'keating-hall': {owner: BuildingOwners.iit.key},
  'life-science-research-building': {owner: BuildingOwners.iit.key},
  'tech-business-center': {owner: BuildingOwners.iit.key},
  'herman-hall': {owner: BuildingOwners.iit.key},
  'iit-tower': {owner: BuildingOwners.iit.key},
  'iit-stuart-school-of-business': {owner: BuildingOwners.iit.key},
  'john-t-rettaliata-engineering-center': {owner: BuildingOwners.iit.key},
  'mc-cormick-tribune-campus-center': {owner: BuildingOwners.iit.key},

  /**
   * UChicago Buildings
   * Helpful source: https://registrar.uchicago.edu/faculty-staff/classroom-scheduling/buildings-directory-2/
   */
  '1155-e-60th-st': {owner: BuildingOwners.uchicago.key},
  '5841-s-maryland-ave-m-c0985': {owner: BuildingOwners.uchicago.key},
  '6045-kenwood-building': {owner: BuildingOwners.uchicago.key},
  'accelerator-high-energy-physics': {owner: BuildingOwners.uchicago.key},
  'gordon-center-for-integrative-science-gcis': {owner: BuildingOwners.uchicago.key},
  'hinds-laboratory': {owner: BuildingOwners.uchicago.key},
  'jones-laboratory': {owner: BuildingOwners.uchicago.key},
  'searle-chemistry-laboratory': {owner: BuildingOwners.uchicago.key},
  'william-eckhardt-research-center': {owner: BuildingOwners.uchicago.key},

  /**
   * Northwestern Buildings
   * No helpful resource, but Googling each of these will pull up a Northwestern page
   */
  '303-e-superior-street': { owner: BuildingOwners.northwestern.key },
  '320-e-superior-street': { owner: BuildingOwners.northwestern.key },
  '300-e-superior-street': { owner: BuildingOwners.northwestern.key },
  'nmh-olson-pavilion': { owner: BuildingOwners.northwestern.key },
};

export function getBuildingCustomInfo(building: IBuilding): IBuildingCustomInfo | null {
  const buildingSlug = slugify(building.slugSource as string);

  return BuildingsCustomInfo[buildingSlug] ?? null;
}
</script>
