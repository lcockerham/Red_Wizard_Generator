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
        wizards.append(wizard)
    
    with open("red_wizards.json", "w") as outfile:
        json.dump(wizards, outfile, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random Red Wizards of Thay.")
    parser.add_argument("num_wizards", type=int, help="Number of Red Wizards to generate")
    parser.add_argument("level", type=int, choices=range(1, 21), help="Character level (1-20)", nargs='?', default=None)
    args = parser.parse_args()
    main(args.num_wizards, args.level)