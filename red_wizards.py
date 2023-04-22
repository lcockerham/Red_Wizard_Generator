"""Main script to run the Red Wizard Generator and convert the output to HTML."""

import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_wizard_and_html.py <num_wizards> [level]")
        sys.exit(1)

    num_wizards_arg = sys.argv[1]
    level_arg = sys.argv[2] if len(sys.argv) >= 3 else None

    if level_arg:
        generator_command = f"python red_wizard_generator.py {num_wizards_arg} {level_arg}"
    else:
        generator_command = f"python red_wizard_generator.py {num_wizards_arg}"

    print("Running Red_Wizard_Generator...")
    subprocess.run(generator_command, shell=True, check=True)

    print("Running RedWizardToHTML...")
    subprocess.run("python red_wizard_to_html.py", shell=True, check=True)

    print("Done!")
