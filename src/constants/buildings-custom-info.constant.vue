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
  /** Optional source links scoped to specific tags, to validate/cite a tag's claim */
  tagLinks?: Partial<Record<BuildingTags, ILink>>;
}

export interface ILink {
  url: string;
  text: string;
  /** Optional pull quote to show as a tooltip preview */
  preview?: string;
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
  hasGeothermalHeatPump = 'has-geothermal-heat-pump',
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

  /**
   * Geothermal Heat Pump Buildings
   */
  // BVM Hall (Loyola University)
  '175895': {
    tags: [BuildingTags.hasGeothermalHeatPump],
    tagLinks: {
      [BuildingTags.hasGeothermalHeatPump]: {
        url: 'https://www.luc.edu/sustainability/about/ourfacilities/#:~:text=in%20the%20building.-,Geothermal%20System,-%3A%C2%A0A%2091',
        text: 'Loyola University Sustainability - BVM Hall Geothermal System',
        preview:
          'A 91-well geothermal system heats and cools the SES building by tapping into the earth\'s constant temperature deep underground. The system is highly efficient, cutting the building\'s heating and cooling costs by 30 percent.',
      },
    },
  },

  // Eagle Building
  '256537': {
    tags: [BuildingTags.hasGeothermalHeatPump],
    tagLinks: {
      [BuildingTags.hasGeothermalHeatPump]: {
        url: 'https://theeaglebuilding.com/#:~:text=and%20natural%20beauty!-,GEOTHERMAL%20HEATING,-%26%20COOLING',
        text: 'Eagle Building - Geothermal Heating & Cooling',
        preview:
          'Geothermal energy offers tenants significant cost savings... by harnessing the earth\'s natural temperature, these systems require less energy compared to traditional HVAC methods, leading to lower monthly expenses.',
      },
    },
  },
};

/**
 * Validates that a hard-coded GraphQL query filter matches the buildings tagged with the given tag.
 * Pages that use a hard-coded ID filter for performance MUST call this in created() to detect
 * mismatches between the GraphQL query and the tag data.
 *
 * @param tag - The BuildingTags value to validate against
 * @param actualIds - The building IDs returned by the GraphQL query (as strings)
 */
export function validateTaggedBuildings(
  tag: BuildingTags,
  actualIds: string[],
): void {
  const expectedIds = Object.entries(BuildingsCustomInfo)
    .filter(([, info]) => info.tags?.includes(tag))
    .map(([id]) => id)
    .sort();

  const sortedActual = [...actualIds].sort();
  const missing = expectedIds.filter((id) => !sortedActual.includes(id));
  const extra = sortedActual.filter((id) => !expectedIds.includes(id));

  if (missing.length > 0 || extra.length > 0) {
    const details = [
      missing.length > 0 && `Missing: [${missing.join(', ')}]`,
      extra.length > 0 && `Extra: [${extra.join(', ')}]`,
    ]
      .filter(Boolean)
      .join(', ');
    throw new Error(
      `GraphQL query mismatch for tag "${tag}". ${details}. ` +
        'Update GraphQL query to match tagged buildings.',
    );
  }
}

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
