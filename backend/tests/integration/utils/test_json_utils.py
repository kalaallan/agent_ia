import pytest

from app.utils.json_utils import safe_json_load


# -----------------------------
# Cas nominal
# -----------------------------
def test_safe_json_load_valid_json():
    raw = '[{"a": 1}, {"b": 2}]'

    result = safe_json_load(raw)

    assert result == [{"a": 1}, {"b": 2}]


# -----------------------------
# JSON cassé mais récupérable
# -----------------------------
def test_safe_json_load_extracts_list_from_dirty_string():
    raw = 'some noise before [{"a": 1}, {"b": 2}] some noise after'

    result = safe_json_load(raw)

    assert result == [{"a": 1}, {"b": 2}]


# -----------------------------
# JSON complètement invalide
# -----------------------------
def test_safe_json_load_returns_empty_list_on_invalid_json():
    raw = "not json at all"

    result = safe_json_load(raw)

    assert result == []


# -----------------------------
# Liste mal formée
# -----------------------------
def test_safe_json_load_returns_empty_list_if_extracted_json_invalid():
    raw = 'prefix [{"a": 1}, {"b": ] suffix'

    result = safe_json_load(raw)

    assert result == []


# -----------------------------
# Cas edge : plusieurs listes -> regex greedy
# -----------------------------
def test_safe_json_load_handles_multiple_lists_greedy_behavior():
    raw = '[{"a": 1}] some text [{"b": 2}]'

    result = safe_json_load(raw)

    # regex est greedy -> prend tout entre premier [ et dernier ]
    # donc JSON invalide -> []
    assert result == []


# -----------------------------
# Cas edge : liste vide
# -----------------------------
def test_safe_json_load_empty_list():
    raw = "[]"

    result = safe_json_load(raw)

    assert result == []