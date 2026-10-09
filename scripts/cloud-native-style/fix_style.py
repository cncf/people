#!/usr/bin/env python3
"""Compute CNCF 'cloud native' style fixes for free-text fields in people.json.

Only looks at the `bio` and `mentorships[].project_title` string values
(matched line-by-line, since people.json is one key/value per line).
`company` is deliberately excluded: it's a proper/org name field, not prose,
and should never be rewritten by this checker.
Writes a JSON file with a list of {"line": <1-based line number>, "new": <corrected raw JSON line>}
for every line whose value needs to change, leaving everything else alone.

See the CNCF style guide:
https://github.com/cncf/foundation/blob/main/style-guide.md#1-cloud-native-and-open-source
"""
import json
import sys

# Fields that are titles/names rather than prose: always forced to "Cloud Native"
# (Title Case) regardless of sentence position. `bio` is prose and is handled by
# the context-sensitive branches in fix_value instead.
TITLE_CASED_FIELDS = {"project_title"}

import re

LINE = re.compile(r'^(\s*"(bio|project_title)"\s*:\s*")(.*)("\s*,?\s*)$')
TERM = re.compile(r'(?<![\w/.@#=-])cloud[- ]native(?![\w/-]|\.\w)', re.I)
ORG_SUFFIX = re.compile(r'\s+(?:computing\s+foundation|days|rejekts)\b', re.I)
CAPITALIZED_NEXT = re.compile(r'\s+[A-Z]')
OPEN_HEADING = re.compile(r'<h[1-6]\b[^>]*>(?:(?!</h[1-6]\s*>).)*$', re.I | re.S)
TRAILING_WS_AND_TAGS = re.compile(r'(?:\s|<[^>]*>)+$')
BLOCK_TAG = re.compile(r'</?(?:p|li|ul|ol|br|div|h[1-6])\b', re.I)
SENTENCE_END = re.compile(r'[.!?](?:\\"|[\')\]”’])*$')
ABBREVIATION = re.compile(r'\b(?:e\.g|i\.e|vs)\.$', re.I)


def sentence_start(prefix):
    stripped = TRAILING_WS_AND_TAGS.sub("", prefix)
    if not stripped or BLOCK_TAG.search(prefix, len(stripped)):
        return True
    return SENTENCE_END.search(stripped) is not None and not ABBREVIATION.search(stripped)


def fix_value(value, field):
    def replace(m):
        if m.group(0).isupper():
            return m.group(0)
        if (
            ORG_SUFFIX.match(value, m.end())
            # Proper nouns, e.g. "Kubernetes and Cloud Native Associate", "Cloud Native Community Japan"
            or (m.group(0)[0] == "C" and CAPITALIZED_NEXT.match(value, m.end()))
            or field in TITLE_CASED_FIELDS
            or OPEN_HEADING.search(value, 0, m.start())
        ):
            return "Cloud Native"
        if sentence_start(value[: m.start()]):
            return "Cloud native"
        return "cloud native"

    return TERM.sub(replace, value)


def compute_fixes(lines):
    """Given raw JSON file lines, return [{"line": <1-based>, "new": <fixed line>}, ...]."""
    fixes = []
    for i, line in enumerate(lines):
        m = LINE.match(line)
        if not m:
            continue
        fixed = fix_value(m.group(3), m.group(2))
        if fixed != m.group(3):
            fixes.append({"line": i + 1, "new": m.group(1) + fixed + m.group(4)})
    return fixes


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "people.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "fixes.json"

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    fixes = compute_fixes(lines)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(fixes, f)

    print(f"Found {len(fixes)} candidate fix(es)")


if __name__ == "__main__":
    main()
