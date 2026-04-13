# Hardware.md — RaBbLE-OS Hardware Profile

```
transcribe ~ grimoire >> substrate cartographed // %HARDWARE_LOCKED%
```

**Primary target:** ASUS ProArt P16 H7606WV
**Last verified:** 2026-04-08
**System:** ASUS ProArt P16 H7606WV_H7606WV (BIOS H7606WV.319 — 2025-05-07)

> For adding new hardware targets, see `AddingTargets.md`.
> For Ansible role structure, see `Architecture.md`.

---

## CPU

| Field | Value |
|---|---|
| Model | AMD Ryzen AI 9 HX 370 (Strix Point) |
| Cores / Threads | 12C / 24T |
| Architecture | Zen 5 |
| Base / Boost | 2.0 GHz / 5.1 GHz |
| NPU | XDNA2 (integrated, PCI 66:00.1) |

---

## GPUs

| | iGPU | dGPU |
|---|---|---|
| Model | AMD Radeon 890M (RDNA 3.5) | NVIDIA RTX 4060 Max-Q Mobile |
| PCI address | `65:00.0` | `64:00.0` |
| VRAM | Shared (system RAM) | 8 GB GDDR6 |
| Driver | amdgpu (Mesa, radeonsi) | akmod-nvidia |
| **Role** | **Primary — drives display/compositor** | PRIME offload (LLM, CUDA, rendering) |
| API | Vulkan (radeon_icd), VA-API (radeonsi) | CUDA, Vulkan (nvidia_icd) |

> ⚠️ **Optimus Architecture:** This is NOT a desktop with two independent GPUs.
> The RTX 4060 does not drive the display in Hybrid mode.
> Use `DRI_PRIME=pci-0000_64_00_0 <cmd>` to route workloads to NVIDIA.
> See `BootFlow.md` for `AQ_DRM_DEVICES` configuration.

### GPU Mode Switching (supergfxctl)

```bash
supergfxctl --status            # Current mode
supergfxctl --mode Hybrid       # AMD displays, NVIDIA available (recommended default)
supergfxctl --mode Integrated   # AMD only — best battery life
supergfxctl --mode Dedicated    # NVIDIA drives display (requires MUX — not supported here)
supergfxctl --mode Compute      # NVIDIA compute only, no display — ideal for CUDA/ML jobs
```

---

## NPU — AMD XDNA2

| Field | Value |
|---|---|
| Device node | `/dev/accel/accel0` |
| Kernel driver | `amdxdna 0.6.0` (upstream, loaded at init) |
| Userspace | XRT + ONNX Runtime (VitisAI EP) |
| PCI address | `66:00.1` |
| Status | ✅ Confirmed operational |

> XRT package availability for Fedora 43 may require checking `repo.radeon.com`.
> ONNX Runtime VitisAI EP falls back to CPU if XRT is unavailable.

---

## Memory

- **Total:** 32 GiB (30.4 GiB usable)
- **Type:** LPDDR5X — integrated with CPU package (not user-upgradeable)

---

## Storage

| Subvolume | Mount | Snapper Config |
|---|---|---|
| `root` (ID 256) | `/` | `snapper -c root` |
| `home` (ID 257) | `/home` | `snapper -c home` |

Filesystem: **btrfs** (Fedora 43 default, CoW, native snapshots)

---

## Display

- **Panel:** 16" SDC415D
- **Resolution:** 3840×2400 @ 60 Hz
- **Scale:** 2× (HiDPI — configured in `hyprland-machine.conf.j2` and `sddm-hidpi.conf.j2`)
- **Connection:** eDP-1 (internal — driven by AMD iGPU in Hybrid mode)
- **Wayland monitor string:** `eDP-1,3840x2400@60,0x0,2`

---

## Audio

- **Subsystem:** PipeWire + WirePlumber
- **Managed by:** `hardware/x64/asus_proart_p16/tasks/audio.yml`

---

## Network

- **WiFi:** MediaTek MT7925 (`wlp99s0`)
- **Management:** NetworkManager

---

## Power Management

```
asusd  ←→  power-profiles-daemon (PPD)
            Quiet       → power-saver
            Balanced    → balanced
            Performance → performance

supergfxd → GPU mode control

Battery charge limit: configurable via asusctl
  asusctl -c 80    # limit to 80% for longevity
```

Sleep mode: **s2idle (S0ix)** — AMD Strix Point HX 370 does not support S3 deep sleep. This is the correct and only viable sleep mode for this hardware.

---

## Kernel Modules (relevant, verified)

```
amdgpu       — AMD 890M iGPU (primary compositor GPU)
amdxdna      — XDNA2 NPU (loads at t≈2.64s)
nouveau      — ⚠️ MUST BE BLACKLISTED — conflicts with akmod-nvidia
asus_wmi     — ASUS platform driver (loading natively)
asus-nb-wmi  — ASUS WMI hotkeys, fan control, power profiles
gpu_sched    — AMD GPU scheduling
nvidia       — NVIDIA driver (loads after nouveau blacklist + reboot)
nvidia_drm   — DRM bridge for PRIME offload
nvidia_modeset — Modeset for NVIDIA
```

**Blacklist path:** `/etc/modprobe.d/` — managed by `hardware/.../tasks/nvidia.yml`

---

## Verified Commands

```bash
# GPU topology
lspci | grep -E "VGA|3D|Display"
# Expected:
# 64:00.0 VGA: NVIDIA AD107M [GeForce RTX 4060 Max-Q / Mobile]
# 65:00.0 Display: AMD Strix [Radeon 880M / 890M]

# Active OpenGL renderer (should be AMD in Hybrid mode)
glxinfo | grep "OpenGL renderer"
# Expected: AMD Radeon 890M Graphics (radeonsi, gfx1150, ...)

# NVIDIA PRIME offload test
DRI_PRIME=pci-0000_64_00_0 glxinfo | grep "OpenGL renderer"
# Expected: NVIDIA GeForce RTX 4060 ...

# NPU presence
ls /dev/accel/          # accel0
lsmod | grep amdxdna    # amdxdna 217088 0

# NVIDIA driver (after akmod-nvidia install + reboot)
nvidia-smi
lsmod | grep nvidia     # nvidia, nvidia_drm, nvidia_modeset

# ASUS tools
asusctl profile -l              # list power profiles
asusctl battery -c              # current charge limit
supergfxctl --status            # current GPU mode

# Sleep state
cat /sys/power/mem_sleep        # must show [s2idle]
cat /sys/class/power_supply/BAT*/capacity  # battery %
```

---

## Known Hardware Issues

See `KnownIssues.md` for the full active tracker. Hardware-specific notes:

1. **nouveau conflict:** On fresh Fedora 43, `nouveau` loads by default and conflicts with `akmod-nvidia`. The hardware Ansible role blacklists it via `/etc/modprobe.d/`. Requires initramfs rebuild + reboot.

2. **SDDM locale warning:** `Detected locale "C" with encoding ANSI_X3.4-1968` — fixed by `localectl set-locale LANG=en_US.UTF-8`, automated in the `core` role.

3. **s2idle only:** This hardware does not support S3 (deep sleep). `mem_sleep_default=s2idle` must be in the GRUB kernel cmdline. NVIDIA VRAM preservation requires `NVreg_PreserveVideoMemoryAllocations=1`.

4. **asusd intermittent start:** `asusd` occasionally fails to start on first boot after install. `systemctl enable --now asusd` and a check of `/etc/asusd/` config syntax usually resolves it.

---

```
transcribe ~ grimoire >> hardware substrate mapped // %HARDWARE_LOCKED%
```
