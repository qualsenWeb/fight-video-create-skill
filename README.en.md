# Fight Video Create Skill

[中文](README.md) | [English](README.en.md) | [Changelog](changelog.md)

Turn a short fight concept into a usable story beat, action design, spatial route, storyboard, and video-generation prompt. The skill can also classify and ingest user-provided fight references into a searchable library.

> Built for animated dramas, live-action fights, animation, wuxia, xianxia, and ability-driven combat. Reference material informs the work; it never overrides the characters, weapons, outcome, duration, or ending you specify.

## What it does

- **Concept to production draft** — Develops conflict, action causality, staging, storyboards, and generation constraints from a rough premise.
- **Layered retrieval** — Searches scenes, action/storyboard plans, move references, and sample scripts in order; it only reads a source after a keyword match.
- **Move plausibility checks** — Verifies weapon form, range, pose, environmental support, duration, and character abilities before using a technique.
- **Reference ingestion** — Classifies `.docx`, `.txt`, and similar materials as scenes, directing plans, move references, or sample scripts; maintains routing metadata.
- **Verifiable library** — Includes a deterministic router and validation scripts, so unrelated references are not forced into a concept.

## Installation

### Clone the repository

```bash
git clone https://github.com/qualsenWeb/fight-video-create-skill.git
```

### Install through an agent

Send this to an agent that supports Skill installation:

```text
Install this skill: https://github.com/qualsenWeb/fight-video-create-skill
```

## Quick start

### Design a fight

```text
Use fight-video-create-skill:
A man with a spear and a woman with a sword fight in somewhere.
Create a 15-second, 16:9, cinematic storyboard.
```

The skill first identifies the scene and eligible action plan. If several plans match, it recommends one and waits for your choice before producing the design.

### Ingest new references

```text
Use fight-video-create-skill to ingest these references:
`Bamboo Grove Fight.docx`, `Riverside Battle.txt`
```

Before any write, the skill reports the intended destination, reusable material, and duplicate or conflict risks. It writes and validates the library only after confirmation.

## Workflow

1. Extract the locked facts: characters, weapons, abilities, location, combat scale, duration, and ending.
2. Retrieve scene references; create an original setting if nothing matches.
3. Retrieve an action/storyboard plan. You confirm the main plan, or choose an original/custom plan when there is no match.
4. Retrieve move references only when specific weapon techniques, martial-arts binding, or beat-by-beat choreography is needed.
5. Adapt transferable story structure from sample scripts without reusing their proprietary characters or unrelated plot.
6. Deliver the story, action chain, spatial route, storyboard, and generation constraints.

## Repository layout

```text
SKILL.md                                  # Workflow and constraints
reference/
  scenes/                                 # Scene and spatial references
  action-storyboard-design/               # Action / storyboard directing plans
    招式库/                                # Weapon, martial arts, and combo references
  example-scripts/                        # Sample scripts and finished-structure references
scripts/
  route_reference.py                      # Deterministic keyword router
  validate_routes.py                      # Routing metadata validator
```

## Local validation

After ingesting material or changing a route, run:

```bash
python -X utf8 scripts/validate_routes.py
```

Inspect a route with:

```bash
python -X utf8 scripts/route_reference.py design --query "bamboo grove sword chase"
```

## Documentation

- [Workflow and operating instructions](SKILL.md)
- [Changelog](changelog.md)
- [中文 README](README.md)

## Contributing

Contributions of scenes, directing plans, move references, and sample scripts are welcome. When adding, deleting, or renaming material, update the relevant `00-路由元.json` file and run the validator.
