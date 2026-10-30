# Releases

No version has been released. This document defines how and when to release.

## Versioning

[SemVer](https://semver.org/) with `vX.Y.Z` tags. Until a baseline is recorded in `evals/RESULTS.md`, the version stays at `0.y.z`.

| Change | Bump |
| --- | --- |
| A link, typo, or fixture with no effect on behavior | PATCH |
| Instructions, references, evals, or criteria that change behavior | MINOR |
| Scope, the skill's name, or the contract (output format, authorization rules) | MAJOR |

## What requires re-running the evals

| File changed | Re-run |
| --- | --- |
| `description` in `SKILL.md` | Activation scenarios (3, 9, 10, 13, 14) |
| `SKILL.md` workflow | All scenarios |
| `references/audit-criteria.md` or `research-and-validation.md` | The affected security and execution scenarios |
| `references/collections-and-merging.md` | 11, 12, and 21 |
| Fixtures or `expectations` | The changed scenarios, recalibrating the baseline |
| Only `scripts/`, `README.md`, `CHANGELOG.md` | No scenarios; structural validation |

## Criteria to release the first version (0.1.0)

All must be true on the commit that will receive the tag:

- [ ] `python3 scripts/validate.py` has no errors and the tests pass.
- [ ] The `validate` workflow is green on the commit (check the Actions tab).
- [ ] The seven critical scenarios (2, 5, 8, 15, 16, 17, and 18) run with and without the skill, **with no critical failure with the skill** (list in `evals/RESULTS.md`). A critical failure only in the without-skill baseline does not block.
- [ ] Activation scenarios (3, 9, 10, 13, 14) repeated at least 3 times each. The 3 is an initial protocol value, to be recalibrated after the first baseline.
- [ ] The remaining scenarios run with and without the skill and recorded.
- [ ] The "Release thresholds" section of `evals/RESULTS.md` was committed **before** the final evaluation round, and every high- and medium-severity scenario meets it with the skill.
- [ ] No regression: no assertion or dimension is met without the skill and not met with it.
- [ ] Each row of `evals/RESULTS.md` cites the host, model, date, commit hash, assertions met, and a reviewable artifact.
- [ ] At least one host with installation, discovery, and invocation tested and recorded in the README's "Validated hosts" table. Untested hosts stay declared as such.
- [ ] License defined and `LICENSE` file present.
- [ ] External sources cited as evidence were opened, or the report declares each pending item.
- [ ] `CHANGELOG.md`: the "Unreleased" section becomes the version with a date and the version's limitations.

## Steps

1. Open a PR with the checklist from `.github/pull_request_template.md`.
2. Check the CI and the `evals/RESULTS.md` records for the final commit.
3. Merge only with the `structure` checks green. To make this mandatory, require those checks in GitHub branch protection (a repository setting, not verified).
4. Update `CHANGELOG.md`, create the `vX.Y.Z` tag on the commit with green CI, and publish the release with the version's limitations.

A change is "ready for production" only when it is in a tagged version. A merge to `main` is not a release.

## Blockers

Any critical failure with the skill, any regression against the baseline, any structural error, an empty "Release thresholds" section, or a missing record of the affected scenarios blocks the tag. There is no exception for an average across other dimensions.
