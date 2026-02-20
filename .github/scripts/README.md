# GitHub Actions Scripts

This directory contains TypeScript scripts used by GitHub Actions workflows.

## comment-playwright-report.ts

Posts or updates PR comments with Playwright test results. This script:
- Parses Playwright JSON test results
- Fetches artifact IDs for direct download links
- Creates/updates a single PR comment showing passed/failed tests
- Consolidates duplicate test names (Desktop/Mobile)
- Includes expandable sections for test details

Used by `.github/workflows/playwright.yml` after tests run.

## test-comment-script.ts

Local testing harness for `comment-playwright-report.ts`. Mocks the GitHub API and logs what would be called.

**Usage:**
```bash
yarn test-playwright-comment
```

This reads your local `playwright-report/results.json` and shows exactly what comment would be posted to a PR.

**Testing scenarios:**
- Edit line 20 in `test-comment-script.ts` to simulate an existing comment
- Run Playwright tests to generate different results (passed/failed)
- Verify comment formatting without pushing to CI

## Development

Both scripts are written in TypeScript and compiled to JavaScript during CI:

```bash
npx tsc .github/scripts/comment-playwright-report.ts --module commonjs --target ES2020 --esModuleInterop --skipLibCheck
```

The compiled `.js` files are gitignored and generated fresh in CI.
