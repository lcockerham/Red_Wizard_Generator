"""
test_red_wizard_utils.py

This module contains unit tests for the utility functions defined in the red_wizard_utils.py module.
These tests aim to ensure the correct functioning of the functions used in generating Red Wizard characters
for the Red Wizard Generator project.

The tests cover various aspects such as hit point calculations, ability score generation, and other
character-specific traits.

To run the tests, simply execute the following command in the terminal:
    python -m unittest test_red_wizard_utils
"""
import unittest
from red_wizards_utils import calculate_hit_points


class TestCalculateHitPoints(unittest.TestCase):
    """
    This class contains test cases for the calculate_hit_points function in the red_wizard_utils module.

    The test cases cover various scenarios involving different levels and Constitution scores to ensure
    accurate hit point calculations for Red Wizard characters.

    To run the tests in this class, simply execute the following command in the terminal:
        python -m unittest test_red_wizard_utils.TestCalculateHitPoints
    """

    def test_low_level_low_con(self):
        """
        This method tests the calculate_hit_points function with a low level and low Constitution score.
        """
        level = 1
        con_score = 8
        expected_hit_points = 7
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

    def test_low_level_high_con(self):
        """
        This method tests the calculate_hit_points function with a low level and high Constitution score.
        """
        level = 1
        con_score = 18
        expected_hit_points = 12
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

    def test_high_level_low_con(self):
        """
        This method tests the calculate_hit_points function with a high level and low Constitution score.
        """
        level = 20
        con_score = 8
        expected_hit_points = 140
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

    def test_high_level_high_con(self):
        """
        This method tests the calculate_hit_points function with a high level and high Constitution score.
        """
        level = 20
        con_score = 18
        expected_hit_points = 240
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)


if __name__ == "__main__":
    unittest.main()
