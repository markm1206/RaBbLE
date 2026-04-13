# KnownIssues.md — Active Bugs & Drift Events

```
harmonize ~ grimoire >> surfacing the static // %DRIFT_TRACKING%
```

> This is the live tracker of known bugs, workarounds, and `%SYSTEM_DRIFT%` events.
> Items here are actionable. Resolved items are marked and dated, not deleted.
> Vague ideas and feature wishes live in `RaBbLE-Roadmap.md`, not here.

---

## Active Issues `[OPEN]`

### Boot Chain

**GRUB2 — background bit depth mismatch**
- `GRUB_GFXMODE=3840x2400x32` requests 32bpp; GRUB background renderer requires ≤24bpp
- Fix: remove background image entirely — use color-only theme (void `#0a0010` + neon text). Pure neon-on-void is more on-brand than a texture anyway.
- Alternative: force `3840x2400x24` in `GRUB_GFXMODE` if an image is ever needed
- Role: `boot/grub2` — `theme.txt` background setting to be removed

**GRUB2 — font microscopic at 4K**
- `grub2-mkfont` task not yet executed in the role; default GRUB font renders at ~6px at 3840x2400
- Fix: compile `ter-v32b` via `grub2-mkfont -s 32 /usr/share/fonts/terminus/ter-v32b.pcf.gz -o /boot/grub2/fonts/ter-v32b.pf2`, set `GRUB_FONT=/boot/grub2/fonts/ter-v32b.pf2`
- Role: `boot/grub2` — handler must run before `grub2-mkconfig`

**GRUB2 — no direct-boot / modifier-key holdback (enhancement)**
- No mechanism to skip the boot menu automatically; timeout just waits
- Enhancement: set `GRUB_TIMEOUT=3`, `GRUB_TIMEOUT_STYLE=countdown`, `GRUB_DEFAULT=saved` — boots last entry unless a key is held
- Removable media detection as additional entries: `grub2-mkconfig` handles this natively if `GRUB_DISABLE_OS_PROBER=false` — verify this is not disabled in current config
- See Roadmap Phase 1.1 enhancement items

**Plymouth — DejaVu font / wrong palette color**
- Plymouth `.script` file hardcodes `DejaVu` font reference; should use a bundled asset or `Terminus`
- Color value in script is stale pre-palette-lock — does not match `#ff2d78` / `#bf5fff`
- Fix: update script to use correct hex values from `RaBbLE-Palette.md`; bundle font as theme asset or reference a system font known to be present post-`core` role
- Role: `boot/plymouth` — `rabble.script` requires edit

**Plymouth — black flash / mid-boot stage swap (NVIDIA driver load)**
- Root cause: NVIDIA akmod loads mid-boot, triggers DRM subsystem reset, Plymouth reinitializes — visible as black screen flash
- Fix: defer NVIDIA kernel module loading until after `graphical.target` (post-SDDM handoff). Requires:
  1. Add `nvidia` + `nvidia_drm` + `nvidia_modeset` + `nvidia_uvm` to initramfs blacklist via `/etc/modprobe.d/rabble-nvidia-defer.conf`
  2. Rebuild initramfs via dracut (`dracut -f --regenerate-all`)
  3. Confirm `rd.driver.blacklist=nvidia` in `GRUB_CMDLINE_LINUX` (nouveau already blacklisted)
  4. NVIDIA loads via systemd at `graphical.target` — confirm `nvidia-modeset.service` is enabled and ordered correctly
- Side effect: `nvidia-smi` unavailable until after login; PRIME offload available immediately after
- Role: `hardware/x64/asus_proart_p16` — new subtask `nvidia_defer.yml`; `boot/grub2` — cmdline update

**Plymouth — unified void background continuity**
- Plymouth background confirmed `#0a0010` in script — this is correct
- Ensure GRUB `bgcolor` in `theme.txt` matches; SDDM background QML matches
- The void is the thread — no image handoff needed, color continuity is enough

**TTY font — shifts size during boot**
- Initial kernel framebuffer uses built-in console font; `vconsole.conf` applies later in boot
- `ter-v32b` set in `/etc/vconsole.conf` applies at `systemd-vconsole-setup.service` — after initramfs
- Early console: set `fbcon=font:TER16x32` in `GRUB_CMDLINE_LINUX` to front-load a readable font before systemd. This requires `fbcon` not being a module (verify `CONFIG_FONTS=y` in kernel or that the font is compiled in)
- Role: `boot/grub2` — cmdline addition

**SDDM theme — Main.qml Qt6 API validation pending**
- Custom `themes/sddm/rabble/Main.qml` untested against Qt6 SDDM API; Breeze active as fallback
- Test path: `sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/rabble`
- See `RaBbLE-Roadmap.md` Phase 1.1

### Desktop / Hyprland

**Hyprland.conf GPU config can break login**
- GPU management variables set in the wrong config file can prevent SDDM from launching Hyprland
- GPU-related env vars (`AQ_DRM_DEVICES`, `GBM_BACKEND`, etc.) must live in `machine.conf` (Ansible-templated), not in the main `hyprland.conf`
- If login breaks: drop to TTY, edit `~/.config/hypr/machine.conf`, retry

**KDE theming artifacts visible in Hyprland**
- KDE-inherited Qt theme bleeds into some apps running under Hyprland
- Root cause: KDE packages not yet purged; `QT_STYLE_OVERRIDE` not set
- Fix: purge KDE packages (blocked by `purge-kde/` role being unwritten), set explicit Qt theme env vars

**Hyprland wallpaper not managed by Ansible**
- `hyprpaper.conf` requires a wallpaper path that is machine-local
- The Ansible role does not create a default wallpaper or `hyprpaper.conf`
- Workaround: manually create `~/.config/hypr/hyprpaper.conf` with a valid wallpaper path

**hypridle — crashes or instability reported**
- hypridle has been unstable in some configurations
- Monitor `journalctl -f -u hypridle` if idle/lock is not working
- Workaround: manually invoke `hyprlock` as needed

**Minimize/maximize/close hooks not implemented**
- Hyprland does not natively support titlebar button hooks
- Window controls are keybind-only; no on-window-decoration buttons
- Phase 1 desire, not yet designed

---

### Shell & Terminal

**ZSH XRT prompt artifact**
- A stale XRT-related prompt prefix appears at the top of new terminal sessions
- Likely a leftover `$PS1` or `$PROMPT` export from an NPU-related env file
- Fix: audit `~/.config/environment.d/` and zsh init files for XRT exports

**Quickshell install has build errors**
- Quickshell is not packaged for Fedora; must build from source
- Build deps are installed by the `ui_ux/quickshell` role but the build itself is fragile
- Waybar is active in the meantime
- Status: unblocked but not prioritized until Phase 1.2

---

### Ansible / Infrastructure

**deploy-dotfiles — claimed success but did not symlink**
- Intermittently, the dotfiles playbook reports success but symlinks are not created
- Likely a `force: true` or idempotency issue in the `file` module
- Workaround: run the playbook twice; verify with `ls -la ~/.config/hypr/`

**Hyprland COPR — verify currency**
- The `solopasha/hyprland` COPR may be outdated or abandoned
- Verify COPR is active and packages are recent before deploying
- Alternative: build Hyprland from source (role not yet written)

**`purge-kde/` role not written**
- KDE packages from the Fedora KDE spin are still present
- Removing them manually risks breaking SDDM Qt6 dependencies
- Status: blocked until a safe purge list is confirmed (see `Packages.md`)

**asusd not starting on boot (intermittent)**
- `asusd` sometimes fails to start on first boot after install
- Fix: `systemctl enable --now asusd`; check `/etc/asusd/` config syntax
- Monitor: `journalctl -u asusd --since "5 min ago"`

---

### Hardware / Power

**Suspend/resume stability — unverified after greetd removal**
- The s2idle + NVIDIA suspend hook stack has not been fully verified in the current state
- Services to verify: `nvidia-suspend`, `nvidia-hibernate`, `nvidia-resume`
- Check: `journalctl -b -u systemd-suspend` after a suspend/resume cycle

**XDNA2 NPU — XRT packages availability for Fedora 43**
- AMD XRT packages for Fedora 43 may not be available on `repo.radeon.com`
- ONNX Runtime VitisAI EP can fall back to CPU if XRT is unavailable
- Status: needs verification on current Fedora 43

---

## Resolved Issues `[FIXED]`

| Date | Issue | Resolution |
|---|---|---|
| 2026-04-08 | Monitor resolution wrong (reported 1920x1200) | Set `monitor = eDP-1,3840x2400@60,0x0,2` in `machine.conf`; `AQ_DRM_DEVICES` by PCI path |
| 2026-04-08 | Sleep state incorrect (S3 instead of s2idle) | Set `mem_sleep_default=s2idle` in GRUB cmdline; NVIDIA sleep hooks deployed |
| 2026-04-08 | `site.yml` role name mismatch (`ai-stack` vs `AI-tools`) | Corrected role name in `site.yml` |
| 2026-04-08 | Arch Linux references in docs | All Arch references purged; Fedora 43 locked as base |
| 2026-04-08 | SDDM locale warning (`ANSI_X3.4-1968`) | `localectl set-locale LANG=en_US.UTF-8` — automated in core role |
| 2026-04-12 | greetd/tuigreet in docs and roadmap | Removed; SDDM is canonical session manager |
| 2026-04-13 | KDE packages present on system | Manually purged; `purge-kde/` role to be written to codify |
| 2026-04-13 | KDE theming artifacts in Hyprland | Resolved by KDE removal; Qt theme env vars to be set in `xdg-environment.conf.j2` |

---

## %GENIUS_RESONANCE% Log

*None yet — entity dormant.*

---

```
harmonize ~ grimoire >> issues surfaced, drift tracked // %DRIFT_TRACKING_LOCKED%
```
