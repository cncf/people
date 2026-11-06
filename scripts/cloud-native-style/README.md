# Cloud native style check

Checks the `bio` field in `people.json` against the CNCF
[style guide](https://github.com/cncf/foundation/blob/main/style-guide.md#1-cloud-native-and-open-source):
"cloud native" and "open source" are two words, never hyphenated, lowercase except at the start of a
sentence or in proper names. `company` and `project_title` are never checked.

On PRs that change `people.json`, the `Cloud native style` workflow posts inline suggestions on the
added lines and lists them in the run's **Summary** tab on the Actions page.

## Run it locally

From the repo root:

```sh
# Preview: write a markdown before/after report (git-ignored) and change nothing
python scripts/cloud-native-style/fix_style.py people.json --report cloud-native-style-report.md

# Fix people.json in place, then review with `git diff`
python scripts/cloud-native-style/fix_style.py people.json --apply
```

`--apply` refuses to write if the result would not be valid JSON, and running it twice changes nothing
the second time. It rewrites the whole file, so on a large file only the lines you changed are
usually what you want in your PR: review the diff and keep just those hunks.

Without flags, `fix_style.py <people.json> <fixes.json>` writes the list of fixes used by the workflow.

## Tests

```sh
python -m pytest tests/test_fix_style.py
node --test tests/post_suggestions.test.js
```
