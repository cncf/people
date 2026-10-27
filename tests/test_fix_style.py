import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "cloud-native-style"))

import json
import subprocess

from fix_style import build_report, compute_fixes, enrich  # noqa: E402


def lines_for(field, value):
    return [f'    "{field}": "{value}",\n']


def test_mid_sentence_lowercased():
    fixes = compute_fixes(lines_for("bio", "I love cloud-native technologies."))
    assert fixes == [{"line": 1, "new": '    "bio": "I love cloud native technologies.",\n'}]


def test_sentence_start_capitalized():
    fixes = compute_fixes(lines_for("bio", "Cloud-native is my passion."))
    assert fixes[0]["new"] == '    "bio": "Cloud native is my passion.",\n'


def test_company_field_is_never_touched():
    fixes = compute_fixes(lines_for("company", "Acme cloud-native labs"))
    assert fixes == []


def test_project_title_is_never_touched():
    fixes = compute_fixes(lines_for("project_title", "cloud-native open-source mentorship"))
    assert fixes == []


def test_open_source_hyphen_removed():
    fixes = compute_fixes(lines_for("bio", "I maintain open-source tools."))
    assert fixes[0]["new"] == '    "bio": "I maintain open source tools.",\n'


def test_open_source_sentence_start():
    fixes = compute_fixes(lines_for("bio", "Open-source is my passion."))
    assert fixes[0]["new"] == '    "bio": "Open source is my passion.",\n'


def test_open_source_org_name_preserved():
    assert compute_fixes(lines_for("bio", "Speaker at Open Source Summit Europe.")) == []
    assert compute_fixes(lines_for("bio", "Member of the Open Source Initiative.")) == []


def test_open_source_correct_usage_left_alone():
    assert compute_fixes(lines_for("bio", "I love open source.")) == []


def test_org_suffix_days_already_correct_is_left_alone():
    fixes = compute_fixes(lines_for("bio", "I spoke at Cloud Native Days Austin."))
    assert fixes == []


def test_org_suffix_rejekts_detected():
    fixes = compute_fixes(lines_for("bio", "I spoke at cloud native rejekts."))
    assert "Cloud Native" in fixes[0]["new"]


def test_proper_noun_capitalized_next_word_preserved():
    fixes = compute_fixes(lines_for("bio", "Member of Cloud Native Community Japan."))
    assert fixes == []


def test_heading_forces_title_case():
    fixes = compute_fixes(lines_for("bio", "<h2>cloud native journey</h2>"))
    assert "Cloud Native" in fixes[0]["new"]


def test_url_left_untouched():
    fixes = compute_fixes(lines_for("bio", "See https://example.com/cloud-native for details."))
    assert fixes == []


def test_filename_left_untouched():
    fixes = compute_fixes(lines_for("bio", "Logo: cloud-native.png"))
    assert fixes == []


def test_hyphenated_identifier_left_untouched():
    fixes = compute_fixes(lines_for("bio", "Organizer of cloud-native-community-korea."))
    assert fixes == []


def test_all_caps_left_untouched():
    fixes = compute_fixes(lines_for("bio", "CLOUD-NATIVE is in our DNA."))
    assert fixes == []


def test_abbreviation_not_treated_as_sentence_end():
    fixes = compute_fixes(lines_for("bio", "Experienced with tools, e.g. cloud-native platforms."))
    assert fixes[0]["new"] == '    "bio": "Experienced with tools, e.g. cloud native platforms.",\n'


def test_non_target_field_ignored():
    fixes = compute_fixes(lines_for("name", "cloud-native Jones"))
    assert fixes == []


def test_apply_rewrites_file_in_place(tmp_path):
    f = tmp_path / "people.json"
    f.write_text('[\n  {\n    "bio": "I love cloud-native and open-source.",\n    "company": "Acme cloud-native"\n  }\n]\n')
    script = Path(__file__).resolve().parents[1] / "scripts" / "cloud-native-style" / "fix_style.py"
    subprocess.run([sys.executable, str(script), str(f), "--apply"], check=True)
    data = json.loads(f.read_text())
    assert data[0]["bio"] == "I love cloud native and open source."
    assert data[0]["company"] == "Acme cloud-native"
    assert f.read_text().endswith("}\n]\n")


def test_adjacent_terms_are_idempotent():
    first = compute_fixes(lines_for("bio", "A passion for Open Source Cloud-Native technologies."))
    fixed = first[0]["new"]
    assert "open source cloud native technologies" in fixed
    assert compute_fixes([fixed]) == []


def test_open_source_all_caps_left_untouched():
    assert compute_fixes(lines_for("bio", "OPEN-SOURCE is in our DNA.")) == []


def test_open_source_identifiers_and_urls_left_untouched():
    assert compute_fixes(lines_for("bio", "Maintainer of open-source-community-korea.")) == []
    assert compute_fixes(lines_for("bio", "See https://example.com/open-source for details.")) == []
    assert compute_fixes(lines_for("bio", "Logo: open-source.png")) == []


def test_open_source_mid_sentence_capitalized_is_lowercased():
    fixes = compute_fixes(lines_for("bio", "I contribute to Open Source projects."))
    assert fixes[0]["new"] == '    "bio": "I contribute to open source projects.",\n'


def test_report_includes_name_line_and_diff():
    lines = ['    "name": "Ada Lovelace",\n', '    "bio": "I love cloud-native.",\n']
    fixes = compute_fixes(lines)
    assert enrich(lines, fixes)[0]["name"] == "Ada Lovelace"
    report = build_report(lines, fixes)
    assert "Ada Lovelace \u2014 line 2" in report
    assert '-    "bio": "I love cloud-native.",' in report
    assert '+    "bio": "I love cloud native.",' in report
