'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const {
  run,
  addedLineNumbers,
  buildCommentBody,
  MARKER,
} = require('../scripts/cloud-native-style/post_suggestions.js');

test('addedLineNumbers parses a simple hunk', () => {
  const patch = '@@ -10,2 +10,3 @@\n-old line\n+new line\n+added line\n context line';
  const added = addedLineNumbers(patch);
  assert.deepEqual([...added].sort((a, b) => a - b), [10, 11]);
});

test('addedLineNumbers returns an empty set when there is no patch', () => {
  assert.equal(addedLineNumbers(undefined).size, 0);
});

test('buildCommentBody embeds the style guide link, marker and suggestion block', () => {
  const body = buildCommentBody({ line: 5, new: '    "bio": "Cloud native engineer",\n' });
  assert.match(body, /style-guide\.md/);
  assert.ok(body.includes(MARKER));
  assert.match(body, /```suggestion/);
});

test('buildCommentBody does not leave a blank line in the suggestion block', () => {
  // fx.new carries a trailing newline from fix_style.py; buildCommentBody must not double it up.
  const body = buildCommentBody({ line: 5, new: '    "bio": "Cloud native engineer",\n' });
  assert.ok(!body.includes('",\n\n```'), `expected no blank line before the closing fence, got:\n${body}`);
});

test('run posts only fixes on added lines and skips untouched ones', async () => {
  const calls = { deleted: [], created: null, failed: null };
  const github = {
    paginate: async (fn, params) => (await fn(params)).data,
    rest: {
      pulls: {
        listFiles: async () => ({
          data: [{ filename: 'people.json', patch: '@@ -1,1 +1,2 @@\n-old\n+line1\n+line2' }],
        }),
        listReviewComments: async () => ({ data: [] }),
        deleteReviewComment: async ({ comment_id }) => {
          calls.deleted.push(comment_id);
        },
        createReview: async (args) => {
          calls.created = args;
        },
      },
    },
  };
  const context = { payload: { pull_request: { number: 42 } }, repo: { owner: 'o', repo: 'r' } };
  const core = {
    setFailed: (msg) => {
      calls.failed = msg;
    },
  };
  const fixes = [
    { line: 1, new: 'fixed-on-added-line' },
    { line: 99, new: 'fixed-on-untouched-line' },
  ];

  const result = await run({ github, context, core, fixes });

  assert.equal(result.posted, 1);
  assert.equal(calls.created.comments.length, 1);
  assert.equal(calls.created.comments[0].line, 1);
  assert.ok(calls.failed.includes('1 cloud native style issue'));
});

test('run deletes stale bot comments before reposting, leaving other users alone', async () => {
  const deleted = [];
  const github = {
    paginate: async (fn, params) => (await fn(params)).data,
    rest: {
      pulls: {
        listFiles: async () => ({ data: [{ filename: 'people.json', patch: '@@ -1,0 +1,1 @@\n+line1' }] }),
        listReviewComments: async () => ({
          data: [
            { id: 1, user: { login: 'github-actions[bot]' }, body: `${MARKER}\nstale` },
            { id: 2, user: { login: 'someone-else' }, body: `${MARKER}\nnot ours` },
          ],
        }),
        deleteReviewComment: async ({ comment_id }) => {
          deleted.push(comment_id);
        },
        createReview: async () => {},
      },
    },
  };
  const context = { payload: { pull_request: { number: 1 } }, repo: { owner: 'o', repo: 'r' } };
  const core = { setFailed: () => {} };
  const fixes = [{ line: 1, new: 'x' }];

  await run({ github, context, core, fixes });

  assert.deepEqual(deleted, [1]);
});

test('run is a no-op when no fixes fall on added lines', async () => {
  let created = false;
  let failed = false;
  const github = {
    paginate: async (fn, params) => (await fn(params)).data,
    rest: {
      pulls: {
        listFiles: async () => ({ data: [{ filename: 'people.json', patch: '@@ -1,0 +1,1 @@\n+line1' }] }),
        listReviewComments: async () => ({ data: [] }),
        deleteReviewComment: async () => {},
        createReview: async () => {
          created = true;
        },
      },
    },
  };
  const context = { payload: { pull_request: { number: 1 } }, repo: { owner: 'o', repo: 'r' } };
  const core = {
    setFailed: () => {
      failed = true;
    },
  };
  const fixes = [{ line: 99, new: 'x' }]; // not in the added set

  const result = await run({ github, context, core, fixes });

  assert.equal(result.posted, 0);
  assert.equal(created, false);
  assert.equal(failed, false);
});

test('run honors a custom targetFile (used to point at a test fixture, never people.json)', async () => {
  let created = null;
  const github = {
    paginate: async (fn, params) => (await fn(params)).data,
    rest: {
      pulls: {
        listFiles: async () => ({
          data: [{ filename: 'tests/fixtures/people.sample.json', patch: '@@ -1,0 +1,1 @@\n+line1' }],
        }),
        listReviewComments: async () => ({ data: [] }),
        deleteReviewComment: async () => {},
        createReview: async (args) => {
          created = args;
        },
      },
    },
  };
  const context = { payload: { pull_request: { number: 1 } }, repo: { owner: 'o', repo: 'r' } };
  const core = { setFailed: () => {} };
  const fixes = [{ line: 1, new: 'x' }];

  const result = await run({ github, context, core, fixes, targetFile: 'tests/fixtures/people.sample.json' });

  assert.equal(result.posted, 1);
  assert.equal(created.comments[0].path, 'tests/fixtures/people.sample.json');
});

test('run finds targetFile and stale comments beyond the first page (regression for pagination gap)', async () => {
  let created = null;
  const deleted = [];
  // Simulate listFiles/listReviewComments each spanning two pages; github.paginate
  // is expected to flatten both pages before run() filters/searches them.
  const filesPage1 = [{ filename: 'unrelated.json', patch: '@@ -1,0 +1,1 @@\n+noise' }];
  const filesPage2 = [{ filename: 'people.json', patch: '@@ -1,0 +1,1 @@\n+line1' }];
  const commentsPage1 = [{ id: 1, user: { login: 'someone-else' }, body: `${MARKER}\nnot ours` }];
  const commentsPage2 = [{ id: 2, user: { login: 'github-actions[bot]' }, body: `${MARKER}\nstale` }];

  const github = {
    paginate: async (fn) => {
      if (fn.name === 'listFiles') return [...filesPage1, ...filesPage2];
      if (fn.name === 'listReviewComments') return [...commentsPage1, ...commentsPage2];
      return [];
    },
    rest: {
      pulls: {
        listFiles: async function listFiles() {},
        listReviewComments: async function listReviewComments() {},
        deleteReviewComment: async ({ comment_id }) => {
          deleted.push(comment_id);
        },
        createReview: async (args) => {
          created = args;
        },
      },
    },
  };
  const context = { payload: { pull_request: { number: 1 } }, repo: { owner: 'o', repo: 'r' } };
  const core = { setFailed: () => {} };
  const fixes = [{ line: 1, new: 'x' }];

  const result = await run({ github, context, core, fixes });

  assert.equal(result.posted, 1, 'people.json on page 2 of listFiles must still be found');
  assert.deepEqual(deleted, [2], 'the stale bot comment on page 2 of listReviewComments must still be deleted');
  assert.equal(created.comments[0].path, 'people.json');
});
