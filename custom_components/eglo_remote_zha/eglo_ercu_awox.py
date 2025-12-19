"""Device handler for AwoX 99099 Remote (Eglo Remote 2.0)

Last Modified: 2025-12-19 09:32:00 CET
Changes: Remove OnOff cluster entirely - remote sends ON commands but doesn't control device state

This quirk provides simple, single-bank control for the AwoX ERCU_3groups_Zm remote.
It emits 22 button events with hardware long-press support:
- Power: turn_on, turn_off
- Dimming: dim_up, dim_down (short + long versions)
- Colors: color_red, color_green, color_blue, color_cycle (short + long versions)
- Scenes: scene_1, scene_2 (Favourite buttons)
- Color temp: color_temp_up, color_temp_down (short + long versions)
- Candle mode: refresh, refresh_long

Area/light selection is handled by blueprints, not by the quirk.
No bank suffixes (_1, _2, _3) are used in this simplified version.

Note: Power button long press is detected through ZHA event platform in blueprints,
not as separate automation triggers.
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

COMMAND_AWOX_COLOR = "awox_color"
COMMAND_AWOX_REFRESH = "awox_refresh"
COMMAND_ENHANCED_MOVE_HUE = "enhanced_move_hue"
COMMAND_MOVE_TO_COLOR_TEMP = "move_to_color_temp"
COMMAND_MOVE_TO_HUE_SATURATION = "move_to_hue_and_saturation"
COMMAND_RECALL = "recall"
COMMAND_STORE = "store"


class Awox99099Remote(CustomDevice):
    """Custom device representing AwoX 99099 remote (EGLO Remote 2.0)"""

    class AwoxColorCluster(CustomCluster, Color):
        """Awox Remote Custom Color Cluster"""

        server_commands = Color.server_commands.copy()
        server_commands[0x30] = foundation.ZCLCommandDef(
            COMMAND_AWOX_COLOR,
            {"param1": t.uint8_t, "color": t.uint8_t},
            is_manufacturer_specific=True,
        )

    class AwoxLevelControlCluster(CustomCluster, LevelControl):
        """Awox Remote Custom LevelControl Cluster"""

        server_commands = LevelControl.server_commands.copy()
        server_commands[0x10] = foundation.ZCLCommandDef(
            "awox_refresh",
            {"param1": t.uint8_t, "press": t.uint8_t},
            is_manufacturer_specific=True,
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
                    Scenes.cluster_id,
                    # OnOff cluster removed - remote sends ON commands but doesn't control device state
                    # ZHA was auto-generating "On event" for these spurious ON commands
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

    device_automation_triggers = {
        # Power buttons (right=OFF) - left power button doesn't produce COMMAND_ON
        (SHORT_PRESS, TURN_OFF): {COMMAND: COMMAND_OFF, CLUSTER_ID: 6, ENDPOINT_ID: 1},
        
        # Color buttons (Colour top=green, left=red, right=blue, middle=cycle)
        (SHORT_PRESS, "color_green"): {
            COMMAND: COMMAND_AWOX_COLOR,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color": 85},
        },
        (LONG_PRESS, "color_green_long"): {
            COMMAND: COMMAND_MOVE_TO_HUE_SATURATION,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"hue": 85},
        },
        (SHORT_PRESS, "color_red"): {
            COMMAND: COMMAND_AWOX_COLOR,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color": 255},
        },
        (LONG_PRESS, "color_red_long"): {
            COMMAND: COMMAND_MOVE_TO_HUE_SATURATION,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"hue": 255},
        },
        (SHORT_PRESS, "color_cycle"): {
            COMMAND: COMMAND_ENHANCED_MOVE_HUE,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"move_mode": 1},
        },
        (LONG_PRESS, "color_cycle_long"): {
            COMMAND: COMMAND_ENHANCED_MOVE_HUE,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"move_mode": 3},
        },
        (SHORT_PRESS, "color_blue"): {
            COMMAND: COMMAND_AWOX_COLOR,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color": 170},
        },
        (LONG_PRESS, "color_blue_long"): {
            COMMAND: COMMAND_MOVE_TO_HUE_SATURATION,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"hue": 170},
        },
        
        # Candle mode / refresh button
        (SHORT_PRESS, "refresh"): {
            COMMAND: COMMAND_AWOX_REFRESH,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"press": 1},
        },
        (LONG_PRESS, "refresh_long"): {
            COMMAND: COMMAND_AWOX_REFRESH,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"press": 2},
        },
        
        # Dimming buttons - SHORT_PRESS uses DIM_UP/DIM_DOWN constants, LONG_PRESS uses custom strings
        (SHORT_PRESS, DIM_UP): {
            COMMAND: COMMAND_STEP_ON_OFF,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"step_mode": 0},
        },
        (LONG_PRESS, "dim_up_long"): {
            COMMAND: COMMAND_MOVE_TO_LEVEL_ON_OFF,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"level": 254},
        },
        (SHORT_PRESS, DIM_DOWN): {
            COMMAND: COMMAND_STEP_ON_OFF,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"step_mode": 1},
        },
        (LONG_PRESS, "dim_down_long"): {
            COMMAND: COMMAND_MOVE_TO_LEVEL_ON_OFF,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"level": 1},
        },
        
        # Favourite buttons (scene recall/store)
        (SHORT_PRESS, "scene_1"): {
            COMMAND: COMMAND_RECALL,
            CLUSTER_ID: 5,
            ENDPOINT_ID: 1,
            PARAMS: {"scene_id": 1},
        },
        (LONG_PRESS, "scene_1_long"): {
            COMMAND: COMMAND_STORE,
            CLUSTER_ID: 5,
            ENDPOINT_ID: 1,
            PARAMS: {"scene_id": 1},
        },
        (SHORT_PRESS, "scene_2"): {
            COMMAND: COMMAND_RECALL,
            CLUSTER_ID: 5,
            ENDPOINT_ID: 1,
            PARAMS: {"scene_id": 2},
        },
        (LONG_PRESS, "scene_2_long"): {
            COMMAND: COMMAND_STORE,
            CLUSTER_ID: 5,
            ENDPOINT_ID: 1,
            PARAMS: {"scene_id": 2},
        },
        
        # Color temperature buttons (white tone selection)
        (SHORT_PRESS, "color_temp_up"): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"step_mode": 1},
        },
        (LONG_PRESS, "color_temp_up_long"): {
            COMMAND: COMMAND_MOVE_TO_COLOR_TEMP,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color_temp_mireds": 454},
        },
        (SHORT_PRESS, "color_temp_down"): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"step_mode": 3},
        },
        (LONG_PRESS, "color_temp_down_long"): {
            COMMAND: COMMAND_MOVE_TO_COLOR_TEMP,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color_temp_mireds": 153},
        },
    }
