/**
 * Local test harness for the Playwright comment script
 * This mocks the GitHub API and logs what would be called
 */
import commentPlaywrightReport from './comment-playwright-report';

// Mock GitHub API that logs instead of making real calls
const mockGitHub = {
  rest: {
    issues: {
      listComments: async (params: {
        owner: string;
        repo: string;
        issue_number: number;
      }) => {
        console.log('\n📝 [Mock] listComments called with:', params);
        // Return mock data - simulate existing comment or no comment
        // Change this to test different scenarios
        return {
          data: [
            // Uncomment to simulate existing comment:
            // {
            //   id: 12345,
            //   user: { login: 'github-actions[bot]' },
            //   body: '## 🎭 Playwright Visual Test Report\n\nOld content',
            // },
          ],
        };
      },
      updateComment: async (params: {
        owner: string;
        repo: string;
        comment_id: number;
        body: string;
      }) => {
        console.log('\n✏️  [Mock] updateComment called with:');
        console.log('   Comment ID:', params.comment_id);
        console.log('   Owner:', params.owner);
        console.log('   Repo:', params.repo);
        console.log('\n📄 Comment body that would be posted:');
        console.log('─'.repeat(80));
        console.log(params.body);
        console.log('─'.repeat(80));
      },
      createComment: async (params: {
        owner: string;
        repo: string;
        issue_number: number;
        body: string;
      }) => {
        console.log('\n➕ [Mock] createComment called with:');
        console.log('   Issue:', params.issue_number);
        console.log('   Owner:', params.owner);
        console.log('   Repo:', params.repo);
        console.log('\n📄 Comment body that would be posted:');
        console.log('─'.repeat(80));
        console.log(params.body);
        console.log('─'.repeat(80));
      },
    },
    actions: {
      listWorkflowRunArtifacts: async (params: {
        owner: string;
        repo: string;
        run_id: number;
      }) => {
        console.log(
          '\n🔍 [Mock] listWorkflowRunArtifacts called with:',
          params,
        );
        // Return mock artifact data
        return {
          data: {
            artifacts: [
              {
                id: 5596343156,
                name: 'playwright-report',
              },
            ],
          },
        };
      },
    },
  },
};

// Mock GitHub Actions context
const mockContext = {
  repo: {
    owner: 'vkoves',
    repo: 'electrify-chicago',
  },
  runId: 12345678,
  issue: {
    number: 123,
  },
};

// Run the script
console.log('🧪 Testing Playwright comment script locally...\n');
console.log('Context:', {
  owner: mockContext.repo.owner,
  repo: mockContext.repo.repo,
  runId: mockContext.runId,
  issueNumber: mockContext.issue.number,
});

commentPlaywrightReport({
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  github: mockGitHub as any,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  context: mockContext as any,
})
  .then(() => {
    console.log('\n✅ Script completed successfully!');
  })
  .catch((error) => {
    console.error('\n❌ Script failed:', error);
    process.exit(1);
  });
