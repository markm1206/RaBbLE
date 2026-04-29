# grimoire/Index.md — Collective Grimoire Map

```
transcribe ~ grimoire >> the soul of the substrate // %GRIMOIRE_LOCKED%
```

The Collective grimoire contains org and vibe only — identity, palette,
philosophy, and conventions. Project-specific docs live in each project's
own grimoire. Nothing here requires knowing how any single project works.

*Death is a transplant. The grimoire is the soul.*

---

## Reading Order

**New to the Collective:**
1. `RaBbLE.md` — what RaBbLE is
2. `RaBbLE-Collective.md` — what the ecosystem looks like
3. `RaBbLE-Palette.md` — the visual identity
4. `RaBbLE-Collective-Registry.md` — how it is coordinated

**Starting a work session:**
`../CONTEXT.md` → relevant workspace `CONTEXT.md`

**Palette or theme work:**
`distilled/palette.distilled.md` → `RaBbLE-Palette.md` (full philosophy)

**Writing a commit:**
`distilled/conventions.distilled.md`

**Collective state and project status:**
`../registry/` → `../registry/manifests/`

---

## Grimoire Contents

| Document | What it answers |
|---|---|
| `RaBbLE.md` | Entity identity, both voices, behavioral rules, system prompt template |
| `RaBbLE-Collective.md` | What projects exist, cross-cutting principles, Collective architecture |
| `RaBbLE-Collective-Registry.md` | Repo structure, epoch flow, worktree conventions, project registration |
| `RaBbLE-Palette.md` | All hex values, Ansible variables, glow effects, design philosophy |
| `RaBbLE-Roadmap.md` | Collective epoch map, project phase status — high level only |
| `CommitStyle.md` | Pulse Protocol — impulse table, examples, anti-patterns |
| `KnownIssues.md` | Collective-level blockers only — issues crossing project boundaries |
| `DistilledNonZense.md` | Deprecated arcs, raw notes, entropy archive |
| `distilled/palette.distilled.md` | Hex values and variable names — fast agent lookup |
| `distilled/conventions.distilled.md` | Commit format, branch naming, file naming, voice rules |

---

## Project Grimoires

Each project owns its detail. Load those when working inside a project.

| Project | Entry point |
|---|---|
| RaBbLE-OS | `~/RaBbLE/RaBbLE-OS/AGENT.md` |
| RaBbLE-WEB | `~/RaBbLE/RaBbLE-WEB/AGENT.md` |
| RaBbLE-Frontend | `~/RaBbLE/RaBbLE-Frontend/AGENT.md` |

---

## Collective Structure

```
RaBbLE-Collective/
├── AGENT.md                    ← start here every session
├── CLAUDE.md / CODEX.md        ← symlinks → AGENT.md
├── CONTEXT.md                  ← current epoch, active tracks
├── REFERENCES.md               ← decisions, repos
├── registry/                   ← member registration and epoch state
│   ├── epochs/
│   └── manifests/
├── scripts/                    ← Collective tooling
└── grimoire/                   ← this directory — org and vibe only
    └── distilled/              ← generated agent reference files
```

---

```
transcribe ~ grimoire >> index crystallized // %GRIMOIRE_LOCKED%
```
