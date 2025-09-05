import { test, expect } from '@playwright/test';
import { waitForPageReady, pageNameToFileName } from './test-utils';

const CORE_PAGES = [
  { name: 'Building Owner (IIT)', url: '/owner/iit' },
  { name: 'Search', url: '/search' },
  // Map is bulkier and requires external assets, so more flaky
  // { name: 'Map', url: '/map' },
];

test.describe('Core Page Snapshots', () => {
  CORE_PAGES.forEach(({ name, url }) => {
    test(`${name}`, async ({ page }) => {
      await page.goto(url);
      await waitForPageReady(page);

      // Take a full screenshot
      await expect(page).toHaveScreenshot(`${pageNameToFileName(name)}.png`, {
        fullPage: true,
      });
    });
  });
});
