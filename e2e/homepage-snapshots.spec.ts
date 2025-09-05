import { test, expect } from '@playwright/test';
import { waitForPageReady } from './test-utils';

test.describe('Homepage Snapshots', () => {
  test('Home', async ({ page }) => {
    await page.goto('/');
    await waitForPageReady(page);

    // Take a full screenshot
    await expect(page).toHaveScreenshot('home.png', {
      fullPage: true,
    });
  });
});