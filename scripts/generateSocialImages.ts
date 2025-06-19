import * as puppeteer from 'puppeteer';
import * as fs from 'fs-extra';
import * as path from 'path';
import { parse } from 'csv-parse/sync';
import { IBuilding } from '../src/common-functions.vue';

type Browser = puppeteer.Browser;
type Page = puppeteer.Page;

const SOCIAL_IMAGES_DIR = './static/social-images';
const BUILDING_DATA_FILE = './src/data/dist/building-benchmarks.csv';
const BASE_URL = process.env.SOCIAL_CARD_BASE_URL || 'http://localhost:8080';

/**
 * Generate social images for specific building IDs or all buildings
 * @param buildingIds - Optional array of specific building IDs to generate. If not provided, generates for all buildings.
 * @param deleteExisting - Whether to delete existing images before generating new ones. Defaults to true.
 */
export async function generateSocialImages(
  buildingIds: string[] | null = null,
  deleteExisting: boolean = true,
): Promise<void> {
  console.log('🎨 Starting social image generation...');

  // Ensure output directory exists
  await fs.ensureDir(SOCIAL_IMAGES_DIR);

  let buildingData: IBuilding[];

  // Clean out existing images for a fresh start (if requested)
  if (deleteExisting) {
    console.log('🧹 Cleaning existing social images...');
    await fs.emptyDir(SOCIAL_IMAGES_DIR);
    console.log('✅ Social images directory cleaned');
  }

  if (buildingIds) {
    // Generate for specific building IDs
    buildingData = buildingIds.map((id) => ({ ID: id }));
    console.log(`📊 Generating for ${buildingData.length} specific buildings`);
  } else {
    // Read all building data
    const buildingDataRaw = await fs.readFile(BUILDING_DATA_FILE, 'utf8');
    buildingData = parse(buildingDataRaw, {
      columns: true,
      skip_empty_lines: true,
    }) as IBuilding[];
    console.log(`📊 Found ${buildingData.length} buildings to process`);
  }

  // Test if the base URL is accessible first
  console.log(`🔗 Testing base URL: ${BASE_URL}`);

  let browser: Browser;

  try {
    browser = await puppeteer.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
      ],
    });
    const testPage = await browser.newPage();
    await testPage.goto(BASE_URL, { timeout: 10000 });

    // Fetch the <h1> to confirm we actually loaded the page
    const topHeadingSelector = await testPage.locator('h1').waitHandle();
    const fullTitle = await topHeadingSelector?.evaluate(
      (el) => el.textContent,
    );

    await testPage.close();
    console.log(`✅ Base URL is accessible! Found title: ${fullTitle?.trim()}`);
  } catch (error) {
    console.error(
      '❌ Cannot access base URL. Make sure your development server is running.',
    );
    console.error(`   Tried to access: ${BASE_URL}`);
    console.error(`   Error: ${(error as Error).message}`);
    console.error(
      '   Run "yarn develop" or "gridsome develop" to start the server.',
    );
    process.exit(1);
  }

  const BatchSize = 1; // Process in batches to manage memory
  const MaxConsecutiveErrors = 5;

  let processed = 0;
  let consecutiveErrors = 0;
  let lastLogTime = Date.now();

  for (let i = 0; i < buildingData.length; i += BatchSize) {
    const batch = buildingData.slice(i, i + BatchSize);

    const results = await Promise.allSettled(
      batch.map(async (building) => {
        const result = await generateSingleImage(browser, building);
        processed++;

        if (processed % 50 === 0) {
          const currentTime = Date.now();
          const batchDuration = ((currentTime - lastLogTime) / 1000).toFixed(1);
          const percentage = ((processed / buildingData.length) * 100).toFixed(
            1,
          );
          lastLogTime = currentTime;

          console.log(
            `✅ Processed ${processed.toLocaleString()}/${buildingData.length.toLocaleString()} ` +
              `buildings (${percentage}%) (took ${batchDuration}s)`,
          );
        }

        return result;
      }),
    );

    // Check for consecutive errors at the start
    for (const result of results) {
      if (result.status === 'rejected') {
        consecutiveErrors++;

        if (
          consecutiveErrors >= MaxConsecutiveErrors &&
          processed <= MaxConsecutiveErrors
        ) {
          console.error(
            `💥 First ${MaxConsecutiveErrors} images all failed to generate. Exiting...`,
          );
          console.error(
            'This usually means the development server is not running or the URLs are incorrect.',
          );
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
export async function generateSingleImage(
  browser: Browser,
  building: IBuilding,
): Promise<void> {
  const outputPath = path.join(
    SOCIAL_IMAGES_DIR,
    `building-${building.ID}.webp`,
  ) as `${string}.webp`;
  const url = `${BASE_URL}/social-card/${building.ID}`;

  // Skip if image already exists (for incremental builds)
  if (await fs.pathExists(outputPath)) {
    return;
  }

  const page: Page = await browser.newPage();

  try {
    // Set viewport to social media dimensions
    await page.setViewport({ width: 1200, height: 630 });

    // Navigate to social card page
    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 3_000, // Increased timeout for slower systems
    });

    // Take screenshot
    await page.screenshot({
      path: outputPath,
      type: 'webp',
      quality: 70,
      omitBackground: false,
    });
  } catch (error) {
    console.error(
      `❌ Failed to generate image for building ${building.ID} at URL: ${url}`,
    );
    console.error(`   Error: ${(error as Error).message}`);
    throw error;
  } finally {
    await page.close();
  }
}

/**
 * Clean up old social images (optional - for when buildings are removed)
 */
export async function cleanupOldImages(): Promise<void> {
  if (!(await fs.pathExists(SOCIAL_IMAGES_DIR))) {
    return;
  }

  // Read current building IDs
  const buildingDataRaw = await fs.readFile(BUILDING_DATA_FILE, 'utf8');
  const buildingData = parse(buildingDataRaw, {
    columns: true,
    skip_empty_lines: true,
  }) as IBuilding[];

  const currentBuildingIds = new Set(
    buildingData.map((b) => `building-${b.ID}.webp`),
  );

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
