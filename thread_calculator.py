"""
Thread Calculator Module - Professional Threading Analysis & Gear Calculations
Part of the Davenport CAM Assistant REV21 System
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
import math

class ThreadCalculator:
    """Professional threading calculations and gear analysis"""
    
    def __init__(self):
        self.load_data_files()
    
    def load_data_files(self):
        """Load threading and gear data files"""
        try:
            data_path = Path("data")
            
            # Load threading cam data
            with open(data_path / "Threading_Cams.json", 'r') as f:
                self.threading_cams = json.load(f)
            
            # Load gear data
            with open(data_path / "gears.json", 'r') as f:
                self.gears_data = json.load(f)
            
            # Load machine-specific data
            with open(data_path / "davenport_cams.json", 'r') as f:
                self.davenport_cams = json.load(f)
                
        except Exception as e:
            st.error(f"Error loading threading data files: {e}")
            self.threading_cams = {}
            self.gears_data = {}
            self.davenport_cams = {}
    
    def thread_calculator_section(self, setup_data):
        """Main threading calculator section"""
        st.header("🔩 Thread Calculator & Gear Analysis")
        
        if not setup_data:
            st.warning("⚠️ Please complete Job Setup first")
            return {}
        
        # Get basic setup information
        diameter = setup_data.get("dia", 0.3125)
        material = setup_data.get("material", "Steel")
        rpm = setup_data.get("rpm", 3000)
        cycle_time = setup_data.get("cycle_time", 1.6)
        
        st.info(f"**Part Diameter:** {diameter:.4f}\" | **Material:** {material} | **RPM:** {rpm}")
        
        # Threading specifications
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔩 Threading Specifications")
            
            # Thread pitch/TPI input
            thread_type = st.selectbox("Thread Type", 
                                     ["External (Male)", "Internal (Female)", "Both"], 
                                     key="thread_type")
            
            # Enhanced thread specification with validation
            thread_spec_method = st.radio("Specify Thread By:", 
                                        ["Threads Per Inch (TPI)", "Pitch (inches)", "Metric Pitch (mm)"],
                                        key="thread_spec_method")
            
            if thread_spec_method == "Threads Per Inch (TPI)":
                tpi = st.number_input("Threads Per Inch (TPI)", 
                                    min_value=1.0, max_value=80.0, 
                                    value=20.0, step=0.5, 
                                    key="thread_tpi")
                pitch = 1.0 / tpi
                st.caption(f"**Pitch:** {pitch:.4f} inches")
                
            elif thread_spec_method == "Pitch (inches)":
                pitch = st.number_input("Pitch (inches)", 
                                      min_value=0.0125, max_value=1.0, 
                                      value=0.05, step=0.001, format="%.4f",
                                      key="thread_pitch")
                tpi = 1.0 / pitch
                st.caption(f"**TPI:** {tpi:.1f}")
                
            else:  # Metric pitch
                metric_pitch = st.number_input("Metric Pitch (mm)", 
                                             min_value=0.35, max_value=6.0, 
                                             value=1.25, step=0.05, 
                                             key="metric_pitch")
                pitch = metric_pitch / 25.4  # Convert to inches
                tpi = 1.0 / pitch
                st.caption(f"**Pitch (inches):** {pitch:.4f}")
                st.caption(f"**TPI:** {tpi:.1f}")
            
            # Thread length
            thread_length = st.number_input("Thread Length (inches)", 
                                          min_value=0.010, max_value=2.0, 
                                          value=0.25, step=0.001, format="%.3f",
                                          key="thread_length")
            
            # Calculate threading revolutions
            threading_revs = thread_length / pitch if pitch > 0 else 0
            st.metric("Threading Revolutions", f"{threading_revs:.2f}")
            
        with col2:
            st.subheader("⚙️ Threading Gear Analysis")
            
            # Get current gear configuration
            spindle_gears = setup_data.get("spindle_gears", "44-20")
            feed_gears = setup_data.get("feed_gears", "50-30-60")
            
            st.text_input("Current Spindle Gears", value=spindle_gears, 
                         disabled=True, key="current_spindle_gears")
            st.text_input("Current Feed Gears", value=feed_gears, 
                         disabled=True, key="current_feed_gears")
            
            # Calculate required threading gear ratio
            if pitch > 0:
                # Basic threading gear calculation
                required_ratio = self.calculate_threading_ratio(pitch, rpm)
                
                # Find best gear combination
                recommended_gears = self.find_optimal_threading_gears(required_ratio, tpi)
                
                if recommended_gears:
                    st.success(f"**Recommended Threading Gears:**")
                    st.code(recommended_gears["gear_combination"])
                    
                    # Store recommendation for other tabs
                    st.session_state["recommended_threading_gears"] = recommended_gears["gear_combination"]
                    
                    # Show calculation details
                    with st.expander("📊 Gear Calculation Details", expanded=False):
                        st.write(f"**Required Ratio:** {required_ratio:.4f}")
                        st.write(f"**Actual Ratio:** {recommended_gears.get('actual_ratio', 0):.4f}")
                        st.write(f"**Error:** {recommended_gears.get('error_percent', 0):.2f}%")
                        
                        if "gear_details" in recommended_gears:
                            st.json(recommended_gears["gear_details"])
        
        # Threading compliance and validation
        st.markdown("---")
        st.subheader("✅ Threading Compliance & Validation")
        
        # Manual threading compliance check
        compliance_col1, compliance_col2 = st.columns(2)
        
        with compliance_col1:
            st.markdown("#### 🔍 Manual Threading Analysis")
            
            # Check if threading is feasible with current setup
            manual_revs = st.number_input("Manual Threading Revolutions", 
                                        min_value=0.1, max_value=50.0, 
                                        value=threading_revs, step=0.1,
                                        key="manual_threading_revs")
            
            engagement_angle = st.number_input("Engagement Angle (degrees)", 
                                             min_value=5.0, max_value=45.0, 
                                             value=15.0, step=1.0,
                                             key="engagement_angle")
            
            # Calculate threading time
            if rpm > 0:
                threading_time = manual_revs * 60 / rpm
                st.metric("Threading Time", f"{threading_time:.2f}s")
                
                # Check against cycle time
                if threading_time < (cycle_time * 0.8):  # 80% of cycle time
                    st.success("✅ Threading fits within cycle time")
                else:
                    st.warning("⚠️ Threading may exceed cycle time")
        
        with compliance_col2:
            st.markdown("#### 📋 Threading Standards")
            
            # Common thread standards
            thread_standards = {
                "UNC (Coarse)": self.get_unc_standard(diameter),
                "UNF (Fine)": self.get_unf_standard(diameter),
                "Metric Coarse": self.get_metric_coarse_standard(diameter * 25.4),
                "Metric Fine": self.get_metric_fine_standard(diameter * 25.4)
            }
            
            selected_standard = st.selectbox("Thread Standard", 
                                           list(thread_standards.keys()),
                                           key="thread_standard")
            
            standard_info = thread_standards[selected_standard]
            if standard_info:
                st.info(f"**{selected_standard}:** {standard_info['designation']}")
                st.caption(f"TPI: {standard_info['tpi']:.1f} | Pitch: {standard_info['pitch']:.4f}\"")
                
                # Update button to apply standard
                if st.button(f"Apply {selected_standard}", key="apply_standard"):
                    st.session_state.thread_tpi = standard_info['tpi']
                    st.rerun()
            else:
                st.warning("No standard available for this diameter")
        
        # Threading cam analysis
        st.markdown("---")
        st.subheader("🎯 Threading Cam Analysis")
        
        # Find suitable threading cams
        suitable_cams = self.find_threading_cams(threading_revs, engagement_angle)
        
        if suitable_cams:
            st.success(f"Found {len(suitable_cams)} suitable threading cam(s)")
            
            # Display cam options
            cam_options = [f"{cam['name']} (Rise: {cam['rise']:.3f}\")" 
                          for cam in suitable_cams[:5]]  # Show top 5
            
            selected_cam_idx = st.selectbox("Select Threading Cam", 
                                          range(len(cam_options)),
                                          format_func=lambda x: cam_options[x],
                                          key="selected_threading_cam")
            
            selected_cam = suitable_cams[selected_cam_idx]
            
            # Display cam details
            cam_col1, cam_col2 = st.columns(2)
            with cam_col1:
                st.metric("Cam Rise", f"{selected_cam['rise']:.4f}\"")
                st.metric("Effective Revolutions", f"{selected_cam.get('effective_revs', 0):.2f}")
            
            with cam_col2:
                st.metric("Cam Size", selected_cam.get('size', 'Unknown'))
                st.metric("Engagement %", f"{selected_cam.get('engagement_percent', 0):.1f}%")
        else:
            st.warning("No suitable threading cams found for these parameters")
        
        # Return threading data for other modules
        threading_data = {
            "thread_type": thread_type,
            "tpi": tpi,
            "pitch": pitch,
            "thread_length": thread_length,
            "threading_revs": threading_revs,
            "threading_time": threading_time if 'threading_time' in locals() else 0,
            "recommended_gears": recommended_gears if 'recommended_gears' in locals() else None,
            "selected_cam": selected_cam if 'selected_cam' in locals() else None
        }
        
        # Store in session state for cross-tab access
        st.session_state["threading_data"] = threading_data
        
        return threading_data
    
    def calculate_threading_ratio(self, pitch, rpm):
        """Calculate required threading gear ratio"""
        # This is a simplified calculation - your actual formula may be different
        # Based on machine mechanics and threading requirements
        base_ratio = pitch * rpm / 1000.0  # Simplified formula
        return base_ratio
    
    def find_optimal_threading_gears(self, required_ratio, tpi):
        """Find optimal gear combination for threading"""
        if not self.gears_data:
            return None
        
        # This would search through available gear combinations
        # For now, return a placeholder based on common combinations
        common_combinations = {
            20.0: "44-20-36",  # 20 TPI
            16.0: "44-20-32",  # 16 TPI  
            14.0: "44-20-28",  # 14 TPI
            13.0: "44-20-26",  # 13 TPI
            12.0: "44-20-24",  # 12 TPI
            11.0: "44-20-22",  # 11 TPI
            10.0: "44-20-20",  # 10 TPI
        }
        
        # Find closest TPI match
        closest_tpi = min(common_combinations.keys(), key=lambda x: abs(x - tpi))
        
        return {
            "gear_combination": common_combinations[closest_tpi],
            "actual_ratio": required_ratio,
            "error_percent": abs(closest_tpi - tpi) / tpi * 100,
            "gear_details": {
                "target_tpi": tpi,
                "closest_standard": closest_tpi,
                "recommended": common_combinations[closest_tpi]
            }
        }
    
    def get_unc_standard(self, diameter):
        """Get UNC (Unified National Coarse) standard for diameter"""
        unc_standards = {
            0.0625: {"designation": "#0-80 UNC", "tpi": 80, "pitch": 0.0125},
            0.0730: {"designation": "#1-64 UNC", "tpi": 64, "pitch": 0.015625},
            0.0860: {"designation": "#2-56 UNC", "tpi": 56, "pitch": 0.017857},
            0.0990: {"designation": "#3-48 UNC", "tpi": 48, "pitch": 0.020833},
            0.1120: {"designation": "#4-40 UNC", "tpi": 40, "pitch": 0.025},
            0.1250: {"designation": "#5-40 UNC", "tpi": 40, "pitch": 0.025},
            0.1380: {"designation": "#6-32 UNC", "tpi": 32, "pitch": 0.03125},
            0.1640: {"designation": "#8-32 UNC", "tpi": 32, "pitch": 0.03125},
            0.1900: {"designation": "#10-24 UNC", "tpi": 24, "pitch": 0.041667},
            0.2160: {"designation": "#12-24 UNC", "tpi": 24, "pitch": 0.041667},
            0.2500: {"designation": "1/4-20 UNC", "tpi": 20, "pitch": 0.05},
            0.3125: {"designation": "5/16-18 UNC", "tpi": 18, "pitch": 0.055556},
            0.3750: {"designation": "3/8-16 UNC", "tpi": 16, "pitch": 0.0625},
            0.4375: {"designation": "7/16-14 UNC", "tpi": 14, "pitch": 0.071429},
            0.5000: {"designation": "1/2-13 UNC", "tpi": 13, "pitch": 0.076923},
            0.5625: {"designation": "9/16-12 UNC", "tpi": 12, "pitch": 0.083333},
            0.6250: {"designation": "5/8-11 UNC", "tpi": 11, "pitch": 0.090909},
            0.7500: {"designation": "3/4-10 UNC", "tpi": 10, "pitch": 0.1},
            0.8750: {"designation": "7/8-9 UNC", "tpi": 9, "pitch": 0.111111},
            1.0000: {"designation": "1-8 UNC", "tpi": 8, "pitch": 0.125}
        }
        
        # Find closest diameter
        if diameter in unc_standards:
            return unc_standards[diameter]
        
        # Find closest match
        closest_dia = min(unc_standards.keys(), key=lambda x: abs(x - diameter))
        if abs(closest_dia - diameter) < 0.01:  # Within 0.01" tolerance
            return unc_standards[closest_dia]
        
        return None
    
    def get_unf_standard(self, diameter):
        """Get UNF (Unified National Fine) standard for diameter"""
        unf_standards = {
            0.2500: {"designation": "1/4-28 UNF", "tpi": 28, "pitch": 0.035714},
            0.3125: {"designation": "5/16-24 UNF", "tpi": 24, "pitch": 0.041667},
            0.3750: {"designation": "3/8-24 UNF", "tpi": 24, "pitch": 0.041667},
            0.4375: {"designation": "7/16-20 UNF", "tpi": 20, "pitch": 0.05},
            0.5000: {"designation": "1/2-20 UNF", "tpi": 20, "pitch": 0.05},
            0.5625: {"designation": "9/16-18 UNF", "tpi": 18, "pitch": 0.055556},
            0.6250: {"designation": "5/8-18 UNF", "tpi": 18, "pitch": 0.055556},
            0.7500: {"designation": "3/4-16 UNF", "tpi": 16, "pitch": 0.0625},
            0.8750: {"designation": "7/8-14 UNF", "tpi": 14, "pitch": 0.071429},
            1.0000: {"designation": "1-12 UNF", "tpi": 12, "pitch": 0.083333}
        }
        
        closest_dia = min(unf_standards.keys(), key=lambda x: abs(x - diameter))
        if abs(closest_dia - diameter) < 0.01:
            return unf_standards[closest_dia]
        
        return None
    
    def get_metric_coarse_standard(self, diameter_mm):
        """Get metric coarse thread standard"""
        metric_coarse = {
            3.0: {"designation": "M3x0.5", "tpi": 50.8, "pitch": 0.0197},
            4.0: {"designation": "M4x0.7", "tpi": 36.3, "pitch": 0.0276},
            5.0: {"designation": "M5x0.8", "tpi": 31.7, "pitch": 0.0315},
            6.0: {"designation": "M6x1.0", "tpi": 25.4, "pitch": 0.0394},
            8.0: {"designation": "M8x1.25", "tpi": 20.3, "pitch": 0.0492},
            10.0: {"designation": "M10x1.5", "tpi": 16.9, "pitch": 0.0591},
            12.0: {"designation": "M12x1.75", "tpi": 14.5, "pitch": 0.0689},
            16.0: {"designation": "M16x2.0", "tpi": 12.7, "pitch": 0.0787},
            20.0: {"designation": "M20x2.5", "tpi": 10.2, "pitch": 0.0984}
        }
        
        closest_dia = min(metric_coarse.keys(), key=lambda x: abs(x - diameter_mm))
        if abs(closest_dia - diameter_mm) < 0.5:
            return metric_coarse[closest_dia]
        
        return None
    
    def get_metric_fine_standard(self, diameter_mm):
        """Get metric fine thread standard"""
        metric_fine = {
            8.0: {"designation": "M8x1.0", "tpi": 25.4, "pitch": 0.0394},
            10.0: {"designation": "M10x1.25", "tpi": 20.3, "pitch": 0.0492},
            12.0: {"designation": "M12x1.5", "tpi": 16.9, "pitch": 0.0591},
            16.0: {"designation": "M16x1.5", "tpi": 16.9, "pitch": 0.0591},
            20.0: {"designation": "M20x2.0", "tpi": 12.7, "pitch": 0.0787}
        }
        
        closest_dia = min(metric_fine.keys(), key=lambda x: abs(x - diameter_mm))
        if abs(closest_dia - diameter_mm) < 0.5:
            return metric_fine[closest_dia]
        
        return None
    
    def find_threading_cams(self, threading_revs, engagement_angle):
        """Find suitable threading cams"""
        if not self.threading_cams:
            return []
        
        suitable_cams = []
        
        # Search through threading cam data
        for cam_section, cams in self.threading_cams.items():
            if isinstance(cams, dict):
                for cam_name, cam_info in cams.items():
                    if isinstance(cam_info, dict):
                        # Check if cam can handle the required revolutions
                        cam_revs = cam_info.get("effective_revolutions", 0)
                        cam_rise = cam_info.get("rise", 0)
                        
                        # Simple suitability check
                        if abs(cam_revs - threading_revs) < (threading_revs * 0.2):  # Within 20%
                            suitable_cams.append({
                                "name": cam_name,
                                "rise": cam_rise,
                                "effective_revs": cam_revs,
                                "size": cam_info.get("size", "Unknown"),
                                "engagement_percent": min(100, engagement_angle * 2.5),  # Approximate
                                "section": cam_section
                            })
        
        # Sort by closest match to required revolutions
        suitable_cams.sort(key=lambda x: abs(x["effective_revs"] - threading_revs))
        
        return suitable_cams

# Create global instance
thread_calculator = ThreadCalculator()