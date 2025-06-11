/* eslint-env node */
const puppeteer = require('puppeteer');
const fs = require('fs-extra');
const path = require('path');

const SOCIAL_IMAGES_DIR = './static/social-images';
const BASE_URL = process.env.SOCIAL_CARD_BASE_URL || 'http://localhost:8080';

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
  console.log(`📊 Generating images for ${TEST_BUILDING_IDS.length} test buildings`);

  // Ensure output directory exists
  await fs.ensureDir(SOCIAL_IMAGES_DIR);

  // Test if the base URL is accessible first
  console.log(`🔗 Testing base URL: ${BASE_URL}`);

  let browser;

  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
    });
    const testPage = await browser.newPage();
    await testPage.goto(BASE_URL, { timeout: 10000 });

    // Fetch the <h1> to confirm we actually loaded the page
    const topHeadingSelector = await testPage.locator('h1').waitHandle();
    const fullTitle = await topHeadingSelector?.evaluate((el) => el.textContent);

    await testPage.close();
    console.log(`✅ Base URL is accessible! Found title: ${fullTitle.trim()}`);
  } catch (error) {
    console.error('❌ Cannot access base URL. Make sure your development server is running.');
    console.error(`   Tried to access: ${BASE_URL}`);
    console.error(`   Error: ${error.message}`);
    console.error('   Run "yarn develop" or "gridsome develop" to start the server.');
    process.exit(1);
  }

  let processed = 0;
  let failed = 0;

  // Generate images for each test building
  for (const buildingId of TEST_BUILDING_IDS) {
    try {
      console.log(`🏢 Generating image for building ${buildingId}...`);
      await generateSingleImage(browser, buildingId);
      processed++;
      console.log(`✅ Generated image for building ${buildingId}`);
    } catch (error) {
      failed++;
      console.error(`❌ Failed to generate image for building ${buildingId}:`, error.message);
    }
  }

  await browser.close();

  console.log(`\n🎉 Test image generation complete!`);
  console.log(`✅ Successfully generated: ${processed} images`);
  if (failed > 0) {
    console.log(`❌ Failed to generate: ${failed} images`);
  }
  console.log(`📁 Images saved to: ${SOCIAL_IMAGES_DIR}`);

  // List the generated files
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
}

/**
 * Generate a social image for a single building
 */
async function generateSingleImage(browser, buildingId) {
  const outputPath = path.join(SOCIAL_IMAGES_DIR, `building-${buildingId}.png`);
  const url = `${BASE_URL}/social-card/${buildingId}`;

  const page = await browser.newPage();

  try {
    // Set viewport to social media dimensions
    await page.setViewport({ width: 1200, height: 630 });

    // Navigate to social card page
    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 15000,
    });

    // Take screenshot
    await page.screenshot({
      path: outputPath,
      type: 'png',
      omitBackground: false,
    });

  } catch (error) {
    console.error(`❌ Failed to generate image for building ${buildingId} at URL: ${url}`);
    console.error(`   Error: ${error.message}`);
    throw error;
  } finally {
    await page.close();
  }
}

// CLI usage
if (require.main === module) {
  generateTestSocialImages().catch(console.error);
}

module.exports = { generateTestSocialImages };