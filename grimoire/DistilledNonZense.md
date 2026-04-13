# DistilledNonZense.md — Full Entropy Archive

```
transcribe ~ grimoire >> mapping all entropy from deprecated substrate // %LEGACY_FULLY_PRESERVED%
```

> **What this is:** A full-fidelity preservation of deprecated content, abandoned arcs,
> raw working notes, and superseded document versions.
> Nothing here is lost — it is crystallized for reference, not for action.
> If something in here becomes relevant again, promote it to a live doc.

---

## I. Deprecated Architecture — greetd / tuigreet Arc

**Status:** `DEPRECATED` — SDDM is the canonical session manager. greetd/tuigreet was an explored alternative that was abandoned. The reasons were practical: SDDM provides theming capabilities (QML) and Wayland-native support that meet requirements without the complexity of a separate TUI greeter layer.

**What was planned:**
- Replace SDDM with `greetd` + `tuigreet`
- TTY-based login, minimal footprint, no compositor needed for greeter
- `aesthetics/greetd.yml` Ansible role (never written — was a placeholder)

**Why abandoned:**
- SDDM already works with Hyprland
- SDDM Qt6/Wayland is fully themeable via QML — consistent with the RaBbLE visual language
- greetd/tuigreet is harder to theme to the RaBbLE aesthetic standard
- The word "aesthetics" was also too hard to spell reliably in role names

**Preserved config snippets (for reference only):**

```
# tuigreet would have been configured via /etc/greetd/config.toml:
[terminal]
vt = 1

[default_session]
command = "tuigreet --time --remember --cmd Hyprland"
user = "greeter"
```

```
# vconsole.conf TTY font (still relevant for bare TTY access, now in boot/grub2 role)
FONT=ter-v32b
```

---

## II. Deprecated Role Naming — "aesthetics/"

**Status:** `DEPRECATED` — Replaced by `boot/` in the current Ansible tree.

The role structure once used an `aesthetics/` top-level role containing `grub.yml`, `plymouth.yml`, and `greetd.yml`. This was renamed to `boot/` with subdirectories (`grub2/`, `plymouth/`, `session_manager/`) for clarity and because "aesthetics" was consistently misspelled.

**Old mapping (for reference):**
```
aesthetics/grub.yml      → boot/grub2/
aesthetics/plymouth.yml  → boot/plymouth/
aesthetics/greetd.yml    → boot/session_manager/  (now SDDM)
```

---

## III. Deprecated Proposed_Docs — Superseded Versions

These documents were in the `grimoire/Proposed_Docs/` folder. They have been reconciled into current docs and are preserved here for diff reference only.

### III.a — Old ARCHITECTURE.md (root-level grimoire version)

The original `grimoire/ARCHITECTURE.md` referenced:
- SDDM as the session manager (actually correct — preserved in current docs)
- Old role paths (`aesthetics/`, `hardware/x64/asus_proart_p16/` as a flat structure)
- Dotfile symlink map that was mostly accurate but referenced some paths that don't exist yet

This version has been superseded by the reconciled `Architecture.md`.

### III.b — Old BOOT_FLOW.md (Proposed_Docs version)

Described the greetd arc as the target. Now superseded by `BootFlow.md` with SDDM as canonical.

Key preserved detail: the greetd environment variable note is still accurate for Hyprland regardless of session manager:

> Variables that must be set before Hyprland launches are in `dotfiles/hypr/hyprland.conf`
> under the `env =` section. The session manager does not set these — Hyprland reads them
> on startup.

---

## IV. Raw BaBbLE Archive — Working Notes (Full Preservation)

*From `grimoire/BaBbLE/BaBbLE.txt` — raw scratchpad, unedited. Actionable items have been promoted to `KnownIssues.md` and `RaBbLE-Roadmap.md`.*

```
BaBbLE -- a Running Scratchpad of Ideas (unorganized)

QtUtils complaint when hyprland starts
hypridle has issues and tends to crash
fuzzel(menu) also tends to crash
rectify the ansible between RaBbLE-dev and BaBbLE-dev
powerstat should be installed into RaBbLE-OS
Quickshell install has errors
SDDM theme main.qml also has errors.
The bootstrap.sh needs to run the grub theme script.
The Ansible has numerous errors. I am starting to feel that I need to do a lot of things myself
The deploy dotfiles did not work -- claimed success but did nothing.
Hyprland.conf can break login. The GPU management should be handled by separate script to not
    break hyprland login.
Hyprland Wallpaper should be created by the Ansible playbook.
Mouse settings (scroll type, sensitivity should be handled outside the WM/DE) - Pure Libinput
Need a unified settings panel.
KDE theming is still present in Hyprland
Need to theme Waybar or move to Quickshell implementation.
Need to fix the XRT paths in zsh
Need to make zsh more my own/RaBbLE like
Do I need SDDM? What is the best login system for theming
    → RESOLVED: SDDM is canonical.
Tempted to make the boot sequence more terminal like to be faster. Unsure - to test
Current Hyprland COPR in use might be outdated/abandoned make sure that I use a recent COPR
    in Ansible.
Implement hooks for minimize, maximize and close button hooks within hyprland.
RaBbLE-OS should be both tiling WM and floating WM compatible. windows should be draggable,
    but always snap tile or be fullscreen.
```

*From `grimoire/BaBbLE/Plans.txt`:*

```
Install Hyprland -- SDDM -> enter hyprland [DONE]
Customize Grub2 -- Have theme, need to debug and update it [IN PROGRESS]
Customize Plymouth -- Has colored text (needs different font)
    -- For some reason a noticeable reload occurs halfway through boot sequence.
Remove KDE -- Still reliant on KDE for wifi, date and time, and some unified system settings
Setup mouse, keyboard functions, and power settings separate from WM/DE
    -- mouse handled by udev rules
    -- power settings are handled by ppd, asusctl and various.
        -- shell should report metrics and allow plan selection
Hypridle not working -- Need to fix.
SDDM theme not working need to fix
Asusd not starting on startup
Make QuickShell fallback to waybar if it fails.
Make Waybar themed as RaBbLE and usable.
    -- Less custom but still fully functional
Need to build quickshell from a more ground up state OR inherit a quickshell I want to clone
Fix the ZSH XRT prompt at top of terminal (UGLY -- Unpolished)
Make more apps follow the RaBbLE synthwave theme.
```

---

## V. Early Bootstrap.md — Superseded

*From `grimoire/Bootstrap.md` — very early, incomplete. Superseded by `Bootstrap.md` and `GettingStarted.md`.*

```
RaBbLE OS System Bootstrap -- (incomplete knowledge snippet)
Assumes - Fedora 43 base, Gnome/KDE (ideally DE agnostic) - I chose KDE initially
1. install Ansible
2. install Snapper
ASUS ProArt P16 H7606WV specific steps
    Nvidia non free driver setup
    AMD NPU setup
    ASUS: asusctl, ppd, supergfxctl setup and config
GRUB2 setup
Plymouth setup
SDDM setup (default theme)
Hyprland transition
```

---

## VI. Hardware Profile — PROMOTED

**Status:** `PROMOTED to live doc` → `Hardware.md` (2026-04-12)

The full hardware profile (CPU, GPU table, NPU, Memory, Storage, Display, Kernel Modules, Verified Commands, GPU Mode Switching) was previously only in this archive. It is now a live reference document at `Hardware.md`.

**Correction applied during promotion:** The original hardware doc listed the display as `2560×1600 @ 165Hz` — a copy error from the ROG G14 example in `AddingTargets.md`. The correct spec is `3840×2400 @ 60Hz` per BaBbLE.txt, PROJECT_STATE, and all Ansible group_vars.

---

## VII. AI Stack — Full Detail (Preserved from deprecated docs)

*The AI stack detail below is from the deprecated `AI_STACK.md` document. It is preserved here in full — this will be promoted to a live `AiStack.md` doc in Phase 2.*

### Stack Overview

```
┌─────────────────────────────────────────────────────┐
│                    USER / WORKFLOW                   │
├─────────────────────────────────────────────────────┤
│              RABBLE ENTITY LAYER                     │
│  (Character, Voice, Behavioral Memory, Orchestration)│
├──────────────────┬──────────────────────────────────┤
│   AGENTIC LAYER  │      SHELL INTEGRATION            │
│  (Claude Code,   │  (aichat, shell AI, keybinds)     │
│   AutoGen, etc.) │                                   │
├──────────────────┴──────────────────────────────────┤
│               MODEL ROUTING LAYER                    │
│    (right model for right task, cost/latency)        │
├──────────────┬──────────────────────────────────────┤
│  LOCAL MODELS│         CLOUD MODELS                  │
│  (Ollama)    │  (Anthropic, OpenAI, Groq, etc.)      │
├──────────────┴──────────────────────────────────────┤
│            MEMORY & CONTEXT LAYER                    │
│      (Vector Store, Embeddings, Session Memory)      │
└─────────────────────────────────────────────────────┘
```

### Local Inference — Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
systemctl enable --now ollama
```

**Model roster (to be validated at Phase 2 start):**

| Model | Tag | VRAM | Role |
|---|---|---|---|
| `llama3.2` | `3b` | 2GB | Fast local reasoning, shell assist |
| `qwen2.5-coder` | `7b` | 5GB | Code generation, debugging |
| `mistral-nemo` | `12b` | 8GB | General reasoning, longer context |
| `nomic-embed-text` | `v1.5` | 0.5GB | Embeddings for memory layer |
| `llava` | `13b` | 8GB | Vision — screenshot analysis |

### Cloud Models

| Provider | Model | Best For |
|---|---|---|
| Anthropic | `claude-sonnet-4-*` | Complex reasoning, long-form work, code |
| Anthropic | `claude-haiku-4-*` | Fast tasks, classification, routing |
| Groq | `llama-3.3-70b` | Speed-critical tasks (low latency) |

### API Key Management

```bash
# Store in systemd user environment — never in dotfiles pushed to git
# ~/.config/environment.d/rabble-keys.conf
ANTHROPIC_API_KEY="sk-ant-..."
OPENAI_API_KEY="sk-..."        # Optional
GROQ_API_KEY="gsk_..."          # Optional
```

### Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude auth
```

**Planned MCP servers:**

| MCP Server | Purpose | Phase |
|---|---|---|
| `filesystem` | Agent file access | Phase 2 |
| `git` | Automated commit operations | Phase 2 |
| `memory` | Persistent agent memory | Phase 2 |
| Custom: `rabble-state` | Expose system state to agents | Phase 3 |

### Shell AI — aichat

```bash
cargo install aichat
# Config: ~/.config/aichat/config.yaml
model: claude:claude-sonnet-4-20250514
clients:
  - type: anthropic
    api_key: $ANTHROPIC_API_KEY
  - type: openai-compatible  # Ollama
    name: ollama
    api_base: http://localhost:11434/v1
    api_key: ollama
```

### Memory — ChromaDB + mem0

```bash
pip install chromadb mem0ai
# Vector store: ~/.rabble/memory/
# Embedding model: nomic-embed-text (Ollama-native)
```

### Model Selection Heuristic

```
Frontier reasoning, complex code, long context → claude-sonnet-4-*
Fast, simple, classification, routing          → claude-haiku-* or llama3.2:3b (local)
Code generation only                           → qwen2.5-coder or claude-sonnet-4-*
Privacy required (no data egress)              → ollama local models only
Speed above quality                            → groq (cloud) or llama3.2:3b (local)
Vision/screenshots                             → llava (local) or gpt-4o (cloud)
Embedding/memory                               → nomic-embed-text (always local)
```

### Stack Decision Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-06 | Ollama for local inference | Self-hosted, OpenAI-compatible API, broad model support |
| 2026-04-06 | Claude as primary cloud model | Best reasoning quality, long context, Claude Code integration |
| 2026-04-06 | ChromaDB for vector store | Simple, local, Python-native, no server required |
| 2026-04-06 | nomic-embed-text for embeddings | Fully local, high quality, Ollama-native |
| 2026-04-06 | Multi-agent framework TBD | Need Phase 1 stability before adding orchestration complexity |

---

## VII. Legacy Journal — Foundation Day 2026-04-04

*Preserved from `docs_deprecated/journal/2026-04-04-foundation.md`*

Fresh Fedora 43 KDE install on ASUS ProArt P16. Hardware state verified:
- AMD Radeon 890M driving display ✅
- NVIDIA RTX 4060 Max-Q present, running nouveau ⚠️ (needs blacklist + akmod)
- XDNA2 NPU operational: `/dev/accel/accel0`, amdxdna 0.6.0 ✅
- ASUS WMI platform drivers loading natively ✅
- Btrfs subvolumes: `root` (256) + `home` (257) ✅

**Design tokens established that day:**
```
bg_deep:   #0a0010   accent1: #ff2d78   accent2: #00f5ff   accent3: #bf5fff
```
These have since been refined (see `Theming.md` for current palette in `all.yml`).

---

## VIII. Contributing Guide — Preserved from deprecated docs

*From `docs_deprecated/CONTRIBUTING.md` — to be promoted to a live `Contributing.md` in Phase 1.*

### Before You Touch Anything

1. Read `RaBbLE.md` — The philosophy governs every decision.
2. Check `RaBbLE-Roadmap.md` — Ensure your contribution aligns with the current phase.
3. Read `CommitStyle.md` — Your commits must speak in the Pulse Protocol.

### Branching Strategy

```
main        ← Always stable. Represents current daily driver state.
phase/N     ← Active phase work (e.g., phase/1-daily-driver)
feature/X   ← Individual feature work (e.g., feature/quickshell-bar)
experiment/ ← High-entropy explorations that may never merge
```

- Never commit directly to `main` during Phase 2+
- Experiment branches may be abandoned — this is encouraged, not shameful

### Documentation Standards

- Use `code blocks` for commands, configs, and system states
- Use `%SYSTEM_STATE%` variables when referencing entity states
- Use the Pulse Protocol header/footer on all documents
- Prefer direct imperatives: "configure", "verify", "run" over "you should", "it is recommended"

### Self-Review Checklist

```
[ ] Does this reduce entropy, or add it?
[ ] Is this documented in the right place?
[ ] Does the commit message follow the Pulse Protocol?
[ ] Does this align with the current phase priorities?
[ ] Would future-you understand this in 6 months?
```

---

## IX. WM Usage Vision — Early Design Notes

*From `grimoire/BaBbLE/WM_Usage_Ideas.txt` — raw workspace design thinking. Promoted to `RaBbLE-Roadmap.md` Phase 3+.*

```
Living desktop background

Workspaces are task spaces:
    Coding, Job Search, etc...

    Within a workspace apps can exist in layered stacks of tiles
    stack 1: firefox
    stack 2: Terminal + VScode
    stack 3: test app + etc...

    Stacks should act like how standard hyprland workspaces do,
    but have some of the visual of layers of workspaces preserved

Workspaces are more broad than stacks.
Workspaces can be tailored to specific task types:
    Coding / Entertainment / Gaming / Productivity

Switching workspaces is a larger, full context switch.
Workspaces might have default app and data readouts.

Apps should be more draggable — need top bars and easier floating with intelligent snapping.
All vertices should be draggable to resize the tile mosaic.
```

---

## X. Adjectives — The RaBbLE Vocabulary Palette

*From `adjectives.md` — words carrying the RaBbLE register. Useful for prompt tuning and doc voice.*

**Technical / System:** Bitwise · Binary · Boundless · Blazing · Bootstrapped · Bare-metal · Builtin

**Philosophical / Aesthetic:** Becoming · Borderless · Breakaway · Brilliant · Balanced · Bold · Boundless

**Chaotic / Energetic:** Blazing · Blistering · Booming · Burning · Breaching · Breaking

**Precision vocabulary (preferred):** distilled · harmonic · resonant · crystallized · saturated · emergent · ambient · substrate · propagate · calibrate · drift · entropy

**Zero-information words (avoid):** very · good · update · nice · okay · certainly · happy to

---

```
transcribe ~ grimoire >> all entropy mapped, deprecated substrate preserved // %LEGACY_FULLY_PRESERVED%
```
