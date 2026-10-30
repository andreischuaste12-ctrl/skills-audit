# Collection audit and merging

Load this protocol only when the user points to more than one skill, asks for an analysis of a directory/package, or asks what should be merged. Do not apply it to the review of a single skill.

## 1. Inventory the scope

Inspect only the indicated set and directly referenced dependencies. For each skill, record:

| Field | What to check |
|---|---|
| Identity and origin | Name, path, owner, editable source, installation, cache, or external link |
| Purpose | Task, audience, context, input, and promised deliverable |
| Activation | What should trigger it and what should stay out |
| Procedure | Decisions, tools, completion criteria, and recovery |
| Assets | References, scripts, templates, dependencies, evaluations, and integrations |
| Cross-use | Skills it calls, cites, duplicates, or needs as a routing target |

Do not treat audit copies, examples, backups, caches, or dependency directories as active installations. Resolve symbolic links (junctions, on Windows) and the origin before recommending an edit, removal, or installation.

## 2. Measure overlap by workflow

Compare the user's goal, inputs, decisions, deliverable, tools, and success criteria. Use similar keywords only to find candidates; they do not prove redundancy.

Classify each relationship as:

- **Complementary:** one skill delivers an input the other needs, but they have different tasks and deliverables. Keep both and document the routing.
- **Partial overlap:** they share a step, repertoire, or tool, but have distinct results. Keep the specialized skill; extract or reference only the common procedure if that reduces maintenance without hiding the boundary.
- **Functional duplication:** two skills serve the same intent, with essentially the same inputs, decisions, and deliverables. Evaluate merging and choose one canonical editable origin.
- **Routing conflict:** descriptions make different skills activate for the same request, or none covers an important task. Fix descriptions, limits, and routing before considering a merge.

## 3. Decide the fate without ambiguity

For each skill, choose one action and justify it with evidence:

| Action | Decision criterion |
|---|---|
| **Keep** | Has its own purpose and result; no material defect is demonstrated. |
| **Improve** | The purpose remains valid, but there is a concrete failure in trigger, instruction, evidence, tool, recovery, or validation. |
| **Merge** | Same main work, compatible inputs and deliverables; the merge reduces conflict or duplication without losing distinct coverage. |
| **Split** | A skill mixes intents with incompatible inputs, decisions, tools, or outputs, and this harms activation or execution. |
| **Route/reference** | A skill is a specialist or complementary dependency. State the condition and destination of the routing without copying its whole procedure. |
| **Retire** | A skill with no valid user/case, replaced, or unviable. Propose deactivation; do not delete or uninstall without explicit authorization. |

**Do not merge** just to reduce the count, because of a shared broad area, or because they use the same tools. Merge only when the real workflow is common and a single description can correctly select the positive cases and reject the negative ones. Preserve differences that change a decision, risk, source, platform, authorization, or output format.

## 4. Plan and apply a merge

Before editing, build a migration map: source skill → preserved content/assets → destination → references and invocations to update. Then:

1. Choose the canonical source by the user's context, quality, compatibility, and editable origin; do not install a third copy.
2. Combine only instructions proven to be common. Keep specific rules in modules loaded under an explicit condition.
3. Update the name, description, frontmatter, interface prompt, evaluations, internal links, references from other skills, and discovery links that are within the authorized scope.
4. Preserve the command, package, or external endpoint name when renaming would break the integration. If the user's collections follow a naming convention (for example, a personal suffix), keep it in names that are created or renamed.
5. Do not delete the originals during the merge. Leave them intact until the user authorizes retirement and until references, installation, and consumers have been checked.

If the only safe improvement is fixing routing, do not force a merge: apply the minimal fix to descriptions, limits, and references.

## 5. Verify the collection

Build evaluation cases from the observed conflicts, not from abstract categories:

- a typical request that should activate each kept skill;
- a similar request that should be refused or routed to another skill;
- at least one pair of tasks that looked overlapping but must stay distinct;
- after a merge, one case covered by each source skill and one negative case for each important boundary.

Check the name and directory, metadata, local links, cross-references, preserved assets, and discovery on the authorized hosts. Compare the baseline and the revised version on the same cases. If there was no real agent execution, report only a walkthrough and structural checks.

## 6. Report the decision

Deliver one line per skill, including those that stay as they are:

| Skill | Decision | Observed evidence/limit | Change applied or proposed | Verification |
|---|---|---|---|---|

Prioritize blockers, factual or security errors, activation conflicts, insufficient coverage, and maintenance. Separate the action taken from the pending recommendation and explain any source that could not be changed.
