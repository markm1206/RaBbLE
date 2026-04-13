# BootFlow.md — From Power On to Desktop

```
transcribe ~ boot-chain >> the sequence made visible // %BOOT_FLOW_LOCKED%
```

> Palette reference: `RaBbLE-Palette.md`
> Hardware details: `Hardware.md`
> Theming guide: `Theming.md`

---

## The Chain

```
BIOS/UEFI
  └── GRUB2          ~0.5s    Synthwave theme, HiDPI font, void bg + magenta text
        └── Kernel   ~1-2s    AMD iGPU init, NVIDIA blacklisted until akmod loads
              └── Plymouth    ~2-3s    Void background + magenta RaBbLE text + cyan spinner
                    └── SDDM            Outrun QML greeter, Wayland-native, HiDPI scaled
                          └── Hyprland  Full Wayland session, AMD 890M compositor
```

**Target:** Power button to usable desktop in under 10 seconds.

Each stage uses the same palette — deep void background (`#0a0010`), hot magenta (`#ff2d78`) as the primary identity color, electric cyan (`#00f5ff`) as the secondary accent. The boot sequence should feel like one continuous performance, not a series of different programs.

---

## GRUB2

**Role:** `ansible/roles/boot/grub2/`

**Hardware note:** Internal display is 3840×2400. Default GRUB font is microscopic at native resolution — see `Hardware.md`.

**Configuration:**
- Font: `ter-v32b` (Terminus, 32pt) — compiled into GRUB via `grub2-mkfont`
- Resolution: `GRUB_GFXMODE=3840x2400x32,auto`
- Timeout: 3 seconds, boots last successful entry
- Theme files: `themes/grub2/rabble/` → `/boot/grub2/themes/rabble/`

**Palette targets:**
- Background: `#0a0010` (deep void)
- Selected entry text: `#ff2d78` (hot magenta)
- Active highlight: `#00f5ff` (electric cyan)
- Unselected entries: `#6b6880` (muted)

**Templates:**
- `grub.j2` → `/etc/default/grub`
- `vconsole.conf.j2` → `/etc/vconsole.conf`

**Handler:** `grub2-mkconfig -o /boot/grub2/grub.cfg` + `dracut -f --regenerate-all`

---

## Plymouth

**Role:** `ansible/roles/boot/plymouth/`

**Plugin:** `script` — full animation control via `.script` files.

**Theme:** `rabble`
- Background: `#0a0010` (deep void — matches GRUB, no visual jump)
- "RaBbLE" text: `#ff2d78` (hot magenta)
- Tagline "Low Entropy. Infinite Resonance.": `#bf5fff` (soft violet)
- Spinner frames: `#00f5ff` → `#ff2d78` sweep
- Theme files: `themes/plymouth/rabble/` → `/usr/share/plymouth/themes/rabble/`

**Rebuild initrd after changes:**
```bash
plymouth-set-default-theme -R rabble
```
The `-R` flag rebuilds initrd automatically. Or via Ansible handler: `dracut -f --regenerate-all`.

**Known issue:** A mid-boot visual reload has been observed. See `KnownIssues.md`.

---

## SDDM

**Role:** `ansible/roles/boot/session_manager/`

**Why SDDM:**
- Qt6/Wayland native — no X11 dependency for the greeter
- Fully themeable via QML — consistent outrun visual language achievable
- Session-agnostic — shows all `.desktop` files in `/usr/share/wayland-sessions/`
- KDE Plasma remains selectable as fallback during transition

**Configuration:**
- Theme: `themes/sddm/rabble/` → `/usr/share/sddm/themes/rabble/`
- `sddm.conf.j2` → `/etc/sddm.conf.d/rabble.conf`
- `sddm-hidpi.conf.j2` → `/etc/sddm.conf.d/hidpi.conf`

**Palette targets in `Main.qml`:**
- Background: `#0a0010`
- Input field background: `#12132a` (surface)
- Input field border (focus): `#ff2d78` + `DropShadow { color: "#ff2d78"; radius: 12 }` (glow)
- Button background: `#ff2d78`, text: `#0a0010`
- User/label text: `#e8e6f0` / `#6b6880`

**Testing without reboot:**
```bash
sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/rabble
```

**Handler:** `systemctl restart sddm`

**Known issue:** `Main.qml` needs Qt6 API validation. See `KnownIssues.md`.

---

## Hyprland

**Role:** `ansible/roles/ui_ux/hyprland/`

**Dotfiles:** `dotfiles/hyprland/` → `~/.config/hypr/` (symlinked)

**GPU configuration:**
- Compositor GPU: AMD Radeon 890M (iGPU, PCI 65:00.0) — deterministic via `AQ_DRM_DEVICES`
- NVIDIA RTX 4060: Optimus offload only — `DRI_PRIME=pci-0000_64_00_0 <cmd>`

**Machine-specific config** (Ansible-templated, not symlinked):
- `~/.config/hypr/machine.conf` ← `hyprland-machine.conf.j2`
- Contains: monitor layout, cursor scale, HiDPI env vars, GPU device path

**Session startup** (`dotfiles/hyprland/conf.d/autostart.conf`):
```
polkit-kde-authentication-agent-1
hyprpaper         ← wallpaper daemon
hypridle          ← idle/lock management
mako              ← notification daemon
waybar            ← status bar (active — Quickshell pending Phase 1)
```

**Palette targets in `look.conf`:**
```ini
col.active_border   = rgba(ff2d78ff) rgba(bf5fffff) 45deg   # magenta → violet gradient
col.inactive_border = rgba(2a2840ff)                         # border inactive
col.background      = rgba(0a0010ff)
```

> ⚠️ **GPU config lives in `machine.conf` only** — never in the main `hyprland.conf`.
> A broken GPU env var in the main conf can prevent SDDM from launching Hyprland at all.

---

## Environment Variables — Propagation

Variables set before Hyprland launches live in two places:
1. `~/.config/environment.d/rabble.conf` — systemd user environment, Ansible-templated from `xdg-environment.conf.j2`
2. `~/.config/hypr/machine.conf` — Hyprland-specific, Ansible-templated from `hyprland-machine.conf.j2`

Critical variables for this hardware:
```bash
AQ_DRM_DEVICES=/dev/dri/by-path/pci-0000:65:00.0-card  # force AMD iGPU
GBM_BACKEND=radeonsi
LIBVA_DRIVER_NAME=radeonsi
QT_QPA_PLATFORM=wayland
XCURSOR_SIZE=48                                          # HiDPI
GDK_SCALE=2
```

---

## Suspend/Resume

**Services** (enabled by hardware Ansible role):
```
nvidia-hibernate.service
nvidia-suspend.service
nvidia-resume.service
```

**Key modprobe params** (`/etc/modprobe.d/`):
```
NVreg_EnableS0ixPowerManagement=1        — s2idle support for Strix Point
NVreg_PreserveVideoMemoryAllocations=1   — survives suspend without corruption
```

**Verify sleep state:**
```bash
cat /sys/power/mem_sleep    # must show [s2idle]
```

AMD Strix Point HX 370 does not support S3 deep sleep. `s2idle` is the only valid mode for this hardware — see `Hardware.md`.

---

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Hyprland won't start | Wrong DRM device path | Check `AQ_DRM_DEVICES` in `machine.conf` matches PCI path |
| Monitor wrong resolution | Config stale | Verify `monitor = eDP-1,3840x2400@60,0x0,2` in `machine.conf` |
| System won't sleep | Wrong sleep state | `cat /sys/power/mem_sleep` — must show `[s2idle]`; check GRUB cmdline |
| Wake from sleep broken | NVIDIA VRAM issue | `systemctl status nvidia-resume`; verify `NVreg_PreserveVideoMemoryAllocations=1` |
| SDDM theme not loading | Qt6 API mismatch | Run `sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/rabble` |
| asusctl errors | asusd not running | `systemctl status asusd`; check `/etc/asusd/` config syntax |
| Brightness keys not working | Not in video group | `sudo usermod -aG video $USER`, relogin |
| GRUB font microscopic | gfxmode / font not configured | Verify `GRUB_GFXMODE` and `GRUB_FONT` in `/etc/default/grub` |
| Plymouth reload mid-boot | dracut / initramfs issue | See `KnownIssues.md` |

---

```
transcribe ~ boot-chain >> flow documented, outrun locked // %BOOT_FLOW_LOCKED%
```
