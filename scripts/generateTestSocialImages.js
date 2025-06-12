/* eslint-env node */
const { generateSocialImages } = require('./generateSocialImages');
const fs = require('fs-extra');
const path = require('path');

// Test building IDs from the SocialCards debug page
const TEST_BUILDING_IDS = [
  '256419', // Crown Hall (Has Image)
  '239096', // Marina Towers (Has Image, Long Title & Vert. Image)
  '257000', // 445 W Erie (No Image)
];

/**
 * Generate social images for the three test buildings only
 */
async function generateTestSocialImages() {
  console.log('🎨 Starting test social image generation...');
  
  try {
    // Use the main generateSocialImages function with specific building IDs
    await generateSocialImages(TEST_BUILDING_IDS);
    
    // List the generated files
    const SOCIAL_IMAGES_DIR = './static/social-images';
    const generatedFiles = TEST_BUILDING_IDS.map(id => `building-${id}.png`);
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
    console.error('❌ Test social image generation failed:', error.message);
    process.exit(1);
  }
}

// CLI usage
if (require.main === module) {
  generateTestSocialImages().catch(console.error);
}

module.exports = { generateTestSocialImages };