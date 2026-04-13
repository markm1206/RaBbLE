# GettingStarted.md — From Zero to RaBbLE

```
spark ~ bootstrap-organ >> first contact sequence // %ENTITY_DORMANT%
```

> Read `RaBbLE.md` before proceeding. The philosophy governs every decision.
> This is not optional.

---

## Prerequisites

| Requirement | Spec | Notes |
|---|---|---|
| **Hardware** | x86_64, 16 GB+ RAM, 512 GB+ NVMe | Primary target: ASUS ProArt P16 H7606WV |
| **OS** | Fedora Linux 43 installed | KDE spin or minimal base both work |
| **Filesystem** | Btrfs (root + home subvolumes) | Fedora default — accept it during install |
| **Internet** | Stable broadband | Required for COPR repos, package downloads |
| **Sudo access** | Required | Ansible needs it for system changes |

---

## Phase 0: Install Fedora 43

Download Fedora 43 from [fedoraproject.org](https://fedoraproject.org/workstation/download).

**Installer settings:**
- Filesystem: **btrfs** (accept the Fedora default — do not change to ext4)
- Partition layout: let Fedora create the default `root` and `home` subvolumes
- Hostname: set something meaningful — this becomes your Ansible inventory hostname

After install, verify you have two Btrfs subvolumes:
```bash
sudo btrfs subvolume list /
# Should show both 'root' and 'home' subvolumes
```

---

## Phase 1: Bootstrap the Substrate

```bash
# Clone the repository
git clone https://github.com/markm1206/RaBbLE-OS.git ~/RaBbLE-OS
cd ~/RaBbLE-OS

# Install Ansible
sudo dnf install ansible ansible-core python3-dnf -y
ansible-galaxy collection install community.general

# Take a snapshot before touching anything
sudo dnf install snapper btrfs-progs -y
sudo snapper -c root create-config /
sudo snapper -c root create --description "pre-rabble-baseline"

# Run the bootstrap
bash bootstrap.sh
```

The bootstrap presents an interactive menu. For a fresh install, the recommended sequence is:

1. **Core** — base packages, repos, locale, fonts
2. **Hardware** → ASUS ProArt P16 *(or your target)*
3. **Reboot** after hardware layer (nouveau must unload, akmod-nvidia must build)
4. **Boot layer** — GRUB2 + Plymouth + SDDM
5. **Snapper** — configure snapshot policies
6. **UI/UX** — Hyprland, shell, terminal, dotfiles

---

## Phase 2: First Boot into Hyprland

After the UI/UX layer deploys, log out of KDE (or reboot) and select **Hyprland** from the SDDM session list.

**Verify the environment:**
```bash
# Monitor configuration (should show 3840x2400 @ 60Hz, scale 2)
hyprctl monitors

# GPU compositor (should show AMD 890M)
hyprctl dispatch exec -- glxinfo | grep renderer

# NVIDIA PRIME offload available
DRI_PRIME=pci-0000_64_00_0 glxinfo | grep renderer   # should show RTX 4060

# Sleep state
cat /sys/power/mem_sleep   # should show [s2idle]

# ASUS tools
asusctl profile -l         # power profiles
supergfxctl --status       # GPU mode (Hybrid)
```

---

## Phase 3: Shell & Editor

```bash
# Set zsh as default shell (if not already)
chsh -s $(which zsh)

# Re-link dotfiles if needed
ansible-playbook -i ansible/inventory/hosts.yml ansible/deploy-dotfiles.yml -K

# Verify zsh prompt
exec zsh    # should load p10k theme
```

**Neovim** is the target terminal based editor. Configuration is pending (see `RaBbLE-Roadmap.md` Phase 1.3). For now, VSCodium or Nano work as fallbacks.

**VSCodium** is the primary GUI based IDE for generic development. Plugins should also be part of the VSCodium RaBbLE-OS packages.
---

## Working with Dotfiles

All configs are static files in `dotfiles/` symlinked into `~/.config/`. Edit the repo file — the symlink keeps things in sync with no copy step:

```bash
# Edit hyprland config
$EDITOR ~/RaBbLE-OS/dotfiles/hyprland/conf.d/keybinds.conf
hyprctl reload   # live reload, no logout needed

# Edit zsh config
$EDITOR ~/RaBbLE-OS/dotfiles/shell/zsh/aliases.zsh
exec zsh         # reload shell

# Commit your changes
cd ~/RaBbLE-OS
git add dotfiles/
git commit -m "transcribe ~ hyprland >> updated keybindings // %CONFIG_EVOLVED%"
```

---

## Phase 4: AI Tooling (Phase 2 — Future)

AI stack deployment is controlled by `ai_stack.phase` in `ansible/inventory/group_vars/all.yml`.

```bash
# Phase 0: install deps only (default — safe)
# Phase 1: build llama.cpp with CUDA (requires working NVIDIA driver)
# Phase 2: install vLLM + FastFlowLM (requires XRT/NPU working)

# To advance:
# 1. Edit ansible/inventory/group_vars/all.yml → ai_stack.phase: 1
# 2. Re-run:
ansible-playbook -i ansible/inventory/hosts.yml ansible/site.yml -K --tags AI-tools
```

See ROADMAP.md Phase 2 and the AI stack section of DistilledNonZense.md for full detail.

---

## Troubleshooting

See `BootFlow.md` for the full troubleshooting table. Quick reference:

```bash
# Hyprland won't start — check GPU path
cat ~/.config/hypr/machine.conf | grep AQ_DRM_DEVICES

# SDDM theme broken — test in isolation
sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/rabble

# Sleep not working
cat /sys/power/mem_sleep           # must show [s2idle]
journalctl -b -u systemd-suspend   # last suspend logs

# asusctl not starting
systemctl status asusd
journalctl -u asusd --since "10 min ago"

# Roll back to pre-install snapshot
sudo snapper -c root list
sudo snapper -c root undochange <N>..0
```

---

## Known Issues

See `KnownIssues.md` for the current tracker of active bugs, workarounds, and drift events.

---

```
harmonize ~ bootstrap-organ >> substrate initialized // %LOW_ENTROPY_LOCKED%
```
