"""
Davenport CAM Assistant REV21 - Professional Multi-Spindle Machining System
Main Application Entry Point

A comprehensive CAM programming assistant for Davenport multi-spindle automatic machines.
Includes job setup, CAM operations, threading, quote building, simulation, and reference charts.
"""

import streamlit as st
import sys
from pathlib import Path

# Add SRC directory to path for imports (your modules ARE in SRC!)
src_path = Path(__file__).parent / "SRC"  # Note: SRC not src
sys.path.insert(0, str(src_path))

# Import all modules with comprehensive error handling
try:
    from data_loader import load_data_files
    from utils import JobSetup
    from cam_operations import cam_operations
    from thread_calculator import thread_calculator
    from quote_builder import quote_builder_section  # CORRECTED IMPORT
    from simulation import simulation_system
    from reference_charts import reference_charts
except ImportError as e:
    st.error(f"❌ **Import Error:** {e}")
    st.error("Please ensure all module files are in the 'SRC' directory")
    
    # Show your ACTUAL file structure
    st.markdown("""
    **Expected file structure (matching your screenshots):**
    ```
    📁 _CAM ASSISTANT/
    ├── 📄 main.py                    ← You are here
    ├── 📁 SRC/                       ← Your modules are here
    │   ├── 📄 data_loader.py
    │   ├── 📄 utils.py
    │   ├── 📄 cam_operations.py
    │   ├── 📄 thread_calculator.py
    │   ├── 📄 quote_builder.py
    │   ├── 📄 simulation.py
    │   └── 📄 reference_charts.py
    └── 📁 data/
        ├── 📄 davenport_cams.json
        ├── 📄 materials.json
        └── 📄 ... (other JSON files)
    ```
    """)
    st.stop()

def main():
    """Main application function"""
    
    # Configure Streamlit page
    st.set_page_config(
        page_title="Davenport CAM Assistant REV21",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load data files with error handling
    try:
        data_files = load_data_files()
        if not data_files:
            st.error("⚠️ **No data files loaded.** Please check the 'data' directory.")
            st.info("**Expected location:** C:/Users/Valued Customer/OneDrive/Documents/_CAM ASSISTANT/data/")
            st.stop()
    except Exception as e:
        st.error(f"❌ **Data Loading Error:** {e}")
        st.stop()
    
    # Initialize job setup with error handling
    try:
        job_setup = JobSetup(data_files)
    except Exception as e:
        st.error(f"❌ **Job Setup Error:** {e}")
        st.stop()
    
    # Main header
    st.title("⚙️ Davenport CAM Assistant REV21")
    st.markdown("**Professional Multi-Spindle Machining System** | *Complete CAM Programming Solution*")
    
    # Sidebar for job information
    with st.sidebar:
        st.header("📋 Job Information")
        
        try:
            # Get job setup data
            setup_data = job_setup.job_setup_sidebar()
        except Exception as e:
            st.error(f"Job Setup Error: {e}")
            setup_data = None
        
        # Display current job summary
        if setup_data:
            st.markdown("---")
            st.subheader("📊 Current Job Summary")
            st.text(f"Part: {setup_data.get('part_number', 'Not Set')}")
            st.text(f"Diameter: {setup_data.get('dia', 'Not Set')}\"")
            st.text(f"Material: {setup_data.get('material', 'Not Set')}")
            st.text(f"Machine: {setup_data.get('machine_type', 'Not Set')}")
            st.text(f"RPM: {setup_data.get('rpm', 'Not Set')}")
            st.text(f"Cycle Time: {setup_data.get('cycle_time', 'Not Set')}s")
            
            # Quick access buttons
            st.markdown("---")
            st.subheader("🚀 Quick Actions")
            if st.button("🔄 Reset All Data"):
                # Clear session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            
            if st.button("💾 Save Configuration"):
                st.success("Configuration saved!")
                
            if st.button("📤 Export Data"):
                st.success("Data exported!")
        else:
            st.info("Complete job setup to see summary")
    
    # CORRECTED TAB ORDER - Quote Builder is Tab 1 (Primary Layout/Setup)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 Quote Builder",   # Tab 1 - Primary layout/setup sheet
        "🏗️ Job Setup", 
        "⚙️ CAM Operations", 
        "🔩 Threading", 
        "🎯 Simulation",
        "📚 Reference Charts"
    ])
    
    # Tab 1: Quote Builder - PRIMARY TAB (Layout/Setup Sheet)
    with tab1:
        if not setup_data:
            st.warning("⚠️ Please complete job setup in the sidebar first")
            st.info("👈 Enter basic job information in the sidebar to begin")
        else:
            try:
                # Use the corrected quote builder function
                quote_data = quote_builder_section()
                
                # Store results for other tabs
                if quote_data:
                    st.session_state['quote_data'] = quote_data
            except Exception as e:
                st.error(f"❌ **Quote Builder Error:** {e}")
                st.info("Please check your quote_builder.py file")
                # Show the actual error for debugging
                import traceback
                st.code(traceback.format_exc())
    
    # Tab 2: Job Setup (Detailed Configuration)
    with tab2:
        st.header("🏗️ Job Setup & Machine Configuration")
        
        if not setup_data:
            st.warning("⚠️ Please complete the job setup in the sidebar first")
            st.info("👈 Use the sidebar to enter basic job information")
        else:
            # Enhanced job setup display
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("📋 Part Information")
                st.metric("Part Number", setup_data.get('part_number', 'Not Set'))
                st.metric("Diameter", f"{setup_data.get('dia', 0):.4f}\"")
                st.metric("Length", f"{setup_data.get('length', 0):.3f}\"")
                
            with col2:
                st.subheader("🔧 Machine Setup")
                st.metric("Machine Type", setup_data.get('machine_type', 'Not Set'))
                st.metric("Positions", setup_data.get('machine_config', {}).get('positions', 'Not Set'))
                st.metric("RPM", setup_data.get('rpm', 'Not Set'))
                
            with col3:
                st.subheader("⚡ Performance")
                st.metric("Cycle Time", f"{setup_data.get('cycle_time', 0):.2f}s")
                cpm = 60.0 / setup_data.get('cycle_time', 1) if setup_data.get('cycle_time', 0) > 0 else 0
                st.metric("CPM", f"{cpm:.1f}")
                st.metric("Material", setup_data.get('material', 'Not Set'))
            
            # Material and bar information
            st.markdown("---")
            st.subheader("📦 Material & Bar Information")
            
            bar_col1, bar_col2, bar_col3 = st.columns(3)
            with bar_col1:
                st.metric("Parts per Bar", setup_data.get('parts_per_bar', 'Not Set'))
            with bar_col2:
                st.metric("Bar Weight", f"{setup_data.get('bar_weight', 0):.2f} lbs")
            with bar_col3:
                st.metric("Weight per Part", f"{setup_data.get('part_weight', 0):.4f} lbs")
            
            # Gear configuration display
            if 'spindle_gears' in setup_data or 'feed_gears' in setup_data:
                st.markdown("---")
                st.subheader("⚙️ Current Gear Configuration")
                gear_col1, gear_col2 = st.columns(2)
                with gear_col1:
                    st.text_input("Spindle Gears", value=setup_data.get('spindle_gears', ''), disabled=True)
                with gear_col2:
                    st.text_input("Feed Gears", value=setup_data.get('feed_gears', ''), disabled=True)
            
            # Show simulation results if available
            if 'simulation_results' in st.session_state:
                st.markdown("---")
                st.subheader("🎯 Simulation Results")
                results = st.session_state['simulation_results']
                
                sim_col1, sim_col2, sim_col3, sim_col4 = st.columns(4)
                with sim_col1:
                    st.metric("Total Cycle Time", f"{results.get('total_cycle_time', 0):.2f}s")
                with sim_col2:
                    st.metric("Efficiency", f"{results.get('efficiency', 0):.1f}%")
                with sim_col3:
                    st.metric("Parts/Hour", f"{results.get('parts_per_hour', 0):.0f}")
                with sim_col4:
                    st.metric("Est. Runtime", f"{results.get('estimated_runtime', 0):.1f}h")
    
    # Tab 3: CAM Operations
    with tab3:
        if not setup_data:
            st.warning("⚠️ Please complete Job Setup first")
        else:
            try:
                # Get material data for CAM operations
                material_data = data_files.get('materials', {}).get(setup_data.get('material', 'Steel'), {})
                
                # Run CAM operations
                spindle_data = cam_operations.cam_operations_section(setup_data, material_data)
                
                # Store results for other tabs
                if spindle_data:
                    st.session_state['spindle_operations'] = spindle_data
                    # Also calculate and store cycle time
                    total_cycle_time = sum([op.get('cycle_time', 0) for op in spindle_data if isinstance(op, dict)])
                    st.session_state['cycle_time_from_cam'] = total_cycle_time
            except Exception as e:
                st.error(f"❌ **CAM Operations Error:** {e}")
                st.info("Please check your JSON data files and try again.")
    
    # Tab 4: Threading Calculator
    with tab4:
        if not setup_data:
            st.warning("⚠️ Please complete Job Setup first")
        else:
            try:
                # Run threading calculator
                threading_data = thread_calculator.thread_calculator_section(setup_data)
                
                # Store results for other tabs
                if threading_data:
                    st.session_state['threading_data'] = threading_data
            except Exception as e:
                st.error(f"❌ **Threading Calculator Error:** {e}")
                st.info("Please check your threading JSON data files.")
    
    # Tab 5: Simulation
    with tab5:
        if not setup_data:
            st.warning("⚠️ Please complete Job Setup first")
        else:
            try:
                # Get all available data for simulation
                spindle_ops = st.session_state.get('spindle_operations', [])
                threading_data = st.session_state.get('threading_data', {})
                quote_data = st.session_state.get('quote_data', {})
                
                # Run simulation using the correct method
                sim_results = simulation_system.simulation_interface(setup_data, spindle_ops)
                
                # Store results
                if sim_results:
                    st.session_state['simulation_results'] = sim_results
            except Exception as e:
                st.error(f"❌ **Simulation Error:** {e}")
                import traceback
                st.code(traceback.format_exc())
    
    # Tab 6: Reference Charts
    with tab6:
        try:
            reference_charts.reference_charts_interface()
        except Exception as e:
            st.error(f"❌ **Reference Charts Error:** {e}")
            import traceback
            st.code(traceback.format_exc())
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; font-size: 12px; margin-top: 20px;'>
        🏭 <strong>Davenport CAM Assistant REV21</strong> | 
        Professional Multi-Spindle Programming System | 
        Built for Manufacturing Excellence ⚙️
        </div>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = True
        st.session_state.current_job = {}
        st.session_state.spindle_operations = []
        st.session_state.threading_data = {}
        st.session_state.quote_data = {}
        st.session_state.simulation_results = {}
        st.session_state.cycle_time_from_cam = 1.6

if __name__ == "__main__":
    # Initialize session state
    initialize_session_state()
    
    # Run main application
    main()