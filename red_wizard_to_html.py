"""A script to convert Red Wizard data from JSON to HTML using a Jinja2 template."""

import json
import os
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 template engine
template_env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))
template = template_env.get_template("red_wizard_template.html")

# Read the JSON data
with open("red_wizards.json", "r", encoding="utf-8") as infile:
    wizards = json.load(infile)

# Render the HTML output
html_output = template.render(wizards=wizards)

# Save the generated HTML to a file
with open("red_wizards.html", "w", encoding="utf-8") as outfile:
    outfile.write(html_output)
