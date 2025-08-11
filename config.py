"""
Configuration Module - Complete REV21 Davenport Configuration
Updated to use existing file structure and naming conventions
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Application Configuration
APP_VERSION = "REV21-1.0.0"
APP_NAME = "Davenport CAM Assistant REV21"
APP_DESCRIPTION = "Professional CAM Programming & Production Analysis Tool"

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Data file paths - Updated to match your existing files
DATA_PATHS = {
    'materials': 'data/material_data.json',
    'materials_simple': 'data/materials.json',
    'jobs': 'data/job_data.json',
    'gears': 'data/gears.json',
    'cams': 'data/davenport_cams.json',
    'cams_data': 'data/cams_data.json',
    'config': 'data/config.json',
    'tool_definitions': 'data/tool_definitions.json',
    'tool_library_side': 'data/tool_library_side.json',
    'threading_cams': 'data/Threading_Cams.json',
    'sfm_guidelines': 'data/sfm_guidelines.json',
    'setup_library': 'data/setup_library.json',
    'quote_templates': 'data/quote_templates.json',
    'cycle_data_75': 'data/75_cycle_time_eff_revs_COMPLETE.json',
    'cycle_data_60': 'data/60_cycle_time_eff_revs.json',
    'cycle_data_45': 'data/45_cycle_time_eff_revs.json',
    'spindle_gears_75': 'data/75_CYCLE_SPINDLE_GEARS_INCH.json',
    'spindle_gears_60': 'data/60_CYCLE_SPINDLE_GEARS_INCH.json',
    'spindle_gears_45': 'data/45_CYCLE_SPINDLE_GEARS_INCH.json'
}

# Streamlit Configuration
CONFIG = {
    "page_title": f"{APP_NAME}",
    "page_icon": "⚙️",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "theme": {
        "primaryColor": "#2a5298",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f8f9fa",
        "textColor": "#262730"
    }
}

# REV21 Davenport Machine Configuration
DAVENPORT_CONFIG = {
    "machine_types": {
        "5_spindle_standard": {
            "name": "5-Spindle Standard",
            "positions": 5,
            "max_diameter": 2.0,
            "max_length": 6.0,
            "cpm_options": [75, 60, 45],
            "description": "Standard 5-spindle Davenport"
        },
        "5_spindle_high_speed": {
            "name": "5-Spindle High Speed",
            "positions": 5,
            "max_diameter": 1.5,
            "max_length": 4.0,
            "cpm_options": [75, 60],
            "description": "High-speed 5-spindle configuration"
        },
        "6_spindle": {
            "name": "6-Spindle",
            "positions": 6,
            "max_diameter": 1.75,
            "max_length": 5.0,
            "cpm_options": [60, 45],
            "description": "6-spindle Davenport machine"
        },
        "8_spindle": {
            "name": "8-Spindle",
            "positions": 8,
            "max_diameter": 1.25,
            "max_length": 3.0,
            "cpm_options": [45],
            "description": "8-spindle high-production machine"
        }
    },
    "default_machine": "5_spindle_standard",
    "default_cpm": 75,
    "default_positions": 5
}
# Add this after DAVENPORT_CONFIG (around line 80)

# Machine Configuration Class
class MachineConfig:
    """Machine configuration class for Davenport machines"""
    
    def __init__(self, machine_type: str = "5_spindle_standard"):
        self.machine_type = machine_type
        self.config = DAVENPORT_CONFIG["machine_types"].get(
            machine_type, 
            DAVENPORT_CONFIG["machine_types"]["5_spindle_standard"]
        )
    
    @property
    def name(self) -> str:
        return self.config["name"]
    
    @property
    def positions(self) -> int:
        return self.config["positions"]
    
    @property
    def max_diameter(self) -> float:
        return self.config["max_diameter"]
    
    @property
    def max_length(self) -> float:
        return self.config["max_length"]
    
    @property
    def cpm_options(self) -> list:
        return self.config["cpm_options"]
    
    @property
    def description(self) -> str:
        return self.config["description"]
    
    def get_cycle_time(self, cpm: int) -> float:
        """Calculate cycle time based on CPM"""
        if cpm in self.cpm_options:
            return 60.0 / cpm
        return 60.0 / self.cpm_options[0]  # Default to first CPM option
    
    def get_index_time(self, cpm: int) -> float:
        """Get index time based on CPM setting"""
        index_times = {75: 0.4, 60: 0.5, 45: 0.7}
        return index_times.get(cpm, 0.5)
    
    def validate_diameter(self, diameter: float) -> bool:
        """Validate if diameter is within machine limits"""
        return 0.0625 <= diameter <= self.max_diameter
    
    def validate_length(self, length: float) -> bool:
        """Validate if length is within machine limits"""
        return 0.125 <= length <= self.max_length
    
    def get_recommended_cpm(self, diameter: float, material: str) -> int:
        """Get recommended CPM based on diameter and material"""
        # Smaller diameters can handle higher CPM
        if diameter <= 0.5:
            return max(self.cpm_options)
        elif diameter <= 1.0:
            return self.cpm_options[min(1, len(self.cpm_options)-1)]
        else:
            return min(self.cpm_options)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "machine_type": self.machine_type,
            "name": self.name,
            "positions": self.positions,
            "max_diameter": self.max_diameter,
            "max_length": self.max_length,
            "cpm_options": self.cpm_options,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(data.get("machine_type", "5_spindle_standard"))

# Material Properties (fallback if data files not available)
MATERIAL_PROPERTIES = {
    "Steel": {
        "density": 0.284,
        "hardness": "Medium",
        "machinability": 75,
        "sfm": 150,
        "cost_per_pound": 0.85,
        "thermal_expansion": 6.5,
        "thermal_conductivity": 25,
        "machining_notes": "Standard feeds and speeds, use carbide tooling",
        "color": "#8B4513"
    },
    "Stainless Steel": {
        "density": 0.29,
        "hardness": "Hard",
        "machinability": 50,
        "sfm": 120,
        "cost_per_pound": 2.15,
        "thermal_expansion": 9.6,
        "thermal_conductivity": 8,
        "machining_notes": "Reduce speeds 20-30%, use positive rake tools",
        "color": "#C0C0C0"
    },
    "Brass": {
        "density": 0.307,
        "hardness": "Soft",
        "machinability": 100,
        "sfm": 300,
        "cost_per_pound": 3.25,
        "thermal_expansion": 10.4,
        "thermal_conductivity": 60,
        "machining_notes": "High speeds possible, watch for work hardening",
        "color": "#FFD700"
    },
    "Bronze": {
        "density": 0.32,
        "hardness": "Medium-Soft",
        "machinability": 90,
        "sfm": 200,
        "cost_per_pound": 4.50,
        "thermal_expansion": 9.8,
        "thermal_conductivity": 26,
        "machining_notes": "Similar to brass but more forgiving",
        "color": "#CD7F32"
    },
    "Aluminum": {
        "density": 0.098,
        "hardness": "Soft",
        "machinability": 150,
        "sfm": 400,
        "cost_per_pound": 1.95,
        "thermal_expansion": 13.1,
        "thermal_conductivity": 120,
        "machining_notes": "High speeds possible, built-up edge concerns",
        "color": "#D3D3D3"
    },
    "Cast Iron": {
        "density": 0.26,
        "hardness": "Medium",
        "machinability": 60,
        "sfm": 100,
        "cost_per_pound": 0.45,
        "thermal_expansion": 6.0,
        "thermal_conductivity": 30,
        "machining_notes": "Good for dry machining, use sharp tools",
        "color": "#36454F"
    },
    "Tool Steel": {
        "density": 0.284,
        "hardness": "Very Hard",
        "machinability": 30,
        "sfm": 80,
        "cost_per_pound": 5.25,
        "thermal_expansion": 6.2,
        "thermal_conductivity": 20,
        "machining_notes": "Very low speeds, ceramic or CBN tooling",
        "color": "#2F4F4F"
    }
}

# REV21 Threading Methods (exact Davenport manual specifications)
THREADING_METHODS = {
    "6:1": {
        "description": "Standard Threading - 6:1 Ratio",
        "rpm_formula": "Work Spindle RPM ÷ 6",
        "combined_ratio": 0.1667,
        "gear_ratios": [
            {"description": "40T to 240T primary", "ratio": 6.0},
            {"description": "Standard cam spacing", "spaces": 6}
        ],
        "speed_range": "Low to Medium Speed",
        "material_suitability": ["Steel", "Cast Iron", "Tool Steel"],
        "cam_spaces": "6 spaces standard",
        "recommended_tpi_range": [8, 32],
        "notes": "Most common threading method for general applications",
        "max_diameter": 2.0,
        "efficiency": 0.85
    },
    "4:1": {
        "description": "Half Speed Threading - 4:1 Ratio",
        "rpm_formula": "Work Spindle RPM ÷ 4",
        "combined_ratio": 0.25,
        "gear_ratios": [
            {"description": "40T to 160T primary", "ratio": 4.0},
            {"description": "Half speed cam", "spaces": 4}
        ],
        "speed_range": "Medium Speed",
        "material_suitability": ["Stainless Steel", "Hard Steel", "Bronze"],
        "cam_spaces": "4 spaces for half speed",
        "recommended_tpi_range": [12, 40],
        "notes": "Ideal for harder materials requiring slower threading speeds",
        "max_diameter": 1.75,
        "efficiency": 0.90
    },
    "2:1": {
        "description": "High Speed Threading - 2:1 Ratio",
        "rpm_formula": "Work Spindle RPM ÷ 2",
        "combined_ratio": 0.5,
        "gear_ratios": [
            {"description": "40T to 80T primary", "ratio": 2.0},
            {"description": "High speed cam", "spaces": 2}
        ],
        "speed_range": "High Speed",
        "material_suitability": ["Brass", "Bronze", "Aluminum"],
        "cam_spaces": "2 spaces for high speed",
        "recommended_tpi_range": [16, 56],
        "notes": "Best for soft, free-machining materials at high production rates",
        "max_diameter": 1.5,
        "efficiency": 0.95
    }
}

# Tool Definitions (fallback if data files not available)
TOOL_DEFINITIONS = {
    "end_working": {
        "DRILL": {
            "description": "Standard HSS Twist Drill",
            "type": "drilling",
            "material_suitability": ["Steel", "Brass", "Aluminum"],
            "recommended_feed": 0.005,
            "max_depth": 2.0,
            "diameter_range": [0.0625, 1.0],
            "tool_life": 500,
            "cost": 15.00
        },
        "CENTER DRILL": {
            "description": "60° Center Drill",
            "type": "center_drilling",
            "material_suitability": ["Steel", "Stainless Steel", "Cast Iron"],
            "recommended_feed": 0.003,
            "max_depth": 0.25,
            "diameter_range": [0.0625, 0.5],
            "tool_life": 300,
            "cost": 25.00
        },
        "REAMER": {
            "description": "Machine Reamer HSS",
            "type": "reaming",
            "material_suitability": ["Steel", "Brass", "Bronze"],
            "recommended_feed": 0.008,
            "max_depth": 1.5,
            "diameter_range": [0.125, 1.0],
            "tool_life": 800,
            "cost": 35.00
        },
        "TAP": {
            "description": "Machine Tap HSS",
            "type": "tapping",
            "material_suitability": ["Steel", "Brass", "Aluminum"],
            "recommended_feed": 0.050,
            "max_depth": 1.0,
            "diameter_range": [0.125, 0.75],
            "tool_life": 200,
            "cost": 45.00
        },
        "COUNTERBORE": {
            "description": "Counterbore End Mill",
            "type": "counterboring",
            "material_suitability": ["Steel", "Aluminum", "Brass"],
            "recommended_feed": 0.006,
            "max_depth": 0.5,
            "diameter_range": [0.25, 1.0],
            "tool_life": 400,
            "cost": 55.00
        },
        "COUNTERSINK": {
            "description": "82° Countersink",
            "type": "countersinking",
            "material_suitability": ["Steel", "Aluminum", "Brass"],
            "recommended_feed": 0.004,
            "max_depth": 0.25,
            "diameter_range": [0.25, 1.0],
            "tool_life": 600,
            "cost": 30.00
        }
    },
    "side_working": {
        "KNURL": {
            "description": "Diamond Knurling Tool",
            "type": "knurling",
            "material_suitability": ["Steel", "Brass", "Aluminum"],
            "recommended_feed": 0.003,
            "max_engagement": 0.5,
            "force_rating": 500,
            "tool_life": 2000,
            "cost": 125.00
        },
        "SHAVE": {
            "description": "Shaving Tool Carbide",
            "type": "shaving",
            "material_suitability": ["Steel", "Stainless Steel"],
            "recommended_feed": 0.002,
            "max_engagement": 1.0,
            "surface_finish": 32,
            "tool_life": 1500,
            "cost": 85.00
        },
        "CUTOFF": {
            "description": "Parting Tool HSS",
            "type": "cutoff",
            "material_suitability": ["Steel", "Brass", "Bronze"],
            "recommended_feed": 0.004,
            "max_width": 0.125,
            "max_diameter": 2.0,
            "tool_life": 300,
            "cost": 40.00
        },
        "FORM TOOL": {
            "description": "Custom Form Tool",
            "type": "forming",
            "material_suitability": ["Steel", "Brass", "Bronze"],
            "recommended_feed": 0.003,
            "max_engagement": 0.75,
            "custom_profile": True,
            "tool_life": 1000,
            "cost": 150.00
        },
        "THREAD ROLL": {
            "description": "Thread Rolling Tool",
            "type": "thread_rolling",
            "material_suitability": ["Steel", "Stainless Steel"],
            "recommended_feed": 0.050,
            "max_diameter": 1.0,
            "thread_range": [8, 32],
            "tool_life": 5000,
            "cost": 200.00
        }
    }
}

# Default Tools (organized by category)
DEFAULT_TOOLS_END = [
    "None", "DRILL", "CENTER DRILL", "REAMER", "TAP", 
    "COUNTERBORE", "COUNTERSINK", "BORING BAR"
]

DEFAULT_TOOLS_SIDE = [
    "None", "KNURL", "SHAVE", "CUTOFF", "FORM TOOL", 
    "THREAD ROLL", "GROOVE TOOL", "CHAMFER TOOL"
]

# Knurling Specifications (REV21 Professional)
KNURLING_SPECIFICATIONS = {
    "14 Pitch Diamond": {
        "pitch": 0.0714,
        "penetration": 0.0050,
        "type": "Diamond",
        "force_factor": 1.0,
        "finish_factor": 1.0,
        "description": "Standard diamond knurl - 14 pitch"
    },
    "20 Pitch Diamond": {
        "pitch": 0.0500,
        "penetration": 0.0035,
        "type": "Diamond", 
        "force_factor": 0.8,
        "finish_factor": 1.2,
        "description": "Fine diamond knurl - 20 pitch"
    },
    "30 Pitch Diamond": {
        "pitch": 0.0333,
        "penetration": 0.0025,
        "type": "Diamond",
        "force_factor": 0.6,
        "finish_factor": 1.5,
        "description": "Very fine diamond knurl - 30 pitch"
    },
    "14 Pitch Straight": {
        "pitch": 0.0714,
        "penetration": 0.0040,
        "type": "Straight",
        "force_factor": 0.9,
        "finish_factor": 0.9,
        "description": "Standard straight knurl - 14 pitch"
    },
    "20 Pitch Straight": {
        "pitch": 0.0500,
        "penetration": 0.0030,
        "type": "Straight",
        "force_factor": 0.7,
        "finish_factor": 1.1,
        "description": "Fine straight knurl - 20 pitch"
    }
}

# Cost Parameters (fallback if quote_templates.json not available)
COST_PARAMETERS = {
    "overhead_rates": {
        "shop_overhead": 0.35,
        "administrative": 0.15,
        "profit_margin": 0.20,
        "tooling_amortization": 0.05,
        "quality_control": 0.08
    },
    "labor_rates": {
        "setup_hour": 85.00,
        "machine_hour": 65.00,
        "programming_hour": 95.00,
        "quality_hour": 75.00,
        "inspection_hour": 70.00
    },
    "machine_costs": {
        "davenport_5_spindle": {
            "hourly_rate": 45.00,
            "setup_cost": 125.00,
            "tooling_cost_per_hour": 8.50,
            "maintenance_factor": 0.12
        },
        "davenport_6_spindle": {
            "hourly_rate": 55.00,
            "setup_cost": 150.00,
            "tooling_cost_per_hour": 10.00,
            "maintenance_factor": 0.15
        },
        "davenport_8_spindle": {
            "hourly_rate": 65.00,
            "setup_cost": 200.00,
            "tooling_cost_per_hour": 12.00,
            "maintenance_factor": 0.18
        }
    },
    "quantity_breaks": {
        "prototype": {
            "min_qty": 1,
            "max_qty": 100,
            "setup_factor": 1.5,
            "material_factor": 1.2,
            "overhead_factor": 1.3
        },
        "production": {
            "min_qty": 100,
            "max_qty": 10000,
            "setup_factor": 1.0,
            "material_factor": 1.0,
            "overhead_factor": 1.0
        },
        "annual": {
            "min_qty": 10000,
            "max_qty": 1000000,
            "setup_factor": 0.8,
            "material_factor": 0.9,
            "overhead_factor": 0.85
        }
    },
    "material_waste_factors": {
        "Steel": 0.08,
        "Stainless Steel": 0.12,
        "Brass": 0.06,
        "Bronze": 0.06,
        "Aluminum": 0.05,
        "Cast Iron": 0.10,
        "Tool Steel": 0.15
    },
    "default_markups": {
        "prototype": 45,
        "production": 35,
        "annual": 25,
        "rush_job": 60
    }
}

# Cost Factors (material-based cost multipliers)
COST_FACTORS = {
    "material_factors": {
        "Steel": 1.0,
        "Stainless Steel": 1.8,
        "Brass": 2.2,
        "Bronze": 2.5,
        "Aluminum": 1.3,
        "Cast Iron": 0.8,
        "Tool Steel": 3.2
    },
    "complexity_factors": {
        "simple": 1.0,
        "moderate": 1.15,
        "complex": 1.35,
        "very_complex": 1.55
    },
    "operation_factors": {
        "drilling": 1.0,
        "reaming": 1.1,
        "tapping": 1.3,
        "threading": 1.4,
        "knurling": 1.2,
        "forming": 1.6,
        "cutoff": 1.1
    },
    "volume_factors": {
        "prototype": 1.5,
        "production": 1.0,
        "annual": 0.85
    }
}

# Validation Rules
VALIDATION_RULES = {
    "diameter": {
        "min": 0.0625,
        "max": 2.0,
        "increment": 0.0625,
        "tolerance": 0.0001
    },
    "length": {
        "min": 0.125,
        "max": 6.0,
        "increment": 0.125,
        "tolerance": 0.001
    },
    "rpm": {
        "min": 50,
        "max": 2000,
        "increment": 10,
        "common_values": [300, 400, 500, 600, 800, 1000, 1200, 1500]
    },
    "feed_rate": {
        "min": 0.0005,
        "max": 0.050,
        "increment": 0.0005,
        "decimal_places": 4
    },
    "surface_speed": {
        "min": 50,
        "max": 800,
        "increment": 10,
        "optimal_range": {
            "Steel": [120, 180],
            "Stainless Steel": [80, 140],
            "Brass": [200, 400],
            "Bronze": [150, 250],
            "Aluminum": [300, 600],
            "Cast Iron": [80, 120]
        }
    }
}

# Session State Keys
SESSION_KEYS = {
    "setup_data": {},
    "spindle_data": [],
    "thread_calc_results": {},
    "quote_data": {},
    "machine_config": {},
    "current_job": None,
    "last_modified": None,
    "backup_timestamp": None,
    "user_preferences": {},
    "calculation_cache": {},
    "active_tab": "Job Setup"
}

# UI Constants
UI_CONSTANTS = {
    "page_width": "wide",
    "sidebar_width": 300,
    "chart_height": 400,
    "table_height": 300,
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "timeout_seconds": 30,
    "refresh_interval": 1000
}

# File Format Constants
FILE_FORMATS = {
    "export_formats": [".xlsx", ".csv", ".pdf", ".json"],
    "import_formats": [".json", ".csv", ".xlsx"],
    "backup_format": ".json",
    "report_format": ".pdf"
}

# Performance Constants
PERFORMANCE_CONSTANTS = {
    "cache_size": 1000,
    "max_calculations": 10000,
    "batch_size": 100,
    "memory_limit": "500MB",
    "calculation_timeout": 30
}

# Error Messages
ERROR_MESSAGES = {
    "file_not_found": "Data file not found. Using default values.",
    "invalid_data": "Invalid data format detected. Please check file structure.",
    "calculation_error": "Calculation error occurred. Please verify inputs.",
    "connection_error": "Connection error. Please check your network.",
    "permission_error": "Permission denied. Please check file permissions.",
    "memory_error": "Insufficient memory. Please close other applications.",
    "timeout_error": "Operation timed out. Please try again."
}

# Success Messages  
SUCCESS_MESSAGES = {
    "data_loaded": "Data loaded successfully",
    "calculation_complete": "Calculations completed successfully",
    "file_saved": "File saved successfully",
    "backup_created": "Backup created successfully",
    "session_restored": "Session restored successfully",
    "export_complete": "Export completed successfully"
}

# Application Settings
SETTINGS = {
    "debug_mode": False,
    "auto_save": True,
    "auto_backup": True,
    "backup_interval": 300,  # seconds
    "max_backups": 10,
    "show_tooltips": True,
    "show_warnings": True,
    "decimal_precision": 4,
    "angle_precision": 2,
    "force_precision": 1
}

# Export this configuration for other modules
__all__ = [
    'APP_VERSION', 'APP_NAME', 'APP_DESCRIPTION',
    'DATA_PATHS', 'CONFIG', 'DAVENPORT_CONFIG',
    'MATERIAL_PROPERTIES', 'THREADING_METHODS', 'TOOL_DEFINITIONS',
    'DEFAULT_TOOLS_END', 'DEFAULT_TOOLS_SIDE', 'KNURLING_SPECIFICATIONS',
    'COST_PARAMETERS', 'COST_FACTORS', 'VALIDATION_RULES', 'SESSION_KEYS',
    'UI_CONSTANTS', 'FILE_FORMATS', 'PERFORMANCE_CONSTANTS',
    'ERROR_MESSAGES', 'SUCCESS_MESSAGES', 'SETTINGS'
]