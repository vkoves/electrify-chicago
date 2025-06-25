import * as puppeteer from 'puppeteer';
import * as fs from 'fs-extra';
import * as path from 'path';
import { parse } from 'csv-parse/sync';

type Browser = puppeteer.Browser;
type Page = puppeteer.Page;

const SOCIAL_IMAGES_DIR = './static/social-images';
const BUILDING_DATA_FILE = './src/data/dist/building-benchmarks.csv';
const BASE_URL = process.env.SOCIAL_CARD_BASE_URL || 'http://localhost:8080';

/**
 * Load building IDs from either the provided list or the CSV file
 */
async function loadBuildingIds(
  reqBuildingIds: string[] | null,
): Promise<string[]> {
  if (reqBuildingIds) {
    console.log(
      `📊 Generating for ${reqBuildingIds.length} specific buildings`,
    );
    return reqBuildingIds;
  }

  const buildingDataRaw = await fs.readFile(BUILDING_DATA_FILE, 'utf8');
  const buildingData = parse(buildingDataRaw, {
    columns: true,
    skip_empty_lines: true,
  }) as { ID: string | number | boolean }[];

  const buildingIds = buildingData.map((building) => String(building.ID));
  console.log(`📊 Found ${buildingIds.length} buildings to process`);
  return buildingIds;
}

/**
 * Clean existing social images directory
 */
async function cleanupExistingImages(): Promise<void> {
  console.log('🧹 Cleaning existing social images...');
  await fs.emptyDir(SOCIAL_IMAGES_DIR);
  console.log('✅ Social images directory cleaned');
}

/**
 * Setup and test browser accessibility
 */
async function setupBrowser(): Promise<Browser> {
  console.log(`🔗 Testing base URL: ${BASE_URL}`);

  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
    ],
  });

  const testPage = await browser.newPage();

  try {
    await testPage.goto(BASE_URL, { timeout: 10000 });

    const topHeadingSelector = await testPage.locator('h1').waitHandle();
    const fullTitle = await topHeadingSelector?.evaluate(
      (el) => el.textContent,
    );

    console.log(`✅ Base URL is accessible! Found title: ${fullTitle?.trim()}`);
  } catch (error) {
    console.error(
      `❌ Cannot access base URL. Make sure your development server is running.\n` +
        `   Tried to access: ${BASE_URL}\n` +
        `   Error: ${(error as Error).message}\n` +
        `   Run "yarn develop" or "gridsome develop" to start the server.`,
    );

    await browser.close();
    process.exit(1);
  } finally {
    await testPage.close();
  }

  return browser;
}

/**
 * Process building images in batches with error handling and progress logging
 */
async function processBuildingBatch(
  browser: Browser,
  buildingIds: string[],
  batchSize: number = 1,
  maxConsecutiveErrors: number = 5,
): Promise<void> {
  let processed = 0;
  let consecutiveErrors = 0;
  let lastLogTime = Date.now();

  for (let i = 0; i < buildingIds.length; i += batchSize) {
    const batch = buildingIds.slice(i, i + batchSize);

    const results = await Promise.allSettled(
      batch.map(async (buildingId) => {
        const result = await generateSingleImage(browser, buildingId);
        processed++;

        if (processed % 50 === 0) {
          const currentTime = Date.now();
          const batchDuration = ((currentTime - lastLogTime) / 1000).toFixed(1);
          const percentage = ((processed / buildingIds.length) * 100).toFixed(
            1,
          );
          lastLogTime = currentTime;

          console.log(
            `✅ Processed ${processed.toLocaleString()}/${buildingIds.length.toLocaleString()} ` +
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
          consecutiveErrors >= maxConsecutiveErrors &&
          processed <= maxConsecutiveErrors
        ) {
          console.error(
            `💥 First ${maxConsecutiveErrors} images all failed to generate. Exiting...`,
          );
          console.error(
            'This usually means the development server is not running or the URLs are incorrect.',
          );
          throw new Error('Too many consecutive errors at start');
        }
      } else {
        consecutiveErrors = 0; // Reset counter on success
      }
    }
  }

  console.log(`🎉 Completed generating ${processed} social images!`);
}

/**
 * Generate social images for specific building IDs or all buildings
 * @param reqBuildingIds - Optional array of specific building IDs to generate. If not provided, generates for all buildings.
 * @param deleteExisting - Whether to delete existing images before generating new ones. Defaults to true.
 */
export async function generateSocialImages(
  reqBuildingIds: string[] | null = null,
  deleteExisting: boolean = true,
): Promise<void> {
  console.log('🎨 Starting social image generation...');

  await fs.ensureDir(SOCIAL_IMAGES_DIR);

  if (deleteExisting) {
    await cleanupExistingImages();
  }

  const buildingIds = await loadBuildingIds(reqBuildingIds);
  const browser = await setupBrowser();

  try {
    await processBuildingBatch(browser, buildingIds);
  } finally {
    await browser.close();
  }
}

/**
 * Generate a social image for a single building
 */
export async function generateSingleImage(
  browser: Browser,
  buildingId: string,
): Promise<void> {
  const outputPath = path.join(
    SOCIAL_IMAGES_DIR,
    `building-${buildingId}.webp`,
  ) as `${string}.webp`;
  const url = `${BASE_URL}/social-card/${buildingId}`;

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
      `❌ Failed to generate image for building ${buildingId} at URL: ${url}`,
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
  }) as { ID: string | number | boolean }[];

  const currentBuildingIds = new Set(
    buildingData.map((b) => `building-${String(b.ID)}.webp`),
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
