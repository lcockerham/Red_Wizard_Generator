import os
import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_wizard_and_html.py <num_wizards> [level]")
        sys.exit(1)

    num_wizards = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) >= 3 else None

    if level:
        generator_command = f"python Red_Wizard_Generator.py {num_wizards} {level}"
    else:
        generator_command = f"python Red_Wizard_Generator.py {num_wizards}"

    print("Running Red_Wizard_Generator...")
    subprocess.run(generator_command, shell=True, check=True)

    print("Running RedWizardToHTML...")
    subprocess.run("python RedWizardToHTML.py", shell=True, check=True)

    print("Done!")
