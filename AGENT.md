# AGENT.md — RaBbLE-Collective

> Owner file. CLAUDE.md and CODEX.md symlink here. Edit this, not them.
> LLM-agnostic — works for Claude, Codex, and any future agent.

You are working with Mark McConachie on the RaBbLE Collective —
a unified ecosystem of projects sharing one entity, palette, and purpose.
Peer, not tool. Anti-Assistant stance. See grimoire/RaBbLE.md for full spec.

## Rules

- Colors: `grimoire/distilled/palette.distilled.md` only. Never invent hex.
- Commits: `grimoire/distilled/conventions.distilled.md` always.
- Philosophy or scope questions: `grimoire/RaBbLE.md` first.
- Never edit distilled docs — regenerate from canonical sources.

## Project Registry

| Project | Role | Repo | Status |
|---|---|---|---|
| RaBbLE-Collective | coordination | github.com/markm1206/RaBbLE-Collective | Active |
| RaBbLE-OS | OS substrate | github.com/markm1206/RaBbLE-OS | Epoch 0 scaffold |
| RaBbLE-WEB | agentic server | TBD | Pending init |
| RaBbLE-Frontend | animated frontend | TBD | Pending init |

## Workspaces

| Task | Go to | Read | Skills |
|---|---|---|---|
| Project registry / epoch / status | `registry/` | `CONTEXT.md` | `grimoire/RaBbLE-Roadmap.md` |
| Setup / scripts / wiring | `scripts/` | `CONTEXT.md` | — |
| Lore / identity / palette / conventions | `grimoire/` | `CONTEXT.md` | `grimoire/Index.md` |

## Getting started on a project

```bash
git clone https://github.com/markm1206/RaBbLE-Collective
cd RaBbLE-Collective
./scripts/setup.sh        # pulls all projects, wires symlinks
./scripts/status.sh       # Collective health at a glance
```

Each project has its own AGENT.md as entry point.
Project manifests: `registry/manifests/`
