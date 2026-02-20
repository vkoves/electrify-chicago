/* eslint-env node */
/**
 * Posts or updates a PR comment with links to the Playwright test report artifact
 * @param {object} params - Parameters from GitHub Actions
 * @param {object} params.github - GitHub API client
 * @param {object} params.context - GitHub Actions context
 */
module.exports = async ({ github, context }) => {
  const artifactUrl = `https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}/artifacts`;
  const runUrl = `https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId}`;
  const body = `## 🎭 Playwright Test Report\n\n[📦 Download Playwright Report](${artifactUrl})\n\n[🔍 View Full Run Details](${runUrl})`;

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
};
