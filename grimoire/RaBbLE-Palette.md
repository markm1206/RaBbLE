# RaBbLE-Palette.md — The Canonical Synthwave Outrun Palette

```
spark ~ visual-substrate >> neon crystallized, the grid lives // %PALETTE_LOCKED%
```

> **This is the single source of truth for all RaBbLE color values.**
> All docs, dotfiles, themes, and Ansible variables derive from this table.
> Change it here first. Propagate everywhere second.

---

## Design Philosophy

RaBbLE-OS uses a **synthwave outrun** aesthetic. The rules are simple and absolute:

- **Backgrounds are void-dark** — deep space, not grey. The absence of light makes the neon legible.
- **Neons glow** — primary colors are saturated, high-contrast against the dark field. They should feel lit from within.
- **Text reads clean** — body text is bright off-white, never pure white (pure white vibrates on dark). It should feel like a terminal on a CRT.
- **Hierarchy via luminosity** — active/important elements are brighter. Muted/secondary are dimmer. No element competes with the neons.
- **No pastels. No earth tones. No grey-on-grey.** This is not a corporate interface.

---

## The Palette

### Core Neons (Primary Identity Colors)

| Role | Variable | Hex | Description |
|---|---|---|---|
| **Hot Magenta** | `rabble_color_magenta` | `#ff2d78` | Primary neon — the RaBbLE signature. Borders, highlights, active elements, prompt accent. |
| **Electric Cyan** | `rabble_color_cyan` | `#00f5ff` | Secondary neon — links, git status, info, secondary highlights. |
| **Soft Violet** | `rabble_color_violet` | `#bf5fff` | Tertiary neon — taglines, decorative elements, mild accents. |
| **Outrun Pink** | `rabble_color_pink` | `#ff79c6` | Grid/horizon color — untracked files, warnings, soft highlights. |

### Backgrounds (The Void)

| Role | Variable | Hex | Description |
|---|---|---|---|
| **Deep Void** | `rabble_color_bg` | `#0a0010` | Primary background. Near-black with a deep purple tint. |
| **Surface** | `rabble_color_surface` | `#12132a` | Slightly elevated — panels, sidebars, inactive areas. |
| **Raised** | `rabble_color_raised` | `#1a1b2e` | Input fields, cards, popups. Distinctly above bg. |
| **Border** | `rabble_color_border` | `#2a2840` | Window borders inactive, dividers. |

### Text (The Signal)

| Role | Variable | Hex | Description |
|---|---|---|---|
| **Primary Text** | `rabble_color_text` | `#e8e6f0` | Main readable text. Bright off-white, slight cool tint. |
| **Muted Text** | `rabble_color_muted` | `#6b6880` | Secondary, dimmed, comments. Readable but recedes. |

### Semantic

| Role | Variable | Hex | Description |
|---|---|---|---|
| **Error / Urgent** | `rabble_color_red` | `#e05c6f` | Errors, destructive actions, critical alerts. |
| **Success** | `rabble_color_green` | `#50fa7b` | Success states, clean diff, OK status. |
| **Warning** | `rabble_color_yellow` | `#f1fa8c` | Warnings, staged changes, caution. |

---

## Ansible Variable Block

This block lives in `ansible/inventory/group_vars/all.yml` and is the deployment source for all themed components:

```yaml
# RaBbLE Synthwave Outrun Palette
# Single source of truth — all themed layers derive from these values
rabble_palette:
  # Core neons
  magenta:  "#ff2d78"   # Hot magenta — primary identity color
  cyan:     "#00f5ff"   # Electric cyan — secondary neon
  violet:   "#bf5fff"   # Soft violet — tertiary neon
  pink:     "#ff79c6"   # Outrun pink — grid/horizon

  # Backgrounds (void-dark)
  bg:       "#0a0010"   # Deep void — primary background
  surface:  "#12132a"   # Slightly elevated surface
  raised:   "#1a1b2e"   # Cards, input fields, popups
  border:   "#2a2840"   # Inactive borders, dividers

  # Text (the signal)
  text:     "#e8e6f0"   # Primary readable text
  muted:    "#6b6880"   # Secondary, dimmed text

  # Semantic
  red:      "#e05c6f"   # Error / urgent
  green:    "#50fa7b"   # Success / clean
  yellow:   "#f1fa8c"   # Warning / staged
```

---

## Glow Effect Guidance

The "glowing core" effect is achieved at the application level through configuration — not by changing hex values. Each themed layer implements it differently:

| Layer | Glow Method |
|---|---|
| **Hyprland borders** | Active border: gradient `#ff2d78 → #bf5fff`, `col.active_border` |
| **Waybar / Quickshell** | CSS `text-shadow: 0 0 8px #ff2d78` on active neon elements |
| **Terminal (Foot/Kitty)** | Font rendering + background darkness creates natural perceived glow |
| **GRUB** | Magenta text on void background — contrast is the glow |
| **Plymouth** | Script plugin renders text with outline pass for perceived glow |
| **SDDM** | QML `layer` effects or `DropShadow` with neon color |
| **Starship prompt** | Bold + neon color against dark terminal bg |

---

## Component Mapping

How each Ansible variable maps to themed components:

```
rabble_palette.magenta  →  Hyprland active border (primary)
                        →  GRUB text color
                        →  Plymouth primary text
                        →  SDDM focus/active elements
                        →  Starship prompt character
                        →  Waybar active workspace

rabble_palette.cyan     →  Hyprland active border (gradient end)
                        →  Git clean status
                        →  Waybar network/wifi widget
                        →  Terminal hyperlinks

rabble_palette.violet   →  Plymouth tagline
                        →  Hyprland inactive border
                        →  Starship git branch
                        →  Mako notification border

rabble_palette.pink     →  Git untracked files
                        →  Waybar battery warning
                        →  SDDM secondary accents

rabble_palette.bg       →  All background surfaces (root)
                        →  Terminal background
                        →  GRUB background
                        →  Plymouth background
                        →  SDDM background
                        →  Hyprland background color

rabble_palette.text     →  All primary readable text
                        →  Terminal foreground
                        →  SDDM input text

rabble_palette.red      →  Errors everywhere
                        →  Git conflicts
                        →  Hyprland urgent window border
```

---

## Cross-Reference

- Palette deployed via Ansible: `ansible/inventory/group_vars/all.yml`
- Theming guide and component locations: `grimoire/Theming.md`
- Architecture palette propagation: `grimoire/Architecture.md` → HiDPI Variable Flow
- Visual layer by layer: `grimoire/BootFlow.md`

---

```
harmonize ~ visual-substrate >> palette crystallized, outrun locked // %PALETTE_LOCKED%
```
