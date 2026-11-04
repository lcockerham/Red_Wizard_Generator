# Red Wizard Generator

## Security: read first (added 2026-11-03, updated 2026-11-03)

This repo is **public** (lcockerham/Red_Wizard_Generator).

Resolved on branch `security/tier0-hardening`:

- **jinja2 pin:** was `jinja2>=2.11.3,<3.0` (4 moderate CVEs). It is now `jinja2>=3.1.6`, and no code or template changes were needed. Don't cap it below 3.x again: 2.11.3 also fails to import on a fresh install because current MarkupSafe removed `soft_unicode`.
- **Workflow actions:** bumped to `actions/checkout@v4`, `actions/setup-python@v5`, and `github/codeql-action/*@v3`.
- **EOL Python in CI:** `run_tests.yml` and `pylint.yml` now test on 3.12 and 3.13, with `permissions: contents: read`. CodeQL keeps its job-level `security-events: write`.

Still relevant:

- **Check Dependabot before bumping a dependency by hand.** Security-update PRs were enabled 2026-11-03, so run `gh pr list` first.
- **After any jinja2 change, check that rendering still works:** run `python red_wizard_generator.py 3 && python red_wizard_to_html.py`, then open `red_wizards.html`. Both output files are gitignored.
