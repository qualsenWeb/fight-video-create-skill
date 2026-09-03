# Fight Video Create Skill

[![中文](https://img.shields.io/badge/文档-中文-1677ff)](README.md) [![English](https://img.shields.io/badge/docs-English-64748b)](README.en.md) [![Changelog](https://img.shields.io/badge/changelog-更新日志-8b5cf6)](changelog.md)

> Turn one rough fight idea into executable story beats, action chains, spatial routes, storyboards, and video-generation prompts.

Built for animated dramas, live-action fights, animation, wuxia, xianxia, and ability-driven combat. References provide structure, mechanisms, and quality standards; they never override the characters, weapons, abilities, outcome, duration, or ending you specify.

## Core capabilities

| Capability | What it solves |
| --- | --- |
| **Concept to production draft** | Turns a vague premise into conflict, escalation, action causality, staging, and camera structure. |
| **Layered retrieval** | Searches scenes, action/storyboard plans, move references, conditional skills, and sample scripts in sequence; reads a source only after a match. |
| **Move plausibility gate** | Checks weapon form, range, pose, support points, character abilities, duration, and action continuity. |
| **Skill condition gate** | Gives moves priority, retrieves skills only by single-target/group scope, then checks required artifacts, body parts, media, and states. |
| **Reference ingestion** | Sorts `.docx`, `.txt`, and similar material into scenes, directing plans, move references, conditional skills, or sample scripts. |
| **Deterministic routing** | Uses keywords, field weights, and semantic signatures to return explainable candidates instead of relying on vague similarity. |
| **Verifiable delivery** | Validates inventory, files, IDs, keywords, and routing metadata after library changes. |

## Quick start

### 1. Design a fight

Send this minimal request to an agent that supports Skills:

```text
Use fight-video-create-skill:
A man with a spear fights a woman with a sword.
Create a 15-second, 16:9 cinematic storyboard.
```

The Skill extracts locked facts first, then routes through scene and action/storyboard references. If multiple plans match, it presents the recommended plan and alternatives, then waits for your confirmation before generating the design.

### 2. Ingest references

```text
Use fight-video-create-skill to ingest these references:
`Bamboo Grove Fight.docx`, `Riverside Battle.txt`
```

Before writing anything, the Skill reports for each file:

- the proposed destination and primary purpose;
- reusable spatial, action, camera, or story mechanisms;
- duplicate, conflict, and split risks against the current library.

It only deduplicates, writes, updates routing metadata, and validates after confirmation.

## Creation workflow

```text
Lock the facts
      ↓
Scene routing → scene summary or original setting
      ↓
Action/storyboard routing → user confirms one primary plan
      ↓
Move routing → plausibility gate (only when needed)
      ↓
Skill routing → single-target/group candidates → prerequisite confirmation (only when needed)
      ↓
Sample-script routing → transfer mechanisms, not proprietary content
      ↓
Story + action chain + spatial route + storyboard + generation constraints
```

### Operating principles

1. **User facts come first** — Characters, weapons, abilities, action order, outcome, duration, aspect ratio, and ending cannot be overwritten by a reference.
2. **Route before reading** — Automatic retrieval requires at least one route-keyword match; zero matches means the relevant part is original work.
3. **One primary plan at a time** — Action/storyboard plans require confirmation before their protocols are used or combined.
4. **Every move must be executable** — Key actions need a setup, body path, opponent response, contact or miss, force feedback, result, and next-state condition.
5. **Moves take priority over skills** — Anything expressible as a martial, weapon, or body-action chain stays in the move library. A selected skill must satisfy its artifact, body-part, medium, or state prerequisites.
6. **Transfer mechanisms only** — Reuse escalation, spatial phases, reversals, climax interfaces, and ending structure without copying proprietary characters, distinctive sentences, or unrelated plot.

## What the output contains

Unless you request another format, the default delivery includes:

1. **Basis of adaptation** — Confirmed plans, scene references, move and skill sources, sample scripts, and original sections;
2. **Story design** — Objective, conflict, escalation, reversal, causal outcome, and ending;
3. **Character action signatures** — Opening stance, range, movement, primary offense, counters, damage response, and finisher;
4. **Action design** — Purpose → body path → opponent response → contact feedback → displacement result → next-action condition;
5. **Spatial route and storyboard table** — Positions, viewing axis, camera handoff, camera endpoint, and sound;
6. **Generation constraints** — Stable characters and weapons, no body fusion, no turn-based resets, no random axis jumps, and no effects hiding key contacts.

The draft must also enter effective action quickly, give important actions clear consequences, carry each segment's final state into the next, avoid queueing enemies in group fights, derive the ending from an earlier opening, and keep the subject, camera, or environmental aftermath moving in the final frame.

## Reference library

```text
reference/
├── scenes/                                 # Scenes, environments, and spatial routes
├── action-storyboard-design/               # Action and storyboard directing plans
│   ├── 招式库/                              # Weapons, martial arts, footwork, and combos
│   └── 技能库/                              # Conditional standalone ability mechanisms
└── example-scripts/                         # Sample scripts and finished structures

scripts/
├── route_reference.py                      # Deterministic keyword router
└── validate_routes.py                      # Routing metadata validator
```

The skill library currently contains **10 conditional ability mechanisms**. It retrieves candidates only by single-target or group scope; secondary prerequisites never participate in matching. The sample-script library contains **28 cases**, covering sword fights, xianxia ranged qi exchanges, water-blade crowd clearing, multi-level architectural pursuit, formation-based suppression, cooperative combat, and large-scale ability finishers. The authoritative inventory and keywords are maintained in each directory's `00-路由元.json`.

## Local use and validation

Run routing commands from the repository root:

```bash
# Search action/storyboard plans
python -X utf8 scripts/route_reference.py design --query "bamboo grove sword chase"

# Search sample scripts
python -X utf8 scripts/route_reference.py scripts --query "water blade dark mist cooperative army clear"

# Retrieve skill candidates by scope; secondary prerequisites are not matched
python -X utf8 scripts/route_reference.py skills --query "群体"
```

After ingesting material or adding, removing, renaming, merging, or changing a route, run:

```bash
python -X utf8 scripts/validate_routes.py
```

On Windows, if the `python` command is not registered, use the Python Launcher:

```powershell
py -3 -X utf8 scripts/validate_routes.py
```

`eligible` contains only candidates with at least one keyword match. `available` lists all manually selectable plans and does not imply an automatic match. Skill routing always leaves `primary` empty; after selecting a candidate, inspect the secondary prerequisites in `selection_notice`.

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

## Documentation

- [Workflow and operating constraints](SKILL.md)
- [Changelog](changelog.md)
- [中文 README](README.md)

## Contributions and reference hygiene

Contributions of scenes, directing plans, move references, conditional skills, and sample scripts are welcome. When adding, removing, splitting, merging, or renaming material:

1. place it in the directory with the clearest responsibility;
2. update the relevant `00-路由元.json`;
3. use natural, discriminative search terms;
4. run `validate_routes.py` and smoke-test one strong keyword per new route;
5. preserve source notes and never present an inference as an original source fact.

## License

This repository currently has no separate license declaration. Confirm copyright and permission requirements before using, distributing, or submitting external reference material.