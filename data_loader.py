"""
Data Loader Module - Professional Data Management
REV21 Style Implementation with Complete JSON File Loading
"""

import json
import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """Professional data management for CAM operations - REV21 style"""
    
    def __init__(self):
        """Initialize data manager with proper paths"""
        self.base_path = Path(__file__).parent
        self.data_path = self.base_path / "data"
        
        # Ensure data directory exists
        self.data_path.mkdir(exist_ok=True)
        
        # Cache for loaded data
        self._cache = {}
        
        # File mappings - REV21 style organization
        self.file_mappings = {
            "materials": "materials.json",
            "tools_end": "tool_library_end.json",
            "tools_side": "tool_library_side.json",
            "tool_definitions": "tool_definitions.json",
            "threading_cams": "Threading_Cams.json",
            "davenport_cams": "davenport_cams.json",
            "sfm_guidelines": "sfm_guidelines.json",
            "gears": "gears.json",
            "config": "config.json",
            "cams_data": "cams_data.json"
        }
        
        logger.info(f"DataManager initialized with data path: {self.data_path}")
    
    @lru_cache(maxsize=32)
    def load_json_file(self, filename: str) -> Dict[str, Any]:
        """Load JSON file with caching - REV21 style"""
        try:
            file_path = self.data_path / filename
            
            if not file_path.exists():
                logger.warning(f"File not found: {filename}")
                return self._get_fallback_data(filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Successfully loaded: {filename}")
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {filename}: {e}")
            return self._get_fallback_data(filename)
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return self._get_fallback_data(filename)
    
    def load_gear_table(self, cpm_setting: str) -> Dict[str, Any]:
        """Load gear table for specific CPM setting - REV21 style"""
        filename_map = {
            "75": "75_CYCLE_SPINDLE_GEARS_INCH.json",
            "60": "60_CYCLE_SPINDLE_GEARS_INCH.json", 
            "45": "45_CYCLE_SPINDLE_GEARS_INCH.json"
        }
        
        filename = filename_map.get(cpm_setting, "75_CYCLE_SPINDLE_GEARS_INCH.json")
        gear_data = self.load_json_file(filename)
        
        # Process gear data for easier access - REV21 style
        processed_gears = {}
        
        if isinstance(gear_data, dict):
            for gear_combo, data in gear_data.items():
                if isinstance(data, dict):
                    processed_gears[gear_combo] = {
                        "feed_rate": data.get("feed_per_rev", 0.005),
                        "description": data.get("description", "Standard gear"),
                        "ratio": data.get("ratio", 1.0),
                        "applications": data.get("applications", [])
                    }
        
        return processed_gears
    
    def load_cycle_time_data(self, cpm_setting: str = "75") -> Dict[str, Any]:
        """Load cycle time data for CPM setting - REV21 style"""
        filename_map = {
            "75": "75_cycle_time_eff_revs_COMPLETE.json",
            "60": "60_cycle_time_eff_revs.json",
            "45": "45_cycle_time_eff_revs.json"
        }
        
        filename = filename_map.get(cpm_setting, "75_cycle_time_eff_revs_COMPLETE.json")
        return self.load_json_file(filename)
    
    def load_material_data(self) -> Dict[str, Any]:
        """Load material properties and guidelines - REV21 style"""
        materials = self.load_json_file("materials.json")
        sfm_guidelines = self.load_json_file("sfm_guidelines.json")
        
        # Combine material data with SFM guidelines
        combined_data = {}
        
        for material, props in materials.items():
            combined_data[material] = {
                **props,
                "sfm_data": sfm_guidelines.get(material, {})
            }
        
        return combined_data
    
    def load_tool_libraries(self) -> Dict[str, List]:
        """Load complete tool libraries - REV21 style"""
        return {
            "end_working": self.load_json_file("tool_library_end.json"),
            "side_working": self.load_json_file("tool_library_side.json"),
            "definitions": self.load_json_file("tool_definitions.json")
        }
    
    def load_threading_data(self) -> Dict[str, Any]:
        """Load threading cam and configuration data - REV21 style"""
        threading_cams = self.load_json_file("Threading_Cams.json")
        
        # Process threading data for easier access
        processed_threading = {
            "methods": {},
            "cam_configurations": {},
            "gear_recommendations": {}
        }
        
        if isinstance(threading_cams, dict):
            for method, data in threading_cams.items():
                if isinstance(data, dict):
                    processed_threading["methods"][method] = {
                        "description": data.get("description", f"{method} Threading"),
                        "rpm_factor": data.get("rpm_factor", 1.0),
                        "cam_settings": data.get("cam_settings", {}),
                        "gear_ratios": data.get("gear_ratios", []),
                        "applications": data.get("applications", [])
                    }
        
        return processed_threading
    
    def load_davenport_cams(self) -> Dict[str, Any]:
        """Load Davenport cam data - REV21 style"""
        return self.load_json_file("davenport_cams.json")
    
    def load_machine_config(self) -> Dict[str, Any]:
        """Load machine configuration data - REV21 style"""
        config_data = self.load_json_file("config.json")
        
        # Add default machine specifications if missing
        defaults = {
            "machine_type": "5-Spindle",
            "max_rpm": 2000,
            "min_rpm": 100,
            "default_rpm": 600,
            "cpm_settings": ["75", "60", "45"],
            "collet_sizes": ["1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8", "1"],
            "position_count": 5
        }
        
        # Merge with defaults
        for key, value in defaults.items():
            if key not in config_data:
                config_data[key] = value
        
        return config_data
    
    def get_tool_feed_recommendations(self, tool_type: str, material: str) -> Dict[str, float]:
        """Get tool feed recommendations for material - REV21 style"""
        tool_defs = self.load_json_file("tool_definitions.json")
        material_data = self.load_json_file("materials.json")
        
        # Get base tool data
        tool_data = tool_defs.get(tool_type, {})
        material_props = material_data.get(material, {})
        
        # Calculate recommendations
        base_feed = tool_data.get("default_feed", 0.005)
        material_factor = material_props.get("feed_factor", 1.0)
        
        return {
            "recommended_feed": base_feed * material_factor,
            "min_feed": base_feed * material_factor * 0.5,
            "max_feed": base_feed * material_factor * 1.5,
            "surface_speed": material_props.get("sfm", 100)
        }
    
    def get_threading_recommendations(self, thread_type: str, material: str, 
                                   diameter: float) -> Dict[str, Any]:
        """Get threading recommendations - REV21 style"""
        threading_data = self.load_threading_data()
        material_data = self.load_material_data()
        
        material_props = material_data.get(material, {})
        
        # Determine best threading method based on material
        if material in ["Brass", "Bronze", "Aluminum"]:
            recommended_method = "2:1"
        elif material in ["Stainless Steel", "Tool Steel"]:
            recommended_method = "4:1"
        else:
            recommended_method = "6:1"  # Default for steel
        
        method_data = threading_data["methods"].get(recommended_method, {})
        
        # Calculate threading parameters
        base_rpm = 600  # Default setup RPM
        threading_rpm = base_rpm * method_data.get("rpm_factor", 1.0)
        surface_speed = (3.14159 * diameter * threading_rpm) / 12
        
        return {
            "recommended_method": recommended_method,
            "threading_rpm": threading_rpm,
            "surface_speed": surface_speed,
            "method_description": method_data.get("description", ""),
            "cam_settings": method_data.get("cam_settings", {}),
            "gear_ratios": method_data.get("gear_ratios", [])
        }
    
    def get_knurling_specifications(self, knurl_type: str) -> Dict[str, Any]:
        """Get knurling specifications - REV21 style"""
        # Process knurl type to match data structure
        knurl_key = knurl_type.lower().replace(" ", "_")
        
        # Default knurling specifications
        knurl_specs = {
            "12_tpi": {"pitch": 0.0833, "penetration": 0.0050},
            "16_tpi": {"pitch": 0.0625, "penetration": 0.0040},
            "20_tpi": {"pitch": 0.0500, "penetration": 0.0035},
            "25_tpi": {"pitch": 0.0400, "penetration": 0.0030},
            "30_tpi": {"pitch": 0.0333, "penetration": 0.0025},
            "64_dp": {"pitch": 0.0491, "penetration": 0.0040},
            "96_dp": {"pitch": 0.0327, "penetration": 0.0030}
        }
        
        return knurl_specs.get(knurl_key, {
            "pitch": 0.0500,
            "penetration": 0.0035,
            "description": "Standard knurl"
        })
    
    def save_session_data(self, data: Dict[str, Any], filename: str) -> bool:
        """Save session data to file - REV21 style"""
        try:
            file_path = self.data_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Session data saved to: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving session data to {filename}: {e}")
            return False
    
    def load_session_data(self, filename: str) -> Dict[str, Any]:
        """Load session data from file - REV21 style"""
        return self.load_json_file(filename)
    
    def validate_data_files(self) -> Dict[str, bool]:
        """Validate that all required data files exist - REV21 style"""
        validation_results = {}
        
        required_files = [
            "materials.json",
            "tool_definitions.json",
            "75_CYCLE_SPINDLE_GEARS_INCH.json",
            "75_cycle_time_eff_revs_COMPLETE.json",
            "Threading_Cams.json"
        ]
        
        for filename in required_files:
            file_path = self.data_path / filename
            validation_results[filename] = file_path.exists()
            
            if not validation_results[filename]:
                logger.warning(f"Missing required file: {filename}")
        
        return validation_results
    
    def _get_fallback_data(self, filename: str) -> Dict[str, Any]:
        """Get fallback data when file is missing - REV21 style"""
        fallback_data = {
            "materials.json": {
                "Steel": {"sfm": 150, "density": 0.284, "machinability": 75},
                "Brass": {"sfm": 300, "density": 0.307, "machinability": 100},
                "Aluminum": {"sfm": 400, "density": 0.098, "machinability": 100}
            },
            "tool_definitions.json": {
                "DRILL": {"default_feed": 0.005, "type": "End Working"},
                "REAMER": {"default_feed": 0.003, "type": "End Working"},
                "TAP": {"default_feed": 0.002, "type": "End Working"},
                "KNURL": {"default_feed": 0.005, "type": "Side Working"},
                "SHAVE": {"default_feed": 0.003, "type": "Side Working"}
            },
            "Threading_Cams.json": {
                "6:1": {
                    "description": "6:1 Threading (Steel)",
                    "rpm_factor": 1.0,
                    "applications": ["Steel", "General threading"]
                },
                "2:1": {
                    "description": "2:1 Threading (Brass)",
                    "rpm_factor": 2.0,
                    "applications": ["Brass", "Bronze", "High speed"]
                }
            }
        }
        
        return fallback_data.get(filename, {})
    
    def get_file_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all data files - REV21 style"""
        status = {}
        
        for category, filename in self.file_mappings.items():
            file_path = self.data_path / filename
            status[category] = {
                "filename": filename,
                "exists": file_path.exists(),
                "size": file_path.stat().st_size if file_path.exists() else 0,
                "path": str(file_path)
            }
        
        return status
    
    def refresh_cache(self):
        """Clear cache to force reload of data files - REV21 style"""
        self.load_json_file.cache_clear()
        self._cache.clear()
        logger.info("Data cache cleared")
    
    def get_gear_combination_details(self, cpm_setting: str, 
                                   effective_revs: float) -> Dict[str, Any]:
        """Get recommended gear combination for effective revolutions - REV21 style"""
        gear_data = self.load_gear_table(cpm_setting)
        
        best_match = None
        best_score = float('inf')
        
        for gear_combo, data in gear_data.items():
            # Calculate how well this gear matches the required effective revs
            feed_rate = data.get("feed_rate", 0.005)
            if feed_rate > 0:
                # Estimate revolutions needed for typical operation
                estimated_revs = 1.0 / feed_rate  # Rough estimate
                score = abs(estimated_revs - effective_revs)
                
                if score < best_score:
                    best_score = score
                    best_match = {
                        "combination": gear_combo,
                        **data,
                        "match_score": score
                    }
        
        return best_match or {
            "combination": "Standard",
            "feed_rate": 0.005,
            "description": "Default gear combination"
        }
    
    def export_data_summary(self) -> Dict[str, Any]:
        """Export summary of all loaded data - REV21 style"""
        summary = {
            "data_files": self.get_file_status(),
            "material_count": len(self.load_material_data()),
            "tool_count": {
                "end_working": len(self.load_tool_libraries()["end_working"]),
                "side_working": len(self.load_tool_libraries()["side_working"])
            },
            "threading_methods": len(self.load_threading_data()["methods"]),
            "gear_combinations": {
                "75_cpm": len(self.load_gear_table("75")),
                "60_cpm": len(self.load_gear_table("60")),
                "45_cpm": len(self.load_gear_table("45"))
            }
        }
        
        return summary
    
    def get_all_data(self) -> Dict[str, Any]:
        """Get all loaded data in one comprehensive dictionary - REV21 style"""
        return {
            "materials": self.load_material_data(),
            "tools": self.load_tool_libraries(),
            "threading": self.load_threading_data(),
            "davenport_cams": self.load_davenport_cams(),
            "gears": {
                "75_cpm": self.load_gear_table("75"),
                "60_cpm": self.load_gear_table("60"),
                "45_cpm": self.load_gear_table("45")
            },
            "cycle_times": {
                "75_cpm": self.load_cycle_time_data("75"),
                "60_cpm": self.load_cycle_time_data("60"),
                "45_cpm": self.load_cycle_time_data("45")
            },
            "machine_config": self.load_machine_config()
        }

# Create global data manager instance
data_manager = DataManager()

def load_data_files():
    """Load all data files and return comprehensive data structure"""
    try:
        return data_manager.get_all_data()
    except Exception as e:
        logger.error(f"Error loading data files: {e}")
        return {}

# Export main classes and functions
__all__ = [
    'DataManager', 
    'data_manager',
    'load_data_files'
]