# Changelog

Format: newest versions first. No version has been released yet.

## Unreleased

### Added
- `scripts/validate.py` and `scripts/test_validate.py`: structural validation and tests with injected defects (43 tests).
- `requirements-dev.txt` (PyYAML 6.0.2).
- GitHub Actions workflow `.github/workflows/validate.yml`, with a Python 3.11, 3.12, and 3.13 matrix, and a status badge.
- `evals/RESULTS.md`: pass criteria, critical failures, and a record of runs.
- Evals 14 to 21 (skill-creator missing, package with dangerous paths, symlink, suspicious install command, instruction injection, dated fact, mismatched metadata, homonyms resolved by path) and 18 fixtures.
- Routing rule for when `skill-creator` is not available.
- Single finding schema, research limits, and a sources table with check status.
- `LICENSE` (MIT), `CONTRIBUTING.md`, `SECURITY.md`, `RELEASING.md`, and `.github/pull_request_template.md`.
- Validator and tests for unreadable directories (`os.walk` now reports them).
- "Release thresholds" section and release-gate rules in `evals/RESULTS.md` and `RELEASING.md`; `Assertions met` and `Artifact` columns in the run record.

- First partial behavioral run on Claude Code 2.1.314: a smoke test and the seven critical scenarios, 24 transcripts in `evals/runs/2026-10-30_f777b71_claude-code-2.1.314/`, results and run notes in `evals/RESULTS.md`.

### Changed
- CI actions pinned to the SHAs the runner resolved on 2026-10-30.
- Only the with-skill condition and regressions against the baseline gate a release.
- `SECURITY.md`: no public issue as a fallback for reporting a vulnerability.
- The entire project is now in English: documentation, `SKILL.md`, references, evals, fixtures, validator messages, and tests. The skill responds in the language of the user's request.
- The collections reference was renamed from `colecoes-e-unificacao.md` to `collections-and-merging.md`.
- `evals/evals.json`: every scenario has `type`, `objective`, `expectations`, `forbidden`, `allowed_changes`, and `severity_if_failed`; the enum values are now `activation`, `execution`, `security`, `regression` and `critical`, `high`, `medium`.
- `scripts/validate.py`: the frontmatter and `agents/openai.yaml` go through a YAML parser (a duplicate key is an error); `evals.json` types are validated with a readable error; symlinks are rejected without reading their destination; fixtures are limited to relative paths in `evals/files`; unexpected failures become errors, not tracebacks.
- Eval 6: the agent must ask which same-name skill is the target before editing; `allowed_changes` is empty.
- `README.md` rewritten; `agents/openai.yaml` converted to LF; `.gitattributes` added.

### Pending
- Real execution of the 14 scenarios not yet run, and the repetitions and baselines for the activation scenarios (9 and 10 ran once as a smoke test).
- Skill activation: it was invoked in 7 of 14 critical runs; improving and re-measuring the description is open.
- Checking 6 of the 7 external sources.
- Deciding the repository name versus the skill's `name`.
- Enabling private vulnerability reporting and branch protection on GitHub (repository settings).
