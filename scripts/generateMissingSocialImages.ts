import { generateSocialImages } from './generateSocialImages';
import {
  loadAllBuildingData,
  ensureSocialImagesDirectory,
  findMissingImages,
} from './social-images-helpers';

/**
 * Generate social images only for buildings that don't already have images
 * Uses the existing generateSocialImages function with deleteExisting: false
 */
async function generateMissingSocialImages(): Promise<void> {
  console.log('🔍 Checking for missing social images...');

  await ensureSocialImagesDirectory();

  const allBuildings = await loadAllBuildingData();
  const missingIds = await findMissingImages();

  console.log(
    `📊 Found ${allBuildings.length} total buildings\n` +
      `🔍 ${missingIds.length} buildings are missing social images!\n`,
  );

  if (missingIds.length === 0) {
    console.log('✅ All buildings already have social images! Nothing to do.');
    return;
  }

  await generateSocialImages(null, false);
}

// CLI usage
if (require.main === module) {
  generateMissingSocialImages().catch(console.error);
}
