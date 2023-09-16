"""
red_wizard_generator.py

This module provides functionality to generate Red Wizards of Thay, a group of powerful
spellcasters in the Dungeons & Dragons universe. The module includes functions for generating
random ability scores, character levels, skill bonuses, saving throws, and other attributes
specific to Red Wizards.

The main function, `generate_red_wizards`, takes the number of wizards to generate and an optional
level range as input, and returns a list of dictionaries containing the generated wizards' 
attributes.

Example usage:

    from red_wizard_generator import generate_red_wizards

    # Generate 10 random Red Wizards
    wizards = generate_red_wizards(10)

    # Generate 5 Red Wizards with levels between 5 and 15
    wizards = generate_red_wizards(5, (5, 15))
"""
import argparse
import json
import red_wizards_utils

def main(num_wizards, level=None):
    """
    Generate Red Wizards of Thay with specified parameters and save them to a JSON file.

    :param num_wizards: The number of Red Wizards to generate.
    :param level: The level of the Red Wizards. If not specified, a random level will be 
    generated for each wizard.
    """
    wizards = []
    for _ in range(num_wizards):
        wizard = {}
        wizard["name"] = red_wizards_utils.generate_thayan_name()
        if level is None:
            wizard["level"] = red_wizards_utils.generate_random_level()
        else:
            wizard["level"] = level
        wizard["race"] = red_wizards_utils.generate_race()
        wizard["living_status"] = red_wizards_utils.generate_living_status()
        wizard["arcane_tradition"] = red_wizards_utils.generate_arcane_tradition()
        if wizard["living_status"] == "living":
            wizard["age"] = red_wizards_utils.generate_age()
        wizard["alignment"] = red_wizards_utils.generate_alignment()
        wizard["ability_scores"] = red_wizards_utils.generate_ability_scores(wizard["level"])
        wizard["ability_modifiers"] = red_wizards_utils.generate_ability_modifiers(
            wizard["ability_scores"])
        wizard["armor_class"] = 10 + wizard["ability_modifiers"]["dex_modifier"]
        wizard["hit_points"] = red_wizards_utils.calculate_hit_points(
            wizard["level"], wizard["ability_scores"]["CON"])
        wizard["proficiency_bonus"] = red_wizards_utils.calculate_proficiency_bonus(
            wizard["level"])
        wizard["saving_throws"] = red_wizards_utils.calculate_wizard_saving_throws(
            wizard["level"], wizard["ability_modifiers"])
        wizard["spell_save_dc"] = red_wizards_utils.generate_spell_save_dc(
            wizard["proficiency_bonus"], wizard["ability_modifiers"]["int_modifier"])
        wizard["spell_attack_bonus"] = red_wizards_utils.generate_spell_attack_bonus(
            wizard["proficiency_bonus"], wizard["ability_modifiers"]["int_modifier"])
                
        if wizard["level"] <= 4:
            level_category = "low_level"
        elif 4 < wizard["level"] <= 13:
            level_category = "mid_level"
        else:
            level_category = "high_level"

        wizard["spell_list"] = red_wizards_utils.get_spell_list(
            wizard["arcane_tradition"], level_category)


        # Add skill bonuses
        wizard["skills"] = {
            "Arcana": red_wizards_utils.calculate_skill_bonus(
                wizard["level"], "Arcana", wizard["ability_modifiers"], True),
            "Deception": red_wizards_utils.calculate_skill_bonus(
                wizard["level"], "Deception", wizard["ability_modifiers"], True),
            "Insight": red_wizards_utils.calculate_skill_bonus(
                wizard["level"], "Insight", wizard["ability_modifiers"], True),
            "Stealth": red_wizards_utils.calculate_skill_bonus(
                wizard["level"], "Stealth", wizard["ability_modifiers"], True),
            "Passive_Perception": 10 + red_wizards_utils.calculate_skill_bonus(
                wizard["level"], "Perception", wizard["ability_modifiers"], False)
        }
        wizard["languages"] = red_wizards_utils.generate_languages()

        wizards.append(wizard)

    with open("red_wizards.json", "w", encoding="utf-8") as outfile:
        json.dump(wizards, outfile, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random Red Wizards of Thay.")
    parser.add_argument("num_wizards", type=int, help="Number of Red Wizards to generate")
    parser.add_argument(
        "level", type=int, choices=range(1, 21), 
        help="Character level (1-20)", nargs='?', default=None)
    args = parser.parse_args()
    main(args.num_wizards, args.level)
