import { test, expect } from '@playwright/test';
import { waitForPageReady, pageNameToFileName } from './test-utils';

const BUILDING_PAGES = [
  { name: 'All Electric Building', url: '/building-id/239096' },
  { name: 'Mix Building (Merch Mart)', url: '/building-id/103656' },
  { name: 'No Image Building', url: '/building-id/103727' },
];

test.describe('Building Page Snapshots', () => {
  BUILDING_PAGES.forEach(({ name, url }) => {
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
