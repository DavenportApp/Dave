"""
Reference Charts Module - Professional Reference Data & Charts
Part of the Davenport CAM Assistant REV21 System
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
import math

class ReferenceCharts:
    """Professional reference charts and data management"""
    
    def __init__(self):
        """Initialize reference charts system"""
        self.charts_data = {}
        self.load_reference_data()
    
    def load_reference_data(self):
        """Load reference chart data"""
        try:
            # Load basic reference data (can be expanded with JSON files later)
            self.charts_data = {
                'drill_charts': self.get_drill_chart_data(),
                'tap_charts': self.get_tap_chart_data(),
                'thread_data': self.get_thread_reference_data(),
                'material_data': self.get_material_reference_data(),
                'sfm_data': self.get_sfm_reference_data(),
                'feed_data': self.get_feed_reference_data()
            }
        except Exception as e:
            st.error(f"Error loading reference data: {e}")
            self.charts_data = {}
    
    def reference_charts_interface(self):
        """Main reference charts interface"""
        st.header("📊 Reference Charts & Data")
        
        # Chart selection tabs
        chart_tabs = st.tabs([
            "🔩 Drill Charts",
            "🔧 Tap Charts", 
            "🧵 Threading Data",
            "🔬 Material Data",
            "⚡ SFM Guidelines",
            "📏 Feed Rates",
            "📐 Conversions"
        ])
        
        with chart_tabs[0]:
            self.display_drill_charts()
        
        with chart_tabs[1]:
            self.display_tap_charts()
        
        with chart_tabs[2]:
            self.display_threading_data()
        
        with chart_tabs[3]:
            self.display_material_data()
        
        with chart_tabs[4]:
            self.display_sfm_guidelines()
        
        with chart_tabs[5]:
            self.display_feed_rates()
        
        with chart_tabs[6]:
            self.display_conversions()
    
    def display_drill_charts(self):
        """Display drill size and feed rate charts"""
        st.subheader("🔩 Drill Size & Feed Rate Reference")
        
        # Drill size selection
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Standard Drill Sizes")
            
            # Number drills
            number_drills = self.get_number_drill_data()
            df_number = pd.DataFrame(number_drills)
            st.dataframe(df_number, use_container_width=True)
        
        with col2:
            st.markdown("### Letter Drills")
            
            # Letter drills
            letter_drills = self.get_letter_drill_data()
            df_letter = pd.DataFrame(letter_drills)
            st.dataframe(df_letter, use_container_width=True)
        
        # Fractional drills
        st.markdown("### Fractional Drill Sizes")
        fractional_drills = self.get_fractional_drill_data()
        df_fractional = pd.DataFrame(fractional_drills)
        st.dataframe(df_fractional, use_container_width=True)
        
        # Interactive drill calculator
        st.markdown("### Drill Speed Calculator")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            drill_diameter = st.number_input(
                "Drill Diameter (inches)",
                min_value=0.001,
                max_value=1.0,
                value=0.125,
                step=0.001,
                format="%.4f"
            )
        
        with col2:
            material_type = st.selectbox(
                "Material",
                ["Steel", "Stainless Steel", "Aluminum", "Brass", "Bronze"]
            )
        
        with col3:
            sfm_values = {
                "Steel": 100, "Stainless Steel": 80, "Aluminum": 300, 
                "Brass": 200, "Bronze": 150
            }
            recommended_sfm = sfm_values.get(material_type, 100)
            calculated_rpm = (recommended_sfm * 12) / (3.14159 * drill_diameter)
            
            st.metric("Recommended SFM", recommended_sfm)
            st.metric("Calculated RPM", f"{calculated_rpm:.0f}")
    
    def display_tap_charts(self):
        """Display tap drill and threading charts"""
        st.subheader("🔧 Tap Drill & Threading Reference")
        
        # Tap drill chart
        tap_data = self.get_tap_drill_chart()
        df_tap = pd.DataFrame(tap_data)
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            thread_type = st.selectbox(
                "Thread Type",
                ["All", "UNC (Coarse)", "UNF (Fine)", "Metric"]
            )
        
        with col2:
            size_range = st.selectbox(
                "Size Range", 
                ["All", "Small (#0-#12)", "Medium (1/4-1/2)", "Large (5/8+)"]
            )
        
        # Filter data based on selection
        filtered_df = df_tap.copy()
        if thread_type != "All":
            if thread_type == "UNC (Coarse)":
                filtered_df = filtered_df[filtered_df['Type'] == 'UNC']
            elif thread_type == "UNF (Fine)":
                filtered_df = filtered_df[filtered_df['Type'] == 'UNF']
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # Tapping speed calculator
        st.markdown("### Tapping Speed Calculator")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_thread = st.selectbox(
                "Thread Size",
                ["#4-40", "#6-32", "#8-32", "#10-24", "#10-32", "1/4-20", "1/4-28", "5/16-18", "3/8-16"]
            )
        
        with col2:
            tap_material = st.selectbox(
                "Material Type",
                ["Steel", "Stainless Steel", "Aluminum", "Brass", "Bronze"],
                key="tap_material"
            )
        
        with col3:
            tap_sfm_values = {
                "Steel": 30, "Stainless Steel": 25, "Aluminum": 100, 
                "Brass": 80, "Bronze": 50
            }
            tap_diameter = self.get_tap_diameter_from_thread(selected_thread)
            recommended_tap_sfm = tap_sfm_values.get(tap_material, 30)
            calculated_tap_rpm = (recommended_tap_sfm * 12) / (3.14159 * tap_diameter)
            
            st.metric("Recommended SFM", recommended_tap_sfm)
            st.metric("Calculated RPM", f"{calculated_tap_rpm:.0f}")
    
    def display_threading_data(self):
        """Display threading reference data"""
        st.subheader("🧵 Threading Reference Data")
        
        # Threading methods comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Threading Methods")
            threading_methods = {
                "Method": ["2:1 Threading", "4:1 Threading", "6:1 Threading", "Single Point"],
                "Speed Ratio": ["2:1", "4:1", "6:1", "1:1"],
                "Best For": ["Soft materials", "Medium materials", "Hard materials", "Special threads"],
                "Typical Materials": ["Brass, Aluminum", "Bronze, Mild Steel", "Steel, Stainless", "Custom threads"]
            }
            df_methods = pd.DataFrame(threading_methods)
            st.dataframe(df_methods, use_container_width=True)
        
        with col2:
            st.markdown("### Thread Pitch Reference")
            thread_pitch_data = {
                "Thread Size": ["#4-40", "#6-32", "#8-32", "#10-24", "#10-32", "1/4-20", "1/4-28", "5/16-18", "3/8-16"],
                "Pitch (in)": [0.025, 0.03125, 0.03125, 0.04167, 0.03125, 0.050, 0.03571, 0.05556, 0.0625],
                "TPI": [40, 32, 32, 24, 32, 20, 28, 18, 16]
            }
            df_pitch = pd.DataFrame(thread_pitch_data)
            st.dataframe(df_pitch, use_container_width=True)
        
        # Threading calculator
        st.markdown("### Threading Speed Calculator")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            thread_size_calc = st.selectbox(
                "Thread Size",
                ["1/4-20", "5/16-18", "3/8-16", "1/2-13", "5/8-11"],
                key="thread_calc"
            )
        
        with col2:
            threading_method = st.selectbox(
                "Threading Method",
                ["2:1", "4:1", "6:1"]
            )
        
        with col3:
            base_spindle_rpm = st.number_input(
                "Base RPM",
                min_value=100,
                max_value=2000,
                value=600
            )
        
        with col4:
            method_ratio = int(threading_method.split(':')[0])
            threading_rpm = base_spindle_rpm // method_ratio
            
            st.metric("Threading RPM", threading_rpm)
            thread_pitch = self.get_thread_pitch_from_size(thread_size_calc)
            st.metric("Thread Pitch", f"{thread_pitch:.4f}\"")
    
    def display_material_data(self):
        """Display material properties and guidelines"""
        st.subheader("🔬 Material Properties & Guidelines")
        
        # Material properties table
        material_props = {
            "Material": ["Steel (1018)", "Steel (1045)", "Stainless 304", "Stainless 316", 
                        "Aluminum 6061", "Brass 360", "Bronze C544", "Tool Steel"],
            "Density (lb/in³)": [0.284, 0.284, 0.290, 0.290, 0.098, 0.307, 0.320, 0.284],
            "Hardness (HB)": [126, 163, 201, 217, 95, 75, 85, 248],
            "Machinability": [78, 72, 45, 36, 90, 100, 80, 30],
            "Typical SFM": [150, 120, 100, 80, 400, 300, 200, 60]
        }
        
        df_materials = pd.DataFrame(material_props)
        st.dataframe(df_materials, use_container_width=True)
        
        # Material comparison chart
        st.markdown("### Material Comparison Chart")
        
        fig = go.Figure()
        
        # Add traces for different properties
        materials = df_materials['Material']
        
        fig.add_trace(go.Bar(
            name='SFM',
            x=materials,
            y=df_materials['Typical SFM'],
            yaxis='y',
            marker_color='blue'
        ))
        
        fig.add_trace(go.Bar(
            name='Machinability',
            x=materials,
            y=df_materials['Machinability'],
            yaxis='y2',
            marker_color='orange'
        ))
        
        fig.update_layout(
            title='Material Properties Comparison',
            xaxis=dict(title='Material'),
            yaxis=dict(title='SFM', side='left'),
            yaxis2=dict(title='Machinability Rating', side='right', overlaying='y'),
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_sfm_guidelines(self):
        """Display SFM guidelines for different operations"""
        st.subheader("⚡ Surface Speed (SFM) Guidelines")
        
        # SFM guidelines by operation
        sfm_data = {
            "Material": ["Steel", "Stainless Steel", "Aluminum", "Brass", "Bronze"],
            "Drilling": [100, 80, 300, 200, 150],
            "Reaming": [80, 60, 250, 180, 120],
            "Tapping": [30, 25, 100, 80, 50],
            "Turning": [150, 120, 400, 300, 200],
            "Threading": [25, 20, 80, 60, 40],
            "Cutoff": [120, 100, 350, 250, 180]
        }
        
        df_sfm = pd.DataFrame(sfm_data)
        st.dataframe(df_sfm, use_container_width=True)
        
        # Interactive SFM calculator
        st.markdown("### SFM Calculator")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            calc_material = st.selectbox(
                "Material",
                ["Steel", "Stainless Steel", "Aluminum", "Brass", "Bronze"],
                key="sfm_calc_material"
            )
        
        with col2:
            calc_operation = st.selectbox(
                "Operation",
                ["Drilling", "Reaming", "Tapping", "Turning", "Threading", "Cutoff"]
            )
        
        with col3:
            calc_diameter = st.number_input(
                "Tool/Work Diameter (in)",
                min_value=0.001,
                max_value=2.0,
                value=0.250,
                step=0.001,
                format="%.4f"
            )
        
        # Calculate and display results
        material_index = ["Steel", "Stainless Steel", "Aluminum", "Brass", "Bronze"].index(calc_material)
        recommended_sfm = df_sfm.iloc[material_index][calc_operation]
        calculated_rpm = (recommended_sfm * 12) / (3.14159 * calc_diameter)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Recommended SFM", recommended_sfm)
        with col2:
            st.metric("Calculated RPM", f"{calculated_rpm:.0f}")
    
    def display_feed_rates(self):
        """Display feed rate guidelines"""
        st.subheader("📏 Feed Rate Guidelines")
        
        # Feed rate guidelines
        feed_data = {
            "Operation": ["Drilling", "Reaming", "Tapping", "Turning", "Boring", "Cutoff"],
            "Steel (in/rev)": [0.005, 0.003, "Pitch", 0.010, 0.005, 0.003],
            "Aluminum (in/rev)": [0.008, 0.005, "Pitch", 0.015, 0.008, 0.005],
            "Brass (in/rev)": [0.006, 0.004, "Pitch", 0.012, 0.006, 0.004],
            "General Rule": ["1% of diameter", "0.5% of diameter", "Equal to pitch", "0.010-0.020", "0.5% of diameter", "0.003-0.005"]
        }
        
        df_feeds = pd.DataFrame(feed_data)
        st.dataframe(df_feeds, use_container_width=True)
        
        # Feed rate calculator
        st.markdown("### Feed Rate Calculator")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            feed_operation = st.selectbox(
                "Operation Type",
                ["Drilling", "Reaming", "Turning", "Boring", "Cutoff"]
            )
        
        with col2:
            feed_material = st.selectbox(
                "Material",
                ["Steel", "Aluminum", "Brass", "Bronze"],
                key="feed_material"
            )
        
        with col3:
            tool_diameter = st.number_input(
                "Tool Diameter (in)",
                min_value=0.001,
                max_value=2.0,
                value=0.250,
                step=0.001,
                format="%.4f",
                key="feed_tool_dia"
            )
        
        # Calculate recommended feed
        feed_multipliers = {
            "Steel": {"Drilling": 0.01, "Reaming": 0.005, "Turning": 0.010, "Boring": 0.005, "Cutoff": 0.003},
            "Aluminum": {"Drilling": 0.015, "Reaming": 0.008, "Turning": 0.015, "Boring": 0.008, "Cutoff": 0.005},
            "Brass": {"Drilling": 0.012, "Reaming": 0.006, "Turning": 0.012, "Boring": 0.006, "Cutoff": 0.004},
            "Bronze": {"Drilling": 0.01, "Reaming": 0.005, "Turning": 0.010, "Boring": 0.005, "Cutoff": 0.003}
        }
        
        if feed_operation in ["Drilling", "Reaming", "Boring"]:
            recommended_feed = tool_diameter * feed_multipliers[feed_material][feed_operation]
        else:
            recommended_feed = feed_multipliers[feed_material][feed_operation]
        
        st.metric("Recommended Feed Rate", f"{recommended_feed:.4f} in/rev")
    
    def display_conversions(self):
        """Display unit conversions and formulas"""
        st.subheader("📐 Unit Conversions & Formulas")
        
        # Common conversions
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Length Conversions")
            conversion_data = {
                "From": ["Inches", "Millimeters", "Feet", "Meters"],
                "To": ["mm", "inches", "inches", "inches"],
                "Multiply by": [25.4, 0.03937, 12, 39.37]
            }
            df_conversions = pd.DataFrame(conversion_data)
            st.dataframe(df_conversions, use_container_width=True)
            
            st.markdown("### Interactive Converter")
            convert_value = st.number_input("Value to Convert", value=1.0)
            convert_from = st.selectbox("From Unit", ["Inches", "Millimeters", "Feet"])
            convert_to = st.selectbox("To Unit", ["Millimeters", "Inches", "Inches"])
            
            if convert_from == "Inches" and convert_to == "Millimeters":
                result = convert_value * 25.4
                st.metric("Result", f"{result:.4f} mm")
            elif convert_from == "Millimeters" and convert_to == "Inches":
                result = convert_value * 0.03937
                st.metric("Result", f"{result:.4f} in")
        
        with col2:
            st.markdown("### Machining Formulas")
            formulas = {
                "Formula": ["Surface Speed (SFM)", "RPM Calculation", "Feed Rate (IPM)", "Cycle Time", "Material Removal Rate"],
                "Equation": [
                    "SFM = (π × D × RPM) / 12",
                    "RPM = (SFM × 12) / (π × D)",
                    "IPM = Feed/Rev × RPM",
                    "Time = Length / IPM",
                    "MRR = IPM × Width × Depth"
                ]
            }
            df_formulas = pd.DataFrame(formulas)
            st.dataframe(df_formulas, use_container_width=True)
            
            # Quick calculator
            st.markdown("### RPM Calculator")
            sfm_input = st.number_input("SFM", value=100)
            diameter_input = st.number_input("Diameter (in)", value=0.250, format="%.4f")
            
            if diameter_input > 0:
                calculated_rpm = (sfm_input * 12) / (3.14159 * diameter_input)
                st.metric("Calculated RPM", f"{calculated_rpm:.0f}")
    
    # Helper methods for data generation
    def get_drill_chart_data(self):
        """Get drill chart reference data"""
        return {
            'number_drills': self.get_number_drill_data(),
            'letter_drills': self.get_letter_drill_data(),
            'fractional_drills': self.get_fractional_drill_data()
        }
    
    def get_number_drill_data(self):
        """Get number drill data"""
        return [
            {"Size": "#80", "Decimal": 0.0135, "mm": 0.343},
            {"Size": "#79", "Decimal": 0.0145, "mm": 0.368},
            {"Size": "#78", "Decimal": 0.0160, "mm": 0.406},
            {"Size": "#77", "Decimal": 0.0180, "mm": 0.457},
            {"Size": "#76", "Decimal": 0.0200, "mm": 0.508},
            {"Size": "#75", "Decimal": 0.0210, "mm": 0.533},
            {"Size": "#74", "Decimal": 0.0225, "mm": 0.572},
            {"Size": "#73", "Decimal": 0.0240, "mm": 0.610},
            {"Size": "#72", "Decimal": 0.0250, "mm": 0.635},
            {"Size": "#71", "Decimal": 0.0260, "mm": 0.660}
        ]
    
    def get_letter_drill_data(self):
        """Get letter drill data"""
        return [
            {"Size": "A", "Decimal": 0.234, "mm": 5.944},
            {"Size": "B", "Decimal": 0.238, "mm": 6.045},
            {"Size": "C", "Decimal": 0.242, "mm": 6.147},
            {"Size": "D", "Decimal": 0.246, "mm": 6.248},
            {"Size": "E", "Decimal": 0.250, "mm": 6.350},
            {"Size": "F", "Decimal": 0.257, "mm": 6.528},
            {"Size": "G", "Decimal": 0.261, "mm": 6.629},
            {"Size": "H", "Decimal": 0.266, "mm": 6.756},
            {"Size": "I", "Decimal": 0.272, "mm": 6.909},
            {"Size": "J", "Decimal": 0.277, "mm": 7.036}
        ]
    
    def get_fractional_drill_data(self):
        """Get fractional drill data"""
        return [
            {"Size": "1/64", "Decimal": 0.0156, "mm": 0.396},
            {"Size": "1/32", "Decimal": 0.0313, "mm": 0.794},
            {"Size": "3/64", "Decimal": 0.0469, "mm": 1.191},
            {"Size": "1/16", "Decimal": 0.0625, "mm": 1.588},
            {"Size": "5/64", "Decimal": 0.0781, "mm": 1.984},
            {"Size": "3/32", "Decimal": 0.0938, "mm": 2.381},
            {"Size": "7/64", "Decimal": 0.1094, "mm": 2.778},
            {"Size": "1/8", "Decimal": 0.1250, "mm": 3.175},
            {"Size": "9/64", "Decimal": 0.1406, "mm": 3.572},
            {"Size": "5/32", "Decimal": 0.1563, "mm": 3.969}
        ]
    
    def get_tap_drill_chart(self):
        """Get tap drill chart data"""
        return [
            {"Thread": "#4-40", "Type": "UNC", "Tap Drill": "#43", "Drill Size": 0.089},
            {"Thread": "#6-32", "Type": "UNC", "Tap Drill": "#36", "Drill Size": 0.106},
            {"Thread": "#8-32", "Type": "UNC", "Tap Drill": "#29", "Drill Size": 0.136},
            {"Thread": "#10-24", "Type": "UNC", "Tap Drill": "#25", "Drill Size": 0.150},
            {"Thread": "#10-32", "Type": "UNF", "Tap Drill": "#21", "Drill Size": 0.159},
            {"Thread": "1/4-20", "Type": "UNC", "Tap Drill": "#7", "Drill Size": 0.201},
            {"Thread": "1/4-28", "Type": "UNF", "Tap Drill": "#3", "Drill Size": 0.213},
            {"Thread": "5/16-18", "Type": "UNC", "Tap Drill": "F", "Drill Size": 0.257},
            {"Thread": "3/8-16", "Type": "UNC", "Tap Drill": "5/16", "Drill Size": 0.313}
        ]
    
    def get_thread_reference_data(self):
        """Get threading reference data"""
        return {
            'methods': ['2:1', '4:1', '6:1', 'Single Point'],
            'applications': ['Soft materials', 'Medium materials', 'Hard materials', 'Custom threads']
        }
    
    def get_material_reference_data(self):
        """Get material reference data"""
        return {
            'materials': ['Steel', 'Stainless Steel', 'Aluminum', 'Brass', 'Bronze'],
            'properties': ['Density', 'Hardness', 'Machinability', 'SFM']
        }
    
    def get_sfm_reference_data(self):
        """Get SFM reference data"""
        return {
            'operations': ['Drilling', 'Reaming', 'Tapping', 'Turning', 'Threading', 'Cutoff'],
            'materials': ['Steel', 'Stainless Steel', 'Aluminum', 'Brass', 'Bronze']
        }
    
    def get_feed_reference_data(self):
        """Get feed rate reference data"""
        return {
            'operations': ['Drilling', 'Reaming', 'Turning', 'Boring', 'Cutoff'],
            'guidelines': ['1% of diameter', '0.5% of diameter', '0.010-0.020', '0.5% of diameter', '0.003-0.005']
        }
    
    def get_tap_diameter_from_thread(self, thread_size):
        """Get tap diameter from thread size"""
        diameter_map = {
            "#4-40": 0.112, "#6-32": 0.138, "#8-32": 0.164,
            "#10-24": 0.190, "#10-32": 0.190,
            "1/4-20": 0.250, "1/4-28": 0.250,
            "5/16-18": 0.3125, "3/8-16": 0.375
        }
        return diameter_map.get(thread_size, 0.250)
    
    def get_thread_pitch_from_size(self, thread_size):
        """Get thread pitch from thread size"""
        pitch_map = {
            "1/4-20": 0.050, "5/16-18": 0.05556, "3/8-16": 0.0625,
            "1/2-13": 0.07692, "5/8-11": 0.09091
        }
        return pitch_map.get(thread_size, 0.050)

# Create global instance
reference_charts = ReferenceCharts()

# Export
__all__ = ['ReferenceCharts', 'reference_charts']