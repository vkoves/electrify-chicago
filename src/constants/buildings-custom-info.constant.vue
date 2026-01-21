<script lang="ts">
import slugify from '@sindresorhus/slugify';
import { IBuilding } from '../common-functions.vue';
import buildingOwnersData from './building-owners.json';
import buildingOwnersMapping from './building-owners-mapping.json';

export default {};

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
  links?: Array <ILink>; // Extra links for supplementary info
}

export interface IBuildingOwners {
  [ownerKey: string]: IBuildingOwner;
}

/**
 * Building owners data loaded from centralized JSON file
 *
 * To add new building owners, update src/constants/building-owners.json
 */
export const BuildingOwners: IBuildingOwners = buildingOwnersData;

export function getAvailableOwnerIds(): string[] {
  return Object.keys(BuildingOwners);
}

export interface IBuildingCustomInfo {
  links?: Array<ILink>;
  tags?: Array<BuildingTags>;
}

export interface ILink {
  url: string;
  text: string;
}

/**
 * Custom Tags for associating groups of buildings for later retrieval, like those that participated
 * in city programs
 *
 * IMPORTANT: If you modify buildings tagged with hasRetrofitCaseStudy, you MUST also update
 * the hard-coded GraphQL filter in src/pages/RetrofitChicagoParticipants.vue for performance
 * optimization. The validation in that component will detect mismatches and throw an error.
 * */
export enum BuildingTags {
  hasRetrofitCaseStudy = 'has-retrofit-case-study',
}

/**
 * An object containing supplementary custom details about buildings (tags, links, etc.)
 *
 * Building owner assignments are now managed in building-owners-mapping.json
 */
export const BuildingsCustomInfo: {
  [buildingId: string]: IBuildingCustomInfo;
} = {
  '166134': {
    links: [
      {
        url: 'https://www.sheddaquarium.org/stories/sustainability-at-shedd',
        text: 'Sustainability at Shedd | Shedd Aquarium',
      },
    ],
  },

  /**
   * City Retrofit Data (PDFs)
   */
  // Rookery Building Retrofit
  '103721': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/The%20Rookery.pdf',
        text: 'Rookery Building Retrofit Report',
      },
    ],
  },
  // Wrigley Building
  '101920': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/Wrigley.pdf',
        text: 'Wrigley Building Retrofit Report',
      },
    ],
  },
  // Institute of Cultural Affairs
  '102336': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/ICAGreenRise.pdf',
        text: 'Institute of Cultural Affairs Retrofit Report',
      },
    ],
  },

  // Sheraton Chicago Hotel & Towers
  // Listed as Sheraton Grand(Retrofit) or Sheraton Grand Chicago Riverwalk (google maps)
  '101852': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/TheSheraton.pdf',
        text: 'Sheraton Grand Chicago Hotel Retrofit Report',
      },
    ],
  },

  // John T. Richardson Library (DePaul)
  '251328': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/Richardson%20Library.pdf',
        text: 'Richardson Library Retrofit Report',
      },
    ],
  },

  // Mansueto Library at UChicago
  '252064': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/UChicagoMansueto.pdf',
        text: 'Mansueto Library Retrofit Report',
      },
    ],
  },

  // 303 E Superior Street (Lurie Medical Research Center - Northwestern)
  '256405': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/Northwestern%20Lurie.pdf',
        text: 'Lurie Medical Research Center - 303 E Superior St Retrofit Report',
      },
    ],
  },

  // 280 Building, 280 S Columbus Dr (SAIC)
  '252065': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/SAIC.pdf',
        text: 'SAIC 280 S Columbus Building Retrofit Report',
      },
    ],
  },
};

export function getBuildingCustomInfo(
  building: IBuilding,
): IBuildingCustomInfo | null {
  const buildingSlug = slugify(building.ID as string);

  return BuildingsCustomInfo[buildingSlug] ?? null;
}

/**
 * Returns the owner object for a given building by checking building-owners-mapping.json,
 * or null if not found
 *
 * TODO: See if we can do this via the main benchmarking CSV and GraphQL
 */
export function getBuildingOwner(building: IBuilding): IBuildingOwner | null {
  const buildingSlug = slugify(building.ID as string);

  // Check each owner's list of buildings
  for (const [ownerKey, buildingIds] of Object.entries(buildingOwnersMapping)) {
    if ((buildingIds as string[]).includes(buildingSlug)) {
      return BuildingOwners[ownerKey] || null;
    }
  }

  return null;
}
</script>
