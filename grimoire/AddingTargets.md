# AddingTargets.md — Hardware Target Guide

```
transcribe ~ grimoire >> expanding the hardware substrate // %TARGET_PROTOCOL%
```

This guide walks through adding a new hardware target to RaBbLE-OS. The pattern is consistent across all targets — create the role, add inventory entries, reference in site.yml, add a bootstrap menu option.

---

## Example: ASUS ROG Zephyrus G14

### 1. Create the Ansible role directory

```bash
mkdir -p ansible/roles/hardware/x64/asus_rog_g14/{tasks,defaults,handlers,templates,files}
```

### 2. Create tasks/main.yml

```yaml
# ansible/roles/hardware/x64/asus_rog_g14/tasks/main.yml
- name: Include subtasks
  ansible.builtin.include_tasks: "{{ item }}"
  loop:
    - amd_gfx.yml      # copy and adapt from asus_proart_p16 as reference
    - asusctl.yml
    - power.yml
  tags: always
```

### 3. Create defaults/main.yml

```yaml
# ansible/roles/hardware/x64/asus_rog_g14/defaults/main.yml
rabble_rog_g14_power_profile: balanced
rabble_rog_g14_gpu_mode: Hybrid
```

### 4. Add group_vars

```yaml
# ansible/inventory/group_vars/asus_rog_g14.yml
rabble_hidpi_scale: 1
rabble_gfx_mode: "2560x1600x165,auto"
rabble_console_font: "ter-v24b"
rabble_hypr_monitor: "eDP-1,2560x1600@165,0x0,1.6"
rabble_hypr_monitor_fallback: ",preferred,auto,1"
```

### 5. Add the host to inventory

```yaml
# ansible/inventory/hosts.yml — add under the appropriate group:
asus_rog_g14:
  hosts:
    my-rog-laptop:
      ansible_host: localhost
      ansible_connection: local
      ansible_user: myuser
```

### 6. Reference in site.yml

```yaml
# ansible/site.yml — add after the ProArt P16 block:
- name: Hardware layer — ASUS ROG G14
  hosts: asus_rog_g14
  become: true
  tags: [hardware, asus_rog_g14]
  roles:
    - role: hardware/x64/asus_rog_g14
```

### 7. Add to the hardware bootstrap menu

```bash
# bootstrap/menus/hardware.menu.sh — add a new option:
draw_menu "Hardware Layer" \
    "Auto-detect and deploy" \
    "ASUS ProArt P16 (hybrid GFX + NPU + asusctl)" \
    "ASUS ROG G14 (hybrid GFX + asusctl)" \   # ← new
    "Generic x64" \
    "← Back"

# Add the matching case:
3) run_named_playbook "deploy-hardware" --extra-vars "rabble_target=asus_rog_g14" ;;
```

### 8. Dry-run and apply

```bash
# Dry-run first
ansible-playbook \
  -i ansible/inventory/hosts.yml \
  ansible/deploy-hardware.yml \
  --extra-vars "rabble_target=asus_rog_g14" \
  --check --diff

# Then apply
./bootstrap.sh → Deploy by layer → Hardware layer → [your target]
```

---

## aarch64 Targets (SBCs)

Same pattern, but under `ansible/roles/hardware/aarch64/<target>/` and add to the `aarch64` host group in inventory.

The `boot/grub2` role may need adjustment for U-Boot based systems — consider a separate `boot/uboot` role for SBC targets that lack GRUB EFI support.

---

## DMI Verification (Planned)

Hardware roles should self-verify using DMI data before applying machine-specific configuration. Once implemented, each hardware role's `tasks/main.yml` will include a verification step:

```yaml
- name: Verify hardware target matches
  ansible.builtin.fail:
    msg: "This role targets {{ expected_dmi_product }} — running on {{ ansible_product_name }}. Pass -e rabble_skip_dmi_check=true to override."
  when:
    - not rabble_skip_dmi_check | default(false)
    - ansible_product_name != expected_dmi_product
```

This prevents accidentally applying ASUS-specific config to non-ASUS hardware.

---

```
transcribe ~ grimoire >> target protocol documented // %TARGET_PROTOCOL_LOCKED%
```
