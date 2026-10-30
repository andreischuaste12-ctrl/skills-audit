# Research and validation

## Prepare questions that change decisions

Start from the goal and the findings: does the rule still hold? Does the endpoint exist in this version? What data is missing to compute the recommendation? Does the description distinguish the domain? Does the behavior really fail, or does the wording just look unusual?

Tie each question to a possible change and a way to verify it. Do not research the whole industry with no connection to the workflow's decisions.

## When to research and how far

- **Need no external search:** a broken link, an internal contradiction, an unsafe instruction, invalid frontmatter, and any defect provable in the file itself.
- **Require external search:** a platform rule, an API version or signature, a regional policy, a host-specific limit or field, and any factual claim the audited skill makes about the world.
- **Default limit:** at most one verifiable question per finding that depends on an external source, and one primary source per question. Widen only when the source is ambiguous, outdated, or diverges from another primary source, and record the reason for widening.
- **Stop:** end when each material decision has a source or reproduction and each remaining uncertainty is recorded as pending.

## Search and cross-check evidence

1. Inspect the applicable local documentation, code, tests, and examples.
2. Look up the vendor's or maintainer's official documentation, specifications, and relevant original research.
3. Open the exact page, check the date, version, and context, and follow necessary references. Search results are leads, not proof.
4. For important or contested claims, check additional evidence or reproduce the behavior. Do not require two sources when one unambiguous normative reference settles the question.
5. Resolve divergences by the actual environment, version, source authority, and execution evidence. State uncertainties explicitly.

Do not send private code, customer data, credentials, or sensitive internal terms to public searches. Search for concepts and sanitized terms. Prefer authorized connectors for private data and verify tools before assuming they exist.

Keep a compact record outside the installed skill:

| Question/finding | Source or reproduction | Date and version | Decision | How to verify |
| --- | --- | --- | --- | --- |
| Concrete failure | Section URL or file/line | Applicable context | Change or keep | Observable criterion |

Do not replace evidence with verbal confidence or a search link. Put into the permanent material only the sources needed for future execution. Avoid copying large excerpts from third parties.

## Separate the validation levels

**Structural:** YAML parsing, host constraints, links, presence of resources, and the syntax of changed files. Proves basic integrity, not the quality of decisions.

**Manual walkthrough:** apply the workflow to a scenario and check the decisions and the result. Identifies gaps, but does not measure the reliability of new model runs.

**Real execution:** run the skill in the agent with defined inputs and criteria, collect the outputs, and compare versions. Separate development cases from reserved ones when the set allows. Do not open another agent or consume paid APIs without applicable authorization.

Cover normal use, a relevant limit, and a negative case. For calculations, include expected values; for scripts, exercise relevant errors; for risk domains, widen proportionally.

Compare versions with the same inputs and controlled conditions. If possible, hide the version from the evaluator to reduce preference for new text. Do not generalize from a single success. If there is only a walkthrough, call it a walkthrough.

## Verify without running unnecessary effects

- Inspect commands and dependencies before running third-party scripts.
- Use fixtures and mocks for integrations that publish, send messages, bill, or remove data. Improving the instruction does not authorize running the action it describes.
- Check the affected files first; widen according to risk.
- Review the diff and confirm the fix did not make another path unworkable.
- If access is missing, report which behavior was not confirmed. Do not fabricate data, sources, or results to pass a check.

## Official starting sources

Reviewed on 2026-10-26. Review trigger: recheck the list every 90 days, or sooner when a host changes version. Reopen the documentation when depending on versions, host support, or product status; this list does not replace research in the audited skill's own domain. Do not treat a portable specification as a guarantee of identical support in Codex, Claude Code, the API, or plugins.

Being on this list does not mean the source was consulted in an audit: cite a source as consulted only if the page was opened in that run. If a source cannot be accessed, record that in the report and keep the decision pending.

| Source | Type | Purpose | Recorded check |
| --- | --- | --- | --- |
| [Agent Skills: Specification](https://agentskills.io/specification) | Normative (portable format) | Portable structure and fields. Distinguish a specification requirement from concrete per-host support. | Not accessed on 2026-10-30 (host outside the allowed network). |
| [Claude Code: Skills](https://code.claude.com/docs/en/skills) | Host documentation | Frontmatter, discovery, invocation, and auxiliary files in Claude Code. | Opened on 2026-10-30: `description` and `when_to_use` together are capped at 1,536 characters in the listing; `name` need not match the folder; unknown fields are ignored. In claude.ai and the Skills API, only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools` are accepted. The final part of the page was not read. |
| [OpenAI: Skills](https://developers.openai.com/api/docs/guides/tools-skills) | Platform documentation | Format, discovery, and organization of resources for skills in the API. Confirm the local environment's conventions separately. | Not accessed on 2026-10-30 (host outside the allowed network). |
| [Agent Skills: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) | Recommendation | Execution knowledge, proportional detail, progressive disclosure, and recommended defaults instead of menus. | Not accessed on 2026-10-30 (host outside the allowed network). |
| [Agent Skills: Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) | Recommendation | Realistic cases, a baseline without the skill or with the previous version, and comparison-based evaluation. | Not accessed on 2026-10-30 (host outside the allowed network). |
| [OpenAI: Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Recommendation for the described product/model (not a universal rule) | Short, precise descriptions, progressive disclosure, and the risk of redundant or excessive instructions. | Not accessed on 2026-10-30 (host outside the allowed network). Confirm the page exists before depending on it. |
| [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Recommendation / platform documentation | Goals, case sets, and verifiable criteria. The page reports changes in the availability of the Evals platform; check the current notice before recommending an API or product, and prefer compatible local evaluations when the user only needs to validate a skill. | Not accessed on 2026-10-30 (host outside the allowed network). |

### Source maintenance

- When adding a source, record the reason for using it, the type (normative, host documentation, recommendation), and the date of the check.
- When depending on a source in an audit, reopen the page and note the date and version when the information varies by product or host.
- Separate a normative rule from a recommendation when justifying a change. A recommendation supports an optional improvement, not a defect.
- An automatic link checker detects an invalid URL, but does not prove that the content is current or applicable.
