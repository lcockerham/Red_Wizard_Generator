# Red Wizard Generator — Project Summary

## Overview

A D&D 5th Edition NPC generator that creates randomized **Red Wizards of Thay** — powerful arcane magic-users from the Forgotten Realms setting. The tool produces complete character sheets (ability scores, spells, saving throws, hit points, skills) and exports them as both JSON data and a rendered HTML card, suitable for Dungeon Masters prepping encounters.

**Stack:** Python 3.8+, Jinja2 (HTML templating), GitHub Actions (CI/CD)

**Entry Points:**
- `red_wizard_generator.py` — CLI: `python red_wizard_generator.py <num_wizards> [--level N]`
- `red_wizard_to_html.py` — converts `red_wizards.json` → `red_wizards.html`
- `red_wizards.py` — wrapper script that runs both of the above via subprocess

---

## Architecture

```
RED_Wizard_Generator/
├── red_wizard_generator.py     # CLI entry point; orchestrates generation; writes red_wizards.json
├── red_wizards_utils.py        # All D&D mechanics (names, stats, spells, HP, skills, saves)
├── red_wizard_to_html.py       # Jinja2 renderer: red_wizards.json → red_wizards.html
├── red_wizards.py              # Subprocess wrapper that chains generator + renderer
├── test_red_wizard_utils.py    # Unit tests (partially broken — see tasks below)
├── values.json                 # First/last name pools for Thayan name generation
├── wizard_spell_lists.json     # Spell lists keyed by arcane tradition and frequency
├── red_wizard_template.html    # Jinja2 template for character card output
├── requirements.txt            # jinja2>=2.11.3,<3.0
└── .github/workflows/          # CI: run_tests.yml, pylint.yml, codeql.yml
```

### Key modules

| File | Responsibility |
|------|---------------|
| `red_wizards_utils.py` | Name generation, ability scores, HP, proficiency, saving throws, skill bonuses, spell selection, arcane tradition, race, alignment, age, living status, languages |
| `red_wizard_generator.py` | Argument parsing, calling utils functions in sequence, assembling wizard dict, writing JSON |
| `red_wizard_to_html.py` | Loading JSON output, rendering Jinja2 template, writing HTML |

---

## Current Test State

**Effective coverage: ~12%**

Only 3 of ~20 utility functions are tested. The `TestWizardSpellJSON` class (5 tests) is entirely broken and will not run.

| Test Class | Tests | Status | Notes |
|------------|-------|--------|-------|
| `TestCalculateHitPoints` | 4 | Passing | No boundary/edge cases |
| `TestGenerateAbilityScores` | 1 | Passing | Range check only, no distribution validation |
| `TestGenerateSpellSaveDC` | 2 | Passing | Formula only, not integrated |
| `TestWizardSpellJSON` | 5 | **Broken** | Missing imports, hardcoded Windows path, wrong key assertions |

**Untested functions:** `generate_thayan_name`, `generate_race`, `generate_alignment`, `generate_living_status`, `generate_age`, `generate_arcane_tradition`, `generate_languages`, `generate_random_level`, `calculate_modifier`, `calculate_proficiency_bonus`, `calculate_wizard_saving_throws`, `calculate_skill_bonus`, `generate_ability_modifiers`, `get_spell_list`

No integration tests exist for the full generation pipeline, CLI parsing, JSON output, or HTML rendering.

---

## Improvement Tasks

### CRITICAL — Fix Broken Code

- [ ] **Fix `TestWizardSpellJSON` imports**
  Add `import os` and `import json` to `test_red_wizard_utils.py`. These are missing, causing an `ImportError` that breaks the entire class.

- [ ] **Fix hardcoded path in `TestWizardSpellJSON`**
  Replace `"C:\Git\Red_Wizard_Generator\wizard_spell_lists.json"` with a relative path using `os.path.join(os.path.dirname(__file__), "wizard_spell_lists.json")`.

- [ ] **Fix key assertions in `TestWizardSpellJSON`**
  Tests assert keys `"at-will"`, `"1/day each"`, `"2/day each"` but the JSON uses `"at_will"`, `"1_per_day"`, `"2_per_day"`. Update assertions to match actual JSON structure.

- [ ] **Fix stub spell validation in `test_spell_integrity`**
  The test validates against `["spell1", "spell2", "spell3"]` — hardcoded dummy values. Replace with actual spell names from `wizard_spell_lists.json`.

- [ ] **Fix `red_wizards.py` subprocess security issue**
  Both `subprocess.run()` calls use `shell=True`, which is a shell injection risk. Refactor to use list-form args with `shell=False`.

---

### TDD — Fix Broken Tests

- [ ] **Repair and re-enable `TestWizardSpellJSON`**
  After fixing imports and paths (see Critical tasks above), verify all 5 tests actually pass and reflect current JSON structure.

- [ ] **Add edge cases to `TestCalculateHitPoints`**
  Test minimum HP (level 1, CON 3), maximum reasonable HP (level 20, CON 20), and non-integer modifier boundary (CON score 10/11 = modifier 0/-1 transition).

- [ ] **Strengthen `TestGenerateAbilityScores`**
  Verify that the returned score set matches the standard array (`[15, 14, 13, 12, 10, 8]` before bonus assignment), not just that scores are in range. Verify INT is always assigned the highest score.

- [ ] **Strengthen `TestGenerateSpellSaveDC`**
  Integrate with real `calculate_proficiency_bonus()` output rather than passing hardcoded integers. This catches regressions in the proficiency formula.

---

### TDD — Missing Tests (write these)

Each of these functions in `red_wizards_utils.py` has zero test coverage:

- [ ] **`calculate_modifier(score)`**
  D&D formula: `(score - 10) // 2`. Test score 10 → 0, score 8 → -1, score 20 → 5, score 3 → -4. This is pure math with no randomness — easy to test exhaustively.

- [ ] **`calculate_proficiency_bonus(level)`**
  D&D table: levels 1-4 → +2, 5-8 → +3, 9-12 → +4, 13-16 → +5, 17-20 → +6. Test all 6 breakpoints.

- [ ] **`generate_ability_modifiers(ability_scores)`**
  Should return a dict of 6 modifiers. Test that each modifier equals `calculate_modifier(score)` for its ability.

- [ ] **`calculate_wizard_saving_throws(level, ability_scores)`**
  Wizards are proficient in INT and WIS saves. Test that INT/WIS saves include proficiency bonus and others don't.

- [ ] **`calculate_skill_bonus(skill, level, ability_scores, proficient)`**
  Test proficient vs non-proficient path. Test that the correct ability modifier is applied per skill (e.g. Arcana uses INT, Stealth uses DEX).

- [ ] **`generate_thayan_name()`**
  Test that the result is a non-empty string. Test that it is a combination of a first and last name from `values.json`. (Mock/patch the file load if needed.)

- [ ] **`generate_race()`**
  Test that the result is one of the valid race strings. Optionally: run N iterations and assert Human appears ~80% of the time (probabilistic test with tolerance).

- [ ] **`generate_alignment()`**
  Test that the result is one of the D&D alignment strings defined in the function.

- [ ] **`generate_living_status()`**
  Test that the result is either `"living"` or `"undead"`. Optionally: assert undead appears roughly 20% of the time across many iterations.

- [ ] **`generate_age(race)`**
  Test that human age is within expected human range. Test that non-human races return appropriate ranges if implemented.

- [ ] **`generate_arcane_tradition()`**
  Test that result is one of the 8 valid traditions (Abjurer, Conjurer, Diviner, Enchanter, Evoker, Illusionist, Necromancer, Transmuter).

- [ ] **`get_spell_list(arcane_tradition, level)`**
  Test that a valid tradition + level returns a dict with `at_will`, `1_per_day`, `2_per_day` keys. Test that an unknown tradition falls back gracefully.

- [ ] **`generate_random_level()`**
  Test that result is always an integer in [1, 20]. Run many iterations and assert no out-of-range values.

- [ ] **Integration test: full wizard generation**
  Call the main generation function with a fixed level and assert the returned dict has all required keys: name, race, alignment, level, hit_points, ability_scores, saving_throws, skills, spells, arcane_tradition, languages, living_status.

- [ ] **CLI argument parsing test**
  Test that `--level` accepts 1–20 and rejects values outside that range. Test that `num_wizards` must be a positive integer.

---

### Code Quality — Refactors

- [ ] **Create a `Wizard` dataclass or named structure**
  Replace the plain `dict` with a `dataclass` or at minimum a `TypedDict`. This makes the shape of a wizard explicit, catches typos in key names, and improves IDE support.

- [ ] **Move JSON file loading out of module scope**
  `values.json` and `wizard_spell_lists.json` are loaded at import time with hardcoded relative paths. Wrap loading in a function, resolve paths relative to `__file__`, and accept the data as parameters in utility functions. This makes tests cleaner (no file I/O needed for pure-logic tests).

- [ ] **Replace magic numbers with named constants**
  `0.2` (undead probability), `8` (CON floor for HP), age distribution lists — all should be named constants at the top of `red_wizards_utils.py` with a comment explaining the D&D rule or design decision behind each value.

- [ ] **Standardize skill proficiency assignment**
  All 5 skills in `red_wizard_generator.py` are hardcoded as `proficient=True`. Red Wizards should have variation. At minimum, pull the proficient skill set from a configuration dict; ideally vary by arcane tradition.

- [ ] **Fix Gaussian level generation**
  `random.gauss()` clipped to [1, 20] creates heavy bias at the boundaries. Use `random.choices()` with a weighted distribution or `scipy.stats.truncnorm` for a statistically sound result.

- [ ] **Remove confusing `red_wizards.py` wrapper**
  The subprocess wrapper adds complexity and a security risk for little benefit. Either integrate its logic into `red_wizard_generator.py` directly, or document why it exists as a separate process.

---

### Feature Gaps — From TODO + Analysis

- [ ] **Differentiate spell lists by arcane tradition**
  All 8 traditions currently have identical spell lists. An Evoker should have Fireball/Lightning Bolt; a Necromancer should have Animate Dead/Inflict Wounds. Populate `wizard_spell_lists.json` with school-appropriate spells.

- [ ] **Fix Abjurer JSON nesting error**
  The `Abjurer` entry in `wizard_spell_lists.json` contains a nested `Conjurer` object — a copy-paste error. Remove it.

- [ ] **Parameterize Spell Save DC by level and INT** *(from TODO.txt)*
  Currently DC is calculated once and not level-scaled beyond proficiency. Verify the formula accounts for INT ASI progression across levels.

- [ ] **Parameterize Arcane Burst damage by level** *(from TODO.txt)*
  If Arcane Burst exists as a feature, its damage should scale with wizard level per D&D 5e conventions.

- [ ] **Add custom spell list support** *(from TODO.txt)*
  Allow users to supply a custom `wizard_spell_lists.json` path via CLI argument, enabling custom D&D settings or homebrew content.

- [ ] **Add error handling for missing/invalid data files**
  Currently the app crashes with a bare exception if `values.json` or `wizard_spell_lists.json` is missing or malformed. Add a clear, user-friendly error message.

---

## Quick Reference: Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Generate 3 wizards at random levels
python red_wizard_generator.py 3

# Generate 5 wizards all at level 10
python red_wizard_generator.py 5 --level 10

# Render generated wizards to HTML
python red_wizard_to_html.py

# Run tests
python -m unittest discover
```
