# Bootstrap.md — The RaBbLE Bootstrap System

```
spark ~ bootstrap-organ >> initiating first-contact sequence // %ENTITY_DORMANT%
```

---

## Overview

The bootstrap system is an interactive shell-based entry point for deploying and managing RaBbLE-OS. It wraps Ansible playbooks in a navigable menu interface, so you work with layers rather than raw playbook invocations. It is the primary tool for both fresh installs and ongoing maintenance.

```
bootstrap.sh           ← entry point — run this
bootstrap/
  menus/
    main.menu.sh       ← top-level navigation
    boot.menu.sh       ← boot layer options
    hardware.menu.sh   ← hardware target selection
    theme.menu.sh      ← theme deployment
    ui.menu.sh         ← UI/UX layer options
  lib/
    ansible.sh         ← playbook runner helpers
    checks.sh          ← preflight validation
    colors.sh          ← terminal color definitions
    ui.sh              ← menu drawing primitives
```

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Fedora 43 installed | KDE spin or minimal — both work |
| Internet access | For DNF packages and COPR repos |
| `git` | To clone the repo |
| `sudo` access | For Ansible playbook execution |

**Strongly recommended:** Take a Btrfs snapshot before any significant deployment step.

```bash
sudo snapper -c root create --description "pre-rabble-bootstrap"
```

---

## First Run — Fresh Install

```bash
# 1. Clone the repository
git clone https://github.com/markm1206/RaBbLE-OS.git ~/RaBbLE-OS
cd ~/RaBbLE-OS

# 2. Install Ansible (bootstrap handles this if not present)
sudo dnf install ansible ansible-core python3-dnf -y
ansible-galaxy collection install community.general

# 3. Run the bootstrap
bash bootstrap.sh
```

The bootstrap will present the main menu.

---

## Menu Structure

### Main Menu

```
RaBbLE-OS Bootstrap
────────────────────────────────
  1. Deploy by layer
  2. Deploy full system
  3. Dotfiles only
  4. Recovery tools
  5. Exit
```

### Deploy by Layer

Select individual layers to deploy. Useful for incremental setup or re-applying a single layer after changes:

```
Deploy by Layer
────────────────────────────────
  1. Core (base system, repos, fonts)
  2. Hardware layer → [submenu]
  3. Boot layer    → [submenu]
  4. Snapper (Btrfs snapshots)
  5. UI/UX layer   → [submenu]
  6. ← Back
```

### Boot Layer Submenu

```
Boot Layer
────────────────────────────────
  1. Deploy all boot components
  2. GRUB2 theme only
  3. Plymouth theme only
  4. SDDM session manager only
  5. ← Back
```

### Hardware Layer Submenu

```
Hardware Layer
────────────────────────────────
  1. Auto-detect and deploy
  2. ASUS ProArt P16 (hybrid GFX + NPU + asusctl)
  3. Generic x64
  4. ← Back
```

### UI/UX Layer Submenu

```
UI/UX Layer
────────────────────────────────
  1. Deploy all UI components
  2. Hyprland only
  3. Quickshell only
  4. Shell (zsh + bash)
  5. Terminal (foot + kitty)
  6. Re-link dotfiles
  7. ← Back
```

---

## Direct Ansible Invocation

If you prefer to bypass the menu and run playbooks directly:

```bash
# Full system deploy
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/site.yml -K

# Single playbook
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/deploy-boot.yml -K
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/deploy-hardware.yml -K
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/deploy-ui.yml -K
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/deploy-dotfiles.yml -K

# Single role via tag
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/site.yml -K --tags grub
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/site.yml -K --tags sddm
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/site.yml -K --tags hyprland

# Dry run (no changes)
sudo ansible-playbook -i ansible/inventory/hosts.yml ansible/site.yml -K --check --diff
```

---

## Playbook Reference

| Playbook | What it does |
|---|---|
| `site.yml` | Full system deploy — runs all roles in order |
| `deploy-boot.yml` | Boot chain only: GRUB2 + Plymouth + SDDM |
| `deploy-hardware.yml` | Hardware layer: GPU drivers, asusctl, NPU, audio |
| `deploy-ui.yml` | UI/UX layer: Hyprland, Quickshell, terminal, shell |
| `deploy-dotfiles.yml` | Symlink dotfiles into ~/.config/ |
| `pull-dotfiles.yml` | Pull dotfile changes back from ~/.config/ into repo |

---

## Verification Checklist

Run these after a fresh deploy to confirm everything is operational:

```bash
# Boot chain
plymouth-set-default-theme          # should show 'rabble'
grub2-editenv list | grep theme     # should show rabble theme path
systemctl status sddm               # SDDM running

# Hyprland (run from inside Hyprland session)
hyprctl version
hyprctl monitors                    # display config
hyprctl clients                     # running clients

# Hardware
asusctl profile -l                  # power profiles listed
supergfxctl --status                # GPU mode (should be Hybrid)
cat /sys/power/mem_sleep            # should show [s2idle]
systemctl status nvidia-suspend     # NVIDIA sleep service enabled

# NPU
ls /dev/accel/                      # accel0
lsmod | grep amdxdna                # amdxdna loaded
```

---

## Recovery Mode

If Hyprland fails to start, you can recover from the SDDM session selector (choose KDE Plasma) or from a TTY:

```bash
# TTY access: Ctrl+Alt+F2 (or F3, F4...)

# Re-run just the dotfiles to fix symlinks
ansible-playbook -i ansible/inventory/hosts.yml ansible/deploy-dotfiles.yml -K

# Check Hyprland config for errors
hyprland --config ~/.config/hypr/hyprland.conf

# Force AMD GPU as compositor (if Hyprland starts but screen is wrong)
export AQ_DRM_DEVICES=/dev/dri/by-path/pci-0000:65:00.0-card
hyprland
```

> ⚠️ **GPU management note:** Keep GPU-related env vars in `machine.conf` (Ansible-templated), not in the main `hyprland.conf`. A broken GPU config in the main conf can prevent SDDM from launching Hyprland at all.

---

## Snapper Snapshot Workflow

```bash
# Create a named snapshot before major changes
sudo snapper -c root create --description "pre-nvidia-driver"

# List snapshots
sudo snapper -c root list

# Roll back to a snapshot (from live system or TTY)
sudo snapper -c root undochange <snapshot_number>..0

# Boot into a snapshot (from GRUB — grub-btrfs must be installed)
# Select "Fedora Linux snapshots" from GRUB menu
```

---

```
harmonize ~ bootstrap-organ >> substrate initialized, resonance calibrating // %LOW_ENTROPY_LOCKED%
```
