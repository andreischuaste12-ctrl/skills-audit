# skills-audit

[![validate](https://github.com/andreischuaste12-ctrl/skills-audit/actions/workflows/validate.yml/badge.svg)](https://github.com/andreischuaste12-ctrl/skills-audit/actions/workflows/validate.yml)

The `improve-skills-konvert` skill: evidence-based auditing and improvement of AI agent skills. It reviews activation, workflow, references, security, and evaluation coverage; researches material gaps; and recommends whether each skill should be kept, improved, split, merged, or retired.

Language: English. The skill responds in the language of the user's request. Version: unreleased (see `CHANGELOG.md`).

## Scope

Scope decisions, set by the maintainer on 2026-10-30:

- **Audience:** a public open source project, for people who maintain personal or team skills and need to decide what to fix, merge, or retire. Contributions follow `CONTRIBUTING.md`; vulnerabilities, `SECURITY.md`.
- **Primary host:** Claude Code. Codex is a secondary target, because of `agents/openai.yaml`. Neither has compatibility proven by execution (see "Verification status"). Format compatibility (the files follow the skill structure) is not behavior compatibility (the agent behaves as expected).
- **Default deliverable:** findings with location, evidence, severity, and confidence; a recommendation per skill; changes made; checks run and not run.

### This skill or `skill-creator`?

| Request | Destination |
| --- | --- |
| Diagnose, review, or optimize an existing skill | This skill |
| Compare skills, detect duplication, decide whether to merge | This skill |
| Validate regressions after changing a skill | This skill |
| Create a skill from scratch | `skill-creator` |
| One-off edit without an audit (e.g., changing `default_prompt`) | `skill-creator` |
| Audit a website, SEO, or code with no skill as the target | Neither |

If `skill-creator` is not available, the skill says so and offers to install it or to continue with the audit workflow by explicit choice; it does not run the full audit silently.

## Structure

| Path | Role |
| --- | --- |
| `SKILL.md` | Six-step workflow: target, inspection, research, improvements, verification, delivery |
| `references/audit-criteria.md` | Audit criteria, priorities, and the single finding schema |
| `references/research-and-validation.md` | When and how far to research, validation levels, sources and their upkeep |
| `references/collections-and-merging.md` | Collection protocol: inventory, overlap, fate, and merging |
| `agents/openai.yaml` | Interface metadata (Codex/OpenAI) |
| `evals/evals.json` | 21 scenarios with assertions, forbidden behaviors, and severity |
| `evals/files/` | Scenario fixtures (`.txt` extension, so they are not discovered as skills) |
| `evals/RESULTS.md` | Pass criteria, critical failures, and the record of runs |
| `scripts/validate.py`, `scripts/test_validate.py` | Structural validation and its tests |
| `requirements-dev.txt` | The validator's development dependency (PyYAML, pinned) |
| `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md` | MIT license, contribution guide, and security policy |
| `CHANGELOG.md` | Change history |
| `RELEASING.md` | Versioning, release criteria, and what requires re-running the evals |
| `.github/pull_request_template.md` | PR checklist |

## Installation and updating

The skill name (`improve-skills-konvert`) is what the host uses; this repository's name (`skills-audit`) belongs to the project only. Install by copying the package into a folder named after the skill:

```bash
mkdir -p ~/.claude/skills/improve-skills-konvert
cp -r SKILL.md agents references evals scripts ~/.claude/skills/improve-skills-konvert/
```

The repository is the source of the package. In use, the skill needs `SKILL.md`, `references/`, and `agents/`; `evals/` and `scripts/` are maintenance assets, and `SKILL.md` links to `evals/` (if you omit that folder, those links are broken in the installed copy). To update, repeat the copy over the installed folder without creating a second installation. Other hosts' skills directories may differ; confirm in the host's documentation. The validator emits a warning (not an error) when the repository folder differs from the `name`, because the Claude Code documentation does not require them to match.

## Validation

Requires Python 3 and PyYAML (development only, pinned in `requirements-dev.txt`). Tested locally on Python 3.11, 3.12, and 3.13 with PyYAML 6.0.2; CI runs the same matrix. Other versions were not tested.

```bash
pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s scripts -p "test_*.py"
```

The first command parses the frontmatter and `agents/openai.yaml` with a YAML parser (a duplicate key is an error) and checks types, links, cited paths, evals (structure, types, conditional fields), fixtures (relative paths inside `evals/files` only), line endings, and the description. Any symlink is an error and its destination is not read; a directory that cannot be read is an error, not a silent skip. Each problem is reported with a file and a reason; JSON or YAML with the wrong structure produces a readable error, never a traceback. Without PyYAML, the validator exits with code 2 and installation instructions. The second command injects defects on purpose and checks that the validator detects them.

## Verification status

| Level | What it is | Status |
| --- | --- | --- |
| Structural | Files, YAML, JSON, links, metadata | Automated. The `validate` workflow passed on commits `bffb94f`, `005bc20`, `cc93212`, and `dcaf013` (checked on 2026-10-30); since `cc93212` it runs on Python 3.11, 3.12, and 3.13. The current commit still has to pass CI after the push |
| Walkthrough | The workflow applied manually to a scenario | Not recorded |
| Behavioral execution | An agent runs the scenario on the host, with and without the skill | **Not recorded** (see `evals/RESULTS.md`) |

An evaluation scenario is not an execution: until there are rows in `evals/RESULTS.md`, there is no evidence of performance or of host compatibility.

### Validated hosts

None. A host enters this table only after installation, discovery, and invocation have been tested, with the smoke test recorded.

| Host | Installation procedure | Discovery | Invocation | Smoke test | Date |
| --- | --- | --- | --- | --- | --- |
| Claude Code (primary) | not tested | not tested | not tested | not run | – |
| Codex (secondary) | not tested | not tested | not tested | not run | – |

If only one host is tested, it will be declared the only validated host.

## Known limitations

- No behavioral execution recorded.
- 6 of the 7 sources in `references/research-and-validation.md` were not opened at the last check (2026-10-30); only the Claude Code documentation was read, partially.
- Branch protection requiring the `validate` checks is a GitHub setting and was not verified.
- CI validates structure only; validating behavior needs an agent and costs tokens, so it runs manually (see `RELEASING.md`), not on every PR.
- The workflow actions are pinned to the SHAs the runner resolved for `@v4` and `@v5` on 2026-10-30. The runner warns that both actions target Node.js 20 and run forced on Node.js 24, so move to newer releases once verified. Pins do not update themselves.

## Publishing a change

Details and versioning criteria are in `RELEASING.md`. Summary:

1. Run the two validation commands.
2. If you changed `SKILL.md`, references, fixtures, or criteria, run the affected scenarios with and without the skill and record them in `evals/RESULTS.md`.
3. Block publication on a structural error, a critical failure with the skill, or a regression against the baseline (see `evals/RESULTS.md`).
4. Update `CHANGELOG.md` and record the version's limitations.
5. Check the result of the `validate` workflow on the published commit and, to make the check mandatory, require the `structure` job checks (one per Python version) in GitHub branch protection.

## License

[MIT](LICENSE).
