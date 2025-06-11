const puppeteer = require('puppeteer');
const fs = require('fs-extra');
const path = require('path');
const { parse } = require('csv-parse/sync');

const SOCIAL_IMAGES_DIR = './static/social-images';
const BUILDING_DATA_FILE = './src/data/dist/building-benchmarks.csv';
const BASE_URL = process.env.SOCIAL_CARD_BASE_URL || 'http://localhost:8080';

/**
 * Generate social images for all buildings using Puppeteer screenshots
 */
async function generateSocialImages() {
  console.log('🎨 Starting social image generation...');

  // Ensure output directory exists
  await fs.ensureDir(SOCIAL_IMAGES_DIR);

  // Read building data
  const buildingDataRaw = await fs.readFile(BUILDING_DATA_FILE, 'utf8');
  const buildingData = parse(buildingDataRaw, {
    columns: true,
    skip_empty_lines: true,
  });

  console.log(`📊 Found ${buildingData.length} buildings to process`);

  // Launch browser
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  let processed = 0;
  let consecutiveErrors = 0;
  const batchSize = 10; // Process in batches to manage memory
  const maxConsecutiveErrors = 5;

  for (let i = 0; i < buildingData.length; i += batchSize) {
    const batch = buildingData.slice(i, i + batchSize);

    const results = await Promise.allSettled(
      batch.map(async (building) => {
        const result = await generateSingleImage(browser, building);
        processed++;

        if (processed % 50 === 0) {
          console.log(`✅ Processed ${processed}/${buildingData.length} buildings`);
        }
        
        return result;
      })
    );

    // Check for consecutive errors at the start
    for (const result of results) {
      if (result.status === 'rejected') {
        consecutiveErrors++;
        if (consecutiveErrors >= maxConsecutiveErrors && processed <= maxConsecutiveErrors) {
          console.error(`💥 First ${maxConsecutiveErrors} images all failed to generate. Exiting...`);
          console.error('This usually means the development server is not running or the URLs are incorrect.');
          await browser.close();
          process.exit(1);
        }
      } else {
        consecutiveErrors = 0; // Reset counter on success
      }
    }
  }

  await browser.close();
  console.log(`🎉 Completed generating ${processed} social images!`);
}

/**
 * Generate a social image for a single building
 */
async function generateSingleImage(browser, building) {
  const outputPath = path.join(SOCIAL_IMAGES_DIR, `building-${building.ID}.png`);
  const url = `${BASE_URL}/social-card/${building.ID}`;

  // Skip if image already exists (for incremental builds)
  if (await fs.pathExists(outputPath)) {
    return;
  }

  const page = await browser.newPage();

  try {
    // Set viewport to social media dimensions
    await page.setViewport({ width: 1200, height: 630 });

    // Navigate to social card page
    await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: 3_000 // this is a local page, so it should load in < 3 seconds
    });

    // Wait for fonts and images to load
    await page.waitForTimeout(1000);

    // Take screenshot
    await page.screenshot({
      path: outputPath,
      type: 'png',
      omitBackground: false
    });

  } catch (error) {
    console.error(`❌ Failed to generate image for building ${building.ID} at URL: ${url}`);
    console.error(`   Error: ${error.message}`);
    throw error;
  } finally {
    await page.close();
  }
}

/**
 * Clean up old social images (optional - for when buildings are removed)
 */
async function cleanupOldImages() {
  if (!(await fs.pathExists(SOCIAL_IMAGES_DIR))) {
    return;
  }

  // Read current building IDs
  const buildingDataRaw = await fs.readFile(BUILDING_DATA_FILE, 'utf8');
  const buildingData = parse(buildingDataRaw, {
    columns: true,
    skip_empty_lines: true,
  });

  const currentBuildingIds = new Set(buildingData.map(b => `building-${b.ID}.png`));

  // Get existing images
  const existingImages = await fs.readdir(SOCIAL_IMAGES_DIR);

  // Remove images for buildings that no longer exist
  for (const image of existingImages) {
    if (image.startsWith('building-') && !currentBuildingIds.has(image)) {
      await fs.remove(path.join(SOCIAL_IMAGES_DIR, image));
      console.log(`🗑️  Removed outdated image: ${image}`);
    }
  }
}

// CLI usage
if (require.main === module) {
  const command = process.argv[2];

  if (command === 'clean') {
    cleanupOldImages().catch(console.error);
  } else {
    generateSocialImages().catch(console.error);
  }
}

module.exports = { generateSocialImages, cleanupOldImages };