# registry/CONTEXT.md

```
workspace: registry | epoch: 0
```

## What happens here
The Collective member registry. Every RaBbLE project is registered here.
This is where you understand what exists, what state it's in,
and how to bring a new member into the Collective.

## Contents
`epochs/current.epoch.yml` — active epoch definition
`epochs/archive/` — closed epochs, immutable
`manifests/` — one manifest per registered project

## Registering a new project
```bash
../scripts/new-member.sh --slug RaBbLE-[Name] --role [type]
```
Then add a row to `AGENT.md` Project Registry.

## Current members
See `manifests/` — one file per project.
See `../scripts/status.sh` for live state.
