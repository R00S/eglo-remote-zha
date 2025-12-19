"""Device handler for AwoX 99099 Remote (Eglo Remote 2.0)

Last Modified: 2025-12-19 10:01:00 CET
Changes: Added OnOff cluster back and power button triggers (button_1_press, button_2_press)

This quirk provides simple, numbered button control for the AwoX ERCU_3groups_Zm remote.
Button mapping:
- Button 1: Power ON (left) - button_1_press
- Button 2: Power OFF (right) - button_2_press
- Button 3: Color Green (top) - button_3_press/hold
- Button 4: Color Red (left) - button_4_press/hold
- Button 5: Color Blue (right) - button_5_press/hold
- Button 6: Color Cycle (middle) - button_6_press/hold
- Button 7: Dim Up - button_7_press/hold
- Button 8: Dim Down - button_8_press/hold
- Button 9: Color Temp Warm - button_9_press/hold
- Button 10: Color Temp Cold - button_10_press/hold
- Button 11: Candle/Refresh - button_11_press/hold
- Button 12: Fav 1 - button_12_press (recall) / button_12_hold (store)
- Button 13: Fav 2 - button_13_press (recall) / button_13_hold (store)

Clean, predictable event names for use in automations and blueprints.
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
                    OnOff.cluster_id,  # Needed for power buttons
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
        # Button 1: Power ON (left)
        (SHORT_PRESS, "button_1_press"): {COMMAND: COMMAND_ON, CLUSTER_ID: 6, ENDPOINT_ID: 1},
        
        # Button 2: Power OFF (right)
        (SHORT_PRESS, "button_2_press"): {COMMAND: COMMAND_OFF, CLUSTER_ID: 6, ENDPOINT_ID: 1},
        
        # Button 3: Color Green (top)
        (SHORT_PRESS, "button_3_press"): {
            COMMAND: COMMAND_AWOX_COLOR,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color": 85},
        },
        (LONG_PRESS, "button_3_hold"): {
            COMMAND: COMMAND_MOVE_TO_HUE_SATURATION,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"hue": 85},
        },
        
        # Button 4: Color Red (left)
        (SHORT_PRESS, "button_4_press"): {
            COMMAND: COMMAND_AWOX_COLOR,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color": 255},
        },
        (LONG_PRESS, "button_4_hold"): {
            COMMAND: COMMAND_MOVE_TO_HUE_SATURATION,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"hue": 255},
        },
        
        # Button 5: Color Blue (right)
        (SHORT_PRESS, "button_5_press"): {
            COMMAND: COMMAND_AWOX_COLOR,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color": 170},
        },
        (LONG_PRESS, "button_5_hold"): {
            COMMAND: COMMAND_MOVE_TO_HUE_SATURATION,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"hue": 170},
        },
        
        # Button 6: Color Cycle (middle)
        (SHORT_PRESS, "button_6_press"): {
            COMMAND: COMMAND_ENHANCED_MOVE_HUE,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"move_mode": 1},
        },
        (LONG_PRESS, "button_6_hold"): {
            COMMAND: COMMAND_ENHANCED_MOVE_HUE,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"move_mode": 3},
        },
        
        # Button 7: Dim Up
        (SHORT_PRESS, "button_7_press"): {
            COMMAND: COMMAND_STEP_ON_OFF,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"step_mode": 0},
        },
        (LONG_PRESS, "button_7_hold"): {
            COMMAND: COMMAND_MOVE_TO_LEVEL_ON_OFF,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"level": 254},
        },
        
        # Button 8: Dim Down
        (SHORT_PRESS, "button_8_press"): {
            COMMAND: COMMAND_STEP_ON_OFF,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"step_mode": 1},
        },
        (LONG_PRESS, "button_8_hold"): {
            COMMAND: COMMAND_MOVE_TO_LEVEL_ON_OFF,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"level": 1},
        },
        
        # Button 9: Color Temp Warm
        (SHORT_PRESS, "button_9_press"): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"step_mode": 1},
        },
        (LONG_PRESS, "button_9_hold"): {
            COMMAND: COMMAND_MOVE_TO_COLOR_TEMP,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color_temp_mireds": 454},
        },
        
        # Button 10: Color Temp Cold
        (SHORT_PRESS, "button_10_press"): {
            COMMAND: COMMAND_STEP_COLOR_TEMP,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"step_mode": 3},
        },
        (LONG_PRESS, "button_10_hold"): {
            COMMAND: COMMAND_MOVE_TO_COLOR_TEMP,
            CLUSTER_ID: 768,
            ENDPOINT_ID: 1,
            PARAMS: {"color_temp_mireds": 153},
        },
        
        # Button 11: Candle/Refresh
        (SHORT_PRESS, "button_11_press"): {
            COMMAND: COMMAND_AWOX_REFRESH,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"press": 1},
        },
        (LONG_PRESS, "button_11_hold"): {
            COMMAND: COMMAND_AWOX_REFRESH,
            CLUSTER_ID: 8,
            ENDPOINT_ID: 1,
            PARAMS: {"press": 2},
        },
        
        # Button 12: Fav 1 (Recall scene 1 / Store scene 1)
        (SHORT_PRESS, "button_12_press"): {
            COMMAND: COMMAND_RECALL,
            CLUSTER_ID: 5,
            ENDPOINT_ID: 1,
            PARAMS: {"scene_id": 1},
        },
        (LONG_PRESS, "button_12_hold"): {
            COMMAND: COMMAND_STORE,
            CLUSTER_ID: 5,
            ENDPOINT_ID: 1,
            PARAMS: {"scene_id": 1},
        },
        
        # Button 13: Fav 2 (Recall scene 2 / Store scene 2)
        (SHORT_PRESS, "button_13_press"): {
            COMMAND: COMMAND_RECALL,
            CLUSTER_ID: 5,
            ENDPOINT_ID: 1,
            PARAMS: {"scene_id": 2},
        },
        (LONG_PRESS, "button_13_hold"): {
            COMMAND: COMMAND_STORE,
            CLUSTER_ID: 5,
            ENDPOINT_ID: 1,
            PARAMS: {"scene_id": 2},
        },
    }
