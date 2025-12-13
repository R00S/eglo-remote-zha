# Technical Analysis: Automating Setup Steps

## Current Manual Steps

1. **Create ZHA groups (32778, 32779, 32780)** - Potentially automatable
2. **Touchlink binding (hold button 1/2/3 near lights)** - **NOT automatable**

## Why Touchlink Cannot Be Automated

### Hardware-Level Operation

The Touchlink binding is performed **by the remote's firmware**, not by Home Assistant:

1. User holds button 1/2/3 on remote for 10 seconds
2. **Remote's internal firmware** initiates Touchlink commissioning
3. Remote sends Touchlink frames **directly to nearby lights** (radio proximity required)
4. Lights respond and join the group specified by the remote
5. All happens at **Zigbee physical/MAC layer**, below ZHA's control

### Why ZHA Cannot Do This

- ZHA coordinator is typically **far from the lights** (centralized)
- Touchlink requires **physical proximity** (<30cm) for security
- Remote has specialized **Touchlink commissioning** capability
- ZHA coordinator may not support Touchlink commissioning
- Even if it did, ZHA cannot control the remote to tell it which group to use

### Industry Standard

This is the **designed behavior** for Touchlink remotes like:
- Philips Hue Dimmer Switch
- IKEA Trådfri remotes  
- Legrand/BTicino remotes
- **AwoX/Eglo remotes**

All require physical pairing as a **security feature**.

## What We CAN Automate: ZHA Group Creation

### Current Implementation

The quirk could automatically create the required ZHA groups when the remote pairs.

### Implementation Approach

```python
class Awox99099Remote3Banks(CustomDevice):
    """Custom device with auto-group creation"""
    
    def __init__(self, *args, **kwargs):
        """Initialize and ensure groups exist."""
        super().__init__(*args, **kwargs)
        self._ensure_groups_exist()
    
    def _ensure_groups_exist(self):
        """Create ZHA groups if they don't exist."""
        try:
            from homeassistant.components.zha.core.group import Group
            
            required_groups = {
                0x800A: "Eglo Remote - Bank 1",
                0x800B: "Eglo Remote - Bank 2", 
                0x800C: "Eglo Remote - Bank 3",
            }
            
            for group_id, name in required_groups.items():
                # Check if group exists, create if not
                # Implementation depends on ZHA API
                pass
        except Exception as e:
            # Log but don't fail device pairing
            _LOGGER.warning(f"Could not auto-create groups: {e}")
```

### Challenges

1. **ZHA API access** - Quirks run in zigpy layer, ZHA groups are HA layer
2. **Timing** - Groups need to exist before binding, but device pairs first
3. **Coordinator access** - Need reference to ZHA gateway/coordinator
4. **Group persistence** - Groups need to be saved to HA database

## Alternative Approach: Simplify User Experience

Instead of automating, we can **improve the documentation and tools**:

### Option 1: One-Click Group Creator Script

Provide a Python script users run once:

```python
# create_eglo_groups.py
import requests

HA_URL = "http://homeassistant.local:8123"
TOKEN = "your_long_lived_access_token"

groups = [
    {"group_id": 32778, "name": "Eglo Remote - Bank 1"},
    {"group_id": 32779, "name": "Eglo Remote - Bank 2"},
    {"group_id": 32780, "name": "Eglo Remote - Bank 3"},
]

for group in groups:
    # Use HA REST API to create ZHA group
    response = requests.post(
        f"{HA_URL}/api/services/zha/create_group",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json=group
    )
    print(f"Created group {group['name']}: {response.status_code}")
```

### Option 2: Home Assistant Helper Automation

Create an automation that runs once to set up groups:

```yaml
automation:
  - alias: "Eglo Remote - Create Groups (Run Once)"
    trigger:
      - platform: homeassistant
        event: start
    condition:
      - condition: template
        value_template: "{{ state_attr('sensor.eglo_setup', 'groups_created') != 'true' }}"
    action:
      - service: zha.create_group
        data:
          group_id: 32778
          name: "Eglo Remote - Bank 1"
      - service: zha.create_group
        data:
          group_id: 32779
          name: "Eglo Remote - Bank 2"
      - service: zha.create_group
        data:
          group_id: 32780
          name: "Eglo Remote - Bank 3"
```

### Option 3: Blueprint Validation

The blueprint could check for group existence and guide the user:

```yaml
trigger:
  - platform: device
    # ... 

condition:
  # Check if groups exist
  - condition: template
    value_template: >
      {% set groups = integration_entities('zha') | 
                      select('search', 'group') | list %}
      {{ groups | length >= 3 }}

action:
  # If groups don't exist, send notification
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ groups | length < 3 }}"
        sequence:
          - service: notify.persistent_notification
            data:
              title: "Eglo Remote Setup Incomplete"
              message: >
                Please create ZHA groups 32778, 32779, 32780
                in ZHA settings before using this automation.
```

## Recommended Approach

### What We Can Do ✅

1. **Document clearly** that Touchlink is required (one-time, hardware-level)
2. **Provide automation** to create ZHA groups automatically
3. **Add group existence check** to blueprint with helpful error messages
4. **Create setup wizard** that walks users through both steps
5. **Add visual guide** with photos/videos showing the Touchlink process

### What We Cannot Do ❌

1. Automate the Touchlink binding (hardware limitation)
2. Eliminate the physical proximity requirement (security feature)
3. Bypass the 10-second hold on remote (firmware behavior)

## Updated User Experience

### Simplified Setup Flow

**Step 1: Install Quirk via HACS** ✅ (Automated)

**Step 2: Pair Remote with ZHA** ✅ (Standard ZHA process)

**Step 3: Auto-Create Groups** ✅ (NEW: Automated via quirk or helper script)
- Quirk automatically creates groups 32778, 32779, 32780 on first pair
- Or user clicks "Setup Eglo Groups" button in ZHA device page
- Or user runs one-time automation

**Step 4: Bind Lights to Banks** ⚠️ (Physical, cannot automate)
- User performs Touchlink binding (hold button 1/2/3 near lights)
- **This is the ONLY manual step** (required by hardware design)
- Only needs to be done once per light

**Step 5: Configure Blueprint** ✅ (Standard HA process)

## Conclusion

**We CAN eliminate the manual ZHA group creation** by adding auto-creation to the quirk or providing a helper script.

**We CANNOT eliminate the Touchlink binding** because it's a hardware-level operation performed by the remote's firmware, not by Home Assistant. This is intentional design for security (proximity-based pairing).

The best we can do is:
1. ✅ Auto-create ZHA groups (eliminate step 1)
2. ❌ Cannot automate Touchlink (step 2 remains manual but is hardware-required)
3. ✅ Make documentation crystal clear with visual guides
4. ✅ Add helpful error messages if setup incomplete

**Recommendation**: Focus on auto-creating the ZHA groups, and provide excellent documentation/visuals for the one-time Touchlink binding step.
