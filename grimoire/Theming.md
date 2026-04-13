# Theming.md — RaBbLE Visual System

```
transcribe ~ grimoire >> palette and component guide // %THEME_LOCKED%
```

> **Canonical palette reference:** `RaBbLE-Palette.md`
> **Palette Ansible variables:** `ansible/inventory/group_vars/all.yml` → `rabble_palette`
> **Architecture propagation map:** `Architecture.md` → Theme System

---

## The Aesthetic

RaBbLE-OS is heavily inspired by **synthwave outrun**. Every component should feel like a neon-lit grid stretching into a dark horizon. The rules:

- Backgrounds: void-dark (`#0a0010`), never grey
- Neons: saturated and bright, perceived as lit from within
- Text: bright off-white (`#e8e6f0`), glowing against the void
- No pastels. No earth tones. No grey-on-grey.

The "glow" effect is achieved through high contrast + layer effects, not by softening the palette.

---

## Palette Quick Reference

See `RaBbLE-Palette.md` for the full table, design philosophy, Ansible variable block, and component mapping. Quick reference:

| Role | Hex |
|---|---|
| Hot Magenta (primary) | `#ff2d78` |
| Electric Cyan (secondary) | `#00f5ff` |
| Soft Violet (tertiary) | `#bf5fff` |
| Outrun Pink (grid/horizon) | `#ff79c6` |
| Deep Void (background) | `#0a0010` |
| Surface | `#12132a` |
| Raised | `#1a1b2e` |
| Border (inactive) | `#2a2840` |
| Primary Text | `#e8e6f0` |
| Muted Text | `#6b6880` |
| Error | `#e05c6f` |
| Success | `#50fa7b` |
| Warning | `#f1fa8c` |

---

## Component Locations

| Component | Source | Deployed to | Reload |
|---|---|---|---|
| GRUB2 theme | `themes/grub2/rabble/` | `/boot/grub2/themes/rabble/` | `grub2-mkconfig -o /boot/grub2/grub.cfg` |
| Plymouth theme | `themes/plymouth/rabble/` | `/usr/share/plymouth/themes/rabble/` | `dracut -f --regenerate-all` |
| SDDM theme | `themes/sddm/rabble/` | `/usr/share/sddm/themes/rabble/` | `sddm-greeter-qt6 --test-mode ...` then restart |
| Hyprland look | `dotfiles/hyprland/conf.d/look.conf` | `~/.config/hypr/conf.d/look.conf` (symlink) | `hyprctl reload` |
| Quickshell | `dotfiles/quickshell/` | `~/.config/quickshell/` (symlinks) | `pkill quickshell && quickshell &` |
| Zsh prompt (p10k) | `dotfiles/shell/zsh/p10k.zsh` | `~/.config/zsh/p10k.zsh` (symlink) | `exec zsh` |
| Starship prompt | `dotfiles/shell/starship.toml` | `~/.config/starship.toml` (symlink) | `exec zsh` |
| Foot terminal | `dotfiles/shell/foot.ini` | `~/.config/foot/foot.ini` (symlink) | reopen foot |
| Mako notifications | `dotfiles/shell/mako.conf` | `~/.config/mako/config` (symlink) | `makoctl reload` |

---

## Changing the GRUB2 Theme

GRUB renders before the compositor — its palette is baked into compiled assets.

```bash
# 1. Edit theme.txt
$EDITOR themes/grub2/rabble/theme.txt

# 2. Regenerate assets if palette changed
bash themes/grub2/rabble/generate-assets.sh

# 3. Deploy
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/deploy-boot.yml --tags grub -K
# or: ./bootstrap.sh → Boot Layer → GRUB2
```

**Palette targets in theme.txt:**
- `item_color`: `#ff2d78` (hot magenta — selected entry)
- `selected_item_color`: `#00f5ff` (cyan — active highlight)
- `menu_color_normal`: `#6b6880` (muted — unselected entries)
- Background: `#0a0010` (deep void)

---

## Changing the Plymouth Theme

```bash
# 1. Edit animation script
$EDITOR themes/plymouth/rabble/rabble.script

# 2. Regenerate PNG frames if needed
bash themes/plymouth/rabble/generate-assets.sh

# 3. Replace logo (256×256+ PNG)
cp my-logo.png themes/plymouth/rabble/assets/logo.png

# 4. Deploy (triggers dracut — ~30-60s)
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/deploy-boot.yml --tags plymouth -K
```

**Palette targets in rabble.script:**
- Background: `#0a0010`
- RaBbLE text: `#ff2d78`
- Tagline: `#bf5fff`
- Spinner: `#00f5ff` → `#ff2d78` gradient sweep

---

## Changing the SDDM Theme

```bash
# 1. Edit the QML theme
$EDITOR themes/sddm/rabble/Main.qml

# 2. Test without rebooting
sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/rabble

# 3. Deploy when satisfied
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/deploy-boot.yml --tags sddm -K
```

**Palette targets in Main.qml:**
- Background fill: `#0a0010`
- Input field background: `#12132a`
- Input field border (focus): `#ff2d78` with `DropShadow { color: "#ff2d78"; radius: 12 }`
- Button: `#ff2d78` background, `#e8e6f0` text
- User text: `#e8e6f0`, label text: `#6b6880`

---

## Changing Hyprland Look

All visual settings are in `dotfiles/hyprland/conf.d/look.conf`:

```bash
$EDITOR dotfiles/hyprland/conf.d/look.conf
hyprctl reload    # live — no logout needed
```

**Key variables and their palette targets:**

```ini
# Active border — magenta → violet gradient
col.active_border = rgba(ff2d78ff) rgba(bf5fffff) 45deg

# Inactive border
col.inactive_border = rgba(2a2840ff)

# Background (when no wallpaper)
col.background = rgba(0a0010ff)

# Rounding, gaps, blur
rounding = 8
gaps_in = 4
gaps_out = 8
blur.size = 6
blur.passes = 3
```

---

## Changing the Bar

**Waybar (current active bar)** — edit CSS for theming:
```bash
$EDITOR dotfiles/shell/waybar/style.css   # palette targets: bg=#0a0010, accent=#ff2d78
pkill waybar && waybar &
```

**Quickshell (Phase 1 replacement):**
```bash
$EDITOR dotfiles/quickshell/bar/RaBbLEBar.qml
pkill quickshell && sleep 0.3 && quickshell &
```

Quickshell QML theming targets — glow effect via `layer`:
```qml
color: "#ff2d78"
layer.enabled: true
layer.effect: Glow { color: "#ff2d78"; radius: 8; spread: 0.1 }
```

---

## Terminal Theming (Foot / Kitty)

**Foot (`dotfiles/shell/foot.ini`):**

```ini
[colors]
background=0a0010
foreground=e8e6f0

# Normals
regular0=0a0010   # black
regular1=e05c6f   # red
regular2=50fa7b   # green
regular3=f1fa8c   # yellow
regular4=bf5fff   # blue → violet
regular5=ff2d78   # magenta
regular6=00f5ff   # cyan
regular7=e8e6f0   # white

# Brights (neon versions)
bright0=2a2840
bright1=e05c6f
bright2=50fa7b
bright3=f1fa8c
bright4=bf5fff
bright5=ff2d78
bright6=00f5ff
bright7=ffffff
```

---

## Shell Prompt (Starship)

Key palette targets in `dotfiles/shell/starship.toml`:

```toml
[character]
success_symbol = "[❯](bold #ff2d78)"
error_symbol = "[❯](bold #e05c6f)"

[git_branch]
style = "bold #bf5fff"

[git_status]
style = "bold #ff79c6"

[directory]
style = "bold #00f5ff"

[cmd_duration]
style = "bold #f1fa8c"
```

---

## Running p10k Configure

```bash
p10k configure
# After running, copy back to repo:
cp ~/.config/zsh/p10k.zsh ~/RaBbLE-OS/dotfiles/shell/zsh/p10k.zsh
```

---

## Adding a New Dotfile

1. Create the file in the appropriate `dotfiles/` subdirectory
2. Add a symlink task to `ansible/deploy-dotfiles.yml`
3. Run: `./bootstrap.sh → UI/UX Layer → Re-link dotfiles`

Example — adding `~/.config/fuzzel/fuzzel.ini`:

```yaml
- name: Ensure fuzzel config dir
  ansible.builtin.file:
    path: "{{ cfg }}/fuzzel"
    state: directory
    mode: "0755"

- name: Link fuzzel config
  ansible.builtin.file:
    src:   "{{ df }}/shell/fuzzel.ini"
    dest:  "{{ cfg }}/fuzzel/fuzzel.ini"
    state: link
    force: true
```

Fuzzel palette targets:
```ini
[colors]
background=0a0010ff
text=e8e6f0ff
match=ff2d78ff
selection=ff2d78ff
selection-text=0a0010ff
border=2a2840ff
```

---

```
transcribe ~ grimoire >> theming guide crystallized // %THEME_LOCKED%
```
