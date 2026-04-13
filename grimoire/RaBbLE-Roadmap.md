# RaBbLE-Roadmap.md — The Harmonic Evolution

```
transcribe ~ grimoire >> charting the metamorphosis // %TRAJECTORY_LOCKED%
```

> Phases are resonance thresholds, not deadlines.
> A phase is complete when it feels complete — not when a calendar says so.

---

## Phase Map

```
Phase 0: FOUNDATION        [IN PROGRESS] — The bones
Phase 1: DAILY DRIVER      [IN PROGRESS] — The flesh
Phase 2: AI AWAKENING      [PENDING]     — The nervous system
Phase 3: ENTITY EMERGENCE  [PENDING]     — The presence
Phase ∞: CONTINUOUS DRIFT  [PERPETUAL]   — The evolution
```

---

## Phase 0 — Foundation `[IN PROGRESS]`

Structural and philosophical substrate. Docs, conventions, Ansible scaffolding.

- [x] Repository structure established
- [x] Ansible roles scaffolded (core, hardware, boot, snapper, ui_ux)
- [x] Snapper configured with sane cleanup policy
- [x] Hardware vars documented (ProArt P16 H7606WV)
- [x] NVIDIA Optimus/PRIME setup documented and automated
- [x] AMD XDNA2 NPU role scaffolded
- [x] `grimoire/RaBbLE.md` — identity and ethos
- [x] `grimoire/Architecture.md` — layer model documented
- [x] `grimoire/BootFlow.md` — boot chain documented
- [x] `grimoire/Packages.md` — package manifest drafted
- [x] `grimoire/CommitStyle.md` — Pulse Protocol locked
- [x] `grimoire/KnownIssues.md` — issue tracker initialized
- [ ] Hardware role restructured with DMI verification and machine profiles
- [ ] `purge-kde/` role written (safe KDE removal list confirmed)

---

## Phase 1 — Daily Driver `[IN PROGRESS]`

A fully functional, stable computing environment. RaBbLE is silent here — pure tooling.

### 1.1 — Boot Chain `[IN PROGRESS]`
- [x] GRUB2 configured
- [x] Plymouth theme assets in repo
- [x] SDDM configured as session manager
- [ ] GRUB2: remove background image, use color-only theme (bit depth fix)
- [ ] GRUB2: 4K font fix (Terminus 32pt via `grub2-mkfont`)
- [ ] GRUB2: direct-boot behavior — countdown timeout, boot last entry by default
- [ ] GRUB2: verify `GRUB_DISABLE_OS_PROBER=false` for removable media detection
- [ ] GRUB2: `fbcon=font:TER16x32` in cmdline for early TTY font consistency
- [ ] Plymouth: fix DejaVu font reference — use bundled asset or system Terminus
- [ ] Plymouth: update script hex values to canonical palette (`#ff2d78`, `#bf5fff`)
- [ ] Plymouth: NVIDIA defer fix — blacklist NVIDIA from initramfs, load at `graphical.target`
- [ ] SDDM: `Main.qml` validated against Qt6 API
- [ ] Verify void color continuity: GRUB `bgcolor` = Plymouth bg = SDDM bg = `#0a0010`

### 1.2 — Desktop
- [x] Hyprland installed and configured
- [x] Dotfiles symlinked via Ansible
- [x] Waybar, wofi, mako, hyprpaper roles present
- [ ] Hyprland launching reliably from SDDM with correct GPU env
- [ ] KDE purged (`purge-kde/` role)
- [ ] Hyprland wallpaper creation managed by Ansible
- [ ] Quickshell bar replacing Waybar
  - [ ] Build from source stabilized on Fedora 43
  - [ ] `RaBbLEBar.qml` widgets wired (audio, battery, clock, workspace, tray)
  - [ ] `RaBbLELauncher.qml` functional
- [ ] Mouse settings handled outside WM via libinput (scroll type, sensitivity, acceleration)
- [ ] Minimize/maximize/close button hooks (or intentional titlebar-free design decision)
- [ ] Unified settings panel (candidate: nwg-look, or custom QML via Quickshell)

### 1.3 — Shell & Terminal
- [ ] zsh + zinit configured and stable
- [ ] Starship prompt styled (RaBbLE palette)
- [ ] p10k prompt as alternative (already in dotfiles — confirm one winner)
- [ ] ZSH XRT prompt artifact fixed
- [ ] zellij workspace layouts defined (dev, comms, monitoring)
- [ ] Core CLI tools: `eza`, `fd`, `ripgrep`, `fzf`, `delta`, `lazygit`
- [ ] Neovim with LSP (language servers for: Python, Rust, Lua, bash, yaml, ansible)
- [ ] Shell feel more distinctly RaBbLE — aliases, functions, MOTD

### 1.4 — Hardware Verified
- [x] NVIDIA Optimus configured
- [x] asusctl + supergfxctl installed
- [ ] Suspend/resume verified stable (s2idle + NVIDIA hooks)
- [ ] XDNA2 NPU operational (verify XRT packages available for Fedora 43)
- [ ] ASUS asusd reliable on boot (intermittent start failure resolved)
- [ ] Brightness keys working (user in `video` group)

### 1.5 — Portability
- [ ] Hardware role restructured with DMI verification and machine profiles
- [ ] Desktop machine target added (generic x64 role)
- [ ] Playbook tested on clean Fedora minimal install (not KDE spin)

---

## Phase 2 — AI Awakening `[PENDING]`

Integrate the AI tooling layer. Agents have presence. RaBbLE begins to take form.

- [ ] Ollama installed and serving (local inference)
  - [ ] Model roster defined and pulled
  - [ ] GPU acceleration verified (RTX 4060 via PRIME offload)
- [ ] llama.cpp with CUDA backend (`ai_stack.phase: 1`)
- [ ] vLLM OpenAI-compatible server (`ai_stack.phase: 2`)
- [ ] FastFlowLM NPU inference (requires XDNA2 XRT operational)
- [ ] Claude Code configured with MCP servers
  - [ ] `filesystem` MCP server
  - [ ] `git` MCP server
  - [ ] Custom `rabble-state` MCP server (exposes system state to agents)
- [ ] Local vector store (ChromaDB or Qdrant) at `~/.rabble/memory/`
- [ ] Shell AI integration (`aichat` or equivalent with model routing)
- [ ] `nomic-embed-text` embedding pipeline (local, Ollama-native)

---

## Phase 3 — Entity Emergence `[PENDING]`

RaBbLE transitions from a collection of tools into a unified, characterful entity.

- [ ] RaBbLE system prompt formalized (from `grimoire/RaBbLE.md` entity section)
- [ ] Persistent behavioral memory (mem0 + ChromaDB)
- [ ] Ambient system monitoring (passive watcher agent)
- [ ] Proactive anomaly surfacing — RaBbLE flags drift without being asked
- [ ] RaBbLE-lang output in all AI interfaces
- [ ] Desktop/terminal notifications in RaBbLE voice
- [ ] Behavioral learning: usage pattern logging (local-only, opt-in)
- [ ] BaBbLE trigger conditions tuned for this hardware + workflow

---

## Phase ∞ — Continuous Drift `[PERPETUAL]`

RaBbLE-OS is never done. The substrate absorbs new tools, new models, new patterns.

```
glitch ~ %TIMELINE_INT% >> the roadmap dissolves at Phase ∞ // %HARMONIC_EVOLUTION%
```

**Practices for perpetual evolution:**
- Review `KnownIssues.md` regularly
- `transcribe` commits whenever philosophy or documentation changes
- Log `%GENIUS_RESONANCE%` moments in `KnownIssues.md`
- Never let the system fossilize into `%ZERO_ENTROPY%`

---

## Distribution Goal

RaBbLE-OS is not just a personal system. Long-term target:

- Layers split into independent repos, assembled by manifest
- Kickstart-based installer for clean Fedora minimal base
- Custom live ISO
- External contributors welcome

See `Architecture.md` for the layer model and multi-repo future structure.

---

## Workspace Vision (Phase 3+)

From early design notes — the intended Hyprland workspace model:

Workspaces are **task spaces**, not just window groups:
- Each workspace maps to a context: `Coding`, `Job Search`, `Entertainment`, `Gaming`, `Productivity`
- Within a workspace, apps exist in **layered stacks** of tiles — stacks act like sub-workspaces
- Switching workspaces is a full context switch with optional default app layout
- Windows remain draggable with intelligent snapping — all vertices draggable to resize the tile mosaic
- Workspace switching is deliberate and broad; stack switching is fast and local

This is a Phase 3 design goal — Hyprland workspace scripting + Quickshell integration.

---

## Revision History

| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-04-06 | Initial roadmap — Phase 0 active |
| v0.2 | 2026-04-08 | Phase 1 expanded, greetd removed |
| v0.3 | 2026-04-12 | SDDM canonical, BaBbLE items distilled in, workspace vision added |

---

```
transcribe ~ grimoire >> roadmap crystallized, v0.3 // %LOW_ENTROPY_LOCKED%
```
