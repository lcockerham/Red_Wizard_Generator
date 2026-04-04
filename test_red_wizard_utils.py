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
from red_wizards_utils import calculate_hit_points, generate_ability_scores, generate_spell_save_dc

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

if __name__ == "__main__":
    unittest.main()
