import * as puppeteer from 'puppeteer';
import * as fs from 'fs-extra';
import * as path from 'path';
import {
  SOCIAL_IMAGES_DIR,
  BASE_URL,
  loadBuildingIds as loadAllBuildingIds,
  ensureSocialImagesDirectory,
  getSocialImagePath,
  getPageSocialImagePath,
  getOwnerSocialImagePath,
  getAvailablePageIdsFromConfig,
  getAvailableOwnerIds,
  pageImageExists,
  ownerImageExists,
} from './social-images-helpers';

type Browser = puppeteer.Browser;
type Page = puppeteer.Page;

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

  const buildingIds = await loadAllBuildingIds();
  console.log(`📊 Found ${buildingIds.length} buildings to process`);
  return buildingIds;
}

/**
 * Clean existing social images directory
 */
async function cleanupExistingImages(): Promise<void> {
  console.log(
    '🧹 Cleaning existing social images...\n' +
      '✅ Social images directory cleaned',
  );
  await fs.emptyDir(SOCIAL_IMAGES_DIR);
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
            `💥 First ${maxConsecutiveErrors} images all failed to generate. Exiting...\n` +
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
 * Generate page social images for all configured pages
 */
export async function generatePageSocialImages(
  deleteExisting: boolean = true,
): Promise<void> {
  console.log('🎨 Starting page social image generation...');

  await ensureSocialImagesDirectory();

  const pageIds = getAvailablePageIdsFromConfig();
  console.log(
    `📊 Found ${pageIds.length} pages to process: ${pageIds.join(', ')}`,
  );

  const browser = await setupBrowser();

  try {
    let processed = 0;
    for (const pageId of pageIds) {
      try {
        // Skip if image already exists and we're not deleting existing ones
        if (!deleteExisting && (await pageImageExists(pageId))) {
          console.log(`⏭️  Page ${pageId} already has social image, skipping`);
          continue;
        }

        await generateSinglePageImage(browser, pageId);
        processed++;
        console.log(
          `✅ Generated page social image for ${pageId} (${processed}/${pageIds.length})`,
        );
      } catch (error) {
        console.error(
          `❌ Failed to generate page image for ${pageId}:`,
          (error as Error).message,
        );
      }
    }

    console.log(`🎉 Completed generating ${processed} page social images!`);
  } finally {
    await browser.close();
  }
}

/**
 * Generate owner social images for all configured owners
 */
export async function generateOwnerSocialImages(
  deleteExisting: boolean = true,
): Promise<void> {
  console.log('🏢 Starting owner social image generation...');

  await ensureSocialImagesDirectory();

  const ownerIds = getAvailableOwnerIds();
  console.log(
    `📊 Found ${ownerIds.length} owners to process: ${ownerIds.join(', ')}`,
  );

  const browser = await setupBrowser();

  try {
    let processed = 0;
    for (const ownerId of ownerIds) {
      try {
        // Skip if image already exists and we're not deleting existing ones
        if (!deleteExisting && (await ownerImageExists(ownerId))) {
          console.log(`⏭️  Owner ${ownerId} already has social image, skipping`);
          continue;
        }

        await generateSingleOwnerImage(browser, ownerId);
        processed++;
        console.log(
          `✅ Generated owner social image for ${ownerId} (${processed}/${ownerIds.length})`,
        );
      } catch (error) {
        console.error(
          `❌ Failed to generate owner image for ${ownerId}:`,
          (error as Error).message,
        );
      }
    }

    console.log(`🎉 Completed generating ${processed} owner social images!`);
  } finally {
    await browser.close();
  }
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

  await ensureSocialImagesDirectory();

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
 * Generate building, page, and owner social images
 */
export async function generateAllSocialImages(
  reqBuildingIds: string[] | null = null,
  deleteExisting: boolean = true,
): Promise<void> {
  console.log(
    '🎨 Starting complete social image generation (buildings + pages + owners)...',
  );

  // Generate page social images first (they're faster)
  await generatePageSocialImages(deleteExisting);

  // Generate owner social images (also fast)
  await generateOwnerSocialImages(false); // Don't delete again

  // Then generate building social images (slowest)
  await generateSocialImages(reqBuildingIds, false); // Don't delete again
}

/**
 * Generate a social image for a single building
 */
export async function generateSingleImage(
  browser: Browser,
  buildingId: string,
): Promise<void> {
  const outputPath = getSocialImagePath(buildingId) as `${string}.webp`;
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
      `❌ Failed to generate image for building ${buildingId} at URL: ${url}\n` +
        `   Error: ${(error as Error).message}`,
    );
    throw error;
  } finally {
    await page.close();
  }
}

/**
 * Generate a social image for a single page
 */
export async function generateSinglePageImage(
  browser: Browser,
  pageId: string,
): Promise<void> {
  const outputPath = getPageSocialImagePath(pageId) as `${string}.webp`;
  const url = `${BASE_URL}/page-social-card/${pageId}`;

  // Skip if image already exists (for incremental builds)
  if (await fs.pathExists(outputPath)) {
    return;
  }

  const page: Page = await browser.newPage();

  try {
    // Set viewport to social media dimensions
    await page.setViewport({ width: 1200, height: 630 });

    // Navigate to page social card page
    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 5_000, // Longer timeout for page cards with more content
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
      `❌ Failed to generate page image for ${pageId} at URL: ${url}\n` +
        `   Error: ${(error as Error).message}`,
    );
    throw error;
  } finally {
    await page.close();
  }
}

/**
 * Generate a social image for a single owner
 */
export async function generateSingleOwnerImage(
  browser: Browser,
  ownerId: string,
): Promise<void> {
  const outputPath = getOwnerSocialImagePath(ownerId) as `${string}.webp`;
  const url = `${BASE_URL}/owner-social-card/${ownerId}`;

  // Skip if image already exists (for incremental builds)
  if (await fs.pathExists(outputPath)) {
    return;
  }

  const page: Page = await browser.newPage();

  try {
    // Set viewport to social media dimensions
    await page.setViewport({ width: 1200, height: 630 });

    // Navigate to owner social card page
    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 5_000, // Longer timeout for owner cards with more content
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
      `❌ Failed to generate owner image for ${ownerId} at URL: ${url}\n` +
        `   Error: ${(error as Error).message}`,
    );
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
  const buildingIds = await loadAllBuildingIds();
  const currentBuildingIds = new Set(
    buildingIds.map((id) => `building-${id}.webp`),
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
  } else if (command === 'pages') {
    generatePageSocialImages().catch(console.error);
  } else if (command === 'owners') {
    generateOwnerSocialImages().catch(console.error);
  } else if (command === 'buildings') {
    generateSocialImages().catch(console.error);
  } else {
    // Default to generating all images (buildings + pages + owners)
    generateAllSocialImages().catch(console.error);
  }
}
