import random
import argparse
import json

first_names = [
    "Xyralen", "Vezryn", "Thalvost", "Qorikar", "Nythilis", "Mirelai", "Kaelthor",
    "Jyvareth", "Izrelia", "Huzrath", "Gruvalar", "Freznaar", "Elvarin", "Dravikar",
    "Caldris", "Baelthar", "Azryth", "Avaris", "Ysvalda", "Xarthis"
]

last_names = [
    "Drakthor", "Voskhar", "Zurnath", "Dulgrim", "Yargoth", "Xantos", "Virmaar",
    "Uxalim", "Tharnak", "Sovreth", "Ristavi", "Pyrath", "Orthal", "Nythos",
    "Malzor", "Lathrane", "Korthal", "Jorvath", "Irthos", "Ghulrim"
]

genders = ["he", "she", "they"]

schools_of_magic = [
    "Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation",
    "Illusion", "Necromancy", "Transmutation"
]

def calculate_hit_points(level, con_score):
    con_modifier = calculate_modifier(con_score)
    hit_points = (8 + con_modifier) * level
    return hit_points

def calculate_modifier(score):
    return (score - 10) // 2

def generate_ability_scores(level):
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
    modifiers = {}
    for ability, score in ability_scores.items():
        modifiers[f"{ability.lower()}_modifier"] = calculate_modifier(score)
    return modifiers
    

def generate_thayan_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def generate_living_status():
    undead_chance = 0.2
    return "undead" if random.random() < undead_chance else "living"

def generate_age():
    age_distribution = [21] * 5 + list(range(22, 65)) * 2 + list(range(65, 101))
    return random.choice(age_distribution)

def generate_random_level(mean=10, stddev=3):
    generated_level = int(random.gauss(mean, stddev))
    return max(1, min(20, generated_level))

def generate_school_of_magic():
    return random.choice(schools_of_magic)

def generate_race():
    races = [
        "human", "dragonborn", "dwarf", "elf", "halfling", "orc", "tiefling"
    ]
    race_probabilities = [0.8] + [0.2 / (len(races) - 1)] * (len(races) - 1)
    return random.choices(races, weights=race_probabilities)[0]

def generate_alignment():
    alignments = [
        "Lawful Evil", "Lawful Neutral", "Neutral", "Neutral Evil", "Chaotic Evil"
    ]
    alignment_probabilities = [0.8] + [0.2 / (len(alignments) - 1)] * (len(alignments) - 1)
    return random.choices(alignments, weights=alignment_probabilities)[0]

def calculate_proficiency_bonus(level):
    if 1 <= level <= 4:
        return 2
    elif 5 <= level <= 8:
        return 3
    elif 9 <= level <= 12:
        return 4
    elif 13 <= level <= 16:
        return 5
    elif 17 <= level <= 20:
        return 6
    else:
        raise ValueError("Invalid character level")
    
def calculate_wizard_saving_throws(level, ability_modifiers):
    proficiency_bonus = calculate_proficiency_bonus(level)
    
    int_save = proficiency_bonus + ability_modifiers["int_modifier"]
    wis_save = proficiency_bonus + ability_modifiers["wis_modifier"]

    return {"INT": int_save, "WIS": wis_save}

def calculate_skill_bonus(level, skill, ability_modifiers, proficient):
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
    else:
        return ability_modifier



def main(num_wizards, level=None):
    wizards = []
    for _ in range(num_wizards):
        wizard = {}
        wizard["name"] = generate_thayan_name()
        if level is None:
            wizard["level"] = generate_random_level()
        else:
            wizard["level"] = level      
        wizard["race"] = generate_race()
        wizard["living_status"] = generate_living_status()
        wizard["school_of_magic"] = generate_school_of_magic()
        if wizard["living_status"] == "living":
            wizard["age"] = generate_age()
        wizard["alignment"] = generate_alignment()
        wizard["ability_scores"] = generate_ability_scores(wizard["level"])
        wizard["ability_modifiers"] = generate_ability_modifiers(wizard["ability_scores"])
        wizard["armor_class"] = 10 + wizard["ability_modifiers"]["dex_modifier"]
        wizard["hit_points"] = calculate_hit_points(wizard["level"], wizard["ability_scores"]["CON"])
        wizard["proficiency_bonus"] = calculate_proficiency_bonus(wizard["level"])
        wizard["saving_throws"] = calculate_wizard_saving_throws(wizard["level"], wizard["ability_modifiers"])
        
         # Add skill bonuses
        wizard["skills"] = {
            "Arcana": calculate_skill_bonus(wizard["level"], "Arcana", wizard["ability_modifiers"], True),
            "Deception": calculate_skill_bonus(wizard["level"], "Deception", wizard["ability_modifiers"], True),
            "Insight": calculate_skill_bonus(wizard["level"], "Insight", wizard["ability_modifiers"], True),
            "Stealth": calculate_skill_bonus(wizard["level"], "Stealth", wizard["ability_modifiers"], True)
        }
        wizards.append(wizard)



   
    with open("red_wizards.json", "w") as outfile:
        json.dump(wizards, outfile, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random Red Wizards of Thay.")
    parser.add_argument("num_wizards", type=int, help="Number of Red Wizards to generate")
    parser.add_argument("level", type=int, choices=range(1, 21), help="Character level (1-20)", nargs='?', default=None)
    args = parser.parse_args()
    main(args.num_wizards, args.level)
