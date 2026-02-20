import { test, expect } from '@playwright/test';
import { waitForPageReady, pageNameToFileName } from './test-utils';

const BuildingPages = [
  { name: 'All Electric Building', url: '/building-id/239096' },
  { name: 'Mix Building (Merch Mart)', url: '/building-id/103656' },
  { name: 'No Image Building', url: '/building-id/103727' },
];

// Standard US Letter page size: 8.5" x 11" at 96 DPI
const PrintPageWidth = 816; // 8.5 * 96
const PrintPageHeight = 1056; // 11 * 96

// Configure to only run on Desktop Chrome with print page dimensions
test.use({
  viewport: { width: PrintPageWidth, height: PrintPageHeight }
});

test.describe('Building Page Print Mode Snapshots', () => {

  BuildingPages.forEach(({ name, url }) => {
    test(`${name} (Print Page 1)`, async ({ page }) => {
      await page.goto(url);
      await waitForPageReady(page);

      // Emulate print media to apply print CSS styles first
      await page.emulateMedia({ media: 'print' });

      // Fire the beforeprint event to trigger QR code generation
      await page.evaluate(() => {
        window.dispatchEvent(new Event('beforeprint'));
      });

      // Wait for QR code SVG to be rendered
      await page.waitForSelector('.qr-code svg', { timeout: 5000 });

      // Screenshot just the first page (standard letter size)
      // This ensures all critical info fits on page 1
      await expect(page).toHaveScreenshot(
        `${pageNameToFileName(name)}-print-page1.png`,
        {
          fullPage: false, // Only capture viewport (first page)
        }
      );
    });
  });
});
