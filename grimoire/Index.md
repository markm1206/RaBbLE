# grimoire/

```
transcribe ~ grimoire >> the soul of the substrate // %GRIMOIRE_LOCKED%
```

The grimoire is RaBbLE-OS's living documentation layer — both technical reference and lore. It is the memory that survives hardware death. Every configuration, decision, and design intent lives here. The Ansible roles deploy the substrate; the grimoire explains why it is the way it is.

*Death is a transplant. The grimoire is the soul.*

---

## Document Index

### Identity & Philosophy

| Document | Purpose | Key Cross-References |
|---|---|---|
| [`RaBbLE.md`](RaBbLE.md) | The entity — identity, ethos, both voices, behavioral rules, memory architecture, system prompt template | `RaBbLE-Palette.md` (artistic dimension), `RaBbLE-Roadmap.md` (Phase 3) |
| [`RaBbLE-Palette.md`](RaBbLE-Palette.md) | **Canonical color reference** — all hex values, Ansible variable block, component mapping, glow effect guidance | `Architecture.md`, `Theming.md`, `BootFlow.md` |

### System Architecture

| Document | Purpose | Key Cross-References |
|---|---|---|
| [`Architecture.md`](Architecture.md) | Layer model, Ansible role dependency graph, GPU/power diagrams, desktop component map, dotfile symlink map, observability commands | `Hardware.md`, `RaBbLE-Palette.md`, `BootFlow.md`, `AddingTargets.md` |
| [`Hardware.md`](Hardware.md) | Verified hardware spec — CPU, GPU table, NPU, memory, display, kernel modules, verified commands | `Architecture.md`, `BootFlow.md`, `KnownIssues.md` |
| [`BootFlow.md`](BootFlow.md) | Full boot chain: GRUB → Plymouth → SDDM → Hyprland — per-stage palette targets, config paths, troubleshooting | `Hardware.md`, `RaBbLE-Palette.md`, `Theming.md`, `KnownIssues.md` |

### Theming & Visual System

| Document | Purpose | Key Cross-References |
|---|---|---|
| [`Theming.md`](Theming.md) | Component theming guide — how to change each layer, palette targets per component, terminal colors, prompt config, dotfile workflow | `RaBbLE-Palette.md`, `Architecture.md` (dotfile map) |

### Packages & Manifest

| Document | Purpose | Key Cross-References |
|---|---|---|
| [`Packages.md`](Packages.md) | Full package manifest by layer — repos, COPRs, what to install, what to purge | `Architecture.md` (layers), `RaBbLE-Roadmap.md` (phase gating) |

### Getting Started & Operations

| Document | Purpose | Key Cross-References |
|---|---|---|
| [`GettingStarted.md`](GettingStarted.md) | Fresh install walkthrough — Fedora 43 → full RaBbLE-OS, phase by phase | `Bootstrap.md`, `Hardware.md`, `KnownIssues.md` |
| [`Bootstrap.md`](Bootstrap.md) | Bootstrap system guide — menu structure, direct Ansible invocation, playbook reference, verification checklist, recovery | `GettingStarted.md`, `Architecture.md` |
| [`AddingTargets.md`](AddingTargets.md) | How to add a new hardware target — role structure, inventory, site.yml, bootstrap menu | `Architecture.md`, `Hardware.md` |

### Project Tracking

| Document | Purpose | Key Cross-References |
|---|---|---|
| [`RaBbLE-Roadmap.md`](RaBbLE-Roadmap.md) | Phase map and milestones — Foundation → Daily Driver → AI Awakening → Entity Emergence → workspace vision | `KnownIssues.md`, `RaBbLE.md` (Phase 3), `Architecture.md` (future multi-repo) |
| [`KnownIssues.md`](KnownIssues.md) | Active bugs, workarounds, resolved items, drift events | `BootFlow.md`, `Hardware.md`, `RaBbLE-Roadmap.md` |

### Conventions

| Document | Purpose | Key Cross-References |
|---|---|---|
| [`CommitStyle.md`](CommitStyle.md) | The Pulse Protocol — commit format, impulse vocabulary, anti-patterns | `RaBbLE.md` (RaBbLE-lang) |

### Archive

| Document | Purpose |
|---|---|
| [`DistilledNonZense.md`](DistilledNonZense.md) | Full entropy archive — deprecated arcs (greetd, `aesthetics/`), raw BaBbLE notes, AI stack full detail (for Phase 2 promotion), Contributing guide draft, journal entries |

### Assets

| Path | Contents |
|---|---|
| `components/RaBbLE.svg` | RaBbLE logo / SVG asset |

---

## Reading Order

**New to the project:**
1. `RaBbLE.md` — understand what this is
2. `RaBbLE-Palette.md` — understand the visual identity
3. `Architecture.md` — understand the structure
4. `GettingStarted.md` — deploy it

**Working on the boot chain:**
`BootFlow.md` → `Theming.md` → `Hardware.md` → `KnownIssues.md`

**Adding a new machine:**
`AddingTargets.md` → `Architecture.md` (HiDPI Variable Flow) → `Hardware.md`

**Planning phase work:**
`RaBbLE-Roadmap.md` → `KnownIssues.md` → `CommitStyle.md`

**Debugging a broken system:**
`KnownIssues.md` → `BootFlow.md` (troubleshooting table) → `Bootstrap.md` (recovery mode)

---

## Palette At a Glance

> Full reference: `RaBbLE-Palette.md`

```
#ff2d78  Hot Magenta    — primary neon, RaBbLE signature
#00f5ff  Electric Cyan  — secondary neon
#bf5fff  Soft Violet    — tertiary neon
#ff79c6  Outrun Pink    — grid/horizon
#0a0010  Deep Void      — background
#e8e6f0  Signal White   — primary text
```

---

## Commit Convention

```
[impulse] ~ [organ] >> [revelation] // %SYSTEM_STATE%

spark ~ entity-core >> new capability manifested
harmonize ~ shell-spirit >> entropy reduced
mend ~ boot-chain >> logic-fracture healed
transcribe ~ grimoire >> lore updated
ingest ~ belly >> dependency devoured
glitch ~ %0xINT% >> high entropy event handled
```

Full reference: `CommitStyle.md`

---

```
transcribe ~ grimoire >> index crystallized // %GRIMOIRE_LOCKED%
```
