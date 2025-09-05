import { test, expect } from '@playwright/test';

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

      // Wait for page to be fully loaded
      await page.waitForSelector('header img');
      await page.waitForLoadState('load');

      // Wait for fonts to be done loading
      await page.waitForFunction(() => document.fonts.ready);

      // Take a full screenshot
      await expect(page).toHaveScreenshot(
        `${name.toLowerCase().replace(/\s+/g, '-')}-desktop.png`,
        { fullPage: true },
      );
    });
  });
});
