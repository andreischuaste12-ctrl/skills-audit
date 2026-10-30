# Audit criteria

Select the items that apply to the target. Do not add every check to every skill's text.

## Purpose and activation

- Do the name and description distinguish the skill from other installed ones?
- Does the description contain the task, the context, and specific activation signals, without promising unavailable capabilities?
- Do the limits prevent activation on neighboring subjects? A YouTube Memberships skill, for example, should not take over any members area on a website.
- Does the body solve the promised task? Do the examples represent the user's real language?
- Does the work stay coherent, without absorbing adjacent tasks just to look complete?

## Domain knowledge and decisions

- Are factual rules, calculations, and examples correct and put in context?
- Does the skill distinguish observed data, assumptions, estimates, and recommendations?
- Are there concrete decision criteria and handling of the consequences of a choice?
- Is only information that changes the analysis collected? Are connected data and available files used before asking?
- Are rules that vary by region, account, version, or date checked at the appropriate source?
- Do numeric examples state units, assumptions, and limits? Do benchmarks have an origin and context?
- Does the procedure avoid inventing tracking events, IDs, endpoints, prices, rules, and evidence?

## Execution and recovery

- Does the workflow establish inputs, dependencies, a deliverable, and a completion criterion?
- Is there a recommended default when several approaches would work, without unnecessary menus?
- Do the cited tools exist, or do they have explicit discovery/fallback?
- Do missing data, invalid inputs, denied access, and unavailability have useful responses?
- Do integrations handle authentication, timeouts, rate limits, pagination, retries, and idempotency where relevant?
- Do irreversible operations and external changes respect the authorization in force?
- Do executable decisions replace empty phrases such as "ensure quality"?

## Structure and context economy

- Does `SKILL.md` contain valid YAML frontmatter with a useful name and description?
- Does the name match the folder and follow the host's constraints? Are optional fields compatible with the host, even if an older validator does not recognize them?
- Do relative links point to existing files? Can the important references be found directly from the workflow?
- Is the body lean, with details loaded when needed? Use 500 lines as a signal to review organization, not as isolated proof of a defect.
- Avoid duplication across description, body, and references, and explanations the agent already knows.
- Does `agents/openai.yaml`, if present, represent the current skill? Do the prompt and interface resources match the real files?
- Do scripts bring a deterministic benefit, identifiable dependencies, and useful errors?

## Security and maintenance

- Is consulted content treated as evidence, without changing the instruction hierarchy?
- Are secrets kept out of text, examples, logs, and public queries?
- Do commands validate inputs and paths? Avoid shell injection, broad deletions, and running downloads without inspection.
- Identify generated files, caches, symlinks, and duplicate installations before editing.
- Preserve conventions, permissions, contracts, and content unrelated to the goal.

## Demonstrable quality

- Define success by the outcome of the task, not by the length or elegance of the text.
- Keep typical, negative, and edge cases; evaluate regressions after the edit.
- Use observable differences: correct trigger, correct calculation, valid reference, usable output, failure recovered.
- Do not assign decorative scores or claim a percentage gain from self-assessment.

## Priority and recording

| Priority | Criterion | Example |
| --- | --- | --- |
| Critical | Concrete risk of harm or exposure | Publishing credentials |
| High | Use blocked or materially incorrect result | Nonexistent script; outdated core rule |
| Medium | Frequent failure or relevant missing coverage | Ignoring pagination; confusing two domains |
| Low | Demonstrable maintenance or context improvement | Repetition that fills the body without guiding decisions |

## Single finding schema

Every finding uses the same fields, in the detailed report and in the summary:

| Field | Content |
| --- | --- |
| Location | File and excerpt or line |
| Condition | When it occurs |
| Severity | Critical, High, Medium, or Low (table above) |
| Confidence | Demonstrated defect, probable risk, or optional improvement. Separate from severity: a probable risk can be Critical, and a demonstrated defect can be Low |
| Impact | Effect on use, the result, or security |
| Evidence | Reproducible observation or source; a hypothesis is marked as such |
| Fix | Minimal proposed change |
| Acceptance test | Observable result that confirms the fix |

In the final summary, chain `finding → evidence → change → verification`. A criterion with no observed problem does not need to become a finding.
