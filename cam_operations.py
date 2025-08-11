"""
CAM Operations Module - Multi-Spindle Machining Operations & Tool Management
Part of the Davenport CAM Assistant REV21 System
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import math

class CamOperations:
    """Professional CAM operations management for multi-spindle machines"""
    
    def __init__(self):
        """Initialize CAM operations with data loading"""
        self.spindle_data = []
        
        # Load essential data files
        self.load_data_files()
    
    def load_data_files(self):
        """Load CAM operation data files"""
        try:
            data_path = Path("data")
            
            # Load Davenport cam data
            with open(data_path / "davenport_cams.json", 'r') as f:
                self.davenport_cams = json.load(f)
            
            # Load tool libraries
            with open(data_path / "tool_library_end.json", 'r') as f:
                self.end_tools = json.load(f)
            
            with open(data_path / "tool_library_side.json", 'r') as f:
                self.side_tools = json.load(f)
            
            # Load SFM guidelines
            with open(data_path / "sfm_guidelines.json", 'r') as f:
                self.sfm_guidelines = json.load(f)
                
        except Exception as e:
            st.error(f"Error loading CAM data files: {e}")
            self.davenport_cams = {}
            self.end_tools = []
            self.side_tools = []
            self.sfm_guidelines = {}
    
    def cam_operations_section(self, setup_data, material_data):
        """Main CAM operations section"""
        st.header("⚙️ CAM Operations & Spindle Programming")
        
        if not setup_data:
            st.warning("⚠️ Please complete Job Setup first")
            return {}
        
        # Display current job info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Part", setup_data.get('part_number', 'Not Set'))
            st.metric("Diameter", f"{setup_data.get('dia', 0):.4f}\"")
        with col2:
            st.metric("Material", setup_data.get('material', 'Not Set'))
            st.metric("RPM", setup_data.get('rpm', 'Not Set'))
        with col3:
            st.metric("Machine", setup_data.get('machine_type', 'Not Set'))
            st.metric("Cycle Time", f"{setup_data.get('cycle_time', 0):.2f}s")
        
        st.markdown("---")
        
        # Spindle operations configuration
        st.subheader("🔧 Spindle Operations Configuration")
        
        # Get machine configuration
        machine_type = setup_data.get('machine_type', '5-Spindle')
        position_count = self.get_position_count(machine_type)
        
        # Create tabs for each spindle position
        spindle_tabs = st.tabs([f"Position {i+1}" for i in range(position_count)])
        
        spindle_operations = []
        
        for i, tab in enumerate(spindle_tabs):
            with tab:
                position_num = i + 1
                st.subheader(f"Position {position_num} Operations")
                
                # Operation selection
                operation_types = [
                    "No Operation",
                    "Center Drill",
                    "Drill",
                    "Ream",
                    "Tap",
                    "Counterbore",
                    "Chamfer",
                    "Turn",
                    "Face",
                    "Knurl",
                    "Thread",
                    "Cutoff"
                ]
                
                operation = st.selectbox(
                    f"Operation Type - Position {position_num}",
                    operation_types,
                    key=f"op_type_{position_num}"
                )
                
                if operation != "No Operation":
                    operation_data = self.configure_operation(
                        operation, position_num, setup_data, material_data
                    )
                    if operation_data:
                        spindle_operations.append(operation_data)
        
        # Calculate total cycle time
        if spindle_operations:
            total_cycle_time = self.calculate_total_cycle_time(spindle_operations)
            st.session_state['cycle_time_from_tab2'] = total_cycle_time
            
            st.markdown("---")
            st.subheader("📊 Operation Summary")
            
            # Display operations summary
            summary_data = []
            for op in spindle_operations:
                summary_data.append({
                    "Position": op.get('position', 'N/A'),
                    "Operation": op.get('operation', 'N/A'),
                    "Tool": op.get('tool_description', 'N/A'),
                    "Feed": f"{op.get('feed_rate', 0):.4f}\"",
                    "Speed": f"{op.get('rpm', 0)} RPM",
                    "Time": f"{op.get('cycle_time', 0):.2f}s"
                })
            
            if summary_data:
                df = pd.DataFrame(summary_data)
                st.dataframe(df, use_container_width=True)
                
                # Total metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Operations", len(spindle_operations))
                with col2:
                    st.metric("Total Cycle Time", f"{total_cycle_time:.2f}s")
                with col3:
                    parts_per_hour = 3600 / total_cycle_time if total_cycle_time > 0 else 0
                    st.metric("Parts/Hour", f"{parts_per_hour:.0f}")
        
        return spindle_operations
    
    def configure_operation(self, operation_type, position, setup_data, material_data):
        """Configure specific operation parameters"""
        st.write(f"**{operation_type} Configuration:**")
        
        # Get material properties
        material = setup_data.get('material', 'Steel')
        diameter = setup_data.get('dia', 0.5)
        
        # Operation-specific configuration
        if operation_type in ["Center Drill", "Drill"]:
            return self.configure_drilling_operation(operation_type, position, setup_data, material_data)
        elif operation_type == "Ream":
            return self.configure_reaming_operation(position, setup_data, material_data)
        elif operation_type == "Tap":
            return self.configure_tapping_operation(position, setup_data, material_data)
        elif operation_type in ["Turn", "Face"]:
            return self.configure_turning_operation(operation_type, position, setup_data, material_data)
        elif operation_type == "Knurl":
            return self.configure_knurling_operation(position, setup_data, material_data)
        elif operation_type == "Thread":
            return self.configure_threading_operation(position, setup_data, material_data)
        elif operation_type == "Cutoff":
            return self.configure_cutoff_operation(position, setup_data, material_data)
        else:
            return self.configure_generic_operation(operation_type, position, setup_data, material_data)
    
    def configure_drilling_operation(self, operation_type, position, setup_data, material_data):
        """Configure drilling operations"""
        col1, col2 = st.columns(2)
        
        with col1:
            drill_diameter = st.number_input(
                f"Drill Diameter (in)",
                min_value=0.0156,  # 1/64"
                max_value=1.0,
                value=0.125,
                step=0.0001,
                format="%.4f",
                key=f"drill_dia_{position}"
            )
            
            depth = st.number_input(
                f"Depth (in)",
                min_value=0.001,
                max_value=2.0,
                value=0.250,
                step=0.001,
                format="%.3f",
                key=f"drill_depth_{position}"
            )
        
        with col2:
            # Calculate recommended parameters
            material = setup_data.get('material', 'Steel')
            recommended_sfm = self.get_recommended_sfm(material, 'drilling')
            recommended_rpm = (recommended_sfm * 12) / (3.14159 * drill_diameter)
            recommended_feed = self.get_recommended_feed(drill_diameter, material, 'drilling')
            
            rpm = st.number_input(
                f"RPM",
                min_value=100,
                max_value=5000,
                value=int(recommended_rpm),
                step=50,
                key=f"drill_rpm_{position}"
            )
            
            feed_rate = st.number_input(
                f"Feed Rate (in/rev)",
                min_value=0.0001,
                max_value=0.0500,
                value=recommended_feed,
                step=0.0001,
                format="%.4f",
                key=f"drill_feed_{position}"
            )
        
        # Calculate cycle time
        cycle_time = self.calculate_drilling_time(depth, feed_rate, rpm)
        
        st.info(f"Estimated cycle time: {cycle_time:.2f} seconds")
        
        return {
            'position': position,
            'operation': operation_type,
            'tool_diameter': drill_diameter,
            'depth': depth,
            'rpm': rpm,
            'feed_rate': feed_rate,
            'cycle_time': cycle_time,
            'tool_description': f"{drill_diameter:.4f}\" {operation_type}",
            'material': setup_data.get('material', 'Steel')
        }
    
    def configure_reaming_operation(self, position, setup_data, material_data):
        """Configure reaming operation"""
        col1, col2 = st.columns(2)
        
        with col1:
            reamer_diameter = st.number_input(
                f"Reamer Diameter (in)",
                min_value=0.0625,
                max_value=1.0,
                value=0.250,
                step=0.0001,
                format="%.4f",
                key=f"ream_dia_{position}"
            )
            
            depth = st.number_input(
                f"Depth (in)",
                min_value=0.001,
                max_value=2.0,
                value=0.250,
                step=0.001,
                format="%.3f",
                key=f"ream_depth_{position}"
            )
        
        with col2:
            material = setup_data.get('material', 'Steel')
            recommended_sfm = self.get_recommended_sfm(material, 'reaming')
            recommended_rpm = (recommended_sfm * 12) / (3.14159 * reamer_diameter)
            recommended_feed = self.get_recommended_feed(reamer_diameter, material, 'reaming')
            
            rpm = st.number_input(
                f"RPM",
                min_value=100,
                max_value=3000,
                value=int(recommended_rpm),
                step=25,
                key=f"ream_rpm_{position}"
            )
            
            feed_rate = st.number_input(
                f"Feed Rate (in/rev)",
                min_value=0.0001,
                max_value=0.0200,
                value=recommended_feed,
                step=0.0001,
                format="%.4f",
                key=f"ream_feed_{position}"
            )
        
        cycle_time = self.calculate_drilling_time(depth, feed_rate, rpm)
        st.info(f"Estimated cycle time: {cycle_time:.2f} seconds")
        
        return {
            'position': position,
            'operation': 'Ream',
            'tool_diameter': reamer_diameter,
            'depth': depth,
            'rpm': rpm,
            'feed_rate': feed_rate,
            'cycle_time': cycle_time,
            'tool_description': f"{reamer_diameter:.4f}\" Reamer",
            'material': setup_data.get('material', 'Steel')
        }
    
    def configure_tapping_operation(self, position, setup_data, material_data):
        """Configure tapping operation"""
        col1, col2 = st.columns(2)
        
        with col1:
            thread_sizes = ["#4-40", "#6-32", "#8-32", "#10-24", "#10-32", 
                          "1/4-20", "1/4-28", "5/16-18", "5/16-24", "3/8-16", "3/8-24"]
            thread_size = st.selectbox(
                f"Thread Size",
                thread_sizes,
                key=f"tap_size_{position}"
            )
            
            depth = st.number_input(
                f"Thread Depth (in)",
                min_value=0.050,
                max_value=1.0,
                value=0.125,
                step=0.001,
                format="%.3f",
                key=f"tap_depth_{position}"
            )
        
        with col2:
            # Calculate tapping parameters
            pitch = self.get_thread_pitch(thread_size)
            material = setup_data.get('material', 'Steel')
            recommended_sfm = self.get_recommended_sfm(material, 'tapping')
            tap_diameter = self.get_tap_diameter(thread_size)
            recommended_rpm = (recommended_sfm * 12) / (3.14159 * tap_diameter)
            
            rpm = st.number_input(
                f"Tapping RPM",
                min_value=50,
                max_value=1000,
                value=int(recommended_rpm),
                step=25,
                key=f"tap_rpm_{position}"
            )
            
            st.info(f"Thread Pitch: {pitch:.4f}\"")
            st.info(f"Feed Rate: {pitch:.4f}\" (automatic)")
        
        cycle_time = self.calculate_tapping_time(depth, pitch, rpm)
        st.info(f"Estimated cycle time: {cycle_time:.2f} seconds")
        
        return {
            'position': position,
            'operation': 'Tap',
            'thread_size': thread_size,
            'thread_pitch': pitch,
            'depth': depth,
            'rpm': rpm,
            'feed_rate': pitch,  # Tapping feed = pitch
            'cycle_time': cycle_time,
            'tool_description': f"{thread_size} Tap",
            'material': setup_data.get('material', 'Steel')
        }
    
    def configure_turning_operation(self, operation_type, position, setup_data, material_data):
        """Configure turning/facing operations"""
        col1, col2 = st.columns(2)
        
        with col1:
            if operation_type == "Turn":
                cut_diameter = st.number_input(
                    f"Cut Diameter (in)",
                    min_value=0.0625,
                    max_value=2.0,
                    value=setup_data.get('dia', 0.5),
                    step=0.0001,
                    format="%.4f",
                    key=f"turn_dia_{position}"
                )
                
                cut_length = st.number_input(
                    f"Cut Length (in)",
                    min_value=0.001,
                    max_value=2.0,
                    value=0.100,
                    step=0.001,
                    format="%.3f",
                    key=f"turn_length_{position}"
                )
            else:  # Face
                face_diameter = st.number_input(
                    f"Face Diameter (in)",
                    min_value=0.0625,
                    max_value=2.0,
                    value=setup_data.get('dia', 0.5),
                    step=0.0001,
                    format="%.4f",
                    key=f"face_dia_{position}"
                )
                cut_length = face_diameter / 2  # Face from center to edge
        
        with col2:
            material = setup_data.get('material', 'Steel')
            recommended_sfm = self.get_recommended_sfm(material, 'turning')
            work_diameter = cut_diameter if operation_type == "Turn" else face_diameter
            recommended_rpm = (recommended_sfm * 12) / (3.14159 * work_diameter)
            recommended_feed = self.get_recommended_feed(work_diameter, material, 'turning')
            
            rpm = st.number_input(
                f"RPM",
                min_value=100,
                max_value=3000,
                value=int(recommended_rpm),
                step=25,
                key=f"{operation_type.lower()}_rpm_{position}"
            )
            
            feed_rate = st.number_input(
                f"Feed Rate (in/rev)",
                min_value=0.001,
                max_value=0.050,
                value=recommended_feed,
                step=0.001,
                format="%.3f",
                key=f"{operation_type.lower()}_feed_{position}"
            )
            
            depth_of_cut = st.number_input(
                f"Depth of Cut (in)",
                min_value=0.001,
                max_value=0.200,
                value=0.010,
                step=0.001,
                format="%.3f",
                key=f"{operation_type.lower()}_doc_{position}"
            )
        
        cycle_time = self.calculate_turning_time(cut_length, feed_rate, rpm)
        st.info(f"Estimated cycle time: {cycle_time:.2f} seconds")
        
        return {
            'position': position,
            'operation': operation_type,
            'work_diameter': work_diameter,
            'cut_length': cut_length,
            'depth_of_cut': depth_of_cut,
            'rpm': rpm,
            'feed_rate': feed_rate,
            'cycle_time': cycle_time,
            'tool_description': f"{operation_type} - {work_diameter:.4f}\"",
            'material': setup_data.get('material', 'Steel')
        }
    
    def configure_knurling_operation(self, position, setup_data, material_data):
        """Configure knurling operation"""
        col1, col2 = st.columns(2)
        
        with col1:
            knurl_types = ["12 TPI", "16 TPI", "20 TPI", "25 TPI", "30 TPI", "64 DP", "96 DP"]
            knurl_type = st.selectbox(
                f"Knurl Type",
                knurl_types,
                index=2,  # Default to 20 TPI
                key=f"knurl_type_{position}"
            )
            
            knurl_length = st.number_input(
                f"Knurl Length (in)",
                min_value=0.050,
                max_value=1.0,
                value=0.250,
                step=0.001,
                format="%.3f",
                key=f"knurl_length_{position}"
            )
        
        with col2:
            work_diameter = setup_data.get('dia', 0.5)
            recommended_rpm = 200  # Knurling is typically slow
            
            rpm = st.number_input(
                f"Knurling RPM",
                min_value=50,
                max_value=500,
                value=recommended_rpm,
                step=25,
                key=f"knurl_rpm_{position}"
            )
            
            feed_rate = st.number_input(
                f"Feed Rate (in/rev)",
                min_value=0.005,
                max_value=0.050,
                value=0.015,
                step=0.001,
                format="%.3f",
                key=f"knurl_feed_{position}"
            )
            
            penetration = st.number_input(
                f"Knurl Penetration (in)",
                min_value=0.002,
                max_value=0.020,
                value=0.008,
                step=0.001,
                format="%.3f",
                key=f"knurl_penetration_{position}"
            )
        
        cycle_time = self.calculate_knurling_time(knurl_length, feed_rate, rpm, penetration)
        st.info(f"Estimated cycle time: {cycle_time:.2f} seconds")
        
        return {
            'position': position,
            'operation': 'Knurl',
            'knurl_type': knurl_type,
            'knurl_length': knurl_length,
            'penetration': penetration,
            'rpm': rpm,
            'feed_rate': feed_rate,
            'cycle_time': cycle_time,
            'tool_description': f"{knurl_type} Knurl",
            'material': setup_data.get('material', 'Steel')
        }
    
    def configure_threading_operation(self, position, setup_data, material_data):
        """Configure threading operation"""
        col1, col2 = st.columns(2)
        
        with col1:
            thread_types = ["10-32", "1/4-20", "1/4-28", "5/16-18", "5/16-24", "3/8-16", "3/8-24"]
            thread_type = st.selectbox(
                f"Thread Type",
                thread_types,
                key=f"thread_type_{position}"
            )
            
            thread_length = st.number_input(
                f"Thread Length (in)",
                min_value=0.050,
                max_value=1.0,
                value=0.250,
                step=0.001,
                format="%.3f",
                key=f"thread_length_{position}"
            )
        
        with col2:
            # Threading parameters
            pitch = self.get_thread_pitch(thread_type)
            material = setup_data.get('material', 'Steel')
            
            # Threading method selection
            threading_methods = ["2:1", "4:1", "6:1"]
            method = st.selectbox(
                f"Threading Method",
                threading_methods,
                index=2 if material == 'Steel' else 0,  # 6:1 for steel, 2:1 for others
                key=f"thread_method_{position}"
            )
            
            base_rpm = setup_data.get('rpm', 600)
            threading_rpm = base_rpm // int(method.split(':')[0])
            
            st.info(f"Thread Pitch: {pitch:.4f}\"")
            st.info(f"Threading RPM: {threading_rpm}")
            st.info(f"Method: {method} Threading")
        
        cycle_time = self.calculate_threading_time(thread_length, pitch, threading_rpm, method)
        st.info(f"Estimated cycle time: {cycle_time:.2f} seconds")
        
        return {
            'position': position,
            'operation': 'Thread',
            'thread_type': thread_type,
            'thread_pitch': pitch,
            'thread_length': thread_length,
            'threading_method': method,
            'rpm': threading_rpm,
            'feed_rate': pitch,  # Threading feed = pitch
            'cycle_time': cycle_time,
            'tool_description': f"{thread_type} Thread",
            'material': setup_data.get('material', 'Steel')
        }
    
    def configure_cutoff_operation(self, position, setup_data, material_data):
        """Configure cutoff operation"""
        col1, col2 = st.columns(2)
        
        with col1:
            cutoff_diameter = setup_data.get('dia', 0.5)
            st.metric("Cutoff Diameter", f"{cutoff_diameter:.4f}\"")
            
            blade_width = st.number_input(
                f"Blade Width (in)",
                min_value=0.020,
                max_value=0.125,
                value=0.062,
                step=0.001,
                format="%.3f",
                key=f"cutoff_width_{position}"
            )
        
        with col2:
            material = setup_data.get('material', 'Steel')
            recommended_sfm = self.get_recommended_sfm(material, 'cutoff')
            recommended_rpm = (recommended_sfm * 12) / (3.14159 * cutoff_diameter)
            
            rpm = st.number_input(
                f"Cutoff RPM",
                min_value=100,
                max_value=2000,
                value=int(recommended_rpm),
                step=25,
                key=f"cutoff_rpm_{position}"
            )
            
            feed_rate = st.number_input(
                f"Feed Rate (in/rev)",
                min_value=0.001,
                max_value=0.020,
                value=0.005,
                step=0.001,
                format="%.3f",
                key=f"cutoff_feed_{position}"
            )
        
        # Calculate cutoff time (time to cut through diameter)
        cut_distance = cutoff_diameter + 0.050  # Add overtravel
        cycle_time = self.calculate_cutoff_time(cut_distance, feed_rate, rpm)
        
        st.info(f"Estimated cycle time: {cycle_time:.2f} seconds")
        
        return {
            'position': position,
            'operation': 'Cutoff',
            'cutoff_diameter': cutoff_diameter,
            'blade_width': blade_width,
            'rpm': rpm,
            'feed_rate': feed_rate,
            'cycle_time': cycle_time,
            'tool_description': f"Cutoff - {cutoff_diameter:.4f}\"",
            'material': setup_data.get('material', 'Steel')
        }
    
    def configure_generic_operation(self, operation_type, position, setup_data, material_data):
        """Configure generic operation"""
        st.info(f"Configuring {operation_type} operation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tool_diameter = st.number_input(
                f"Tool Diameter (in)",
                min_value=0.001,
                max_value=2.0,
                value=0.125,
                step=0.001,
                format="%.3f",
                key=f"generic_dia_{position}"
            )
            
            operation_depth = st.number_input(
                f"Operation Depth (in)",
                min_value=0.001,
                max_value=2.0,
                value=0.100,
                step=0.001,
                format="%.3f",
                key=f"generic_depth_{position}"
            )
        
        with col2:
            rpm = st.number_input(
                f"RPM",
                min_value=100,
                max_value=3000,
                value=1000,
                step=50,
                key=f"generic_rpm_{position}"
            )
            
            feed_rate = st.number_input(
                f"Feed Rate (in/rev)",
                min_value=0.001,
                max_value=0.050,
                value=0.005,
                step=0.001,
                format="%.3f",
                key=f"generic_feed_{position}"
            )
        
        cycle_time = operation_depth / feed_rate / rpm * 60  # Basic time calculation
        
        return {
            'position': position,
            'operation': operation_type,
            'tool_diameter': tool_diameter,
            'operation_depth': operation_depth,
            'rpm': rpm,
            'feed_rate': feed_rate,
            'cycle_time': cycle_time,
            'tool_description': f"{operation_type} Tool",
            'material': setup_data.get('material', 'Steel')
        }
    
    # Helper methods for calculations
    def get_position_count(self, machine_type):
        """Get number of positions for machine type"""
        position_map = {
            '5-Spindle': 5,
            '6-Spindle': 6,
            '8-Spindle': 8
        }
        return position_map.get(machine_type, 5)
    
    def get_recommended_sfm(self, material, operation):
        """Get recommended surface speed for material and operation"""
        sfm_data = {
            'Steel': {
                'drilling': 100, 'reaming': 80, 'tapping': 30, 'turning': 150, 'cutoff': 120
            },
            'Stainless Steel': {
                'drilling': 80, 'reaming': 60, 'tapping': 25, 'turning': 120, 'cutoff': 100
            },
            'Aluminum': {
                'drilling': 300, 'reaming': 250, 'tapping': 100, 'turning': 400, 'cutoff': 350
            },
            'Brass': {
                'drilling': 200, 'reaming': 180, 'tapping': 80, 'turning': 300, 'cutoff': 250
            },
            'Bronze': {
                'drilling': 150, 'reaming': 120, 'tapping': 50, 'turning': 200, 'cutoff': 180
            }
        }
        
        return sfm_data.get(material, sfm_data['Steel']).get(operation, 100)
    
    def get_recommended_feed(self, diameter, material, operation):
        """Get recommended feed rate"""
        base_feeds = {
            'drilling': diameter * 0.01,  # 1% of diameter
            'reaming': diameter * 0.005,  # 0.5% of diameter
            'turning': 0.010,             # Standard turning feed
            'cutoff': 0.005               # Standard cutoff feed
        }
        
        material_factors = {
            'Steel': 1.0,
            'Stainless Steel': 0.8,
            'Aluminum': 1.5,
            'Brass': 1.2,
            'Bronze': 1.0
        }
        
        base_feed = base_feeds.get(operation, 0.005)
        material_factor = material_factors.get(material, 1.0)
        
        return max(0.0001, min(0.0500, base_feed * material_factor))
    
    def get_thread_pitch(self, thread_size):
        """Get thread pitch from thread size"""
        pitch_map = {
            '#4-40': 1.0/40, '#6-32': 1.0/32, '#8-32': 1.0/32,
            '#10-24': 1.0/24, '#10-32': 1.0/32,
            '1/4-20': 1.0/20, '1/4-28': 1.0/28,
            '5/16-18': 1.0/18, '5/16-24': 1.0/24,
            '3/8-16': 1.0/16, '3/8-24': 1.0/24,
            '10-32': 1.0/32
        }
        return pitch_map.get(thread_size, 1.0/20)  # Default to 20 TPI
    
    def get_tap_diameter(self, thread_size):
        """Get tap diameter from thread size"""
        diameter_map = {
            '#4-40': 0.112, '#6-32': 0.138, '#8-32': 0.164,
            '#10-24': 0.190, '#10-32': 0.190,
            '1/4-20': 0.250, '1/4-28': 0.250,
            '5/16-18': 0.3125, '5/16-24': 0.3125,
            '3/8-16': 0.375, '3/8-24': 0.375,
            '10-32': 0.190
        }
        return diameter_map.get(thread_size, 0.250)
    
    # Time calculation methods
    def calculate_drilling_time(self, depth, feed_rate, rpm):
        """Calculate drilling/reaming time"""
        if rpm <= 0 or feed_rate <= 0:
            return 0.0
        
        # Time = depth / (feed_rate * rpm / 60)
        feed_per_minute = feed_rate * rpm
        time = depth / feed_per_minute * 60
        return max(0.1, time)  # Minimum 0.1 seconds
    
    def calculate_tapping_time(self, depth, pitch, rpm):
        """Calculate tapping time (includes reverse)"""
        if rpm <= 0:
            return 0.0
        
        # Tapping time includes forward and reverse
        feed_per_minute = pitch * rpm
        forward_time = depth / feed_per_minute * 60
        reverse_time = forward_time  # Same time to back out
        total_time = forward_time + reverse_time + 0.5  # Add dwell time
        
        return max(0.5, total_time)
    
    def calculate_turning_time(self, length, feed_rate, rpm):
        """Calculate turning/facing time"""
        if rpm <= 0 or feed_rate <= 0:
            return 0.0
        
        feed_per_minute = feed_rate * rpm
        time = length / feed_per_minute * 60
        return max(0.1, time)
    
    def calculate_knurling_time(self, length, feed_rate, rpm, penetration):
        """Calculate knurling time"""
        if rpm <= 0 or feed_rate <= 0:
            return 0.0
        
        # Multiple passes for knurling penetration
        passes = max(1, int(penetration / 0.003))  # ~0.003" per pass
        feed_per_minute = feed_rate * rpm
        time_per_pass = length / feed_per_minute * 60
        total_time = time_per_pass * passes
        
        return max(0.5, total_time)
    
    def calculate_threading_time(self, length, pitch, rpm, method):
        """Calculate threading time"""
        if rpm <= 0:
            return 0.0
        
        # Multiple passes for threading
        method_passes = {'2:1': 2, '4:1': 3, '6:1': 4}
        passes = method_passes.get(method, 3)
        
        feed_per_minute = pitch * rpm
        time_per_pass = length / feed_per_minute * 60 * 2  # Forward and back
        total_time = time_per_pass * passes + 1.0  # Add setup time
        
        return max(1.0, total_time)
    
    def calculate_cutoff_time(self, cut_distance, feed_rate, rpm):
        """Calculate cutoff time"""
        if rpm <= 0 or feed_rate <= 0:
            return 0.0
        
        feed_per_minute = feed_rate * rpm
        time = cut_distance / feed_per_minute * 60
        return max(0.5, time)  # Minimum 0.5 seconds
    
    def calculate_total_cycle_time(self, operations):
        """Calculate total cycle time for all operations"""
        total_time = 0.0
        for operation in operations:
            total_time += operation.get('cycle_time', 0.0)
        
        # Add indexing time between positions (0.2s per index)
        indexing_time = len(operations) * 0.2
        
        return total_time + indexing_time

# Create global instance
cam_operations = CamOperations()

# Export
__all__ = ['CamOperations', 'cam_operations']