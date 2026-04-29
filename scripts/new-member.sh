#!/usr/bin/env bash
# =============================================================================
# RaBbLE-Collective — new-member.sh
# Scaffold a new self-contained RaBbLE project module
#
# Usage:
#   ./scripts/new-member.sh --slug RaBbLE-[Name] --role [substrate|server|frontend|tooling]
#
# What it does:
#   1. Creates the project directory under ~/RaBbLE/
#   2. Initializes git
#   3. Scaffolds AGENT.md, CONTEXT.md, REFERENCES.md, workspace CONTEXT.md files
#   4. Syncs core grimoire from RaBbLE-Collective
#   5. Creates CLAUDE.md and CODEX.md as symlinks to AGENT.md
#   6. Creates the manifest entry in RaBbLE-Collective/manifests/
#   7. Registers the project in AGENT.md Project Index
#
# spark ~ collective >> new member scaffolded // %COLLECTIVE_EXPANDED%
# =============================================================================

set -euo pipefail

COLLECTIVE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RABBLE_ROOT="$(dirname "$COLLECTIVE_ROOT")"

MAGENTA='\033[38;2;255;45;120m'
CYAN='\033[38;2;0;245;255m'
GREEN='\033[38;2;80;250;123m'
RED='\033[38;2;224;92;111m'
MUTED='\033[38;2;107;104;128m'
RESET='\033[0m'

pulse()   { echo -e "${MAGENTA}${1}${RESET}"; }
info()    { echo -e "${CYAN}  ${1}${RESET}"; }
success() { echo -e "${GREEN}  ✓ ${1}${RESET}"; }
error()   { echo -e "${RED}  ✗ ${1}${RESET}"; exit 1; }
muted()   { echo -e "${MUTED}  ${1}${RESET}"; }

# --- Argument parsing --------------------------------------------------------
SLUG=""
ROLE="substrate"
DESCRIPTION=""
REMOTE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --slug)        SLUG="$2"; shift 2 ;;
    --role)        ROLE="$2"; shift 2 ;;
    --description) DESCRIPTION="$2"; shift 2 ;;
    --remote)      REMOTE="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: new-member.sh --slug RaBbLE-[Name] --role [substrate|server|frontend|tooling]"
      echo "  --description  One-line project description"
      echo "  --remote       Git remote URL (optional, can add later)"
      exit 0 ;;
    *) error "Unknown argument: $1" ;;
  esac
done

[[ -z "$SLUG" ]] && error "Required: --slug RaBbLE-[Name]"
[[ "$SLUG" != RaBbLE-* ]] && error "Slug must start with RaBbLE- (e.g. RaBbLE-Mobile)"
[[ -z "$DESCRIPTION" ]] && DESCRIPTION="[Add one-line description]"

PROJECT_DIR="$RABBLE_ROOT/$SLUG"
EPOCH=$(grep "^epoch:" "$COLLECTIVE_ROOT/registry/epochs/current.epoch.yml" 2>/dev/null | awk '{print $2}' || echo "1")
EPOCH_BRANCH="epoch/${EPOCH}-$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed 's/rabble-//')"

echo ""
pulse "RaBbLE-Collective — New Member: $SLUG"
pulse "════════════════════════════════════════"
info "Role:         $ROLE"
info "Description:  $DESCRIPTION"
info "Project dir:  $PROJECT_DIR"
info "Epoch branch: $EPOCH_BRANCH"
echo ""

# Guard: don't overwrite an existing project
if [[ -d "$PROJECT_DIR" ]]; then
  error "$PROJECT_DIR already exists. Remove it first or choose a different slug."
fi

# =============================================================================
# 1. Create directory and init git
# =============================================================================
pulse "── Initializing repo"
mkdir -p "$PROJECT_DIR"
git -C "$PROJECT_DIR" init --quiet
success "git init: $PROJECT_DIR"

if [[ -n "$REMOTE" ]]; then
  git -C "$PROJECT_DIR" remote add origin "$REMOTE"
  success "Remote added: $REMOTE"
fi

# =============================================================================
# 2. Create project directory structure
# =============================================================================
pulse "── Scaffolding structure"
mkdir -p "$PROJECT_DIR"/{planning/specs,planning/decisions,src,grimoire/distilled,ops}
success "Directory structure created"

# =============================================================================
# 3. Scaffold AGENT.md
# =============================================================================
cat > "$PROJECT_DIR/AGENT.md" << AGENT_EOF
# AGENT.md — ${SLUG} Agent Primer

> This is the owner file. CLAUDE.md and CODEX.md are symlinks to this file.
> RaBbLE Collective member. Identity, palette, and conventions inherited from:
> \`~/RaBbLE/RaBbLE-Collective/\`
>
> Read this file first. Load additional context on demand.

---

## What This Project Is

${DESCRIPTION}

Role in Collective: ${ROLE}
Active branch: \`${EPOCH_BRANCH}\`
Status: Epoch ${EPOCH} scaffold

---

## Tech Stack

- [TBD]

---

## Workspaces

- \`planning/\` — specs, architecture decisions, ADRs
- \`src/\` — application code / implementation
- \`grimoire/\` — project lore and documentation
- \`ops/\` — deployment, monitoring, operational scripts

---

## Routing

| Task | Go to | Read | Skills |
|---|---|---|---|
| Spec a feature | \`planning/\` | \`CONTEXT.md\` | \`grimoire/Architecture.md\` |
| Write code | \`src/\` | \`CONTEXT.md\` | — |
| Update docs | \`grimoire/\` | \`CONTEXT.md\` | — |
| Deploy / operate | \`ops/\` | \`CONTEXT.md\` | — |

---

## Naming Conventions

\`\`\`
Specs:      planning/specs/[feature-name]_spec.md
ADRs:       planning/decisions/YYYY-MM-DD-[title].md
\`\`\`

---

## Absolute Rules

- All color values from Collective palette — never invent hex values
- All commits follow Pulse Protocol — see conventions.distilled
- [Add project-specific rules here]

---

## Inherited From Collective

| Need | Load From |
|---|---|
| Color values | \`~/RaBbLE/RaBbLE-Collective/grimoire/distilled/palette.distilled.md\` |
| Commit format | \`~/RaBbLE/RaBbLE-Collective/grimoire/distilled/conventions.distilled.md\` |
| Entity identity | \`~/RaBbLE/RaBbLE-Collective/grimoire/RaBbLE.md\` |
| Phase milestones | \`~/RaBbLE/RaBbLE-Collective/grimoire/RaBbLE-Roadmap.md\` |

---

## Project Grimoire Map — Load On Demand

| Question Class | Load This |
|---|---|
| Project architecture | \`grimoire/Architecture.md\` |
| Getting started | \`grimoire/GettingStarted.md\` |

---

## Current State

See \`CONTEXT.md\` for active work and immediate priorities.
AGENT_EOF
success "AGENT.md created"

# =============================================================================
# 4. Scaffold CONTEXT.md
# =============================================================================
cat > "$PROJECT_DIR/CONTEXT.md" << CONTEXT_EOF
# CONTEXT.md — ${SLUG} Current State

\`\`\`
epoch: ${EPOCH} | project: ${SLUG} | status: scaffold
\`\`\`

## What We Are Building

${DESCRIPTION}

## Active Work — Epoch ${EPOCH} Scaffold

- [ ] Tech stack decision
- [ ] Architecture document drafted
- [ ] GettingStarted.md written
- [ ] AGENT.md routing table completed

## What Good Looks Like

[Define what done looks like for this project]

## What To Avoid

[Define anti-patterns specific to this project]

## Immediate Priorities

1. Make tech stack decision and log as ADR
2. Write grimoire/Architecture.md
3. Complete AGENT.md routing table
CONTEXT_EOF
success "CONTEXT.md created"

# =============================================================================
# 5. Scaffold REFERENCES.md
# =============================================================================
cat > "$PROJECT_DIR/REFERENCES.md" << REF_EOF
# REFERENCES.md — ${SLUG} Decisions & Resources

## Architecture Decisions

| Date | Decision | Rationale |
|---|---|---|
| $(date +%Y-%m-%d) | Project scaffolded | Epoch ${EPOCH} Collective expansion |

## Repositories

| Project | Repo | Status |
|---|---|---|
| ${SLUG} | ${REMOTE:-TBD} | Epoch ${EPOCH} scaffold |

## Key External Resources

[Add relevant links]

## Collective Reference

- Identity: \`~/RaBbLE/RaBbLE-Collective/grimoire/RaBbLE.md\`
- Palette: \`~/RaBbLE/RaBbLE-Collective/grimoire/distilled/palette.distilled.md\`
- Conventions: \`~/RaBbLE/RaBbLE-Collective/grimoire/distilled/conventions.distilled.md\`
REF_EOF
success "REFERENCES.md created"

# =============================================================================
# 6. Scaffold workspace CONTEXT.md files
# =============================================================================
for workspace in planning src grimoire ops; do
  cat > "$PROJECT_DIR/$workspace/CONTEXT.md" << WS_EOF
# ${workspace}/CONTEXT.md — ${SLUG}

## What This Workspace Is

[Describe what happens in this workspace]

## What Lives Here

[Describe the files and structure]

## Process

[Describe the workflow for this workspace]

## Skills Needed

[List grimoire docs or distilled files relevant to this workspace]
WS_EOF
  muted "  created: $workspace/CONTEXT.md"
done
success "Workspace CONTEXT.md files created"

# =============================================================================
# 7. Sync core grimoire
# =============================================================================
pulse "── Syncing core grimoire"
bash "$COLLECTIVE_ROOT/scripts/setup.sh" --project "$SLUG" --pull-only 2>/dev/null || true

COLLECTIVE_GRIMOIRE_DOCS=(
  "RaBbLE.md" "RaBbLE-Collective.md" "RaBbLE-Palette.md"
  "RaBbLE-Roadmap.md" "CommitStyle.md" "KnownIssues.md" "DistilledNonZense.md"
)
for doc in "${COLLECTIVE_GRIMOIRE_DOCS[@]}"; do
  src="$COLLECTIVE_ROOT/grimoire/$doc"
  [[ -f "$src" ]] && cp "$src" "$PROJECT_DIR/grimoire/$doc" && muted "  synced: $doc"
done
for doc in "$COLLECTIVE_ROOT/grimoire/distilled/"*.md; do
  [[ -f "$doc" ]] && cp "$doc" "$PROJECT_DIR/grimoire/distilled/$(basename "$doc")" \
    && muted "  synced: distilled/$(basename "$doc")"
done
success "Core grimoire synced"

# =============================================================================
# 8. Create symlinks: CLAUDE.md → AGENT.md, CODEX.md → AGENT.md
# =============================================================================
pulse "── Creating agent symlinks"
ln -s AGENT.md "$PROJECT_DIR/CLAUDE.md"
success "CLAUDE.md → AGENT.md"
ln -s AGENT.md "$PROJECT_DIR/CODEX.md"
success "CODEX.md → AGENT.md"

# =============================================================================
# 9. Create manifest entry
# =============================================================================
pulse "── Creating manifest"
MANIFEST_FILE="$COLLECTIVE_ROOT/registry/manifests/${SLUG}.manifest.yml"
cat > "$MANIFEST_FILE" << MANIFEST_EOF
# manifests/${SLUG}.manifest.yml

name: ${SLUG}
slug: ${SLUG}
description: "${DESCRIPTION}"
role: ${ROLE}

repo: ${REMOTE:-TBD}
branch: main
epoch_branch: ${EPOCH_BRANCH}
worktree_root: ~/RaBbLE/${SLUG}

phase: ${EPOCH}
epoch: ${EPOCH}
status: scaffold

grimoire_sync: true
grimoire_path: grimoire/

palette_version: "1.0"
entity_embedded: true
pulse_protocol: true

notes: >
  Scaffolded $(date +%Y-%m-%d). Epoch ${EPOCH} new member.
MANIFEST_EOF
success "Manifest created: manifests/${SLUG}.manifest.yml"

# =============================================================================
# 10. Initial git commit
# =============================================================================
pulse "── Initial commit"
git -C "$PROJECT_DIR" add .
git -C "$PROJECT_DIR" commit --quiet \
  -m "spark ~ collective >> ${SLUG} scaffolded // %COLLECTIVE_EXPANDED%"
success "Initial commit: spark ~ collective >> ${SLUG} scaffolded"

# =============================================================================
# Done
# =============================================================================
echo ""
pulse "── Complete"
echo ""
info "Project:    $PROJECT_DIR"
info "Manifest:   $MANIFEST_FILE"
info "Next steps:"
echo ""
echo -e "${MUTED}  1. Add $SLUG to the Project Index in RaBbLE-Collective/AGENT.md${RESET}"
echo -e "${MUTED}  2. Add $SLUG to registry/epochs/current.epoch.yml focus section${RESET}"
echo -e "${MUTED}  3. Complete AGENT.md routing table for this project${RESET}"
echo -e "${MUTED}  4. Make tech stack decision → planning/decisions/YYYY-MM-DD-stack.md${RESET}"
echo -e "${MUTED}  5. Set remote: git -C $PROJECT_DIR remote add origin <URL>${RESET}"
echo ""
pulse "spark ~ collective >> ${SLUG} registered // %COLLECTIVE_EXPANDED%"
echo ""
