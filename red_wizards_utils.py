"""
red_wizard_utils.py

This module provides utility functions for generating attributes, stats, and other
characteristics for Red Wizards in a Dungeons & Dragons campaign.

Functions:
- calculate_hit_points(level, con_score)
- calculate_modifier(score)
- generate_ability_scores(level)
- generate_ability_modifiers(ability_scores)
- generate_thayan_name()
- generate_random_level(mean, stddev)
- generate_school_of_magic()
- calculate_proficiency_bonus(level)
- calculate_wizard_saving_throws(level, ability_modifiers)
- calculate_skill_bonus(level, skill, ability_modifiers, proficient)
- generate_living_status()
- generate_age()
- generate_race()
- generate_alignment()

The functions in this module are meant to be used in conjunction with the
red_wizard_generator.py script for generating complete Red Wizard characters.
"""

import random
import json

with open("values.json") as f:
    names = json.load(f)

first_names = names["first_names"]
last_names = names["last_names"]

def generate_thayan_name():
    """
    Generate a random Thayan name by combining a random first name and last name 
    from predefined lists.

    :return: A string containing a randomly generated Thayan name 
        (e.g., "Xyralen Drakthor")
    """
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

genders = ["he", "she", "they"]

arcane_traditions = [
    "Abjurer", "Conjurer", "Diviner", "Enchanter", "Evoker",
    "Illusionist", "Necromancer", "Transmuter"
]

def calculate_hit_points(level, con_score):
    """
    Calculate the hit points of a character based on their level and Constitution score.

    :param level: The character's level (integer).
    :param con_score: The character's Constitution score (integer).
    :return: The calculated hit points (integer).
    """
    con_modifier = calculate_modifier(con_score)
    hit_points = (8 + con_modifier) * level
    return hit_points

def calculate_modifier(score):
    """
    Calculate the ability modifier for a given ability score.

    The ability modifier represents how a character's ability score affects various
    in-game mechanics, such as skill checks, saving throws, and attack rolls.
    The modifier is determined by subtracting 10 from the ability score and dividing
    the result by 2, rounded down.

    Args:
        score (int): The ability score for which to calculate the modifier.

    Returns:
        int: The calculated ability modifier for the given ability score.

    Example:
        >>> calculate_modifier(18)
        4
        >>> calculate_modifier(8)
        -1
    """
    return (score - 10) // 2

def generate_ability_scores(level):
    """
    Generate ability scores for a character based on their level using a standard array method.

    :param level: The character's level (integer).
    :return: A dictionary containing the character's ability scores (integer values) keyed by 
    ability names.
    """
    standard_array = [17, 14, 13, 12, 10, 8]
    abilities = ["STR", "DEX", "CON", "WIS", "CHA"]

    scores = {ability: 0 for ability in abilities}
    scores["INT"] = standard_array.pop(0)

    random.shuffle(standard_array)
    for i, ability in enumerate(abilities):
        scores[ability] = standard_array[i]

    if level >= 8:
        scores["INT"] = 20
    elif level >= 4:
        scores["INT"] = 18

    return scores

def generate_ability_modifiers(ability_scores):
    """
    Calculate ability modifiers for a given set of ability scores.

    :param ability_scores: A dictionary containing the ability scores 
        (e.g., {"STR": 10, "DEX": 14, ...})
    :return: A dictionary containing the ability modifiers 
        (e.g., {"str_modifier": 0, "dex_modifier": 2, ...})
    """
    modifiers = {}
    for ability, score in ability_scores.items():
        modifiers[f"{ability.lower()}_modifier"] = calculate_modifier(score)
    return modifiers

def generate_thayan_name():
    """
    Generate a random Thayan name by combining a random first name and last name 
    from predefined lists.

    :return: A string containing a randomly generated Thayan name 
        (e.g., "Xyralen Drakthor")
    """
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def generate_living_status():
    """
    Randomly generate the living status of a Red Wizard.

    This function randomly determines if a Red Wizard is alive or dead.
    The living status can be useful in storytelling, role-playing scenarios,
    or other situations where the current state of the character is important.

    Returns:
        str: The generated living status of the Red Wizard, either 'Alive' or 'Dead'.

    Example:
        >>> generate_living_status()
        'Alive'
        >>> generate_living_status()
        'Dead'
    """
    undead_chance = 0.2
    return "undead" if random.random() < undead_chance else "living"

def generate_age():
    """
    Randomly generate the age of a Red Wizard.

    This function generates the age of a Red Wizard using a normal distribution.
    The generated age can be useful in storytelling, role-playing scenarios,
    or other situations where the character's age plays a role in the narrative.

    Returns:
        int: The generated age of the Red Wizard.

    Example:
        >>> generate_age()
        73
        >>> generate_age()
        58
    """
    age_distribution = [21] * 5 + list(range(22, 65)) * 2 + list(range(65, 101))
    return random.choice(age_distribution)

def generate_random_level(mean=10, stddev=3):
    """
    Generate a random character level based on a Gaussian distribution with a 
    specified mean and standard deviation.
    :param mean: The mean of the Gaussian distribution used to generate the level, 
        defaults to 10
    :type mean: int, optional
    :param stddev: The standard deviation of the Gaussian distribution used to generate the level,
        defaults to 3
    :type stddev: int, optional
    :return: An integer representing the randomly generated character level, ranging from 1 to 20
    """
    generated_level = int(random.gauss(mean, stddev))
    return max(1, min(20, generated_level))

def generate_arcane_tradition():
    """
    Randomly select and return a school of magic from the available schools in D&D 5th Edition.

    :return: A string representing the chosen school of magic
    """
    return random.choice(arcane_traditions)

def generate_race():
    """
    Randomly select the race of a Red Wizard.

    This function chooses a race for a Red Wizard character based on a predefined
    list of possible races. The race can be useful in storytelling, role-playing
    scenarios, or other situations where a character's race plays a role in the
    narrative.

    Returns:
        str: The selected race for the Red Wizard.

    Example:
        >>> generate_race()
        'Human'
        >>> generate_race()
        'Tiefling'
    """
    races = [
        "human", "dragonborn", "dwarf", "elf", "halfling", "orc", "tiefling"
    ]
    race_probabilities = [0.8] + [0.2 / (len(races) - 1)] * (len(races) - 1)
    return random.choices(races, weights=race_probabilities)[0]

def generate_alignment():
    """
    Randomly select the alignment of a Red Wizard.

    This function chooses an alignment for a Red Wizard character based on a predefined
    list of possible alignments. The alignment can be useful in storytelling, role-playing
    scenarios, or other situations where a character's moral and ethical stance plays a
    role in the narrative.

    Returns:
        str: The selected alignment for the Red Wizard.

    Example:
        >>> generate_alignment()
        'Lawful Evil'
        >>> generate_alignment()
        'Neutral Evil'
    """
    alignments = [
        "Lawful Evil", "Lawful Neutral", "Neutral", "Neutral Evil", "Chaotic Evil"
    ]
    alignment_probability = [0.8] + [0.2 / (len(alignments) - 1)] * (len(alignments) - 1)
    return random.choices(alignments, weights=alignment_probability)[0]

def calculate_proficiency_bonus(level):
    """
    Calculate and return the proficiency bonus for a given character level in D&D 5th Edition.

    :param level: An integer representing the character's level (1-20)
    :return: An integer representing the proficiency bonus for the given level
    :raise ValueError: If the level is not within the valid range (1-20)
    """
    if 1 <= level <= 4:
        return 2
    if 5 <= level <= 8:
        return 3
    if 9 <= level <= 12:
        return 4
    if 13 <= level <= 16:
        return 5
    if 17 <= level <= 20:
        return 6

    raise ValueError("Invalid character level")

def calculate_wizard_saving_throws(level, ability_modifiers):
    """
    Calculate and return the wizard's saving throw values for each ability based 
    on the character level and ability modifiers in D&D 5th Edition.

    :param level: An integer representing the wizard's level (1-20)
    :param ability_modifiers: A dictionary containing the wizard's ability modifiers, 
        keyed by ability names
    :return: A dictionary containing the wizard's saving throw values for each ability, 
        keyed by ability names
    """
    proficiency_bonus = calculate_proficiency_bonus(level)
    int_save = proficiency_bonus + ability_modifiers["int_modifier"]
    wis_save = proficiency_bonus + ability_modifiers["wis_modifier"]
    return {"INT": int_save, "WIS": wis_save}

def calculate_skill_bonus(level, skill, ability_modifiers, proficient):
    """
    Calculate and return the skill bonus for a given skill based on the character level,
    ability modifiers, and proficiency status in D&D 5th Edition.

    :param level: An integer representing the character's level (1-20)
    :param skill: A string representing the skill name (e.g., "Acrobatics", "Arcana")
    :param ability_modifiers: A dictionary containing the character's ability modifiers, 
    keyed by ability names
    :param proficient: A boolean indicating whether the character is proficient in the skill
    :return: An integer representing the skill bonus for the given skill
    """
    skills_5e = {
        "Acrobatics": "DEX",
        "Animal Handling": "WIS",
        "Arcana": "INT",
        "Athletics": "STR",
        "Deception": "CHA",
        "History": "INT",
        "Insight": "WIS",
        "Intimidation": "CHA",
        "Investigation": "INT",
        "Medicine": "WIS",
        "Nature": "INT",
        "Perception": "WIS",
        "Performance": "CHA",
        "Persuasion": "CHA",
        "Religion": "INT",
        "Sleight of Hand": "DEX",
        "Stealth": "DEX",
        "Survival": "WIS"
    }
    ability = skills_5e[skill]
    ability_modifier = ability_modifiers[f"{ability.lower()}_modifier"]

    if proficient:
        proficiency_bonus = calculate_proficiency_bonus(level)
        return ability_modifier + proficiency_bonus

    return ability_modifier

def generate_languages():
    """
    Determine the languages a Red Wizard speaks. All Red Wizards speak Common and Thayan,
    plus three other languages. Draconic and Infernal are the most common additional languages.
    
    Returns:
        list: A list of strings representing the languages the Red Wizard speaks.
    """
    # All Red Wizards speak Common and Thayan
    languages = ["Common", "Thayan"]

    # Additional language options
    additional_languages = ["Abyssal", "Celestial", "Draconic", "Deep Speech", "Dwarvish",
                            "Elvish", "Giant", "Gnomish", "Goblin", "Halfling", "Infernal",
                            "Orc", "Primordial", "Sylvan", "Undercommon"]

    # Set Draconic and Infernal as more common
    additional_languages_weights = [4, 4] + [1] * (len(additional_languages) - 2)

    # Choose three additional languages
    chosen_languages = random.choices(
        additional_languages, weights=additional_languages_weights, k=3)

    # Add the chosen languages to the Red Wizard's languages
    languages.extend(chosen_languages)

    return languages
