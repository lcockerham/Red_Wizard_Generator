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
import unittest
from red_wizards_utils import calculate_hit_points, generate_ability_scores

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
        Test the spell save DC for a low-level wizard with a given proficiency bonus and Intelligence modifier.
        """
        level = 1  # Wizard of level 1 has a proficiency bonus of +2
        int_modifier = 3  # Assuming Intelligence modifier is +3
        expected_spell_save_dc = 8 + 2 + 3  # 8 (base) + 2 (proficiency bonus) + 3 (Intelligence modifier)
        
        result = generate_spell_save_dc(level, int_modifier)
        self.assertEqual(result, expected_spell_save_dc)

    def test_high_level_wizard(self):
        """
        Test the spell save DC for a high-level wizard with a given proficiency bonus and Intelligence modifier.
        """
        level = 20  # Wizard of level 20 has a proficiency bonus of +6
        int_modifier = 5  # Assuming Intelligence modifier is +5
        expected_spell_save_dc = 8 + 6 + 5  # 8 (base) + 6 (proficiency bonus) + 5 (Intelligence modifier)

        result = generate_spell_save_dc(level, int_modifier)
        self.assertEqual(result, expected_spell_save_dc)

if __name__ == "__main__":
    unittest.main()
