---
name: note-maintainer
description: Maintain new and existing research notes in this repository, including metadata, evidence structure, images, README, experimental comparison, validation, and PR publication.
---

# Note Maintainer

Use this skill when adding a new paper note, updating an existing note, correcting research facts, adding figures, or maintaining repository-wide comparison documents.

## Required startup

Read in order:

1. `AGENTS.md`
2. `maintenance/roadmap.md`
3. `docs/new-note-workflow.md`
4. `docs/metadata-schema.md`
5. `docs/note-style-guide.md`
6. `docs/image-assets.md`
7. the active Issue / PR and relevant existing notes

Do not use chat history as the project state source.

## Workflow

### A. Orient

- Inspect repository structure and open PRs / Issues.
- Search for duplicate titles, arXiv IDs, project names and related notes.
- Decide whether the task is a new note, an update, a correction, or research-map maintenance.

### B. Verify

Use primary sources to verify unstable facts:

- proceedings / venue page;
- arXiv version and dates;
- OpenReview;
- official project page;
- official code and model repositories;
- image license.

Do not infer missing facts from paper titles or secondary posts.

### C. Classify

Determine before writing:

- `paper_type`
- `evolution_object`
- `learning_stage`
- `parameter_update`
- `cross_task`

Use `not-applicable` when a Position, Survey, Theory or diagnostic question truly does not implement an evolving system.

### D. Scaffold

For a new note, run `scripts/scaffold_note.py` with explicit classification arguments. Never overwrite an existing note.

### E. Write

Required content:

- 30-second reading layer;
- positioning and research question;
- mechanism card or analysis card;
- method / argument flow;
- experiment or evidence design;
- baselines, metrics, cost and reproducibility;
- claim–evidence–boundary table;
- own judgment and alternative explanations;
- external paper information;
- references.

Preserve useful existing depth when updating.

### F. Govern images

- Localize only when redistribution permission is verified.
- Preserve original bytes for no-derivatives licenses.
- Update manifest, inventory, attribution, hashes and note paths.
- Otherwise keep the external reference with a documented deferral reason.

### G. Synchronize views

Update as applicable:

- note metadata;
- `related_notes`;
- generated README index;
- `surveys/experimental-comparison-data.json`;
- generated experimental comparison;
- image inventory;
- roadmap or research-gap map.

### H. Validate

Run all commands listed in `AGENTS.md`. Fix failures before publication.

### I. Publish

- Branch from current `main` using `codex/<description>`.
- Create a Draft PR by default.
- Describe facts verified, classification, evidence boundaries, image licenses, generated files and checks.
- Update `maintenance/roadmap.md` when the active stage changes.

## New-note completion checklist

- [ ] No duplicate note exists.
- [ ] Primary external sources were checked.
- [ ] Metadata uses schema 1.0 and has no guessed values.
- [ ] Correct mechanism / analysis card is retained.
- [ ] Main claims have evidence and explicit boundaries.
- [ ] Cost and reproducibility are discussed.
- [ ] Images are licensed or deferred.
- [ ] README is regenerated.
- [ ] Experimental comparison data is updated and regenerated.
- [ ] Related notes are meaningful.
- [ ] Full validation passes.
- [ ] Draft PR explains remaining uncertainty.

## Update-note completion checklist

- [ ] `updated` and, when applicable, `last_verified` are refreshed.
- [ ] The top summary still matches the revised evidence.
- [ ] Mechanism / analysis card is synchronized.
- [ ] Claim–evidence–boundary table reflects new results.
- [ ] External status and resources are current.
- [ ] Generated views and image inventory are synchronized.
- [ ] Full validation passes.

## Prohibited shortcuts

- Do not add a note only to README.
- Do not edit generated Markdown without its data source.
- Do not copy figures merely because they are publicly viewable.
- Do not call a same-task search process cross-task learning.
- Do not call auxiliary-policy training base-model training.
- Do not treat an author claim as an established fact.
- Do not leave roadmap state only in a chat message.
