"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
/**
 * Recursively collects all test specs from Playwright suites
 */
function collectTests(suite, allTests) {
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
function parseTestResults() {
    try {
        const resultsPath = path_1.default.join(process.cwd(), 'playwright-report', 'results.json');
        const results = JSON.parse(fs_1.default.readFileSync(resultsPath, 'utf8'));
        const allTests = [];
        const suites = results.suites || [];
        suites.forEach((suite) => collectTests(suite, allTests));
        const totalTests = allTests.length;
        const failedTests = allTests.filter((test) => test.tests.some((t) => t.results.some((r) => r.status === 'failed' || r.status === 'timedOut')));
        const passedTests = totalTests - failedTests.length;
        return { totalTests, passedTests, failedTests };
    }
    catch (error) {
        console.error('Error parsing test results:', error);
        return null;
    }
}
/**
 * Removes ANSI escape codes from a string
 */
function stripAnsiCodes(text) {
    // eslint-disable-next-line no-control-regex
    return text.replace(/\u001b\[[0-9;]*m/g, '');
}
/**
 * Formats test failure information for display
 */
function formatFailures(failedTests) {
    const failures = failedTests.map((spec) => {
        const failedTest = spec.tests.find((t) => t.results.some((r) => r.status === 'failed'));
        const result = failedTest?.results?.find((r) => r.status === 'failed');
        const projectName = failedTest?.projectName || 'Unknown';
        const errorMessage = result?.error?.message || 'Test failed';
        const cleanMessage = stripAnsiCodes(errorMessage);
        return `- **${spec.title}** (${projectName})\n  ${cleanMessage}`;
    });
    return `\n\n<details>\n<summary>Failed Tests</summary>\n\n${failures.join('\n\n')}\n\n</details>`;
}
/**
 * Builds the PR comment body with test results
 */
function buildCommentBody(testResults, artifactUrl, runUrl) {
    let testSummary = '';
    let failureDetails = '';
    if (!testResults) {
        testSummary = '⚠️ Unable to parse test results';
    }
    else if (testResults.failedTests.length === 0) {
        testSummary = `✅ ${testResults.passedTests}/${testResults.totalTests} tests passed!`;
    }
    else {
        testSummary = `❌ ${testResults.failedTests.length}/${testResults.totalTests} tests failed`;
        failureDetails = formatFailures(testResults.failedTests);
    }
    return `## 🎭 Playwright Test Report

${testSummary}${failureDetails}

[📦 Download Full Report](${artifactUrl}) | [🔍 View Run Details](${runUrl})`;
}
/**
 * Posts or updates a PR comment with Playwright test results
 */
async function commentPlaywrightReport({ github, context, }) {
    const artifactUrl = `https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}/artifacts`;
    const runUrl = `https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`;
    const testResults = parseTestResults();
    const body = buildCommentBody(testResults, artifactUrl, runUrl);
    // Find existing comment
    const comments = await github.rest.issues.listComments({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.issue.number,
    });
    const botComment = comments.data.find((comment) => comment.user.type === 'Bot' &&
        comment.body.includes('Playwright Test Report'));
    // Create or update comment
    if (botComment) {
        await github.rest.issues.updateComment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            comment_id: botComment.id,
            body: body,
        });
    }
    else {
        await github.rest.issues.createComment({
            owner: context.repo.owner,
            repo: context.repo.repo,
            issue_number: context.issue.number,
            body: body,
        });
    }
}
exports.default = commentPlaywrightReport;
