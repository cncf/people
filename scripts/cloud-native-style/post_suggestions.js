'use strict';

const STYLE_GUIDE_URL =
  'https://github.com/cncf/foundation/blob/main/style-guide.md#1-cloud-native-and-open-source';
const MARKER = '<!-- cloud-native-style -->';
const BOT_LOGIN = 'github-actions[bot]';

/**
 * Parse a unified diff `patch` (as returned by GET /pulls/{n}/files) and
 * return the set of 1-based line numbers added/changed on the RIGHT (new) side.
 * Mirrors reviewdog's `filter_mode: added` so only lines introduced by this PR
 * are flagged, never pre-existing occurrences elsewhere in the file.
 */
function addedLineNumbers(patch) {
  const added = new Set();
  if (!patch) return added;

  let newLine = 0;
  for (const l of patch.split('\n')) {
    const hunk = l.match(/^@@ -\d+(?:,\d+)? \+(\d+)/);
    if (hunk) {
      newLine = parseInt(hunk[1], 10) - 1;
      continue;
    }
    if (l.startsWith('+') && !l.startsWith('+++')) {
      newLine++;
      added.add(newLine);
    } else if (!l.startsWith('-')) {
      newLine++;
    }
  }
  return added;
}

function buildCommentBody(fix) {
  // fx.new already ends with the line's original trailing newline (see fix_style.py),
  // so don't add another one here or the suggestion block gets a blank line.
  //
  // Deliberately doesn't restate the exact casing applied (lowercase vs.
  // Title Case vs. sentence-start) — that varies by context and the
  // suggestion diff below already shows precisely what changes.
  return (
    `${MARKER}\n` +
    `👋 Thanks for the contribution! Courtesy of the CNCF [style guide](${STYLE_GUIDE_URL}), ` +
    '"cloud native" is written as two words, capitalized based on context (never hyphenated). ' +
    'Feel free to accept the suggestion below, or tweak the wording if something else reads better.\n\n' +
    '```suggestion\n' +
    `${fix.new.replace(/\n$/, '')}\n` +
    '```'
  );
}

/**
 * Orchestrates posting cloud native style suggestions for a PR.
 * `github`, `context`, `core` match the globals injected by actions/github-script.
 * `fixes` is the array produced by fix_style.py: [{line, new}, ...]
 */
async function run({ github, context, core, fixes, targetFile = 'people.json' }) {
  const pull_number = context.payload.pull_request.number;
  const { owner, repo } = context.repo;

  const { data: files } = await github.rest.pulls.listFiles({ owner, repo, pull_number, per_page: 100 });
  const peopleFile = files.find((f) => f.filename === targetFile);
  const added = addedLineNumbers(peopleFile && peopleFile.patch);
  const relevant = fixes.filter((fx) => added.has(fx.line));

  // Clear any stale suggestions we posted on a previous push before re-posting.
  const { data: existing } = await github.rest.pulls.listReviewComments({ owner, repo, pull_number, per_page: 100 });
  for (const c of existing) {
    if (c.user.login === BOT_LOGIN && c.body.includes(MARKER)) {
      await github.rest.pulls.deleteReviewComment({ owner, repo, comment_id: c.id });
    }
  }

  if (relevant.length === 0) {
    console.log('No cloud native style issues in added lines.');
    return { posted: 0 };
  }

  const comments = relevant.map((fx) => ({
    path: targetFile,
    line: fx.line,
    side: 'RIGHT',
    body: buildCommentBody(fx),
  }));

  await github.rest.pulls.createReview({ owner, repo, pull_number, event: 'COMMENT', comments });
  core.setFailed(`${comments.length} cloud native style issue(s) found \u2014 see inline suggestions.`);
  return { posted: comments.length };
}

module.exports = { run, addedLineNumbers, buildCommentBody, MARKER, STYLE_GUIDE_URL };
