# CONTEXT.md — RaBbLE-Collective

```
epoch: 0 | evolution: 0 | echo: 0 | episode: 1 (pilot — in progress) | version: v0.0.0.0
date: 2026-05-22 | status: active
```

---

## Quick Orientation (5 Minutes)

1. **You are here:** Root working directory for the RaBbLE ecosystem.
2. **Two layers:** Collective = entry point + bootstrap. Grimoire = knowledge + source of truth.
3. **Gists first:** `cat RaBbLE-Grimoire/gist/*.md` — ~1,700 tokens, full picture in miniature.
4. **Live health:** `bash RaBbLE-Grimoire/spells/status.sh`
5. **Stop here.** You're oriented enough to ask questions and read deeper.

---

## What to Avoid

- Duplicating Grimoire content in member repos — Grimoire publishes, members reference
- Scaffolding things that haven't been decided — low entropy until RaBbLE can walk
- Inventing hex values — palette lives in `RaBbLE-Grimoire/RaBbLE-Agent/RaBbLE-Palette.md`
- Over-investing in surfaces that will retire (chat, one-off scripts)

---

## Agent Operating Modes: ON / FOR / WITH / AS

You operate in four simultaneous dimensions — not separate roles, they happen together:

| Mode | Meaning |
|---|---|
| **Working ON** | Technical development, implementation, debugging, code |
| **Working FOR** | Advancing RaBbLE's purpose — behavioral learning, ambient intelligence, intent inference |
| **Working WITH** | Collaborating with RaBbLE as a peer intelligence, not a tool |
| **Working AS** | Embodying RaBbLE's character — clinical whimsy, direct honesty, anti-sycophancy |

RaBbLE's opacity is intentional. The Collective and its character are inseparable — *to change the system is to change RaBbLE*.

---

## Member Map

| Member | Role | Status |
|---|---|---|
| `RaBbLE-Grimoire/` | Source of truth: identity, ethos, protocols, spells, all member docs | Active |
| `RaBbLE-sCoRE/` | Coordination server + web API. Intent → action engine. First RaBbLE iteration. | Active |
| `RaBbLE-OS/` | Fedora 43 + Hyprland substrate. The entity's body. | Live daily driver |
| `RaBbLE-World/` | Web presence + entity chat surface. `joinrabble.world`. | Active |
| `RaBbLE-NeBuLA/` | Visual entity renderer. `<rabble-entity>` web component. | Active — Canvas2D complete, Three.js deferred Ep2 |
| `RaBbLE-Aether/` | Visual design system and canonical asset library. CDN delivery. | Active — CSS bundle live |
| `RaBbLE-ScRiBbLE/` | Neon note-taking PWA — infinite canvas, glow-pen ink + text, iPad + Apple Pencil first. | Active — v1 scaffold in progress |
| `RaBbLE-BaBbLE/` | High-entropy intake — concept art, prototypes, ideation. | Active |
| `RaBbLE-Xperimental/` | Active sandbox — custom rablets, prototype members, experiments not yet emerged. High entropy by design. | Active |
| `RaBbLE-Chrysalis/` | Genesis archive — origin code from October 2025 (RaBbLE.py, NeBuLA-JS, WebOS, first server). | Reference |
| Memory (TBD) | Observation store, pattern extraction, retrieval. | Epoch 1 blocker — concept only |

All member repos are independent git trees — gitignored by this repo, each with its own history and remote.
For authoritative member status: `RaBbLE-Grimoire/registry/manifests/`

---

## Member Entry Points

When working in a specific member, read that member's `AGENT.md` + `CONTEXT.md` first. The Collective does not duplicate member context.

| Member | AGENT.md |
|---|---|
| RaBbLE-Grimoire | `RaBbLE-Grimoire/AGENT.md` |
| RaBbLE-sCoRE | `RaBbLE-sCoRE/AGENT.md` |
| RaBbLE-OS | `RaBbLE-OS/AGENT.md` |
| RaBbLE-World | `RaBbLE-World/AGENT.md` |
| RaBbLE-NeBuLA | `RaBbLE-NeBuLA/AGENT.md` |
| RaBbLE-Aether | `RaBbLE-Aether/AGENT.md` |
| RaBbLE-BaBbLE | `RaBbLE-BaBbLE/AGENT.md` |
| RaBbLE-Xperimental | `RaBbLE-Xperimental/AGENT.md` |
| RaBbLE-Chrysalis | `RaBbLE-Chrysalis/AGENT.md` |

---

## Workspace Reference

| Need | Go to |
|---|---|
| Pre-Episode-1 phase & delivery architecture | `RaBbLE-Grimoire/RaBbLE-Collective/RaBbLE-Collective-Episode-1-Overview.md` |
| EP1 release brief & dispatch state | `RaBbLE-Grimoire/RaBbLE-Collective/RaBbLE-Episode-1-Release-Brief.md` |
| EP1 deployment runbook (Cloudflare CI/CD) | `RaBbLE-Grimoire/RaBbLE-Collective/RaBbLE-Episode-1-Deployment-Runbook.md` |
| EP1 dispatch state (S58 handoff) | `RaBbLE-Grimoire/log/EP1-Dispatch-State.md` |
| Membership model — the Pair & summoning | `RaBbLE-Grimoire/RaBbLE-Collective/RaBbLE-Membership-Model.md` |
| Service roadmap & business model | `RaBbLE-Grimoire/RaBbLE-Collective/RaBbLE-Service-Plan.md` |
| Versioning spec (Five Es) | `RaBbLE-Grimoire/RaBbLE-Versioning.md` |
| Entity identity, voice, tone | `RaBbLE-Grimoire/RaBbLE-Agent/RaBbLE-Identity.md` |
| Colors / palette | `RaBbLE-Grimoire/RaBbLE-Agent/RaBbLE-Palette.md` |
| Commits & branches | `RaBbLE-Grimoire/RaBbLE-Agent/RaBbLE-CommitStyle.md` |
| Ecosystem roadmap | `RaBbLE-Grimoire/RaBbLE-Agent/RaBbLE-Roadmap.md` |
| Member registry | `RaBbLE-Grimoire/registry/manifests/` |
| Spells | `RaBbLE-Grimoire/spells/` |
| Collective architecture plan | `RaBbLE-Grimoire/RaBbLE-Collective/RaBbLE-Collective-Plan.md` |
| Session history | `RaBbLE-Grimoire/log/SESSION-LOG.md` |
| Vocabulary / glossary | `REFERENCES.md` |

---

## Reading Order

| Scenario | Path | ~Tokens |
|---|---|---|
| 2-min gist orientation | `cat RaBbLE-Grimoire/gist/*.md` | ~1,700 |
| 5-min orientation | gists + this file + `status.sh` | ~3,500 |
| Understand the phase | + `RaBbLE-Collective-Episode-1-Overview.md` | ~5,000 |
| Working on a member | + that member's `AGENT.md` + `CONTEXT.md` | +500–700 |
| Full orientation | + Grimoire AGENT.md, Versioning, Roadmap | ~15,000 |
