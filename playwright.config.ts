import { defineConfig, devices } from '@playwright/test';

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
// import dotenv from 'dotenv';
// import path from 'path';
// dotenv.config({ path: path.resolve(__dirname, '.env') });

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  testDir: './e2e',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: 'html',
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: 'http://localhost:8080',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    /* Screenshot options for more consistent snapshots */
    screenshot: 'only-on-failure',
  },

  /* Expect options for snapshots */
  expect: {
    /* Threshold for screenshot comparisons (0-1, where 1 is identical) */
    toHaveScreenshot: {
      threshold: 0.2,
    },
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'Desktop Chrome',
      use: { ...devices['Desktop Chrome'] },
    },

    /* Test against a larger mobile viewports */
    {
      name: 'Mobile Chrome',
      use: { ...devices['iPhone 15 Plus'] },
    },
  ],

  /* Run the dev server before starting the tests */
  webServer: {
    command: 'yarn develop',
    url: 'http://localhost:8080',
    // Reuse existing server when running locally (e.g. docker compose up is already running)
    // but always start fresh server in CI environments
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
