"""
Utilities Module - Professional Job Setup and Configuration Management
Part of the Davenport CAM Assistant REV21 System
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import math

class JobSetup:
    """Professional job setup and configuration management"""
    
    def __init__(self, data_files=None):
        """Initialize job setup with data files"""
        self.data_files = data_files or {}
        self.materials = self.data_files.get('materials', {})
        self.machine_config = self.data_files.get('machine_config', {})
    
    def job_setup_sidebar(self):
        """Create comprehensive job setup interface in sidebar"""
        st.sidebar.header("📋 Job Setup")
        
        # Basic part information
        st.sidebar.subheader("Part Information")
        part_number = st.sidebar.text_input("Part Number", value="", help="Enter part number")
        
        # Dimensional inputs
        diameter = st.sidebar.number_input(
            "Diameter (inches)", 
            min_value=0.0625, 
            max_value=2.0, 
            value=0.5000, 
            step=0.0001, 
            format="%.4f",
            help="Part diameter in inches"
        )
        
        length = st.sidebar.number_input(
            "Length (inches)", 
            min_value=0.100, 
            max_value=12.0, 
            value=1.000, 
            step=0.001, 
            format="%.3f",
            help="Part length in inches"
        )
        
        # Material selection
        material_options = list(self.materials.keys()) if self.materials else [
            'Steel', 'Stainless Steel', 'Aluminum', 'Brass', 'Bronze', 'Tool Steel'
        ]
        material = st.sidebar.selectbox("Material", material_options, help="Select material type")
        
        # Machine configuration
        st.sidebar.subheader("Machine Configuration")
        machine_types = ['5-Spindle', '6-Spindle', '8-Spindle']
        machine_type = st.sidebar.selectbox("Machine Type", machine_types)
        
        # Operating parameters
        st.sidebar.subheader("Operating Parameters")
        rpm = st.sidebar.number_input(
            "RPM", 
            min_value=100, 
            max_value=3000, 
            value=1500, 
            step=25,
            help="Spindle RPM"
        )
        
        cycle_time = st.sidebar.number_input(
            "Target Cycle Time (seconds)", 
            min_value=0.5, 
            max_value=10.0, 
            value=1.6, 
            step=0.1,
            help="Target cycle time in seconds"
        )
        
        # Calculate derived values if we have valid inputs
        if part_number and diameter > 0 and length > 0:
            # Calculate part weight
            part_weight = self.calculate_part_weight(diameter, length, material)
            
            # Calculate parts per bar (assuming 12ft bar)
            parts_per_bar = self.calculate_parts_per_bar(length)
            
            # Calculate bar weight
            bar_weight = self.calculate_bar_weight(diameter, material)
            
            # Display calculated values
            st.sidebar.subheader("Calculated Values")
            st.sidebar.metric("Part Weight", f"{part_weight:.4f} lbs")
            st.sidebar.metric("Parts per Bar", parts_per_bar)
            st.sidebar.metric("Bar Weight", f"{bar_weight:.2f} lbs")
            
            # Calculate surface speed
            surface_speed = (3.14159 * diameter * rpm) / 12
            st.sidebar.metric("Surface Speed", f"{surface_speed:.0f} SFM")
            
            # Return complete setup data
            setup_data = {
                'part_number': part_number,
                'dia': diameter,
                'length': length,
                'material': material,
                'machine_type': machine_type,
                'rpm': rpm,
                'cycle_time': cycle_time,
                'part_weight': part_weight,
                'parts_per_bar': parts_per_bar,
                'bar_weight': bar_weight,
                'surface_speed': surface_speed,
                'machine_config': {
                    'positions': self.get_position_count(machine_type),
                    'type': machine_type
                },
                'material_properties': self.materials.get(material, {})
            }
            
            return setup_data
        
        return None
    
    def calculate_part_weight(self, diameter: float, length: float, material: str) -> float:
        """Calculate part weight in pounds"""
        # Calculate volume in cubic inches
        radius = diameter / 2
        volume = 3.14159 * radius * radius * length
        
        # Material density (lbs per cubic inch)
        density_map = {
            'Steel': 0.284,
            'Stainless Steel': 0.290,
            'Aluminum': 0.098,
            'Brass': 0.307,
            'Bronze': 0.320,
            'Tool Steel': 0.284,
            'Cast Iron': 0.260
        }
        
        density = density_map.get(material, 0.284)  # Default to steel
        weight = volume * density
        
        return weight
    
    def calculate_parts_per_bar(self, part_length: float) -> int:
        """Calculate parts per 12-foot bar"""
        bar_length = 144  # 12 feet in inches
        cutoff_allowance = 0.125  # 1/8" cutoff per part
        usable_length = bar_length - 2.0  # 2" waste at ends
        
        parts = int(usable_length / (part_length + cutoff_allowance))
        return max(1, parts)
    
    def calculate_bar_weight(self, diameter: float, material: str = 'Steel') -> float:
        """Calculate 12-foot bar weight in pounds"""
        radius = diameter / 2
        volume = 3.14159 * radius * radius * 144  # 12 feet = 144 inches
        
        density_map = {
            'Steel': 0.284,
            'Stainless Steel': 0.290,
            'Aluminum': 0.098,
            'Brass': 0.307,
            'Bronze': 0.320,
            'Tool Steel': 0.284
        }
        
        density = density_map.get(material, 0.284)
        return volume * density
    
    def get_position_count(self, machine_type: str) -> int:
        """Get number of positions for machine type"""
        position_map = {
            '5-Spindle': 5,
            '6-Spindle': 6,
            '8-Spindle': 8
        }
        return position_map.get(machine_type, 5)
    
    def get_material_properties(self, material: str) -> Dict[str, Any]:
        """Get material properties for calculations"""
        if material in self.materials:
            return self.materials[material]
        
        # Default properties if not in database
        defaults = {
            'Steel': {'sfm': 150, 'feed_factor': 1.0, 'hardness': 'Medium'},
            'Stainless Steel': {'sfm': 100, 'feed_factor': 0.8, 'hardness': 'Hard'},
            'Aluminum': {'sfm': 400, 'feed_factor': 1.5, 'hardness': 'Soft'},
            'Brass': {'sfm': 300, 'feed_factor': 1.2, 'hardness': 'Soft'},
            'Bronze': {'sfm': 200, 'feed_factor': 1.0, 'hardness': 'Medium'}
        }
        
        return defaults.get(material, defaults['Steel'])
    
    def validate_setup_data(self, setup_data: Dict[str, Any]) -> List[str]:
        """Validate setup data and return list of issues"""
        issues = []
        
        if not setup_data.get('part_number'):
            issues.append("Part number is required")
        
        if setup_data.get('dia', 0) <= 0:
            issues.append("Diameter must be greater than 0")
        
        if setup_data.get('length', 0) <= 0:
            issues.append("Length must be greater than 0")
        
        if setup_data.get('rpm', 0) < 100:
            issues.append("RPM should be at least 100")
        
        if setup_data.get('cycle_time', 0) <= 0:
            issues.append("Cycle time must be greater than 0")
        
        # Check surface speed limits
        surface_speed = setup_data.get('surface_speed', 0)
        if surface_speed > 1000:
            issues.append("Surface speed may be too high (>1000 SFM)")
        
        return issues

# Create utility functions for backwards compatibility
def calculate_surface_speed(diameter: float, rpm: int) -> float:
    """Calculate surface speed in SFM"""
    return (3.14159 * diameter * rpm) / 12

def calculate_feed_per_revolution(feed_rate: float, rpm: int) -> float:
    """Calculate feed per revolution"""
    return feed_rate / rpm if rpm > 0 else 0

# Export main class and functions
__all__ = ['JobSetup', 'calculate_surface_speed', 'calculate_feed_per_revolution']