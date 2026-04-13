# Packages.md — RaBbLE-OS Package Manifest

```
transcribe ~ package-layer >> all packages declared // %MANIFEST_LOCKED%
```

> This is the canonical list of packages that constitute a RaBbLE-OS install.
> Goal: a fresh Fedora minimal + this manifest = complete RaBbLE-OS experience.
> This manifest assumes a clean Fedora minimal base — the KDE spin is not required
> and KDE packages are not included.

---

## Layer 0 — Base

### Repositories
- RPM Fusion Free
- RPM Fusion Non-Free
- Flathub (Flatpak)
- solopasha/hyprland (COPR)
- asus-linux (COPR — asusctl, supergfxctl)

### Core System
```
git, curl, wget2, rsync
htop, btop, fastfetch
unzip, p7zip, xz, jq, yq
lm_sensors, nvtop, powertop, stress-ng
btrfs-progs, snapper, python3-dnf-plugin-snapper
NetworkManager, nm-connection-editor
gcc, gcc-c++, make, cmake, git-lfs
python3, python3-pip, python3-devel
google-noto-fonts-common, google-noto-emoji-fonts, jetbrains-mono-fonts
terminus-fonts
flatpak
os-prober          (GRUB removable media detection)
```

---

## Layer 1 — Hardware (ASUS ProArt P16 H7606WV)

### NVIDIA (RTX 4060 Mobile — Optimus offload)
```
akmod-nvidia
xorg-x11-drv-nvidia
xorg-x11-drv-nvidia-cuda
xorg-x11-drv-nvidia-cuda-libs
libva-nvidia-driver
libva-utils
nvidia-driver-cuda
```
> NVIDIA kernel modules are deferred from initramfs — loaded at `graphical.target` after SDDM.
> See `hardware/x64/asus_proart_p16/tasks/nvidia_defer.yml` and `KnownIssues.md`.

### AMD iGPU (Radeon 890M — primary compositor)
```
mesa, mesa-dri-drivers, mesa-vulkan-drivers
libva-mesa-driver
vulkan-tools
radeontop
```

### ASUS Platform (asusctl / supergfxctl)
```
asusctl          (COPR: asus-linux)
supergfxctl      (COPR: asus-linux)
power-profiles-daemon
```

### AMD NPU (XDNA2)
```
amdxdna          (kernel module — akmod or COPR)
xrt-smi          (XRT runtime management)
```

---

## Layer 2 — Boot Chain

### GRUB2
```
grub2
grub2-tools
terminus-fonts      (for 4K readable TTY/GRUB font — ter-v32b)
```

### Plymouth
```
plymouth
plymouth-plugin-script
plymouth-system-theme
```

### Session Manager
```
sddm
qt6-qtdeclarative     (QML rendering for SDDM theme)
qt6-qtwayland         (Wayland backend for Qt6)
```

---

## Layer 3 — Desktop

### Hyprland Stack
```
hyprland         (COPR: solopasha/hyprland — verify COPR is current)
hyprpaper
hypridle
hyprlock
xdg-desktop-portal-hyprland
xdg-desktop-portal-gtk
waybar
wofi
mako
wl-clipboard
grim
slurp
swayimg
qt6-qtwayland
qt6-qtsvg
polkit-kde-agent-1
xorg-x11-server-Xwayland
foot
kitty
brightnessctl
playerctl
```

### Quickshell (Phase 1 — build from source)
```
cmake, ninja-build
qt6-qtdeclarative-devel
qt6-qtbase-devel
qt6-qtwayland-devel
wayland-devel
wayland-protocols-devel
pipewire-devel
pulseaudio-libs-devel
```

### Shell
```
zsh
zinit              (zsh plugin manager)
starship           (cross-shell prompt)
```

---

## Layer 4 — Apps & Dev Tools

### Development
```
vscodium         (via vscodium.gpg repo)
docker, docker-compose
nodejs, npm
rustup
go
neovim
```

### AI Tools (Phase 2 — deps only until ai_stack.phase advances)
```
nvidia-driver-cuda
python3-pip
```
> Full AI stack (llama.cpp, vLLM, FastFlowLM, Ollama) gated behind `ai_stack.phase` variable.
> See `group_vars/all.yml` → `ai_stack` section.

### Apps
> File manager and archive tool (dolphin, ark) have been removed from the system.
> No replacement has been selected yet — decision pending before these are bundled.
> Candidates: Nautilus (GTK-native, Wayland clean), Thunar (lightweight), nnn/yazi (terminal-based).
> Until a decision is made, these are not in the manifest.

---

## To Be Determined

These need decisions before the manifest is final:

- Terminal multiplexer: `zellij` vs `tmux`
- Browser: Firefox (Wayland native) or other
- File manager: replacement for dolphin/ark TBD (see Apps above)
- PDF viewer, image viewer
- Email/calendar client if needed
- App launcher: `wofi` vs `fuzzel` vs other
- Qt theme: `kvantum` (full synthwave control, requires theme authoring) vs `adwaita-dark` (interim, zero-config)

---

## Packages to Purge (KDE Spin Defaults)

KDE has been manually removed from the current system. The `purge-kde/` role codifies this for clean installs.

**Managed by `ansible/roles/purge-kde/tasks/main.yml`:**
```
plasma-desktop
plasma-workspace
plasma-nm
plasma-pa
kwin
kscreen
kdialog
kwalletmanager5
kinfocenter
systemsettings
discover
plasma-systemmonitor
plasma-vault
kdeconnectd
bluedevil
powerdevil
kactivitymanagerd
```

> Use: `ansible-playbook ansible/site.yml -K --tags purge-kde`
> The role uses `autoremove: true` to pull orphaned KDE dependencies.

**Do NOT purge:**
- `polkit-kde-agent-1` — still needed for Hyprland auth dialogs
- `qt6-*` packages — needed for SDDM QML theming
- `dolphin` / `ark` — not in the purge role; these are separate decisions (see Apps above)

---

```
transcribe ~ package-layer >> manifest crystallized, v0.4 // %MANIFEST_LOCKED%
```
