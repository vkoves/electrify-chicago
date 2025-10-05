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
- **`page-social-images/`** - Social media image configurations (see subdirectory README)

## Usage

Import constants and utilities from these files as needed:

```typescript
import { LatestDataYear } from './globals.vue';
import { generatePageMeta } from './meta-helpers.vue';
```
