"""Device handler for AwoX 99099 Remote (Eglo Remote 2.0) with 3-Bank Support

This quirk adds support for the 3-bank functionality of the AwoX ERCU_3groups_Zm remote.
The remote has buttons 1, 2, 3 that select which group (bank) is active.
All control button presses include a groupID (32778/32779/32780) in the Zigbee message.

This quirk exposes 66 separate device automation triggers:
- 22 unique actions (short/long press on 13 control buttons)
- × 3 banks
- = 66 total triggers with group suffix (_1, _2, _3)
"""

from zigpy.profiles import zha
from zigpy.quirks import CustomCluster, CustomDevice
import zigpy.types as t
from zigpy.zcl import foundation
from zigpy.zcl.clusters.general import (
    Basic,
    Groups,
    Identify,
    LevelControl,
    OnOff,
    Scenes,
)
from zigpy.zcl.clusters.lighting import Color
from zigpy.zcl.clusters.lightlink import LightLink

from zhaquirks.const import (
    CLUSTER_ID,
    COMMAND,
    COMMAND_MOVE_TO_LEVEL_ON_OFF,
    COMMAND_OFF,
    COMMAND_ON,
    COMMAND_STEP_COLOR_TEMP,
    COMMAND_STEP_ON_OFF,
    DEVICE_TYPE,
    DIM_DOWN,
    DIM_UP,
    ENDPOINT_ID,
    ENDPOINTS,
    INPUT_CLUSTERS,
    LONG_PRESS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PARAMS,
    PROFILE_ID,
    SHORT_PRESS,
    TURN_OFF,
    TURN_ON,
)

# Command definitions
COMMAND_AWOX_COLOR = "awox_color"
COMMAND_AWOX_REFRESH = "awox_refresh"
COMMAND_ENHANCED_MOVE_HUE = "enhanced_move_hue"
COMMAND_MOVE_TO_COLOR_TEMP = "move_to_color_temp"
COMMAND_MOVE_TO_HUE_SATURATION = "move_to_hue_and_saturation"
COMMAND_RECALL = "recall"

# Touchlink group IDs used by the remote
GROUP_ID_1 = 0x800A  # 32778 - Bank 1
GROUP_ID_2 = 0x800B  # 32779 - Bank 2
GROUP_ID_3 = 0x800C  # 32780 - Bank 3

# Map group IDs to logical bank numbers
GROUP_TO_BANK = {
    GROUP_ID_1: 1,
    GROUP_ID_2: 2,
    GROUP_ID_3: 3,
}


class Awox99099Remote3Banks(CustomDevice):
    """Custom device representing AwoX 99099 remote with 3-bank support"""

    class AwoxOnOffCluster(CustomCluster, OnOff):
        """Custom OnOff Cluster with group tracking"""

        def handle_cluster_request(
            self,
            hdr: foundation.ZCLHeader,
            args: list,
            *,
            dst_addressing=None,
        ):
            """Handle cluster request and extract group ID."""
            import logging
            _LOGGER = logging.getLogger(__name__)
            
            # Debug: Log everything we can see
            _LOGGER.warning(
                "AwoxOnOffCluster: cmd_id=%s, dst_addressing=%s, "
                "has_group=%s, group=%s",
                hdr.command_id,
                dst_addressing,
                hasattr(dst_addressing, 'group') if dst_addressing else False,
                getattr(dst_addressing, 'group', None) if dst_addressing else None
            )
            
            # Extract group ID from destination addressing
            group_id = None
            if dst_addressing and hasattr(dst_addressing, 'group'):
                group_id = dst_addressing.group
                _LOGGER.warning("AwoxOnOffCluster: Extracted group_id=%s", group_id)
                
            # Map group ID to bank number
            bank = GROUP_TO_BANK.get(group_id, 1) if group_id else 1
            _LOGGER.warning("AwoxOnOffCluster: Mapped to bank=%s", bank)
            
            # Store bank for potential use
            self._current_bank = bank
            
            return super().handle_cluster_request(
                hdr, args, dst_addressing=dst_addressing
            )

    class AwoxScenesCluster(CustomCluster, Scenes):
        """Custom Scenes Cluster with group tracking"""

        def handle_cluster_request(
            self,
            hdr: foundation.ZCLHeader,
            args: list,
            *,
            dst_addressing=None,
        ):
            """Handle cluster request and extract group ID."""
            # Extract group ID from destination addressing
            group_id = None
            if dst_addressing and hasattr(dst_addressing, 'group'):
                group_id = dst_addressing.group
                
            # Map group ID to bank number
            bank = GROUP_TO_BANK.get(group_id, 1) if group_id else 1
            
            # Store bank for potential use
            self._current_bank = bank
            
            return super().handle_cluster_request(
                hdr, args, dst_addressing=dst_addressing
            )

    class AwoxColorCluster(CustomCluster, Color):
        """Awox Remote Custom Color Cluster with group tracking"""

        server_commands = Color.server_commands.copy()
        server_commands[0x30] = foundation.ZCLCommandDef(
            COMMAND_AWOX_COLOR,
            {"param1": t.uint8_t, "color": t.uint8_t},
            is_manufacturer_specific=True,
        )

        def handle_cluster_request(
            self,
            hdr: foundation.ZCLHeader,
            args: list,
            *,
            dst_addressing=None,
        ):
            """Handle cluster request and extract group ID."""
            # Extract group ID from destination addressing
            group_id = None
            if dst_addressing and hasattr(dst_addressing, 'group'):
                group_id = dst_addressing.group
                
            # Map group ID to bank number
            bank = GROUP_TO_BANK.get(group_id, 1) if group_id else 1
            
            # Store bank for potential use
            self._current_bank = bank
            
            # Get the command name
            cmd_name = self.server_commands.get(hdr.command_id)
            if cmd_name and hasattr(cmd_name, 'name'):
                cmd_name = cmd_name.name
            
            # For manufacturer-specific commands or standard commands,
            # the parent class will handle event emission
            # We'll let the standard device_automation_triggers handle the mapping
            
            return super().handle_cluster_request(
                hdr, args, dst_addressing=dst_addressing
            )

    class AwoxLevelControlCluster(CustomCluster, LevelControl):
        """Awox Remote Custom LevelControl Cluster with group tracking"""

        server_commands = LevelControl.server_commands.copy()
        server_commands[0x10] = foundation.ZCLCommandDef(
            "awox_refresh",
            {"param1": t.uint8_t, "press": t.uint8_t},
            is_manufacturer_specific=True,
        )

        def handle_cluster_request(
            self,
            hdr: foundation.ZCLHeader,
            args: list,
            *,
            dst_addressing=None,
        ):
            """Handle cluster request and extract group ID."""
            import logging
            _LOGGER = logging.getLogger(__name__)
            
            # Debug: Log everything we can see
            _LOGGER.warning(
                "AwoxLevelControlCluster: cmd_id=%s, dst_addressing=%s, "
                "has_group=%s, group=%s, args=%s",
                hdr.command_id,
                dst_addressing,
                hasattr(dst_addressing, 'group') if dst_addressing else False,
                getattr(dst_addressing, 'group', None) if dst_addressing else None,
                args
            )
            
            # Extract group ID from destination addressing
            group_id = None
            if dst_addressing and hasattr(dst_addressing, 'group'):
                group_id = dst_addressing.group
                _LOGGER.warning("AwoxLevelControlCluster: Extracted group_id=%s", group_id)
                
            # Map group ID to bank number
            bank = GROUP_TO_BANK.get(group_id, 1) if group_id else 1
            _LOGGER.warning("AwoxLevelControlCluster: Mapped to bank=%s", bank)
            
            # Store bank for potential use
            self._current_bank = bank
            
            # For manufacturer-specific commands or standard commands,
            # the parent class will handle event emission
            # We'll let the standard device_automation_triggers handle the mapping
            
            return super().handle_cluster_request(
                hdr, args, dst_addressing=dst_addressing
            )

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=2048
        # device_version=1
        # input_clusters=[0, 3, 4, 4096]
        # output_clusters=[0, 3, 4, 5, 6, 8, 768, 4096]>
        # <SimpleDescriptor endpoint=3 profile=4751 device_type=2048
        # device_version=1
        # input_clusters=[65360, 65361]
        # output_clusters=[65360, 65361]>
        MODELS_INFO: [("AwoX", "ERCU_3groups_Zm")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.COLOR_CONTROLLER,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    LightLink.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Color.cluster_id,
                    LightLink.cluster_id,
                ],
            },
            3: {
                PROFILE_ID: 0x128F,
                DEVICE_TYPE: zha.DeviceType.COLOR_CONTROLLER,
                INPUT_CLUSTERS: [
                    0xFF50,
                    0xFF51,
                ],
                OUTPUT_CLUSTERS: [
                    0xFF50,
                    0xFF51,
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.COLOR_CONTROLLER,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    LightLink.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    AwoxScenesCluster,
                    AwoxOnOffCluster,
                    AwoxLevelControlCluster,
                    AwoxColorCluster,
                    LightLink.cluster_id,
                ],
            },
            3: {
                PROFILE_ID: 0x128F,
                DEVICE_TYPE: zha.DeviceType.COLOR_CONTROLLER,
                INPUT_CLUSTERS: [
                    0xFF50,
                    0xFF51,
                ],
                OUTPUT_CLUSTERS: [
                    0xFF50,
                    0xFF51,
                ],
            },
        }
    }

    # Base trigger definitions (without group suffix)
    _base_triggers = {
        # Power controls - ON/OFF (short press only)
        (SHORT_PRESS, TURN_ON): {COMMAND: COMMAND_ON, CLUSTER_ID: 6},
        (SHORT_PRESS, TURN_OFF): {COMMAND: COMMAND_OFF, CLUSTER_ID: 6},
        
        # Color controls - Red, Green, Blue, Cycle (short + long press)
        (SHORT_PRESS, "red"): {
            COMMAND: COMMAND_AWOX_COLOR,
            CLUSTER_ID: 768,
            PARAMS: {"color": 255},
        },
        (LONG_PRESS, "red"): {
            COMMAND: COMMAND_MOVE_TO_HUE_SATURATION,
            CLUSTER_ID: 768,
            PARAMS: {"hue": 255},
        },
        (SHORT_PRESS, "green"): {
            COMMAND: COMMAND_AWOX_COLOR,
            CLUSTER_ID: 768,
            PARAMS: {"color": 85},
        },
        (LONG_PRESS, "green"): {
            COMMAND: COMMAND_MOVE_TO_HUE_SATURATION,
            CLUSTER_ID: 768,
            PARAMS: {"hue": 85},
        },
        (SHORT_PRESS, "blue"): {
            COMMAND: COMMAND_AWOX_COLOR,
            CLUSTER_ID: 768,
            PARAMS: {"color": 170},
        },
        (LONG_PRESS, "blue"): {
            COMMAND: COMMAND_MOVE_TO_HUE_SATURATION,
            CLUSTER_ID: 768,
            PARAMS: {"hue": 170},
        },
        (SHORT_PRESS, "cycle"): {
            COMMAND: COMMAND_ENHANCED_MOVE_HUE,
            CLUSTER_ID: 768,
            PARAMS: {"move_mode": 1},
        },
        (LONG_PRESS, "cycle"): {
            COMMAND: COMMAND_ENHANCED_MOVE_HUE,
            CLUSTER_ID: 768,
            PARAMS: {"move_mode": 3},
        },
        
        # Scene controls - Heart 1/2 (short press only)
        (SHORT_PRESS, "heart_1"): {
            COMMAND: COMMAND_RECALL,
            CLUSTER_ID: 5,
            PARAMS: {"scene_id": 1},
        },
        (SHORT_PRESS, "heart_2"): {
            COMMAND: COMMAND_RECALL,
            CLUSTER_ID: 5,
            PARAMS: {"scene_id": 2},
        },
        
        # Brightness controls - Dim Up/Down (short + long press)
        (SHORT_PRESS, DIM_UP): {
            COMMAND: COMMAND_STEP_ON_OFF,
            CLUSTER_ID: 8,
            PARAMS: {"step_mode": 0},
        },
        (LONG_PRESS, DIM_UP): {
            COMMAND: COMMAND_MOVE_TO_LEVEL_ON_OFF,
            CLUSTER_ID: 8,
            PARAMS: {"level": 254},
        },
        (SHORT_PRESS, DIM_DOWN): {
            COMMAND: COMMAND_STEP_ON_OFF,
            CLUSTER_ID: 8,
            PARAMS: {"step_mode": 1},
        },
        (LONG_PRESS, DIM_DOWN): {
            COMMAND: COMMAND_MOVE_TO_LEVEL_ON_OFF,
            CLUSTER_ID: 8,
            PARAMS: {"level": 1},
        },
        
        # Color temperature controls - Warm/Cold (short + long press)
        (SHORT_PRESS, "warm"): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            CLUSTER_ID: 768,
            PARAMS: {"step_mode": 1},
        },
        (LONG_PRESS, "warm"): {
            COMMAND: COMMAND_MOVE_TO_COLOR_TEMP,
            CLUSTER_ID: 768,
            PARAMS: {"color_temp_mireds": 454},
        },
        (SHORT_PRESS, "cold"): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            CLUSTER_ID: 768,
            PARAMS: {"step_mode": 3},
        },
        (LONG_PRESS, "cold"): {
            COMMAND: COMMAND_MOVE_TO_COLOR_TEMP,
            CLUSTER_ID: 768,
            PARAMS: {"color_temp_mireds": 153},
        },
        
        # Special functions - Refresh (short + long press)
        (SHORT_PRESS, "refresh"): {
            COMMAND: COMMAND_AWOX_REFRESH,
            CLUSTER_ID: 8,
            PARAMS: {"press": 1},
        },
        (LONG_PRESS, "refresh"): {
            COMMAND: COMMAND_AWOX_REFRESH,
            CLUSTER_ID: 8,
            PARAMS: {"press": 2},
        },
    }

    # Generate device_automation_triggers with group suffixes
    # 22 base actions × 3 banks = 66 total triggers
    device_automation_triggers = {}
    
    for (press_type, action), trigger_def in _base_triggers.items():
        for bank in [1, 2, 3]:
            # Create action name with bank suffix
            action_with_bank = f"{action}_{bank}"
            
            # Create trigger definition with bank number
            trigger_with_bank = trigger_def.copy()
            trigger_with_bank[ENDPOINT_ID] = 1
            trigger_with_bank["bank"] = bank  # Add bank metadata
            
            # Add to device automation triggers
            device_automation_triggers[(press_type, action_with_bank)] = trigger_with_bank
