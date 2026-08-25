import { test, expect } from '@playwright/test';
import { waitForPageReady, pageNameToFileName } from './test-utils';

const LISTING_PAGES = [
  // Mask the map - it loads external tiles, so is a flake risk in visual snapshots
  {
    name: 'All Electric Page',
    url: '/all-electric',
    maskSelectors: ['#buildings-map'],
  },
  { name: 'Ward 47', url: '/ward/47' },
];

test.describe('Listing Page Snapshots', () => {
  LISTING_PAGES.forEach(({ name, url, maskSelectors }) => {
    test(`${name}`, async ({ page }) => {
      await page.goto(url);
      await waitForPageReady(page);

      // Take a full screenshot
      await expect(page).toHaveScreenshot(`${pageNameToFileName(name)}.png`, {
        fullPage: true,
        mask: maskSelectors?.map((selector) => page.locator(selector)),
      });
    });
  });
});
