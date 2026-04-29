# palette.distilled.md — RaBbLE Palette (Agent Reference)

> Generated from: `grimoire/RaBbLE-Palette.md`
> Do not edit directly. Regenerate from canonical source.

## Neons
```
#ff2d78  magenta   rabble_palette.magenta   primary neon, borders, active
#00f5ff  cyan      rabble_palette.cyan      secondary, links, info
#bf5fff  violet    rabble_palette.violet    tertiary, taglines, accents
#ff79c6  pink      rabble_palette.pink      grid, warnings, soft highlights
```

## Backgrounds
```
#0a0010  bg        rabble_palette.bg        primary background
#12132a  surface   rabble_palette.surface   panels, sidebars
#1a1b2e  raised    rabble_palette.raised    cards, inputs, popups
#2a2840  border    rabble_palette.border    inactive borders, dividers
```

## Text
```
#e8e6f0  text      rabble_palette.text      primary readable text
#6b6880  muted     rabble_palette.muted     secondary, dimmed, comments
```

## Semantic
```
#e05c6f  red       rabble_palette.red       error, urgent, destructive
#50fa7b  green     rabble_palette.green     success, clean, ok
#f1fa8c  yellow    rabble_palette.yellow    warning, staged, caution
```

## Usage Rules
- Never hardcode hex values in component configs — use Ansible variables
- All values defined in `ansible/inventory/group_vars/all.yml` in RaBbLE-OS
- Change values in `grimoire/RaBbLE-Palette.md` first, propagate second
- Glow effects via shadow/blur at application layer — not by changing hex
