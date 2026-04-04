"""Main script to run the Red Wizard Generator and convert the output to HTML."""

import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_wizard_and_html.py <num_wizards> [level]")
        sys.exit(1)

    NUM_WIZARDS_ARG = sys.argv[1]
    LEVEL_ARG = sys.argv[2] if len(sys.argv) >= 3 else None

    if LEVEL_ARG:
        generator_command = [sys.executable, "red_wizard_generator.py", NUM_WIZARDS_ARG, LEVEL_ARG]
    else:
        generator_command = [sys.executable, "red_wizard_generator.py", NUM_WIZARDS_ARG]

    print("Running Red_Wizard_Generator...")
    subprocess.run(generator_command, check=True)

    print("Running RedWizardToHTML...")
    subprocess.run([sys.executable, "red_wizard_to_html.py"], check=True)

    print("Done!")
