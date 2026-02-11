# Constants Directory

This directory contains static data and configuration used throughout Electrify Chicago. Due to
Gridsome limitations, these have to be `.vue` files or `.json` files, but cannot be regular
`.ts` files.

## Files

- **`globals.vue`** - Global constants like latest data year
- **`meta-helpers.vue`** - Utility functions for generating page metadata and social media tags
- **`citywide-stats-graph-data.vue`** - Historical statistical data for citywide graphs
- **`building-images.constant.vue`** - Image mappings and metadata for building photos
- **`buildings-custom-info.constant.vue`** - Additional building information and owner data
- **`building-owners.json`** - JSON data for building ownership information
- **`building-owners-mapping.json`** - Maps building IDs to their owners
- **`page-social-images/`** - Social media image configurations (see subdirectory README)

## Usage

Import constants and utilities from these files as needed:

```typescript
import { LatestDataYear } from './globals.vue';
import { generatePageMeta } from './meta-helpers.vue';
```

## Building Ownership Data Sources

When researching and adding building ownership information to `building-owners-mapping.json`, the following sources are helpful:

### Universities & Colleges

- **DePaul**: [Campus Maps](https://www.depaul.edu/campus-maps/Pages/default.aspx)
- **IIT**: [List of IIT Buildings (Wikipedia)](https://en.wikipedia.org/wiki/List_of_Illinois_Institute_of_Technology_buildings)
- **UChicago**: [Buildings Directory](https://registrar.uchicago.edu/faculty-staff/classroom-scheduling/buildings-directory-2/)
- **UIC**: [Buildings Data](https://fimweb.fim.uic.edu/BuildingsData.aspx) (ignore leased buildings)
- **Northwestern**: [Chicago Campus Map](https://maps.northwestern.edu/chicago)
- **Loyola**: [Campus Maps](https://www.luc.edu/welcomeweek/campusmaps/)

### Public Housing & Government

- **CPS (Chicago Public Schools)**: Main data set, schools tagged with '-CPS', plus manually added selective enrollment schools
- **CHA (Chicago Housing Authority)**: [Find Public Housing](https://www.thecha.org/residents/public-housing/find-public-housing)
- **City of Chicago**: [City-Owned Land Inventory](https://www.chicago.gov/city/en/depts/dcd/supp_info/city-owned_land_inventory.html)

### Other Educational Institutions

- **Columbia College**: [Building Codes](https://www.colum.edu/columbia-central/on-campus/building-codes)
- **City Colleges of Chicago**: [Colleges](https://www.ccc.edu/COLLEGES/Pages/default.aspx) | [Facilities & Planning](https://www.ccc.edu/departments/pages/facilities-and-planning.aspx)
