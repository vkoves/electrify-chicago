import * as fs from 'fs-extra';
import * as path from 'path';
import { parse } from 'csv-parse/sync';
import { generateSocialImages } from './generateSocialImages';

const SOCIAL_IMAGES_DIR = './static/social-images';
const BUILDING_DATA_FILE = './src/data/dist/building-benchmarks.csv';

interface Building {
  ID: string;
  // eslint-disable-next-line
  [key: string]: any;
}

/**
 * Generate social images only for buildings that don't already have images
 * Uses the existing generateSocialImages function with deleteExisting: false
 */
async function generateMissingSocialImages(): Promise<void> {
  console.log('🔍 Checking for missing social images...');

  // Ensure output directory exists
  await fs.ensureDir(SOCIAL_IMAGES_DIR);

  // Read all building data
  const buildingDataRaw = await fs.readFile(BUILDING_DATA_FILE, 'utf8');
  const allBuildings = parse(buildingDataRaw, {
    columns: true,
    skip_empty_lines: true,
  }) as Building[];

  // Count missing images
  let missingCount = 0;
  for (const building of allBuildings) {
    const imagePath = path.join(
      SOCIAL_IMAGES_DIR,
      `building-${building.ID}.webp`,
    );
    
    if (!(await fs.pathExists(imagePath))) {
      missingCount++;
    }
  }

  console.log(`📊 Found ${allBuildings.length} total buildings`);
  console.log(`🔍 ${missingCount} buildings are missing social images`);

  if (missingCount === 0) {
    console.log('✅ All buildings already have social images! Nothing to do.');
    return;
  }

  await generateSocialImages(null, false);
}

// CLI usage
if (require.main === module) {
  generateMissingSocialImages().catch(console.error);
}
