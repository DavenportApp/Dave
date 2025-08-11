"""
Simulation Module - Multi-Spindle Machine Simulation System
Part of the Davenport CAM Assistant REV21 System
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
import math

class SimulationSystem:
    """Professional simulation system for multi-spindle operations"""
    
    def __init__(self):
        """Initialize simulation system"""
        self.simulation_data = {}
        self.cycle_history = []
    
    def simulation_interface(self, setup_data, cam_operations_data):
        """Main simulation interface"""
        st.header("🔄 Machine Simulation & Analysis")
        
        if not setup_data:
            st.warning("⚠️ Please complete Job Setup first")
            return {}
        
        if not cam_operations_data:
            st.warning("⚠️ Please configure CAM Operations first")
            return {}
        
        # Simulation controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Simulation Controls")
            simulation_cycles = st.number_input(
                "Number of Cycles to Simulate",
                min_value=1,
                max_value=1000,
                value=100,
                step=10
            )
            
            run_simulation = st.button("🔄 Run Simulation", type="primary")
        
        with col2:
            st.subheader("Current Job")
            st.metric("Part Number", setup_data.get('part_number', 'N/A'))
            st.metric("Machine Type", setup_data.get('machine_type', 'N/A'))
            st.metric("Operations", len(cam_operations_data))
        
        with col3:
            st.subheader("Expected Results")
            if cam_operations_data:
                total_cycle_time = sum(op.get('cycle_time', 0) for op in cam_operations_data)
                parts_per_hour = 3600 / total_cycle_time if total_cycle_time > 0 else 0
                
                st.metric("Cycle Time", f"{total_cycle_time:.2f}s")
                st.metric("Parts/Hour", f"{parts_per_hour:.0f}")
        
        if run_simulation:
            # Run the simulation
            simulation_results = self.run_cycle_simulation(
                setup_data, cam_operations_data, simulation_cycles
            )
            
            # Display results
            self.display_simulation_results(simulation_results)
            
            return simulation_results
        
        return {}
    
    def run_cycle_simulation(self, setup_data, operations, num_cycles):
        """Run multi-cycle simulation"""
        st.info(f"🔄 Running simulation for {num_cycles} cycles...")
        
        # Initialize simulation results
        results = {
            'cycles_completed': 0,
            'total_time': 0.0,
            'average_cycle_time': 0.0,
            'parts_produced': 0,
            'efficiency': 0.0,
            'operation_times': [],
            'cycle_data': []
        }
        
        # Calculate theoretical cycle time
        theoretical_cycle_time = sum(op.get('cycle_time', 0) for op in operations)
        
        # Add machine overhead (indexing, loading, etc.)
        indexing_time = len(operations) * 0.2  # 0.2s per index
        loading_time = 2.0  # 2s for bar loading
        
        # Simulate each cycle
        progress_bar = st.progress(0)
        
        for cycle in range(num_cycles):
            # Simulate cycle with some variation
            cycle_variation = np.random.normal(1.0, 0.05)  # ±5% variation
            actual_cycle_time = (theoretical_cycle_time + indexing_time) * cycle_variation
            
            if cycle == 0:
                actual_cycle_time += loading_time  # First cycle includes loading
            
            # Record cycle data
            cycle_data = {
                'cycle': cycle + 1,
                'cycle_time': actual_cycle_time,
                'operations': self.simulate_operation_times(operations, cycle_variation)
            }
            
            results['cycle_data'].append(cycle_data)
            results['total_time'] += actual_cycle_time
            results['parts_produced'] = cycle + 1
            
            # Update progress
            progress_bar.progress((cycle + 1) / num_cycles)
        
        # Calculate final statistics
        results['cycles_completed'] = num_cycles
        results['average_cycle_time'] = results['total_time'] / num_cycles
        results['parts_per_hour'] = 3600 / results['average_cycle_time']
        results['efficiency'] = theoretical_cycle_time / results['average_cycle_time'] * 100
        
        progress_bar.empty()
        
        return results
    
    def simulate_operation_times(self, operations, variation_factor):
        """Simulate individual operation times with variation"""
        operation_times = []
        
        for operation in operations:
            base_time = operation.get('cycle_time', 0)
            # Add operation-specific variation
            op_variation = np.random.normal(variation_factor, 0.02)  # ±2% additional variation
            actual_time = base_time * op_variation
            
            operation_times.append({
                'position': operation.get('position', 0),
                'operation': operation.get('operation', 'Unknown'),
                'planned_time': base_time,
                'actual_time': actual_time,
                'variation': (actual_time - base_time) / base_time * 100 if base_time > 0 else 0
            })
        
        return operation_times
    
    def display_simulation_results(self, results):
        """Display comprehensive simulation results"""
        st.markdown("---")
        st.subheader("📊 Simulation Results")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Cycles Completed", results['cycles_completed'])
        with col2:
            st.metric("Avg Cycle Time", f"{results['average_cycle_time']:.2f}s")
        with col3:
            st.metric("Parts per Hour", f"{results['parts_per_hour']:.0f}")
        with col4:
            st.metric("Efficiency", f"{results['efficiency']:.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Cycle time trend
            cycle_numbers = [cd['cycle'] for cd in results['cycle_data']]
            cycle_times = [cd['cycle_time'] for cd in results['cycle_data']]
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=cycle_numbers,
                y=cycle_times,
                mode='lines+markers',
                name='Cycle Time',
                line=dict(color='blue', width=2)
            ))
            
            # Add average line
            avg_time = results['average_cycle_time']
            fig_trend.add_hline(y=avg_time, line_dash="dash", 
                               line_color="red", 
                               annotation_text=f"Average: {avg_time:.2f}s")
            
            fig_trend.update_layout(
                title="Cycle Time Trend",
                xaxis_title="Cycle Number",
                yaxis_title="Cycle Time (seconds)",
                height=400
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            # Cycle time distribution
            fig_hist = px.histogram(
                x=cycle_times,
                nbins=20,
                title="Cycle Time Distribution",
                labels={'x': 'Cycle Time (seconds)', 'y': 'Frequency'}
            )
            fig_hist.update_layout(height=400)
            
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Operation analysis
        if results['cycle_data']:
            st.subheader("🔧 Operation Performance Analysis")
            
            # Get operation data from last cycle
            last_cycle_ops = results['cycle_data'][-1]['operations']
            
            if last_cycle_ops:
                op_df = pd.DataFrame(last_cycle_ops)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Operation time comparison
                    fig_ops = go.Figure()
                    
                    positions = op_df['position'].tolist()
                    planned_times = op_df['planned_time'].tolist()
                    actual_times = op_df['actual_time'].tolist()
                    
                    fig_ops.add_trace(go.Bar(
                        x=positions,
                        y=planned_times,
                        name='Planned Time',
                        marker_color='lightblue'
                    ))
                    
                    fig_ops.add_trace(go.Bar(
                        x=positions,
                        y=actual_times,
                        name='Actual Time',
                        marker_color='orange'
                    ))
                    
                    fig_ops.update_layout(
                        title="Operation Times by Position",
                        xaxis_title="Position",
                        yaxis_title="Time (seconds)",
                        barmode='group',
                        height=400
                    )
                    
                    st.plotly_chart(fig_ops, use_container_width=True)
                
                with col2:
                    # Operation details table
                    display_df = op_df[['position', 'operation', 'planned_time', 'actual_time', 'variation']].copy()
                    display_df['planned_time'] = display_df['planned_time'].round(3)
                    display_df['actual_time'] = display_df['actual_time'].round(3)
                    display_df['variation'] = display_df['variation'].round(1)
                    display_df.columns = ['Pos', 'Operation', 'Planned (s)', 'Actual (s)', 'Var (%)']
                    
                    st.dataframe(display_df, use_container_width=True)
        
        # Production summary
        st.subheader("📈 Production Summary")
        
        production_data = {
            'Metric': [
                'Total Simulation Time',
                'Parts Produced', 
                'Average Parts per Hour',
                'Total Machine Time',
                'Efficiency Rating'
            ],
            'Value': [
                f"{results['total_time']:.1f} seconds",
                f"{results['parts_produced']} parts",
                f"{results['parts_per_hour']:.0f} pcs/hr",
                f"{results['total_time']/3600:.2f} hours",
                f"{results['efficiency']:.1f}%"
            ]
        }
        
        summary_df = pd.DataFrame(production_data)
        st.table(summary_df)
        
        # Export option
        if st.button("📊 Export Simulation Data"):
            # Create export data
            export_data = {
                'simulation_summary': results,
                'cycle_data': results['cycle_data']
            }
            
            # Convert to CSV format for display
            csv_data = pd.DataFrame(results['cycle_data'])
            st.download_button(
                label="Download Simulation Results (CSV)",
                data=csv_data.to_csv(index=False),
                file_name=f"simulation_results_{results['cycles_completed']}_cycles.csv",
                mime="text/csv"
            )
    
    def calculate_machine_utilization(self, operations_data):
        """Calculate machine utilization metrics"""
        if not operations_data:
            return {}
        
        # Calculate theoretical maximum throughput
        theoretical_cycle_time = sum(op.get('cycle_time', 0) for op in operations_data)
        
        # Add realistic machine overhead
        setup_time = 2.0  # seconds
        indexing_time = len(operations_data) * 0.2
        
        realistic_cycle_time = theoretical_cycle_time + indexing_time
        
        # Calculate utilization metrics
        utilization = {
            'theoretical_cycle_time': theoretical_cycle_time,
            'realistic_cycle_time': realistic_cycle_time,
            'machine_efficiency': theoretical_cycle_time / realistic_cycle_time * 100,
            'theoretical_pph': 3600 / theoretical_cycle_time if theoretical_cycle_time > 0 else 0,
            'realistic_pph': 3600 / realistic_cycle_time if realistic_cycle_time > 0 else 0
        }
        
        return utilization
    
    def generate_optimization_suggestions(self, simulation_results, operations_data):
        """Generate optimization suggestions based on simulation results"""
        suggestions = []
        
        if not simulation_results or not operations_data:
            return suggestions
        
        efficiency = simulation_results.get('efficiency', 0)
        
        if efficiency < 85:
            suggestions.append("⚡ Consider optimizing feed rates to improve efficiency")
        
        if efficiency < 75:
            suggestions.append("🔧 Review operation sequence for better optimization")
        
        avg_cycle_time = simulation_results.get('average_cycle_time', 0)
        if avg_cycle_time > 3.0:
            suggestions.append("⏱️ Cycle time is high - consider parallel operations")
        
        # Analyze operation balance
        if 'cycle_data' in simulation_results and simulation_results['cycle_data']:
            last_ops = simulation_results['cycle_data'][-1].get('operations', [])
            if last_ops:
                times = [op['actual_time'] for op in last_ops]
                if times:
                    time_variation = (max(times) - min(times)) / max(times) * 100
                    if time_variation > 50:
                        suggestions.append("⚖️ Operations are unbalanced - redistribute work")
        
        return suggestions

# Create global instance
simulation_system = SimulationSystem()

# Export
__all__ = ['SimulationSystem', 'simulation_system']