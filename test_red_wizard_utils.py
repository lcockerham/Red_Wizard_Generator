"""
test_red_wizard_utils.py

This module contains unit tests for the utility functions defined in the red_wizard_utils.py 
module. These tests aim to ensure the correct functioning of the functions used in generating
Red Wizard characters for the Red Wizard Generator project.

The tests cover various aspects such as hit point calculations, ability score generation, 
and other character-specific traits.

To run the tests, simply execute the following command in the terminal:
    python -m unittest test_red_wizard_utils
"""
import json
import os
import unittest
from unittest.mock import patch
from red_wizard_generator import main
from red_wizards_utils import (
    calculate_hit_points, generate_ability_scores, generate_spell_save_dc,
    calculate_modifier, calculate_proficiency_bonus, generate_ability_modifiers,
    calculate_wizard_saving_throws, calculate_skill_bonus,
    generate_thayan_name, generate_race, generate_alignment,
    generate_living_status, generate_age, generate_arcane_tradition,
    get_spell_list, generate_random_level,
)

class TestCalculateHitPoints(unittest.TestCase):
    """
    This class contains test cases for the calculate_hit_points function in the 
    red_wizard_utils module.

    The test cases cover various scenarios involving different levels and Constitution scores 
    to ensure accurate hit point calculations for Red Wizard characters.

    To run the tests in this class, simply execute the following command in the terminal:
        python -m unittest test_red_wizard_utils.TestCalculateHitPoints
    """

    def test_low_level_low_con(self):
        """
        This method tests the calculate_hit_points function with a low level and low Constitution
        score.
        """
        level = 1
        con_score = 8
        expected_hit_points = 7
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

    def test_low_level_high_con(self):
        """
        This method tests the calculate_hit_points function with a low level and high Constitution
        score.
        """
        level = 1
        con_score = 18
        expected_hit_points = 12
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

    def test_high_level_low_con(self):
        """
        This method tests the calculate_hit_points function with a high level and low Constitution
        score.
        """
        level = 20
        con_score = 8
        expected_hit_points = 140
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

    def test_high_level_high_con(self):
        """
        This method tests the calculate_hit_points function with a high level and high Constitution
        score.
        """
        level = 20
        con_score = 18
        expected_hit_points = 240
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

class TestGenerateAbilityScores(unittest.TestCase):
    """
    Test cases for the generate_ability_scores function in the red_wizard_utils module.
    """

    def test_generate_ability_scores(self):
        """
        Test that the ability scores generated are within the expected range.
        """
        for level in range(1, 21):
            ability_scores = generate_ability_scores(level)
            self.assertIsInstance(ability_scores, dict)

            # Test that all abilities have a score between 8 and 20, inclusive
            for score in ability_scores.values():
                # Change the type of the score variable to an integer
                score = int(score)
                self.assertGreaterEqual(score, 3)
                self.assertLessEqual(score, 20)

            # Test that INT score is updated correctly based on level
            if level >= 8:
                self.assertEqual(ability_scores["INT"], 20)
            elif level >= 4:
                self.assertEqual(ability_scores["INT"], 18)
            else:
                self.assertEqual(ability_scores["INT"], 17)

class TestGenerateSpellSaveDC(unittest.TestCase):
    """
    Test cases for the generate_spell_save_dc function in the red_wizards_utils module.
    """

    def test_low_level_wizard(self):
        """
        Test the spell save DC for a low-level wizard with a given proficiency bonus 
        and Intelligence modifier.
        """
        proficiency_bonus = 2  # Wizard of level 1 has a proficiency bonus of +2
        int_modifier = 3  # Assuming Intelligence modifier is +3
        # 8 (base) + 2 (proficiency bonus) + 3 (Intelligence modifier)
        expected_spell_save_dc = 8 + 2 + 3

        result = generate_spell_save_dc(proficiency_bonus, int_modifier)
        self.assertEqual(result, expected_spell_save_dc)

    def test_high_level_wizard(self):
        """
        Test the spell save DC for a high-level wizard with a given proficiency bonus 
        and Intelligence modifier.
        """
        proficiency_bonus = 6  # Wizard of level 20 has a proficiency bonus of +6
        int_modifier = 5  # Assuming Intelligence modifier is +5
        # 8 (base) + 6 (proficiency bonus) + 5 (Intelligence modifier)
        expected_spell_save_dc = 8 + 6 + 5

        result = generate_spell_save_dc(proficiency_bonus, int_modifier)
        self.assertEqual(result, expected_spell_save_dc)

class TestWizardSpellJSON(unittest.TestCase):
    """Tests for the structure and integrity of wizard_spell_lists.json."""

    def setUp(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "wizard_spell_lists.json")
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def test_file_exists(self):
        """Verify the spell list JSON file exists at the expected path."""
        self.assertTrue(os.path.exists(self.file_path))

    def test_valid_json(self):
        """Verify the file parses as a dictionary."""
        self.assertIsInstance(self.data, dict)

    def test_level_categories(self):
        """Each tradition must have low_level, mid_level, and high_level keys."""
        for wizard_type, categories in self.data.items():
            self.assertIn("low_level", categories, f"{wizard_type} missing 'low_level'")
            self.assertIn("mid_level", categories, f"{wizard_type} missing 'mid_level'")
            self.assertIn("high_level", categories, f"{wizard_type} missing 'high_level'")

    def test_spell_structure(self):
        """Each level tier must have at_will, 1_per_day, and 2_per_day spell lists."""
        for wizard_type, levels in self.data.items():
            for level_tier in ("low_level", "mid_level", "high_level"):
                if level_tier not in levels:
                    continue
                spells = levels[level_tier]
                msg = f"{wizard_type}/{level_tier}"
                self.assertIn("at_will", spells, f"{msg} missing 'at_will'")
                self.assertIn("1_per_day", spells, f"{msg} missing '1_per_day'")
                self.assertIn("2_per_day", spells, f"{msg} missing '2_per_day'")

    def test_spell_integrity(self):
        """Each spell entry must be a non-empty string."""
        for wizard_type, levels in self.data.items():
            for level_tier in ("low_level", "mid_level", "high_level"):
                if level_tier not in levels:
                    continue
                for freq_key, spell_list in levels[level_tier].items():
                    self.assertIsInstance(
                        spell_list, list,
                        f"{wizard_type}/{level_tier}/{freq_key} is not a list"
                    )
                    for spell in spell_list:
                        self.assertIsInstance(
                            spell, str,
                            f"Spell in {wizard_type}/{level_tier}/{freq_key} is not a string"
                        )
                        self.assertTrue(
                            len(spell) > 0,
                            f"Empty spell name in {wizard_type}/{level_tier}/{freq_key}"
                        )

class TestCalculateModifier(unittest.TestCase):
    """Tests for the calculate_modifier function using the D&D formula (score - 10) // 2."""

    def test_score_10_returns_0(self):
        """Score of 10 is the baseline and should return modifier 0."""
        self.assertEqual(calculate_modifier(10), 0)

    def test_score_8_returns_minus1(self):
        """Score of 8 is below average and should return -1."""
        self.assertEqual(calculate_modifier(8), -1)

    def test_score_20_returns_5(self):
        """Score of 20 is the typical maximum and should return +5."""
        self.assertEqual(calculate_modifier(20), 5)

    def test_score_3_returns_minus4(self):
        """Score of 3 is the minimum possible and should return -4."""
        self.assertEqual(calculate_modifier(3), -4)

    def test_score_18_returns_4(self):
        """Score of 18 is a common high score and should return +4."""
        self.assertEqual(calculate_modifier(18), 4)


class TestCalculateProficiencyBonus(unittest.TestCase):
    """Tests for the calculate_proficiency_bonus function against the D&D 5e proficiency table."""

    def test_levels_1_to_4_return_2(self):
        """Levels 1-4 should all return a proficiency bonus of +2."""
        self.assertEqual(calculate_proficiency_bonus(1), 2)
        self.assertEqual(calculate_proficiency_bonus(4), 2)

    def test_levels_5_to_8_return_3(self):
        """Levels 5-8 should all return a proficiency bonus of +3."""
        self.assertEqual(calculate_proficiency_bonus(5), 3)
        self.assertEqual(calculate_proficiency_bonus(8), 3)

    def test_levels_9_to_12_return_4(self):
        """Levels 9-12 should all return a proficiency bonus of +4."""
        self.assertEqual(calculate_proficiency_bonus(9), 4)
        self.assertEqual(calculate_proficiency_bonus(12), 4)

    def test_levels_13_to_16_return_5(self):
        """Levels 13-16 should all return a proficiency bonus of +5."""
        self.assertEqual(calculate_proficiency_bonus(13), 5)
        self.assertEqual(calculate_proficiency_bonus(16), 5)

    def test_levels_17_to_20_return_6(self):
        """Levels 17-20 should all return a proficiency bonus of +6."""
        self.assertEqual(calculate_proficiency_bonus(17), 6)
        self.assertEqual(calculate_proficiency_bonus(20), 6)

    def test_invalid_level_raises_value_error(self):
        """Level 0 and level 21 are out of range and should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_proficiency_bonus(0)
        with self.assertRaises(ValueError):
            calculate_proficiency_bonus(21)


class TestGenerateAbilityModifiers(unittest.TestCase):
    """Tests for the generate_ability_modifiers function."""

    def test_returns_six_modifiers(self):
        """Result should contain modifier keys for all six D&D abilities."""
        scores = {"STR": 10, "DEX": 14, "CON": 12, "INT": 17, "WIS": 8, "CHA": 13}
        modifiers = generate_ability_modifiers(scores)
        expected_keys = {
            "str_modifier", "dex_modifier", "con_modifier",
            "int_modifier", "wis_modifier", "cha_modifier"
        }
        self.assertEqual(set(modifiers.keys()), expected_keys)

    def test_modifier_values_match_formula(self):
        """Each modifier should equal (score - 10) // 2 for its corresponding ability."""
        scores = {"STR": 10, "DEX": 14, "CON": 12, "INT": 17, "WIS": 8, "CHA": 13}
        modifiers = generate_ability_modifiers(scores)
        self.assertEqual(modifiers["str_modifier"], 0)
        self.assertEqual(modifiers["dex_modifier"], 2)
        self.assertEqual(modifiers["con_modifier"], 1)
        self.assertEqual(modifiers["int_modifier"], 3)
        self.assertEqual(modifiers["wis_modifier"], -1)
        self.assertEqual(modifiers["cha_modifier"], 1)


class TestCalculateWizardSavingThrows(unittest.TestCase):
    """Tests for the calculate_wizard_saving_throws function."""

    def test_returns_int_and_wis_only(self):
        """Wizard saving throws should contain exactly INT and WIS keys."""
        modifiers = {"int_modifier": 3, "wis_modifier": 1}
        result = calculate_wizard_saving_throws(1, modifiers)
        self.assertEqual(set(result.keys()), {"INT", "WIS"})

    def test_int_save_includes_proficiency(self):
        """INT save = proficiency bonus + int_modifier (level 1 = +2 prof, +3 INT = 5)."""
        modifiers = {"int_modifier": 3, "wis_modifier": 1}
        result = calculate_wizard_saving_throws(1, modifiers)
        self.assertEqual(result["INT"], 5)

    def test_wis_save_includes_proficiency(self):
        """WIS save = proficiency bonus + wis_modifier (level 1 = +2 prof, +1 WIS = 3)."""
        modifiers = {"int_modifier": 3, "wis_modifier": 1}
        result = calculate_wizard_saving_throws(1, modifiers)
        self.assertEqual(result["WIS"], 3)


class TestCalculateSkillBonus(unittest.TestCase):
    """Tests for the calculate_skill_bonus function."""

    def test_proficient_adds_proficiency_bonus(self):
        """Proficient skill bonus = ability modifier + proficiency bonus."""
        modifiers = {"int_modifier": 3, "dex_modifier": 1, "wis_modifier": 1, "cha_modifier": 0}
        # Level 1: proficiency +2; Arcana uses INT (+3) → 5
        result = calculate_skill_bonus(1, "Arcana", modifiers, proficient=True)
        self.assertEqual(result, 5)

    def test_non_proficient_returns_ability_modifier_only(self):
        """Non-proficient skill bonus = ability modifier only, no proficiency added."""
        modifiers = {"int_modifier": 3, "dex_modifier": 1, "wis_modifier": 1, "cha_modifier": 0}
        result = calculate_skill_bonus(1, "Arcana", modifiers, proficient=False)
        self.assertEqual(result, 3)

    def test_stealth_uses_dex_modifier(self):
        """Stealth is a DEX-based skill and should use dex_modifier."""
        modifiers = {"int_modifier": 3, "dex_modifier": 2, "wis_modifier": 1, "cha_modifier": 0}
        # Level 1: proficiency +2; Stealth uses DEX (+2) → 4
        result = calculate_skill_bonus(1, "Stealth", modifiers, proficient=True)
        self.assertEqual(result, 4)


class TestGenerateThayanName(unittest.TestCase):
    """Tests for the generate_thayan_name function."""

    def test_returns_string(self):
        """Generated name must be a string."""
        self.assertIsInstance(generate_thayan_name(), str)

    def test_has_first_and_last_name(self):
        """Generated name must contain a space separating first and last name."""
        name = generate_thayan_name()
        parts = name.split(" ")
        self.assertEqual(len(parts), 2)
        self.assertTrue(len(parts[0]) > 0)
        self.assertTrue(len(parts[1]) > 0)


class TestGenerateRace(unittest.TestCase):
    """Tests for the generate_race function."""

    VALID_RACES = {"human", "dragonborn", "dwarf", "elf", "halfling", "orc", "tiefling"}

    def test_returns_valid_race(self):
        """Generated race must be one of the seven valid D&D races."""
        self.assertIn(generate_race(), self.VALID_RACES)

    def test_always_valid_over_many_iterations(self):
        """All races generated across 100 calls must be from the valid set."""
        for _ in range(100):
            self.assertIn(generate_race(), self.VALID_RACES)


class TestGenerateAlignment(unittest.TestCase):
    """Tests for the generate_alignment function."""

    VALID_ALIGNMENTS = {
        "Lawful Evil", "Lawful Neutral", "Neutral", "Neutral Evil", "Chaotic Evil"
    }

    def test_returns_valid_alignment(self):
        """Generated alignment must be one of the five valid Red Wizard alignments."""
        self.assertIn(generate_alignment(), self.VALID_ALIGNMENTS)

    def test_always_valid_over_many_iterations(self):
        """All alignments generated across 100 calls must be from the valid set."""
        for _ in range(100):
            self.assertIn(generate_alignment(), self.VALID_ALIGNMENTS)


class TestGenerateLivingStatus(unittest.TestCase):
    """Tests for the generate_living_status function."""

    def test_returns_valid_status(self):
        """Living status must be either 'living' or 'undead'."""
        self.assertIn(generate_living_status(), {"living", "undead"})

    def test_returns_undead_when_random_below_threshold(self):
        """When random value is below 0.2, the wizard should be undead."""
        with patch("red_wizards_utils.random.random", return_value=0.1):
            self.assertEqual(generate_living_status(), "undead")

    def test_returns_living_when_random_above_threshold(self):
        """When random value is 0.2 or above, the wizard should be living."""
        with patch("red_wizards_utils.random.random", return_value=0.5):
            self.assertEqual(generate_living_status(), "living")


class TestGenerateAge(unittest.TestCase):
    """Tests for the generate_age function."""

    def test_returns_integer(self):
        """Generated age must be an integer."""
        self.assertIsInstance(generate_age(), int)

    def test_age_in_valid_range(self):
        """Generated age must be between 21 and 100 inclusive."""
        age = generate_age()
        self.assertGreaterEqual(age, 21)
        self.assertLessEqual(age, 100)

    def test_always_in_range_over_many_iterations(self):
        """All ages generated across 100 calls must be within the valid range."""
        for _ in range(100):
            age = generate_age()
            self.assertGreaterEqual(age, 21)
            self.assertLessEqual(age, 100)


class TestGenerateArcaneTradition(unittest.TestCase):
    """Tests for the generate_arcane_tradition function."""

    VALID_TRADITIONS = {
        "Abjurer", "Conjurer", "Diviner", "Enchanter",
        "Evoker", "Illusionist", "Necromancer", "Transmuter"
    }

    def test_returns_valid_tradition(self):
        """Generated tradition must be one of the eight D&D 5e arcane schools."""
        self.assertIn(generate_arcane_tradition(), self.VALID_TRADITIONS)

    def test_always_valid_over_many_iterations(self):
        """All traditions generated across 100 calls must be from the valid set."""
        for _ in range(100):
            self.assertIn(generate_arcane_tradition(), self.VALID_TRADITIONS)


class TestGetSpellList(unittest.TestCase):
    """Tests for the get_spell_list function."""

    def test_valid_tradition_and_level_returns_dict(self):
        """A known tradition and level category should return a spell dict."""
        result = get_spell_list("Necromancer", "low_level")
        self.assertIsInstance(result, dict)

    def test_result_has_expected_keys(self):
        """Spell dict must contain at_will, 1_per_day, and 2_per_day keys."""
        result = get_spell_list("Necromancer", "mid_level")
        self.assertIn("at_will", result)
        self.assertIn("1_per_day", result)
        self.assertIn("2_per_day", result)

    def test_invalid_tradition_returns_default(self):
        """An unknown arcane tradition should fall back to the default spell list string."""
        result = get_spell_list("Chronomancer", "low_level")
        self.assertEqual(result, "Default Spell List")

    def test_every_generatable_tradition_has_real_spells(self):
        """Every tradition the generator can pick must resolve to a real spell list.

        Guards against a tradition being mis-nested in wizard_spell_lists.json
        (Conjurer once sat inside Abjurer), which silently gave those wizards
        the "Default Spell List" string instead of spells.
        """
        for tradition in TestGenerateArcaneTradition.VALID_TRADITIONS:
            for level_category in ("low_level", "mid_level", "high_level"):
                result = get_spell_list(tradition, level_category)
                self.assertIsInstance(result, dict, f"{tradition}/{level_category}")


class TestGenerateRandomLevel(unittest.TestCase):
    """Tests for the generate_random_level function."""

    def test_returns_integer(self):
        """Generated level must be an integer."""
        self.assertIsInstance(generate_random_level(), int)

    def test_always_in_range(self):
        """All levels generated across 200 calls must be between 1 and 20 inclusive."""
        for _ in range(200):
            level = generate_random_level()
            self.assertGreaterEqual(level, 1)
            self.assertLessEqual(level, 20)


class TestWizardIntegration(unittest.TestCase):
    """Integration tests for the full wizard generation pipeline."""

    REQUIRED_KEYS = {
        "name", "level", "race", "living_status", "arcane_tradition",
        "alignment", "ability_scores", "ability_modifiers", "armor_class",
        "hit_points", "proficiency_bonus", "saving_throws", "spell_save_dc",
        "spell_attack_bonus", "spell_list", "skills", "languages",
    }

    def setUp(self):
        """Generate one wizard at a fixed level for all integration tests."""
        main(1, level=5)
        with open("red_wizards.json", encoding="utf-8") as f:
            self.wizard = json.load(f)[0]

    def test_wizard_has_all_required_keys(self):
        """Generated wizard dict must contain all required character sheet keys."""
        for key in self.REQUIRED_KEYS:
            self.assertIn(key, self.wizard, f"Missing key: {key}")

    def test_wizard_level_matches_input(self):
        """Wizard level should match the level passed to main()."""
        self.assertEqual(self.wizard["level"], 5)

    def test_wizard_values_are_correct_types(self):
        """Core wizard fields must have the expected Python types."""
        self.assertIsInstance(self.wizard["name"], str)
        self.assertIsInstance(self.wizard["level"], int)
        self.assertIsInstance(self.wizard["hit_points"], int)
        self.assertIsInstance(self.wizard["ability_scores"], dict)
        self.assertIsInstance(self.wizard["languages"], list)
        self.assertIsInstance(self.wizard["saving_throws"], dict)

    def test_living_wizard_has_age(self):
        """A living wizard must have an age field; an undead wizard must not."""
        if self.wizard["living_status"] == "living":
            self.assertIn("age", self.wizard)
        else:
            self.assertNotIn("age", self.wizard)


if __name__ == "__main__":
    unittest.main()
