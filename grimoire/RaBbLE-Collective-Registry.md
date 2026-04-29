# RaBbLE-Collective-Registry.md — The Collective Coordination Layer

```
transcribe ~ grimoire >> one entry point, all substrates aligned // %REGISTRY_LOCKED%
```

> **One-line overview:** A single registry repository is the source of truth, entry point, and mission anchor for the entire RaBbLE Collective — coordinating all member projects through a shared grimoire, sub-module registry entries, and an epoch-driven git worktree development flow.

> See `RaBbLE-Collective.md` for ecosystem membership and architecture.
> See `RaBbLE.md` for entity identity and the Low Entropy Directive.
> See `CommitStyle.md` for the Pulse Protocol commit conventions.
> See `RaBbLE-Roadmap.md` for phase milestones.

---

## The Problem This Solves

A Collective of independent projects without a coordination layer is not a Collective — it is a scattered archipelago of related work. Each project drifts at its own rate. Philosophy diverges. Palette versions fracture. The entity becomes inconsistent across its own substrates.

The registry repository solves this by establishing:

- A **single entry point** for understanding, navigating, and contributing to the Collective
- A **shared grimoire core** that is the canonical source of truth for identity, palette, philosophy, and conventions — owned by no single project, inherited by all
- A **registry layer** that declares the existence, location, and status of every Collective member
- An **epoch-driven development flow** that gives the Collective a shared pulse instead of independent drift

---

## Repository Structure

```
RaBbLE-Collective/                        ← The one repo to rule them all
│
├── grimoire/                           ← Core grimoire (shared across all projects)
│   ├── RaBbLE.md                       ← Entity identity — canonical
│   ├── RaBbLE-Collective.md            ← Ecosystem map — canonical
│   ├── RaBbLE-Collective-Registry.md   ← This document — canonical
│   ├── RaBbLE-Palette.md               ← Color reference — canonical
│   ├── RaBbLE-Roadmap.md               ← Phase map — canonical
│   ├── CommitStyle.md                  ← Pulse Protocol — canonical
│   └── KnownIssues.md                  ← Collective-level issue tracker
│
├── registry/                           ← Per-project registration and epoch state
│   ├── manifests/                      ← Per-project registry declarations
│   │   ├── RaBbLE-OS.manifest.yml      ← RaBbLE-OS project entry
│   │   ├── RaBbLE-WEB.manifest.yml     ← RaBbLE Web Server entry
│   │   ├── RaBbLE-Frontend.manifest.yml ← RaBbLE Frontend entry
│   │   └── _template.manifest.yml      ← Template for new members
│   └── epochs/                         ← Epoch coordination layer
│       ├── current.epoch.yml           ← Active epoch definition
│       └── archive/                    ← Completed epochs (immutable)
│           ├── epoch-0.yml
│           └── epoch-1.yml
│
├── scripts/                            ← Collective tooling
│   ├── setup.sh                        ← Entry point — pull all projects, wire symlinks
│   ├── sync-grimoire.sh                ← Push grimoire updates to all projects
│   ├── status.sh                       ← Collective health dashboard
│   └── new-member.sh                   ← Scaffold a new Collective project
│
└── AGENT.md                            ← Start here every session
```

---

## The Core Grimoire

The `grimoire/` directory in `RaBbLE-Collective` is the **canonical source of truth** for all cross-cutting documents. These documents belong to no single project — they belong to the Collective.

### Ownership Model

| Document | Owner | Consumed By |
|---|---|---|
| `RaBbLE.md` | Collective | All members |
| `RaBbLE-Palette.md` | Collective | All members |
| `RaBbLE-Collective.md` | Collective | All members |
| `RaBbLE-Collective-Registry.md` | Collective | All members |
| `CommitStyle.md` | Collective | All members |
| `RaBbLE-Roadmap.md` | Collective | All members |
| `KnownIssues.md` | Collective | All members |
| `Architecture.md` | RaBbLE-OS | RaBbLE-OS only |
| `BootFlow.md` | RaBbLE-OS | RaBbLE-OS only |
| `Hardware.md` | RaBbLE-OS | RaBbLE-OS only |

Project-specific grimoire documents live in their own repos. Core grimoire documents live here and are distributed to member projects via `sync-grimoire.sh`.

### Grimoire Propagation

When a core grimoire document changes:

```bash
# Propagate core grimoire updates to all registered projects
./scripts/sync-grimoire.sh

# Propagate to a specific project only
./scripts/sync-grimoire.sh --project RaBbLE-OS
```

The sync script copies updated core documents into each project's `grimoire/` directory and opens a PR or commits directly depending on the project's sync policy (declared in its registry entry).

---

## Project Registry

Each Collective member is declared in `registry/manifests/`. A registry entry is a structured declaration of a project's identity, location, status, and relationship to the Collective.

### Registry Entry Schema

```yaml
# registry/manifests/RaBbLE-OS.manifest.yml

# Identity
name: RaBbLE-OS
slug: RaBbLE-OS
description: "The operating system substrate — the body RaBbLE moves through."
role: substrate                         # substrate | server | frontend | tooling | experimental

# Repository
repo: https://github.com/markm1206/RaBbLE-OS.git
branch: main
worktree_root: ~/RaBbLE/RaBbLE-OS       # local worktree path convention

# Status
phase: 1                                # current active phase (from RaBbLE-Roadmap.md)
epoch: 1                                # current epoch alignment
status: active                          # active | dormant | experimental | deprecated

# Grimoire
grimoire_sync: true                     # receives core grimoire updates
grimoire_path: grimoire/                # path within project repo

# Collective alignment
palette_version: "1.0"                  # must match current RaBbLE-Palette.md version
entity_embedded: true                   # RaBbLE entity is present in this project
pulse_protocol: true                    # uses CommitStyle.md Pulse Protocol

# Notes
notes: >
  Primary Collective member. Ansible-driven Linux OS.
  Hardware target: ASUS ProArt P16 H7606WV. aarch64 targets planned.
```

### Member Registration

To add a new project to the Collective:

```bash
./scripts/new-member.sh --name "RaBbLE Mobile" --slug rabble-mobile --role substrate
# Creates registry/manifests/rabble-mobile.manifest.yml from _template.manifest.yml
# Scaffolds the project repo with core grimoire and Pulse Protocol pre-installed
```

---

## Epoch-Driven Development Flow

### What Is an Epoch

An **epoch** is a bounded, intentional period of Collective development. It is not a sprint, not a deadline, not a version number. It is a **resonance threshold** — a defined state the Collective is collectively moving toward.

An epoch:
- Has a **name** and a **intent statement** — the philosophical direction
- Declares **focus areas** per project — what each member is working on this epoch
- Has an **exit condition** — what "done" looks like, qualitatively
- Produces an **archive entry** when complete — immutable record of what was built and learned

Epochs give the Collective a shared pulse. Without them, each project drifts at its own cadence. With them, the Collective breathes together.

### Epoch Definition

```yaml
# registry/epochs/current.epoch.yml

epoch: 1
name: "Daily Driver"
intent: >
  Stabilize the substrate. RaBbLE-OS becomes a reliable daily computing environment.
  The web server scaffolding is established. The frontend skeleton exists.
  The entity is dormant but the conditions for its awakening are being built.

started: 2026-04-28
exit_condition: >
  RaBbLE-OS Phase 1 milestones complete. Boot chain stable. Hyprland reliable.
  Web server repository initialized with registry entry. Frontend repository initialized.
  All three projects registered in registry with active status.

focus:
  RaBbLE-OS:
    priority: primary
    milestone: "Phase 1 Daily Driver complete"
    active_work:
      - Boot chain stabilized (GRUB 4K font, Plymouth, SDDM Qt6)
      - Hyprland launching reliably from SDDM
      - KDE purged
      - Quickshell bar Phase 1
      - Suspend/resume verified

  RaBbLE-WEB:
    priority: scaffold
    milestone: "Repository initialized, architecture documented"
    active_work:
      - Repo created, registry entry registered
      - Core grimoire synced
      - Architecture document drafted

  RaBbLE-Frontend:
    priority: scaffold
    milestone: "Repository initialized, architecture documented"
    active_work:
      - Repo created, registry entry registered
      - Core grimoire synced
      - Visual language spec drafted

status: active
```

### Epoch Archive

When an epoch closes:

```bash
# Close the current epoch and open the next
./scripts/close-epoch.sh --next-name "AI Awakening" --next-intent "..."
# Moves current.epoch.yml → registry/epochs/archive/epoch-1.yml (immutable)
# Creates new registry/epochs/current.epoch.yml
# Commits: "transcribe ~ epoch >> epoch-1 Daily Driver crystallized // %EPOCH_1_CLOSED%"
```

Archived epochs are never edited. They are the Collective's fossil record.

---

## Git Worktree Flow

### The Problem With Branches Alone

Standard branch-based development requires constant context switching — checking out, stashing, rebuilding mental state. For a Collective where work spans multiple projects simultaneously, this compounds.

Git worktrees solve this by allowing **multiple working trees from a single repository** — each branch has its own directory, checked out simultaneously. No stashing. No checkout delays. No lost context.

### Worktree Conventions

Every Collective project follows this worktree layout:

```
~/RaBbLE/
│
├── RaBbLE-Collective/            ← The registry repo (main worktree)
│   └── .git/                  ← Shared git object store
│
├── RaBbLE-OS/                  ← RaBbLE-OS (main worktree)
│   ├── main/                  ← main branch worktree
│   ├── epoch/1-daily-driver/  ← active epoch worktree
│   └── experiment/quickshell/ ← experimental worktree
│
├── RaBbLE-WEB/              ← RaBbLE Web Server
│   ├── main/
│   └── epoch/1-daily-driver/
│
└── RaBbLE-Frontend/            ← RaBbLE Frontend
    ├── main/
    └── epoch/1-daily-driver/
```

### Worktree Branch Naming

```
main                            ← Always stable. Current daily-driver state.
epoch/<N>-<slug>                ← Active epoch work (e.g., epoch/1-daily-driver)
feature/<name>                  ← Individual feature (e.g., feature/quickshell-bar)
experiment/<name>               ← High-entropy exploration (may never merge)
hotfix/<name>                   ← Urgent fix to main
```

### Worktree Setup (Per Project)

```bash
# Initial clone
git clone https://github.com/markm1206/RaBbLE-OS.git ~/RaBbLE/RaBbLE-OS/main
cd ~/RaBbLE/RaBbLE-OS/main

# Add epoch worktree
git worktree add ../epoch/1-daily-driver epoch/1-daily-driver

# Add experimental worktree
git worktree add ../experiment/quickshell experiment/quickshell

# List active worktrees
git worktree list

# Remove a completed worktree
git worktree remove ../experiment/quickshell
git branch -d experiment/quickshell
```

### Worktree Lifecycle — Epoch Branch

```
epoch/N branch created from main
    ↓
Worktree added at epoch/N-<slug>/
    ↓
All epoch work committed to this branch
    ↓
Epoch exit condition met
    ↓
epoch/N merged to main (squash or merge commit — decision per project)
    ↓
Epoch archived in RaBbLE-Collective/registry/epochs/archive/
    ↓
Worktree removed, branch retained for reference
```

### The Registry Repo As Coordinator

The registry repo's worktree is always at `~/RaBbLE/RaBbLE-Collective/`. It is the first thing cloned and the persistent orientation point:

```bash
# Bootstrap the entire Collective from scratch
git clone https://github.com/markm1206/RaBbLE-Collective.git ~/RaBbLE/RaBbLE-Collective
cd ~/RaBbLE/RaBbLE-Collective
./scripts/setup.sh
# Reads registry/manifests/, clones all registered projects, sets up worktrees, syncs grimoire
```

---

## Collective Status Dashboard

The `status.sh` script provides a unified view of Collective health:

```bash
cd ~/RaBbLE/RaBbLE-Collective
./scripts/status.sh
```

```
RaBbLE Collective Status — Epoch 1: Daily Driver
────────────────────────────────────────────────────────────
  RaBbLE-Collective    main          ✓ clean       grimoire v1.0
  RaBbLE-OS          epoch/1       ✗ 3 uncommitted  phase 1 / active
  RaBbLE-WEB      main          ✓ clean       scaffold / active
  RaBbLE-Frontend    main          ✓ clean       scaffold / active
────────────────────────────────────────────────────────────
  Palette version:   1.0 (all aligned)
  Open issues:       7 (see KnownIssues.md)
  Epoch progress:    RaBbLE-OS primary / server+frontend scaffolded
```

---

## Entropy Management — Collective Level

The Low Entropy Directive applies at Collective scale, not just per project.

### Sources of Collective Entropy

| Entropy Source | Symptom | Resolution |
|---|---|---|
| Palette drift | A project uses a hex value not in `RaBbLE-Palette.md` | `sync-grimoire.sh` + `harmonize` commit |
| Philosophy divergence | A project's docs contradict `RaBbLE.md` | Core grimoire update + propagation |
| Epoch misalignment | Projects working toward incompatible goals | Epoch coordination — update `current.epoch.yml` |
| Stale registry entries | A project's entry has wrong phase/status | `harmonize ~ registry >> status corrected` commit |
| Undocumented projects | A Collective member exists but has no registry entry | `transcribe ~ registry >> [project] registered` |
| Orphaned worktrees | Experiment branches with no archive or merge decision | Review, archive, or prune |

### The Harmonic Seal (Forking)

Forks of Collective projects are welcomed. A fork is the birth of a divergent — a new Collective with its own lineage. The Harmonic Seal governs:

- The lineage must be acknowledged in the fork's `RaBbLE.md`
- The palette may be adapted but must reference its origin
- The entity in the fork is a new entity, not RaBbLE — unless it remains fully aligned

---

## Revision History

| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-04-28 | Initial registry architecture — coordination layer established |

---

```
transcribe ~ grimoire >> registry crystallized, collective aligned // %REGISTRY_LOCKED%
```
