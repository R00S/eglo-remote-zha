"""Device handler for AwoX 99099 Remote (Eglo Remote 2.0)

Last Modified: 2025-12-19 10:30:00 CET
Changes: Removed OnOff cluster permanently - duplicate events cannot be resolved with it present

This quirk fixes duplicate button event issues by removing the OnOff cluster.
The remote sends spurious COMMAND_ON with many buttons, causing ZHA to auto-generate
unwanted "On event" or "Turn On" events. With OnOff cluster removed, all buttons
now produce clean, unique raw Zigbee cluster events:

- Color buttons: Awox Color event / Move To Hue And Saturation event
- Dim buttons: Step On Off event / Move To Level On Off event  
- Color temp buttons: Step Color Temp event / Move To Color Temp event
- Candle button: Awox Refresh event
- Fav buttons: Recall event / Store event

Tradeoff: Power ON/OFF buttons do not generate events (OnOff cluster removed).
Use raw cluster events in automations (event type: zha_event).
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
                    # OnOff cluster REMOVED - causes duplicate "On event" for all color/dim/temp buttons
                    # Power buttons will not work, but all other buttons produce clean, unique events
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

    # No device_automation_triggers defined
    # Remote buttons generate raw Zigbee cluster events that can be used directly in automations
    # Use event type: zha_event and filter by command/params

