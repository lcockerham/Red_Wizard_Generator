import json
import os
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 template engine
template_env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))
template = template_env.get_template("red_wizard_template.html")

# Read the JSON data
with open("red_wizards.json", "r") as infile:
    wizards = json.load(infile)

# Render the HTML output
html_output = template.render(wizards=wizards)

# Save the generated HTML to a file
with open("red_wizards.html", "w") as outfile:
    outfile.write(html_output)

