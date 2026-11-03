# Red Wizard Generator

## Security: read first (added 2026-11-03)

This repo is **public** (lcockerham/Red_Wizard_Generator).

- **jinja2 is capped below 3.0.** `requirements.txt` has `jinja2>=2.11.3,<3.0`, which holds it on 2.11.3 with 4 moderate CVEs (the 4 open Dependabot alerts). Fix: change it to `jinja2>=3.1.6`, then run `python red_wizard_generator.py 3 && python red_wizard_to_html.py` and check `red_wizards.html` still renders.
- **Dependabot may already have a PR for this.** Security-update PRs were enabled 2026-11-03. Check `gh pr list` before making the bump by hand.
- **Workflow actions are outdated.** `run_tests.yml` uses `actions/checkout@v2` / `setup-python@v2`, `pylint.yml` uses `@v3`, and `codeql.yml` uses `codeql-action/*@v2`. Fix: bump each to its latest major version.
- **CI tests on Python 3.8, which is EOL.** `run_tests.yml` pins 3.8 and the `pylint.yml` matrix includes it. Fix: drop 3.8 and test on supported versions (3.10+).
