import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "cloud-native-style"))

from fix_style import compute_fixes  # noqa: E402


def lines_for(field, value):
    return [f'    "{field}": "{value}",\n']


def test_mid_sentence_lowercased():
    fixes = compute_fixes(lines_for("bio", "I love cloud-native technologies."))
    assert fixes == [{"line": 1, "new": '    "bio": "I love cloud native technologies.",\n'}]


def test_sentence_start_capitalized():
    fixes = compute_fixes(lines_for("bio", "Cloud-native is my passion."))
    assert fixes[0]["new"] == '    "bio": "Cloud native is my passion.",\n'


def test_title_field_forces_title_case():
    fixes = compute_fixes(lines_for("company", "Acme cloud-native labs"))
    assert "Cloud Native" in fixes[0]["new"]


def test_project_title_forces_title_case():
    fixes = compute_fixes(lines_for("project_title", "cloud-native mentorship"))
    assert "Cloud Native" in fixes[0]["new"]


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
