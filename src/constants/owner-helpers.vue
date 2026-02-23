<script lang="ts">
import {
  BuildingOwners,
  IBuildingOwner,
} from './buildings-custom-info.constant.vue';
import { IBuilding, IBuildingNode } from '../common-functions.vue';

export default {};

/** Stats for a single building owner */
export interface IOwnerStats {
  buildingCount: number;
  totalGHGEmissions: number;
  avgGHGIntensity: number;
}

/** Owner with calculated stats */
export interface IOwnerWithStats {
  owner: IBuildingOwner;
  stats: IOwnerStats;
}

/**
 * Calculate stats for all building owners from a list of buildings
 * Returns a map of owner key to owner and stats
 */
export function calculateAllOwnerStats(
  buildings: Array<IBuildingNode>,
): Map<string, IOwnerWithStats> {
  const ownerData = new Map<
    string,
    {
      buildings: Array<IBuilding>;
      totalGHGEmissions: number;
      totalGHGIntensity: number;
    }
  >();

  // Group buildings by owner
  buildings.forEach((edge) => {
    const building = edge.node;
    const ownerKey = building.Owner;

    if (ownerKey && BuildingOwners[ownerKey]) {
      if (!ownerData.has(ownerKey)) {
        ownerData.set(ownerKey, {
          buildings: [],
          totalGHGEmissions: 0,
          totalGHGIntensity: 0,
        });
      }

      const data = ownerData.get(ownerKey)!;
      data.buildings.push(building);
      data.totalGHGEmissions += building.TotalGHGEmissions || 0;
      data.totalGHGIntensity += building.GHGIntensity || 0;
    }
  });

  // Calculate stats for each owner
  const ownerStats = new Map<string, IOwnerWithStats>();

  ownerData.forEach((data, ownerKey) => {
    const owner = BuildingOwners[ownerKey];
    const buildingCount = data.buildings.length;

    ownerStats.set(ownerKey, {
      owner,
      stats: {
        buildingCount,
        totalGHGEmissions: data.totalGHGEmissions,
        avgGHGIntensity: data.totalGHGIntensity / buildingCount,
      },
    });
  });

  return ownerStats;
}

/**
 * Get top N owners sorted by total emissions
 */
export function getTopOwnersByEmissions(
  ownerStats: Map<string, IOwnerWithStats>,
  limit: number = 6,
): Array<IOwnerWithStats> {
  return Array.from(ownerStats.values())
    .sort((a, b) => b.stats.totalGHGEmissions - a.stats.totalGHGEmissions)
    .slice(0, limit);
}
</script>
