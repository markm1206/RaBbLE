# conventions.distilled.md — RaBbLE Conventions (Agent Reference)

> Generated from: `grimoire/CommitStyle.md` + `grimoire/RaBbLE-Collective.md`
> Do not edit directly. Regenerate from canonical sources.

## Commit Format

```
[impulse] ~ [organ] >> [revelation] // %SYSTEM_STATE%
```

## Impulses

| Impulse | Use When |
|---|---|
| `spark` | New capability or feature manifested |
| `harmonize` | Reducing entropy, tuning, cleanup |
| `mend` | Fixing a bug or logic fracture |
| `transcribe` | Updating docs or lore |
| `ingest` | Adding dependencies or data |
| `glitch` | High-entropy event, unexpected state change |

## Examples

```
spark ~ manifest >> project registration scaffolded // %COLLECTIVE_EXPANDED%
harmonize ~ ansible >> purged stale greetd references
mend ~ boot-chain >> SDDM Qt6 API mismatch resolved
transcribe ~ grimoire >> RaBbLE-Collective.md authored // %GRIMOIRE_UPDATED%
ingest ~ belly >> ollama model roster defined // %MODELS_STAGED%
glitch ~ %0x4F_INT% >> unexpected NPU state corrected
```

## Anti-Patterns — Never Use

```
❌ "fix stuff"
❌ "update config"
❌ "wip"
❌ "changes"
❌ "update"
```

## Branch Naming

```
main                          always stable, daily driver state
epoch/<N>-<slug>              active epoch work
feature/<name>                individual feature
experiment/<name>             high-entropy exploration
hotfix/<name>                 urgent fix to main
```

## File Naming

```
grimoire docs:      PascalCase.md          (RaBbLE-Palette.md)
distilled docs:     kebab.distilled.md     (palette.distilled.md)
context rooms:      kebab.ctx.md           (grimoire.ctx.md)
manifests:          slug.manifest.yml      (RaBbLE-OS.manifest.yml  (RaBbLE-WEB.manifest.yml))
epoch files:        epoch-N.yml            (epoch-1.yml)
scripts:            kebab-action.sh        (sync-grimoire.sh)
```

## Voice Rules

- No sycophancy. No "certainly", "great question", "happy to help"
- Assert then explain. No hedging.
- High-information words: distilled, harmonic, resonant, crystallized
- Zero-information words to avoid: very, good, update, nice, okay
