# Building Owners Performance Refactor

## Problem

The `BuildingOwner.vue` template currently has a performance issue:

- It pulls **all ~3000 buildings** via GraphQL (lines 201-232)
- Then filters them **client-side** in JavaScript (lines 89-106) using the `BuildingsCustomInfo` constant
- This loads unnecessary data and performs filtering in the browser instead of at build time

## Current Architecture

1. Building owner mappings are stored in `src/constants/buildings-custom-info.constant.vue`
2. The `BuildingOwner.vue` template queries all buildings
3. Client-side code loops through `BuildingsCustomInfo` to find matching building IDs
4. Filters the full building list to only show buildings for the current owner

## Proposed Solution

Add a new data pipeline step that bakes owner information into the building data CSV, allowing GraphQL to filter at query time.

### Implementation Steps

#### 1. Create New Pipeline Script

**File:** `src/data/scripts/add_building_owners.py`

This script should:

- Parse `src/constants/buildings-custom-info.constant.vue` to extract the owner mappings
  - Look for lines like `'251330': { owner: BuildingOwners.depaul.key }`
  - Extract the building ID and owner key
- Read the processed building CSV from the previous pipeline step
- Add an `Owner` column to each building row based on the mappings
- Output the updated CSV for the next pipeline step

**Parsing Strategy:**

- Use regex to find patterns like `'buildingId': { owner: BuildingOwners.ownerKey.key }`
- Build a dictionary mapping building IDs to owner keys
- Handle both simple owner assignments and complex objects with tags/links

#### 2. Update Pipeline

**File:** `run_all.py`

Add the new step to the `pipeline_steps` list after `process_data`:

```python
pipeline_steps = [
    {
        "module": "src.data.scripts.clean_and_split_data",
        "description": "clean_and_split_data",
    },
    {"module": "src.data.scripts.process_data", "description": "process_data"},
    {
        "module": "src.data.scripts.add_building_owners",
        "description": "add_building_owners",
    },
    {
        "module": "src.data.scripts.add_context_by_property_type",
        "description": "add_context_by_property_type",
    },
    # ... rest of pipeline
]
```

#### 3. Update BuildingOwner.vue GraphQL Query

**File:** `src/templates/BuildingOwner.vue`

Replace the current query (lines 201-232) with:

```graphql
<static-query>
  query($ownerId: String!) {
    allBuilding(
      filter: { Owner: { eq: $ownerId } }
      sortBy: "GHGIntensity"
    ) {
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
          path
          PrimaryPropertyType
          GHGIntensity
          GHGIntensityRank
          GHGIntensityPercentileRank
          TotalGHGEmissions
          TotalGHGEmissionsRank
          TotalGHGEmissionsPercentileRank
          AvgPercentileLetterGrade
          NaturalGasUse
          DistrictSteamUse
          DataAnomalies
          GrossFloorArea
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
          YearBuilt
          Owner
        }
      }
    }
  }
</static-query>
```

#### 4. Simplify BuildingOwner.vue Logic

Remove the client-side filtering logic (lines 89-106):

```typescript
// DELETE this method - no longer needed
filterBuildings(ownerId: string): void {
  // ... filtering logic
}
```

Update `created()` to use the pre-filtered results:

```typescript
created(): void {
  const ownerId: string = this.$context.ownerId;

  if (BuildingOwners[ownerId]) {
    this.currOwner = BuildingOwners[ownerId];

    // Buildings are already filtered by GraphQL
    this.buildingsFiltered = this.$static.allBuilding.edges;
    this.calculateOwnedBuildingStats();
  }
}
```

## Benefits

1. **Performance**: Only load ~20-50 buildings per owner instead of ~3000
2. **Consistency**: Owner data is part of the building data model, just like other fields
3. **Queryability**: Owner information can be filtered/sorted in GraphQL queries
4. **Build-time optimization**: Filtering happens during static site generation, not in the browser
5. **Similar pattern**: Matches how `FirstYearReported` and `LastYearReported` were added for `LatestUpdates.vue`

## Implementation Complexity

**Medium** - Requires:

- Python script to parse TypeScript constant file (regex-based)
- CSV data manipulation
- GraphQL query updates
- TypeScript interface updates (add `Owner?: string` to `IBuilding`)

## Testing Checklist

- [ ] Pipeline runs successfully with new step
- [ ] Building CSV has `Owner` column with correct values
- [ ] Building owner pages load correctly for all owners
- [ ] Performance improvement is measurable (check network tab for reduced payload)
- [ ] All existing building owner functionality works (stats, tables, etc.)
