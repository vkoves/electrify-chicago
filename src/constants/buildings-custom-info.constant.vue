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

  cps: {
    key: 'cps',
    name: 'Chicago Public Schools',
    nameShort: 'CPS',
    logoSmall: '/building-owners/northwestern/northwestern-large.png',
    logoLarge: '/building-owners/northwestern/northwestern-large.png',
  },

  cha: {
    key: 'cha',
    name: 'Chicago Housing Authority',
    nameShort: 'CHA',
    logoSmall: '/building-owners/northwestern/northwestern-large.png',
    logoLarge: '/building-owners/northwestern/northwestern-large.png',
  },

  cityofchicago: {
    key: 'cityofchicago',
    name: 'City of Chicago',
    nameShort: 'Chicago',
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
 * TODO: Move to more stable building ID
 */
export const BuildingsCustomInfo: { [buildingSlug: string]: IBuildingCustomInfo } = {
  /**
   * Depaul Buildings
   * Helpful source: https://www.depaul.edu/campus-maps/Pages/default.aspx
   */
  // Mc-Gowan-North
  '251330': {owner: BuildingOwners.depaul.key},
  // Mc-Gowan-South
  '119808': {owner: BuildingOwners.depaul.key},
  // De-Paul-Center
  '101562': {owner: BuildingOwners.depaul.key},
  // Holtschneider-Performance-Center
  '254989': {owner: BuildingOwners.depaul.key},
  // Student-Center
  '251335': {owner: BuildingOwners.depaul.key},
  // Centennial-Hall
  '251326': {owner: BuildingOwners.depaul.key},

  /**
   * IIT buildings
   * Helpful source: https://en.wikipedia.org/wiki/List_of_Illinois_Institute_of_Technology_buildings
   */
  // Crown Hall
  '256419': {owner: BuildingOwners.iit.key},
  // Keating Hall
  '256434': {owner: BuildingOwners.iit.key},
  // Life Science Research Building
  '256439': {owner: BuildingOwners.iit.key},
  // Tech Business Center
  '256438': {owner: BuildingOwners.iit.key},
  // Herman Hall
  '256427': {owner: BuildingOwners.iit.key},
  // IIT Tower
  '256440': {owner: BuildingOwners.iit.key},
  // IIT Stuart School Of Business
  '158403': {owner: BuildingOwners.iit.key},
  // John T Rettaliata Engineering Center
  '256420': {owner: BuildingOwners.iit.key},
  // McCormick Tribune Campus Center
  '256428': {owner: BuildingOwners.iit.key},
  // Stuart Building
  '256424': {owner: BuildingOwners.iit.key},
  // Wishnick Hall
  '256425': {owner: BuildingOwners.iit.key},
  // Siegal Hall
  '256433': {owner: BuildingOwners.iit.key},
  // Incubator?
  '256435': {owner: BuildingOwners.iit.key},

  /**
   * UChicago Buildings
   * Helpful source: https://registrar.uchicago.edu/faculty-staff/classroom-scheduling/buildings-directory-2/
   */
  // 1155 E 60th St
  '136212': {owner: BuildingOwners.uchicago.key},
  // 5841 S Maryland Ave M C0985
  '256838': {owner: BuildingOwners.uchicago.key},
  // 6045 Kenwood Building
  '172151': {owner: BuildingOwners.uchicago.key},
  // Accelerator High Energy Physics
  '252039': {owner: BuildingOwners.uchicago.key},
  // Gordon Center For Integrative Science Gcis
  '110848': {owner: BuildingOwners.uchicago.key},
  // Hinds Laboratory
  '173925': {owner: BuildingOwners.uchicago.key},
  // Jones Laboratory
  '252050': {owner: BuildingOwners.uchicago.key},
  // Searle Chemistry Laboratory
  '134735': {owner: BuildingOwners.uchicago.key},
  // William Eckhardt Research Center
  '254382': {owner: BuildingOwners.uchicago.key},
  // Ratner Athletics Center
  '252037': {owner: BuildingOwners.uchicago.key},
  // Crerar Library
  '252038': {owner: BuildingOwners.uchicago.key},
  // Renee Granville Grossman Residential Commons
  '252043': {owner: BuildingOwners.uchicago.key},
  // Campus Residential North Commons
  '254381': {owner: BuildingOwners.uchicago.key},
  // Burton Judson Courts
  '156942': {owner: BuildingOwners.uchicago.key},
  '254181':  {owner: BuildingOwners.uchicago.key},
  '252047':  {owner: BuildingOwners.uchicago.key},
  // Bookstore!
  '252041': {owner: BuildingOwners.uchicago.key},
  // Booth School
  '102455': {owner: BuildingOwners.uchicago.key},

  /**
   * Northwestern Buildings
   * No helpful resource, but Googling each of these will pull up a Northwestern page
   */
  // 303 E Superior Street
  '256405': { owner: BuildingOwners.northwestern.key },
  // 320 E Superior Street
  '256408': { owner: BuildingOwners.northwestern.key },
  // 300 E Superior Street
  '256410': { owner: BuildingOwners.northwestern.key },
  // NMH Olson Pavilion
  '103748': { owner: BuildingOwners.northwestern.key },
  // Northwestern University Chicago Campus
  '101840': { owner: BuildingOwners.northwestern.key },
  // Morton Medical Research Building
  '256409': { owner: BuildingOwners.northwestern.key },

  /**
   * CPS
   * No helpful resource, but Googling each of these will pull up a Northwestern page
   */

   /**
   * CHA
   * No helpful resource, but Googling each of these will pull up a Northwestern page
   */

   /**
   * City of Chicago
   * No helpful resource, but Googling each of these will pull up a Northwestern page
   */
};

export function getBuildingCustomInfo(building: IBuilding): IBuildingCustomInfo | null {
  const buildingSlug = slugify(building.ID as string);

  return BuildingsCustomInfo[buildingSlug] ?? null;
}
</script>
