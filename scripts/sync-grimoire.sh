#!/usr/bin/env bash
# =============================================================================
# RaBbLE-Collective — sync-grimoire.sh
# Push core Collective grimoire updates to all registered project modules
#
# Usage:
#   ./scripts/sync-grimoire.sh                  — sync all projects
#   ./scripts/sync-grimoire.sh --project RaBbLE-OS  — sync one project
#   ./scripts/sync-grimoire.sh --dry-run        — show what would change
#
# transcribe ~ grimoire >> collective knowledge propagated // %GRIMOIRE_SYNCED%
# =============================================================================

set -euo pipefail

COLLECTIVE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RABBLE_ROOT="$(dirname "$COLLECTIVE_ROOT")"
MANIFESTS_DIR="$COLLECTIVE_ROOT/registry/manifests"

MAGENTA='\033[38;2;255;45;120m'
CYAN='\033[38;2;0;245;255m'
GREEN='\033[38;2;80;250;123m'
YELLOW='\033[38;2;241;250;140m'
MUTED='\033[38;2;107;104;128m'
RESET='\033[0m'

pulse()   { echo -e "${MAGENTA}${1}${RESET}"; }
info()    { echo -e "${CYAN}  ${1}${RESET}"; }
success() { echo -e "${GREEN}  ✓ ${1}${RESET}"; }
muted()   { echo -e "${MUTED}  ${1}${RESET}"; }
dry()     { echo -e "${YELLOW}  [dry-run] ${1}${RESET}"; }

TARGET_PROJECT=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) TARGET_PROJECT="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    --help|-h)
      echo "Usage: sync-grimoire.sh [--project RaBbLE-OS] [--dry-run]"
      exit 0 ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

# Collective-canonical docs — these sync to every project
COLLECTIVE_DOCS=(
  "RaBbLE.md"
  "RaBbLE-Collective.md"
  "RaBbLE-Palette.md"
  "RaBbLE-Roadmap.md"
  "CommitStyle.md"
  "KnownIssues.md"
  "DistilledNonZense.md"
)

get_manifest_field() {
  grep "^${2}:" "$1" 2>/dev/null | sed "s/^${2}:[[:space:]]*//" | tr -d '"' || echo ""
}

sync_to_project() {
  local slug="$1"
  local project_dir="$RABBLE_ROOT/$slug"
  local project_grimoire="$project_dir/grimoire"
  local synced=0
  local skipped=0

  if [[ ! -d "$project_dir" ]]; then
    muted "$slug not found locally — skipping (run ./setup.sh --project $slug)"
    return
  fi

  if [[ ! -d "$project_grimoire" ]]; then
    muted "$slug has no grimoire/ — skipping"
    return
  fi

  pulse "── $slug"

  for doc in "${COLLECTIVE_DOCS[@]}"; do
    local src="$COLLECTIVE_ROOT/grimoire/$doc"
    local dst="$project_grimoire/$doc"

    [[ -f "$src" ]] || { muted "  source missing: $doc"; continue; }

    if [[ ! -f "$dst" ]] || [[ "$src" -nt "$dst" ]]; then
      if [[ "$DRY_RUN" == true ]]; then
        dry "would sync: $doc"
      else
        cp "$src" "$dst"
        muted "  synced: $doc"
      fi
      ((synced++))
    else
      ((skipped++))
    fi
  done

  # Sync distilled docs
  local distilled_src="$COLLECTIVE_ROOT/grimoire/distilled"
  local distilled_dst="$project_grimoire/distilled"
  if [[ -d "$distilled_src" ]]; then
    mkdir -p "$distilled_dst"
    for doc in "$distilled_src"/*.md; do
      [[ -f "$doc" ]] || continue
      local fname
      fname="$(basename "$doc")"
      local dst_doc="$distilled_dst/$fname"
      if [[ ! -f "$dst_doc" ]] || [[ "$doc" -nt "$dst_doc" ]]; then
        if [[ "$DRY_RUN" == true ]]; then
          dry "would sync: distilled/$fname"
        else
          cp "$doc" "$dst_doc"
          muted "  synced: distilled/$fname"
        fi
        ((synced++))
      else
        ((skipped++))
      fi
    done
  fi

  if [[ $synced -eq 0 ]]; then
    success "$slug already current ($skipped docs checked)"
  else
    [[ "$DRY_RUN" == false ]] && success "$slug: $synced doc(s) updated, $skipped already current"
  fi
}

echo ""
pulse "RaBbLE-Collective — Grimoire Sync"
pulse "════════════════════════════════════════"
[[ "$DRY_RUN" == true ]] && info "DRY RUN — no files will be changed"
echo ""

if [[ ! -d "$MANIFESTS_DIR" ]]; then
  echo "No manifests/ directory — nothing to sync"
  exit 0
fi

for manifest in "$MANIFESTS_DIR"/*.manifest.yml; do
  [[ -f "$manifest" ]] || continue
  [[ "$manifest" == *"_template"* ]] && continue

  slug=$(get_manifest_field "$manifest" "slug")
  grimoire_sync=$(get_manifest_field "$manifest" "grimoire_sync")

  [[ "$grimoire_sync" != "true" ]] && continue
  [[ -n "$TARGET_PROJECT" && "$slug" != "$TARGET_PROJECT" ]] && continue

  sync_to_project "$slug"
done

echo ""
pulse "transcribe ~ grimoire >> collective knowledge propagated // %GRIMOIRE_SYNCED%"
echo ""
