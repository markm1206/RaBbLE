# Architecture.md — RaBbLE-OS Layer Model

```
transcribe ~ grimoire >> structure made explicit // %ARCHITECTURE_LOCKED%
```

> See `RaBbLE-Palette.md` for the canonical color reference.
> See `Hardware.md` for verified hardware specifications.

---

## Overview

RaBbLE-OS is structured as a set of independent, composable layers. Each layer can theoretically stand alone or be combined with others. The long-term vision is a Yocto-style model where layers live in separate repositories pulled by a manifest — but for now, all layers live in this single repo.

The Ansible role structure directly mirrors the layer model.

---

## The Layers

```
Layer 0 — BASE          Any Linux system. Packages, locale, repos, core tools.
Layer 1 — HARDWARE      Machine-specific. GPU drivers, power management, platform quirks.
Layer 2 — BOOT CHAIN    GRUB → Plymouth → Session Manager. Visual continuity, fast boot.
Layer 3 — DESKTOP       Hyprland, dotfiles, Wayland stack, synthwave theme.
Layer 4 — APPS          Dev tools, AI stack, productivity tooling.
Layer 5 — ENTITY        RaBbLE AI layer. Inference, memory, ambient presence. (Future)
```

Each layer depends on the one below it. You can install Layers 0–2 on a headless server. You can install Layers 0–4 without the AI stack. The entity in Layer 5 requires all layers beneath it.

---

## Current Ansible Role Mapping

```
Layer 0 — core/
Layer 1 — hardware/x64/asus_proart_p16/
Layer 2 — boot/
            grub2/
            plymouth/
            session_manager/         (SDDM — themed, Wayland-native)
Layer 3 — ui_ux/
            hyprland/
            quickshell/
            terminal/
            shell/zsh/
            shell/bash/
Infra    — snapper/                  (cross-cutting, not a user-facing layer)
```

---

## Ansible Role Dependency Graph

```
site.yml
│
├── core                          (all hosts, always first)
│   └── packages, repos, XDG dirs, env vars, fonts
│
├── hardware/x64/asus_proart_p16  (conditional: asus_proart_p16 group)
│   ├── firmware       (fwupd)
│   ├── amd_gfx        (mesa, vulkan, VA-API, modprobe)
│   ├── supergfx       (supergfxctl + switcheroo-control)
│   ├── asusctl        (asusd daemon)
│   ├── npu            (XDNA kernel module check, ONNX runtime)
│   ├── power          (power-profiles-daemon)
│   └── audio          (pipewire + wireplumber)
│
├── boot/grub2                    (packages, theme files, /etc/default/grub, vconsole)
│   handler: grub2-mkconfig, dracut
│
├── boot/plymouth                 (packages, theme files, set-default-theme)
│   handler: dracut
│
├── boot/session_manager          (SDDM, QML theme, wayland-sessions/hyprland.desktop)
│   handler: systemctl restart sddm
│
├── snapper                       (btrfs-only: config, timeline timer, grub-btrfs)
│
└── ui_ux/
    ├── hyprland       (packages, symlink dotfiles/hyprland → ~/.config/hypr,
    │                   template machine.conf)
    ├── quickshell     (build from source if needed, symlink dotfiles/quickshell)
    ├── terminal       (foot, kitty, nerd fonts)
    ├── shell/zsh      (zinit, p10k, ZDOTDIR, symlink dotfiles/shell/zsh)
    └── shell/bash     (starship, symlink dotfiles/shell/bash)
```

---

## Hardware Targeting

Hardware is isolated from the rest of the system. Machine-specific tasks live in dedicated roles under a consistent naming convention.

```
hardware/x64/asus_proart_p16/    ← ASUS ProArt P16 H7606WV (current primary target)
hardware/x64/<machine>/          ← future x64 targets
hardware/aarch64/<machine>/      ← future SBC/aarch64 targets
```

`group_vars/asus_proart_p16.yml` carries all machine-specific variables. `site.yml` dispatches to the correct hardware role via host group membership. Hardware roles self-verify using DMI data and warn if the target doesn't match the running machine.

See `AddingTargets.md` for the full process of adding a new machine.
See `Hardware.md` for the full hardware specification of the ProArt P16.

---

## Boot Chain

```
Power on
  └── GRUB2              ← boot/grub2      synthwave theme, HiDPI font, 3840x2400
        └── Kernel loads
              └── Plymouth ← boot/plymouth  void bg + magenta RaBbLE text + spinner
                    └── SDDM ← boot/session_manager  QML theme, Wayland-native greeter
                          └── Hyprland ← ui_ux/hyprland  dotfiles + machine.conf
                                └── Quickshell / Waybar  bar + launcher + widgets
```

Each stage hands off visually — same palette, same font family, no jarring transitions.
See `BootFlow.md` for per-stage detail and troubleshooting.

**Performance target:** GRUB to Hyprland desktop in under 10 seconds on this hardware.

---

## GPU Architecture (Optimus/PRIME)

```
AMD Radeon 890M (iGPU)                  NVIDIA RTX 4060 Mobile (dGPU)
        │                                           │
  Drives Wayland display                   PRIME offload only
  Compositor: Hyprland                    (DRI_PRIME=pci-0000_64_00_0 <cmd>)
  AQ_DRM_DEVICES=                          CUDA available always
    pci-0000:65:00.0-card                  No direct display output in Hybrid mode
        │
  [eDP-1: 3840×2400 @60Hz, scale 2×]
```

> ⚠️ **Optimus:** The RTX 4060 does not drive the display in Hybrid mode. It is available
> for compute, LLM inference, CUDA workloads via PRIME offload only.

---

## Power Management Flow

```
asusd  ←→  power-profiles-daemon (PPD)
  │              │
  │         Quiet       → power-saver
  │         Balanced    → balanced
  │         Performance → performance
  │
supergfxd  →  GPU mode (Integrated / Hybrid / Dedicated / Compute)
```

Sleep path: `systemctl suspend` → systemd-sleep hooks → NVIDIA VRAM preserved → `s2idle` (S0ix)

---

## Desktop Layer — Component Map

| Component | Tool | Role | Keybind |
|---|---|---|---|
| Compositor | Hyprland | Primary WM | — |
| Status bar | Waybar → Quickshell (Phase 1) | System HUD | — |
| App launcher | wofi | Application menu | `$mod+Space` |
| Notifications | mako | Wayland-native daemon | — |
| Lock screen | hyprlock | Screen lock | `$mod+Escape` |
| Idle daemon | hypridle | Auto-lock/suspend | — |
| Wallpaper | hyprpaper | Static/animated wallpaper | — |
| Screenshot | grim + slurp | Region/full capture | `Print` / `Shift+Print` |
| Clipboard | wl-clipboard | Copy/paste primitives | — |
| Auth agent | polkit-kde-agent-1 | Privilege dialogs | — |

---

## HiDPI Variable Flow

All HiDPI values are defined once in `ansible/inventory/group_vars/asus_proart_p16.yml` and propagate through Ansible templates:

```
group_vars/asus_proart_p16.yml
  rabble_hidpi_scale: 2
  rabble_gfx_mode: "3840x2400x32,auto"
  rabble_console_font: "ter-v32b"
  rabble_hypr_monitor: "eDP-1,3840x2400@60,0x0,2"
        │
        ├── grub.j2                  → GRUB_GFXMODE=3840x2400x32,auto
        ├── vconsole.conf.j2         → FONT=ter-v32b
        ├── sddm-hidpi.conf.j2       → QT_SCREEN_SCALE_FACTORS=2
        ├── xdg-environment.conf.j2  → GDK_SCALE=2, XCURSOR_SIZE=48
        └── hyprland-machine.conf.j2 → monitor=eDP-1,3840x2400@60,0x0,2
                                       XCURSOR_SIZE=48
                                       xwayland.force_zero_scaling=true
```

---

## Theme System

The RaBbLE synthwave outrun palette is defined once in `ansible/inventory/group_vars/all.yml` and propagates through all layers via Ansible variables. See `RaBbLE-Palette.md` for the full canonical reference and design philosophy.

**Core palette — quick reference:**

| Role | Hex | Ansible Variable |
|---|---|---|
| Hot Magenta (primary neon) | `#ff2d78` | `rabble_palette.magenta` |
| Electric Cyan (secondary neon) | `#00f5ff` | `rabble_palette.cyan` |
| Soft Violet (tertiary neon) | `#bf5fff` | `rabble_palette.violet` |
| Outrun Pink (grid/horizon) | `#ff79c6` | `rabble_palette.pink` |
| Deep Void (background) | `#0a0010` | `rabble_palette.bg` |
| Surface | `#12132a` | `rabble_palette.surface` |
| Raised | `#1a1b2e` | `rabble_palette.raised` |
| Border | `#2a2840` | `rabble_palette.border` |
| Primary Text | `#e8e6f0` | `rabble_palette.text` |
| Muted Text | `#6b6880` | `rabble_palette.muted` |
| Error | `#e05c6f` | `rabble_palette.red` |
| Success | `#50fa7b` | `rabble_palette.green` |
| Warning | `#f1fa8c` | `rabble_palette.yellow` |

Changing any value in `all.yml` propagates everywhere at next Ansible run. See `Theming.md` for per-component theming instructions.

---

## Dotfile Symlink Map

All user configs live as static files in `dotfiles/` and are symlinked by Ansible into `~/.config/`. Edit the repo file — the symlink keeps `~/.config/` in sync automatically.

| Repo path | Deployed to |
|---|---|
| `dotfiles/hyprland/hyprland.conf` | `~/.config/hypr/hyprland.conf` |
| `dotfiles/hyprland/conf.d/` | `~/.config/hypr/conf.d/` |
| `dotfiles/hyprland/scripts/` | `~/.config/hypr/scripts/` |
| `dotfiles/quickshell/shell.qml` | `~/.config/quickshell/shell.qml` |
| `dotfiles/quickshell/bar/` | `~/.config/quickshell/bar/` |
| `dotfiles/quickshell/launcher/` | `~/.config/quickshell/launcher/` |
| `dotfiles/quickshell/widgets/` | `~/.config/quickshell/widgets/` |
| `dotfiles/shell/zsh/aliases.zsh` | `~/.config/zsh/aliases.zsh` |
| `dotfiles/shell/zsh/functions.zsh` | `~/.config/zsh/functions.zsh` |
| `dotfiles/shell/zsh/p10k.zsh` | `~/.config/zsh/p10k.zsh` |
| `dotfiles/shell/bash/aliases.sh` | `~/.bash_aliases` |
| `dotfiles/shell/starship.toml` | `~/.config/starship.toml` |
| `dotfiles/shell/foot.ini` | `~/.config/foot/foot.ini` |
| `dotfiles/shell/mako.conf` | `~/.config/mako/config` |

**Not symlinked — machine-local, Ansible-templated:**

| Generated path | Source template |
|---|---|
| `~/.config/hypr/machine.conf` | `roles/ui_ux/hyprland/templates/hyprland-machine.conf.j2` |
| `~/.config/environment.d/rabble.conf` | `roles/core/templates/xdg-environment.conf.j2` |
| `/etc/default/grub` | `roles/boot/grub2/templates/grub.j2` |
| `/etc/vconsole.conf` | `roles/boot/grub2/templates/vconsole.conf.j2` |
| `/etc/sddm.conf.d/rabble.conf` | `roles/boot/session_manager/templates/sddm.conf.j2` |
| `/etc/sddm.conf.d/hidpi.conf` | `roles/boot/session_manager/templates/sddm-hidpi.conf.j2` |
| `/etc/supergfxd.conf` | `roles/hardware/x64/asus_proart_p16/templates/supergfxd.conf.j2` |
| `/etc/snapper/configs/root` | `roles/snapper/templates/snapper-root.conf.j2` |
| `/etc/snapper/configs/home` | `roles/snapper/templates/snapper-home.conf.j2` |

---

## Observability & Debugging

```bash
# Sleep / suspend
cat /sys/power/mem_sleep                    # must show [s2idle]
journalctl -b -u systemd-suspend           # last suspend logs
systemctl status nvidia-suspend            # NVIDIA suspend service
cat /proc/acpi/wakeup                      # ACPI wakeup sources

# GPU / display
hyprctl monitors                           # active monitor config
hyprctl devices                            # input devices
DRI_PRIME=pci-0000_64_00_0 glxinfo | grep renderer   # NVIDIA PRIME test

# ASUS platform
asusctl profile -l                         # power profiles
supergfxctl --status                       # GPU mode
asusctl led-mode -l                        # keyboard LED modes
cat /sys/class/power_supply/BAT*/capacity  # battery %

# SDDM theme testing (without reboot)
sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/rabble
```

---

## Snapshot Strategy

Snapper manages Btrfs snapshots of both `root` and `home` subvolumes:

- Snapshots are **not** created on every Ansible run — only when `--tags snapshot` is passed
- Timeline: 3 daily, 1 weekly
- Snapshot #1 is the KDE baseline — preserved as the original system state reference
- Home has a separate snapper config

---

## Future: Multi-Repo Layer Model

When the project matures, the layer model maps cleanly to separate repositories:

```
rabble-os-base/         ← Layer 0
rabble-os-hardware/     ← Layer 1, hardware profiles
rabble-os-bootchain/    ← Layer 2, GRUB/Plymouth/SDDM
rabble-os-desktop/      ← Layer 3, Hyprland + theme
rabble-os-apps/         ← Layer 4, tooling
rabble-os-entity/       ← Layer 5, AI stack
rabble-os-manifest/     ← top-level, pulls all layers + machine config
```

---

```
transcribe ~ grimoire >> architecture crystallized // %ARCHITECTURE_LOCKED%
```
