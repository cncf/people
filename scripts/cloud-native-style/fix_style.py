#!/usr/bin/env python3
"""Compute CNCF 'cloud native' style fixes for free-text fields in people.json.

Checks the "cloud native" and "open source" terms, and only in the `bio` string
values (matched line-by-line, since people.json is one key/value per line).
`company` and `project_title` are deliberately excluded: they're proper names,
not prose, and should never be rewritten by this checker.
With --apply, rewrites the input file in place instead.
Otherwise writes a JSON file with a list of {"line": <1-based line number>, "new": <corrected raw JSON line>,
"old": <original line>, "name": <person>}
for every line whose value needs to change, leaving everything else alone.

See the CNCF style guide:
https://github.com/cncf/foundation/blob/main/style-guide.md#1-cloud-native-and-open-source
"""
import argparse
import json
import re

LINE = re.compile(r'^(\s*"(bio)"\s*:\s*")(.*)("\s*,?\s*)$')
TERM = re.compile(r'(?<![\w/.@#=-])(cloud[- ]native|open[- ]source)(?![\w/-]|\.\w)', re.I)
ORG_SUFFIX = re.compile(r'\s+(?:computing\s+foundation|days|rejekts|initiative)\b', re.I)
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


def is_proper_noun_cue(value, m):
    """Capitalized term followed by another capitalized word, e.g. "Cloud Native Community"."""
    nxt = CAPITALIZED_NEXT.match(value, m.end())
    if not (m.group(0)[0].isupper() and nxt):
        return False
    # an adjacent term is rewritten itself, so it isn't a proper-noun cue
    return not TERM.match(value, nxt.end() - 1)


def fix_value(value):
    def replace(m):
        if m.group(0).isupper():
            return m.group(0)
        first, second = ("cloud", "native") if m.group(1)[0] in "Cc" else ("open", "source")
        if (
            ORG_SUFFIX.match(value, m.end())
            # Proper nouns, e.g. "Kubernetes and Cloud Native Associate", "Open Source Summit"
            or is_proper_noun_cue(value, m)
            or OPEN_HEADING.search(value, 0, m.start())
        ):
            return f"{first.capitalize()} {second.capitalize()}"
        if sentence_start(value[: m.start()]):
            return f"{first.capitalize()} {second}"
        return f"{first} {second}"

    return TERM.sub(replace, value)


def compute_fixes(lines):
    """Given raw JSON file lines, return [{"line": <1-based>, "new": <fixed line>}, ...]."""
    fixes = []
    for i, line in enumerate(lines):
        m = LINE.match(line)
        if not m:
            continue
        fixed = fix_value(m.group(3))
        if fixed != m.group(3):
            fixes.append({"line": i + 1, "new": m.group(1) + fixed + m.group(4)})
    return fixes


def apply_fixes(lines, fixes):
    """Return a copy of lines with each fix's corrected line substituted in."""
    out = list(lines)
    for fix in fixes:
        out[fix["line"] - 1] = fix["new"]
    return out


NAME = re.compile(r'^\s*"name"\s*:\s*"(.*)",?\s*$')


def enrich(lines, fixes):
    """Add the original line and the person's name (nearest preceding "name") to each fix."""
    out = []
    for fix in fixes:
        name = ""
        for line in reversed(lines[: fix["line"] - 1]):
            m = NAME.match(line)
            if m:
                name = m.group(1)
                break
        out.append({**fix, "old": lines[fix["line"] - 1], "name": name})
    return out


def build_report(lines, fixes):
    """Markdown dry-run report of every fix, as before/after diffs."""
    parts = [
        "# Cloud native style checker dry run\n",
        f"Total candidate fixes: **{len(fixes)}**\n",
    ]
    for i, fix in enumerate(enrich(lines, fixes), 1):
        parts.append(
            f"## {i}. {fix['name'] or '(unknown)'} \u2014 line {fix['line']}\n\n"
            f"```diff\n-{fix['old'].rstrip()}\n+{fix['new'].rstrip()}\n```\n"
        )
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("path", nargs="?", default="people.json")
    parser.add_argument("out", nargs="?", default="fixes.json", help="fixes JSON output (ignored with --apply)")
    parser.add_argument("--report", metavar="FILE", help="write a markdown dry-run report to FILE")
    parser.add_argument("--apply", action="store_true", help="rewrite PATH in place with the fixes")
    args = parser.parse_args()

    # newline="" preserves the file's existing line endings
    with open(args.path, encoding="utf-8", newline="") as f:
        lines = f.readlines()

    fixes = compute_fixes(lines)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(build_report(lines, fixes))
        print(f"Wrote report for {len(fixes)} fix(es) to {args.report}")
        return

    if args.apply:
        fixed = apply_fixes(lines, fixes)
        json.loads("".join(fixed))  # refuse to write a file that is no longer valid JSON
        with open(args.path, "w", encoding="utf-8", newline="") as f:
            f.writelines(fixed)
        print(f"Applied {len(fixes)} fix(es) to {args.path}")
        return

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(enrich(lines, fixes), f)

    print(f"Found {len(fixes)} candidate fix(es)")


if __name__ == "__main__":
    main()
