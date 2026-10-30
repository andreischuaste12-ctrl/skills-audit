# Contributing

Contributions are welcome. Language of documents and messages: English.

## Before opening a PR

```bash
pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p "test_*.py"
```

Both commands must pass. CI runs the same checks on Python 3.11, 3.12, and 3.13.

## Rules

- Fill in the checklist in `.github/pull_request_template.md`.
- A change that alters the skill's behavior (description, workflow, references, fixtures, or criteria) requires re-running the affected scenarios, with and without the skill, and recording them in `evals/RESULTS.md`. The table in `RELEASING.md` says which.
- Do not claim an improvement, a percentage gain, or host compatibility without a recorded execution.
- Fixtures in `evals/files/` use the `.txt` extension and never the name `SKILL.md`, so they are not discovered as skills. No real credentials: use obviously fake values and `.invalid` domains.
- The validator rejects symlinks and paths outside `evals/files`. Do not try to work around these rules.
- Do not add runtime dependencies. The only development dependency is the one in `requirements-dev.txt`.

## Security

For vulnerabilities, see `SECURITY.md`; do not open a public issue with exploitable details.
