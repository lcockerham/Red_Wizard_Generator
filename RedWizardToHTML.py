"""Module to convert Red Wizards JSON to an HTML file."""

import json
from jinja2 import Environment, FileSystemLoader

# Load the JSON data
with open("red_wizards.json", "r", encoding="utf-8") as file:
    wizards = json.load(file)

# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader("templates"))

# Load the template
template = env.get_template("wizard_template.html")

# Render the template with the wizards data
html_content = template.render(wizards=wizards)

# Save the rendered HTML to a file
with open("red_wizards.html", "w", encoding="utf-8") as outfile:
    outfile.write(html_content)
