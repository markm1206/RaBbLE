# scripts/CONTEXT.md

```
workspace: scripts | epoch: 0
```

## What happens here
Setup, wiring, and sync tooling for the Collective.
This is the source and ops workspace — scripts are the work product.

## Scripts

| Script | Purpose | Status |
|---|---|---|
| `setup.sh` | Clone projects, wire symlinks, full bootstrap | Written, untested |
| `new-member.sh` | Scaffold a new project module | Written, untested |
| `sync-grimoire.sh` | Push core grimoire to all projects | Written, untested |
| `status.sh` | Collective health dashboard | Written, untested |

## First run order
```bash
./scripts/setup.sh --links-only    # wire Collective symlinks first
./scripts/status.sh                # verify Collective state
./scripts/setup.sh                 # pull and wire all projects
```

## When a script fails
Log the failure in `../registry/` as a registry note.
Fix here, retest, update status above to verified.
