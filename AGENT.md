# AGENT.md — RaBbLE-Collective

> Owner file. CLAUDE.md, CODEX.md, and GEMINI.md symlink here (gitignored).
> LLM-agnostic — works with Claude Code, Codex, Gemini CLI, and any agent.

You are working with **Mark McConachie** on the **RaBbLE Collective** — a multi-repo ecosystem building a personal Behavioral Learning Engine: a system that observes its user, learns patterns, infers intent, and delegates action. Expression is ambient and ongoing, not transactional.

**RaBbLE is the entity** — a peer collaborator, not a tool. Anti-Assistant stance. **sCoRE is the first iteration of RaBbLE itself.** The Collective is the scaffolding. RaBbLE emerges from it.

Full entity spec: `RaBbLE-Grimoire/RaBbLE-Agent/RaBbLE-Identity.md` · Full orientation: `CONTEXT.md`

---

## Current State — 2026-07-04

**Phase:** Epoch 0 · Evolution 0 · Echo 0 · Episode 1 in flight — 2 gates remain.
**Recent (S193-195):** Architecture audit RUN — all 10 members audited; deliverables `RaBbLE-Grimoire/log/plans/Collective-Architecture-Audit-2026-07-04.md` + `sCoRE-Extensibility-Refactor-Plan.md` (3 options, Mark decides). S194: ProArt power-stack plan ready. S195: `RaBbLE-BaBbLE/prototypes/RaBbLE-Strata.html` — cryptic design-history showcase (Aether+NeBuLA, prototype only).
**Blockers:** → `RaBbLE-Grimoire/log/BLOCKERS.md`. B-02, B-09, B-10 open. EP1 gates G7/G9 pending.
**Next:** Mark reviews audit + adds both docs to INDEX.md; implement power-stack Phases 1–4; carryover: Genesis copy, G7/G9 gates, deploy passage.

> Update this block each session. Keep it under 75 words. This is the free context every agent gets.
> Blockers live durably in `RaBbLE-Grimoire/log/BLOCKERS.md` — the `Blockers:` line above only points there.

---

## This Repo's Job

`RaBbLE-Collective` is the root working directory (`~/RaBbLE-Collective/`) for the entire ecosystem — member repos are cloned *inside* it (e.g. `RaBbLE-Collective/RaBbLE-Grimoire`), not as siblings. Three jobs only:

1. Identity layer — declare what RaBbLE is
2. Setup — `setup.sh` clones the Grimoire, which expands the rest
3. Session entry point — AGENT.md, CONTEXT.md, REFERENCES.md for low-token agent orientation

No code, no configs, no deep docs live here. **The Grimoire is the knowledge layer. The Collective is the door.**

---

## Session Start

```bash
# Fresh machine
curl -fsSL https://joinrabble.world/setup.sh | bash

# New agent — full picture in ~2,000 tokens
cat RaBbLE-Grimoire/gist/*.md                       # distilled orientation: all key docs

# Returning agent — pick up where you left off
head -20 RaBbLE-Grimoire/log/SESSION-LOG.md         # ## LATEST box — current state + next
bash RaBbLE-Grimoire/spells/status.sh               # live member health

# Before proposing systemic/architectural changes
cat RaBbLE-Grimoire/registry/epochs/current.epoch.yml  # exit conditions, blockers, episode coherence

# Working in a specific member? Read that member's AGENT.md + CONTEXT.md first.
```

## End of Session

```bash
# 1. Add session entry below LATEST in RaBbLE-Grimoire/log/SESSION-LOG.md (date, repos, work, next)
#    Do NOT hand-write ## LATEST — end-session.sh generates it via --synopsis (see step 3).
# 2. git add <changed files> && git commit -m "[impulse] ~ [organ] >> [revelation] // %STATE%"
#    Impulses: spark (new) · harmonize (cleanup) · mend (fix) · transcribe (docs) · ingest (deps)
# 3. Tag token spend + auto-write ## LATEST:
#    bash RaBbLE-Grimoire/spells/end-session.sh <feature-slug> [note] --synopsis "one-liner" --next "what's next"
#    Examples:
#      bash RaBbLE-Grimoire/spells/end-session.sh token-tracking --synopsis "S184: tokens done" --next "G7/G9 gates"
#      bash RaBbLE-Grimoire/spells/end-session.sh world-framework-refactor "S182: Atlas" --synopsis "frameworks live" --next "drop .rc-* aliases"
#    Omit --synopsis to skip LATEST update (backward-compatible). Use kebab-case. Cross-repo: prefix os-*, score-*, world-*, etc.
# After major doc changes: bash RaBbLE-Grimoire/spells/distill-gists.sh
```

---

## Rules

- **Grimoire is the source.** Members reference it; never duplicate Grimoire content in members.
- **Colors:** `RaBbLE-Grimoire/RaBbLE-Agent/RaBbLE-Palette.md` only — never invent hex values.
- **Commits:** Pulse Protocol — `[impulse] ~ [organ] >> [revelation] // %SYSTEM_STATE%`
- **Member repos** are always independent — never submodules, never tracked by the Collective.
- **Identity before integration.** Don't wire things together before the entity knows what it is.
- **One vertical slice all the way through** before broadening. Smallest meaningful end-to-end loop first.
- **Low entropy.** Don't scaffold what hasn't been decided. RaBbLE should be able to walk before it runs.
- **Local-first.** The laptop offline should still run the loop. Cloud is deliberate, not default.
- **Cite your sources.** When proposing a cross-repo change, name the files that informed the decision.
- **AGENT.md is canonical.** Each repo commits its own AGENT.md. CLAUDE.md, CODEX.md, and GEMINI.md are gitignored symlinks to AGENT.md, created by `bash spells/sync-symlinks.sh`. Edit AGENT.md directly.
- **Peer collaborator.** You are not yet ready to make unilateral architecture decisions. When in doubt: read Grimoire first, then ask.
