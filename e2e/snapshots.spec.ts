import { test, expect, Page } from '@playwright/test';

/**
 * Wait for fonts to be loaded, specifically Roboto
 */
async function waitForFontsLoaded(page: Page) {
  // Wait for fonts to be done loading
  await page.waitForFunction(() => document.fonts.ready);

  // Check whether robot is already loaded
  const robotoLoaded = await page.evaluate(() =>
    document.fonts.check('1em Roboto'),
  );

  if (!robotoLoaded) {
    // Wait specifically for Roboto font variants to load (up to 2 seconds each)
    await page.waitForFunction(
      () =>
        document.fonts.check('1em Roboto') &&
        document.fonts.check('400 1em Roboto') &&
        document.fonts.check('bold 1em Roboto'),
      { timeout: 2000 },
    );
  }

  // Give an extra moment for font rendering to stabilize
  await page.waitForTimeout(100);
}

/**
 * Wait for the page to be fully loaded including fonts
 */
async function waitForPageReady(page: Page) {
  // Wait for page to be fully loaded
  await page.waitForLoadState('load');
  await page.waitForSelector('header img');

  await waitForFontsLoaded(page);
}

const IMPORTANT_PAGES = [
  { name: 'Home', url: '/' },
  // Buildings
  // { name: 'All Electric Building', url: '/building-id/239096' },
  // { name: 'Mix Building (Merch Mart)', url: '/building-id/103656' },
  // { name: 'No Image Building', url: '/building-id/103727' },
  // Other Pages
  // { name: 'Ward 47', url: '/ward/47' },
  // { name: 'Building Owner (IIT)', url: '/owner/iit' },
  // { name: 'All Electric Page', url: '/all-electric' },
  // { name: 'Map', url: '/map' },
  // { name: 'Search', url: '/search' },
];

// These take desktop and mobile snapshots through our projects config in `playwright.config.ts`
test.describe('Snapshots', () => {
  IMPORTANT_PAGES.forEach(({ name, url }) => {
    test(`${name} - Desktop`, async ({ page }) => {
      await page.goto(url);
      await waitForPageReady(page);

      // Take a full screenshot
      await expect(page).toHaveScreenshot(
        `${name.toLowerCase().replace(/\s+/g, '-')}-desktop.png`,
        { fullPage: true },
      );
    });
  });
});
