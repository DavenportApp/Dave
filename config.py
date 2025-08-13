"""
Configuration and constants for the Davenport CAM Assistant
Contains tool definitions, machine configurations, and global settings
"""

import json
import os

# Hardcoded Davenport configuration (simplified)
DAVENPORT_CONFIG = {
    "max_rpm": 4500,
    "positions": 5,
    "cycle_rates": [75, 60, 45],
    "block_ranges": {
        1: (0.8, 1.2),
        2: (0.8, 1.2),
        3: (0.8, 1.2),
        4: (0.8, 1.2),
        5: (0.8, 1.2)
    }
}

# Load tool definitions and config
def load_config_files():
    """Load tool definitions and configuration from JSON files"""
    try:
        with open("tool_definitions.json", "r") as f:
            tool_definitions = json.load(f)
            # Convert feed_range lists back to tuples
            for tool_name, tool_data in tool_definitions.items():
                if "feed_range" in tool_data:
                    tool_data["feed_range"] = tuple(tool_data["feed_range"])
    except FileNotFoundError:
        tool_definitions = {}

    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            # Convert string keys to integers for block_setting_ranges
            if "block_setting_ranges" in config:
                config["block_setting_ranges"] = {int(k): tuple(v) for k, v in config["block_setting_ranges"].items()}
    except FileNotFoundError:
        config = {}
    
    return tool_definitions, config

# Initialize configurations
TOOL_DEFINITIONS, CONFIG = load_config_files()

# Fallback configurations if files don't exist
if not CONFIG:
    CONFIG = {
        "block_setting_ranges": DAVENPORT_CONFIG["block_ranges"],
        "threading_tools": ["TAP", "DIE HEAD", "THREAD ROLL"],
        "default_tools_end": ["DRILL", "REAMER", "TAP", "DIE HEAD", "CENTER"],
        "default_tools_side": ["BOXTOOL", "FORM TOOL", "SHAVE", "KNURL", "BROACH"]
    }

if not TOOL_DEFINITIONS:
    TOOL_DEFINITIONS = {
        "DRILL": {"type": "TURNING"},
        "REAMER": {"type": "TURNING"},
        "TAP": {"type": "TURNING"},
        "DIE HEAD": {"type": "TURNING"},
        "CENTER": {"type": "TURNING"},
        "BOXTOOL": {"type": "TURNING"},
        "FORM TOOL": {"type": "FORM"},
        "SHAVE": {"type": "FORM"},
        "KNURL": {"type": "FORM"},
        "BROACH": {"type": "TURNING"},
        "THREAD ROLL": {"type": "FORM"}
    }

# Extract constants from CONFIG
BLOCK_SETTING_RANGES = CONFIG.get("block_setting_ranges", {})
THREADING_TOOLS = CONFIG.get("threading_tools", [])
DEFAULT_TOOLS_END = CONFIG.get("default_tools_end", [])
DEFAULT_TOOLS_SIDE = CONFIG.get("default_tools_side", [])