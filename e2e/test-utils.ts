import { Page } from '@playwright/test';

/**
 * Wait for fonts to be loaded, specifically Roboto
 */
export async function waitForFontsLoaded(page: Page) {
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
export async function waitForPageReady(page: Page) {
  // Wait for page to be fully loaded
  await page.waitForLoadState('load');
  await page.waitForSelector('header img');

  await waitForFontsLoaded(page);
}

/**
 * Convert a page name to a filename for snapshots
 */
export function pageNameToFileName(name: string): string {
  return name.toLowerCase().replace(/\s+/g, '-');
}
