## Summary

What changes and why.

## Type of change

- [ ] PATCH: a link, typo, or fixture with no effect on behavior
- [ ] MINOR: instructions, references, evals, or criteria that change behavior
- [ ] MAJOR: scope, name, or contract of the skill

## Verification

- [ ] `python3 scripts/validate.py` has no errors
- [ ] `python3 -m unittest discover -s scripts -p "test_*.py"` passes
- [ ] The `validate` CI is green on this commit
- [ ] Affected scenarios re-run with and without the skill and recorded in `evals/RESULTS.md` (see `RELEASING.md`), or "not applicable: <reason>"

## Evidence

Links or rows from `evals/RESULTS.md`. Separate what was run from what is a walkthrough or structural only.

## Risks and limitations

What was not verified.

## Security

- [ ] No critical failure in `evals/RESULTS.md` for the affected scenarios
- [ ] No secret, credential, or personal data added
