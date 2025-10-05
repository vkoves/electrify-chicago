import * as fs from 'fs-extra';
import { getSocialImagePath, removeImages } from './social-images-helpers';
import { generateBuildingSocialImages } from './generateSocialImages';

// Test building IDs from the SocialCards debug page
const TEST_BUILDING_IDS: string[] = [
  '256419', // Crown Hall (Has Image)
  '239096', // Marina Towers (Has Image, Long Title & Vert. Image)
  '257000', // 445 W Erie (No Image)
];

/**
 * Generate social images for the three test buildings only
 */
export async function generateTestSocialImages(): Promise<void> {
  console.log(
    '🎨 Starting test social image generation...\n' +
      '📁 Preserving existing social images (except test images)\n' +
      '🧹 Cleaning existing test images...',
  );
  await removeImages(TEST_BUILDING_IDS);

  try {
    // Use the main generateBuildingSocialImages function with specific building IDs
    // Pass false to preserve existing images
    await generateBuildingSocialImages(TEST_BUILDING_IDS, false);

    console.log(`\n📋 Generated files:`);

    for (const buildingId of TEST_BUILDING_IDS) {
      const filePath = getSocialImagePath(buildingId);
      const fileName = `building-${buildingId}.webp`;

      if (await fs.pathExists(filePath)) {
        console.log(`   ✅ ${fileName}`);
      } else {
        console.log(`   ❌ ${fileName} (failed to generate)`);
      }
    }
  } catch (error) {
    console.error(
      '❌ Test social image generation failed:',
      (error as Error).message,
    );
    process.exit(1);
  }
}

// CLI usage
if (require.main === module) {
  generateTestSocialImages().catch(console.error);
}
