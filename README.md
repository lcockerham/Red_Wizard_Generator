# Red Wizard Generator
Generated with ChatGPT

The Red Wizard Generator is a Python script that generates random Red Wizards of Thay characters, a group of powerful wizards in the Dungeons & Dragons universe. It includes a command line interface for generating wizards, as well as a simple HTML template to display the generated character information.

## Goals

This repo generates random Red Wizards of Thay as ready-to-use D&D 5e NPCs.

- **Generate wizards** with varied levels, races, schools of magic,
  alignments and ability scores, and the stats that follow from them.
- **Follow the 5e rules** for every derived stat: hit points, armor class,
  proficiency, saves and skills.
- **Show them** as JSON and as an HTML stat block.
- **Not here:** other factions or general-purpose NPC generators.

## Features

- Generates random Red Wizard characters with varying levels, races, living status, schools of magic, alignments, and ability scores.
- Calculates hit points, armor class, proficiency bonus, saving throws, and skill bonuses for each character.
- Generates a JSON file containing the generated wizards' information.
- Utilizes an HTML template with Jinja2 to display the generated character information.

## Requirements

- Python 3.8 or higher
- Jinja2

## Installation

1. Clone the repository: `git clone https://github.com/lcockerham/Red_Wizard_Generator`
2. Install the required packages: `pip install -r requirements.txt`


## Usage

1. Run the script with the desired number of wizards and an optional character level: python red_wizard_generator.py <num_wizards> [level]
Replace `<num_wizards>` with the number of wizards you want to generate, and `[level]` with the character level if you want all generated wizards to have the same level.

2. A JSON file named `red_wizards.json` will be generated in the same directory, containing the generated wizards' information.

3. Use the HTML template to display the generated wizards' information.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)


