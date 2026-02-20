import fs from 'fs';
import path from 'path';

interface PlaywrightTest {
  projectName?: string;
  results: Array<{
    status: string;
    error?: { message?: string };
  }>;
  expectedStatus?: string;
}

interface PlaywrightSpec {
  title: string;
  tests: PlaywrightTest[];
}

interface PlaywrightSuite {
  specs?: PlaywrightSpec[];
  suites?: PlaywrightSuite[];
}

interface PlaywrightResults {
  suites?: PlaywrightSuite[];
}

interface TestResults {
  totalTests: number;
  passedTests: PlaywrightSpec[];
  failedTests: PlaywrightSpec[];
}

interface GitHubContext {
  repo: { owner: string; repo: string };
  runId: number;
  issue: { number: number };
}

interface GitHubAPI {
  rest: {
    issues: {
      listComments: (params: {
        owner: string;
        repo: string;
        issue_number: number;
      }) => Promise<{
        data: Array<{ user: { type: string }; body: string; id: number }>;
      }>;
      updateComment: (params: {
        owner: string;
        repo: string;
        comment_id: number;
        body: string;
      }) => Promise<void>;
      createComment: (params: {
        owner: string;
        repo: string;
        issue_number: number;
        body: string;
      }) => Promise<void>;
    };
    actions: {
      listWorkflowRunArtifacts: (params: {
        owner: string;
        repo: string;
        run_id: number;
      }) => Promise<{
        data: { artifacts: Array<{ id: number; name: string }> };
      }>;
    };
  };
}

/**
 * Recursively collects all test specs from Playwright suites
 */
function collectTests(suite: PlaywrightSuite, allTests: PlaywrightSpec[]): void {
  if (suite.specs) {
    allTests.push(...suite.specs);
  }
  if (suite.suites) {
    suite.suites.forEach((s) => collectTests(s, allTests));
  }
}

/**
 * Reads and parses Playwright test results from JSON file
 */
function parseTestResults(): TestResults | null {
  try {
    const resultsPath = path.join(
      process.cwd(),
      'playwright-report',
      'results.json'
    );
    const results = JSON.parse(
      fs.readFileSync(resultsPath, 'utf8')
    ) as PlaywrightResults;

    const allTests: PlaywrightSpec[] = [];
    const suites = results.suites || [];
    suites.forEach((suite) => collectTests(suite, allTests));

    const totalTests = allTests.length;
    const failedTests = allTests.filter((test) =>
      test.tests.some((t) =>
        t.results.some((r) => r.status === 'failed' || r.status === 'timedOut')
      )
    );
    const passedTests = allTests.filter((test) =>
      !failedTests.includes(test)
    );

    return { totalTests, passedTests, failedTests };
  } catch (error) {
    console.error('Error parsing test results:', error);
    return null;
  }
}

/**
 * Removes ANSI escape codes from a string
 */
function stripAnsiCodes(text: string): string {
  // Control character (\u001b = ESC) is intentional for matching ANSI codes
  // eslint-disable-next-line no-control-regex
  return text.replace(/\u001b\[[0-9;]*m/g, '');
}

/**
 * Extracts the key error message from Playwright error output
 */
function extractKeyError(errorMessage: string): string {
  const clean = stripAnsiCodes(errorMessage);

  // Look for pixel difference messages
  const pixelDiffMatch = clean.match(/(\d+) pixels \(ratio [0-9.]+.*?\) are different/);
  if (pixelDiffMatch) {
    return pixelDiffMatch[0];
  }

  // Look for image size differences
  const sizeDiffMatch = clean.match(/Expected an image .+?\. \d+ pixels \(ratio [0-9.]+.*?\) are different/);
  if (sizeDiffMatch) {
    return sizeDiffMatch[0];
  }

  // Fall back to first non-empty line
  const lines = clean.split('\n').map(l => l.trim()).filter(l => l.length > 0);
  return lines[0] || 'Test failed';
}

/**
 * Formats test failure information for display
 */
function formatFailures(failedTests: PlaywrightSpec[]): string {
  const failures = failedTests.map((spec) => {
    const failedTest = spec.tests.find((t) =>
      t.results.some((r) => r.status === 'failed')
    );
    const result = failedTest?.results?.find((r) => r.status === 'failed');
    const projectName = failedTest?.projectName || 'Unknown';

    const errorMessage = result?.error?.message || 'Test failed';
    const keyError = extractKeyError(errorMessage);

    return `- **${spec.title}** (${projectName})\n  ${keyError}`;
  });

  return `\n\n<details>\n<summary>Failed Tests (${failedTests.length})</summary>\n\n${failures.join('\n\n')}\n\n</details>`;
}

/**
 * Formats passed test information for display
 */
function formatPassed(passedTests: PlaywrightSpec[]): string {
  const passed = passedTests.map((spec) => {
    const passedTest = spec.tests.find((t) =>
      t.results.some((r) => r.status === 'passed')
    );
    const projectName = passedTest?.projectName || 'Unknown';

    return `- **${spec.title}** (${projectName})`;
  });

  return `\n\n<details>\n<summary>Passed Tests (${passedTests.length})</summary>\n\n${passed.join('\n')}\n\n</details>`;
}

/**
 * Builds the PR comment body with test results
 */
function buildCommentBody(
  testResults: TestResults | null,
  artifactUrl: string,
  runUrl: string
): string {
  let testSummary = '';
  let testDetails = '';

  if (!testResults) {
    testSummary = '⚠️ Unable to parse test results';
  } else if (testResults.failedTests.length === 0) {
    // Get unique page names from all tests
    const allPages = [...new Set(testResults.passedTests.map((t) => t.title))];
    const pageList = allPages.slice(0, 5).join(', ');
    const morePages =
      allPages.length > 5 ? ` and ${allPages.length - 5} more` : '';

    testSummary = `**✅ ${testResults.passedTests.length}/${testResults.totalTests} tests passed!** 🎉\n\nWe didn't detect any visual changes on: ${pageList}${morePages}`;
    testDetails = formatPassed(testResults.passedTests);
  } else {
    // Get unique page names from failed tests
    const failedPages = [
      ...new Set(testResults.failedTests.map((t) => t.title)),
    ];
    const pageList = failedPages.join(', ');

    testSummary = `**❌ ${testResults.failedTests.length}/${testResults.totalTests} tests failed**\n\nWe've detected visual changes on: ${pageList}`;
    testDetails = formatFailures(testResults.failedTests) + formatPassed(testResults.passedTests);
  }

  return `## 🎭 Playwright Visual Test Report

${testSummary}${testDetails}

[📦 Download Full Report](${artifactUrl}) | [🔍 View Run Details](${runUrl})`;
}

/**
 * Posts or updates a PR comment with Playwright test results
 */
export default async function commentPlaywrightReport({
  github,
  context,
}: {
  github: GitHubAPI;
  context: GitHubContext;
}): Promise<void> {
  const runUrl = `https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`;

  // Fetch the artifact ID for the playwright-report
  let artifactUrl = `https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}/artifacts`;
  try {
    const artifacts = await github.rest.actions.listWorkflowRunArtifacts({
      owner: context.repo.owner,
      repo: context.repo.repo,
      run_id: context.runId,
    });

    const playwrightArtifact = artifacts.data.artifacts.find(
      (artifact: { name: string }) => artifact.name === 'playwright-report'
    );

    if (playwrightArtifact) {
      artifactUrl = `https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}/artifacts/${playwrightArtifact.id}`;
    }
  } catch (error) {
    console.error('Failed to fetch artifact ID:', error);
    // Fall back to generic artifacts URL
  }

  const testResults = parseTestResults();
  const body = buildCommentBody(testResults, artifactUrl, runUrl);

  // Find existing comment
  const comments = await github.rest.issues.listComments({
    owner: context.repo.owner,
    repo: context.repo.repo,
    issue_number: context.issue.number,
  });

  const botComment = comments.data.find(
    (comment) =>
      comment.user.type === 'Bot' &&
      comment.body.includes('Playwright Test Report')
  );

  // Create or update comment
  if (botComment) {
    await github.rest.issues.updateComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      comment_id: botComment.id,
      body: body,
    });
  } else {
    await github.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: context.issue.number,
      body: body,
    });
  }
}
