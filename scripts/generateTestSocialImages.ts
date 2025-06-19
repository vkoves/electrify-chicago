import { generateSocialImages } from './generateSocialImages.js';
import * as fs from 'fs-extra';
import * as path from 'path';

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
  console.log('🎨 Starting test social image generation...');
  console.log('📁 Preserving existing social images (except test images)');

  const SOCIAL_IMAGES_DIR = './static/social-images';

  // Delete only the test images we're about to regenerate
  console.log('🧹 Cleaning existing test images...');
  for (const buildingId of TEST_BUILDING_IDS) {
    const testImagePath = path.join(SOCIAL_IMAGES_DIR, `building-${buildingId}.webp`);
    if (await fs.pathExists(testImagePath)) {
      await fs.remove(testImagePath);
      console.log(`   🗑️  Removed building-${buildingId}.webp`);
    }
  }

  try {
    // Use the main generateSocialImages function with specific building IDs
    // Pass false to preserve existing images
    await generateSocialImages(TEST_BUILDING_IDS, false);

    // List the generated files
    const generatedFiles = TEST_BUILDING_IDS.map((id) => `building-${id}.webp`);

    console.log(`\n📋 Generated files:`);

    for (const file of generatedFiles) {
      const filePath = path.join(SOCIAL_IMAGES_DIR, file);

      if (await fs.pathExists(filePath)) {
        console.log(`   ✅ ${file}`);
      } else {
        console.log(`   ❌ ${file} (failed to generate)`);
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
