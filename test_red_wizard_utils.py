import unittest
from red_wizard_utils import calculate_hit_points


class TestCalculateHitPoints(unittest.TestCase):
    def test_low_level_low_con(self):
        level = 1
        con_score = 8
        expected_hit_points = 7
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

    def test_low_level_high_con(self):
        level = 1
        con_score = 18
        expected_hit_points = 13
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

    def test_high_level_low_con(self):
        level = 20
        con_score = 8
        expected_hit_points = 140
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)

    def test_high_level_high_con(self):
        level = 20
        con_score = 18
        expected_hit_points = 260
        self.assertEqual(calculate_hit_points(level, con_score), expected_hit_points)


if __name__ == "__main__":
    unittest.main()
