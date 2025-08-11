# Drill Chart Content for Reference Charts Tab (tab5)
# Replace the content in tab5 with this code:

    with tab5:
        st.header("📚 Reference Charts & Tables")
        st.markdown("#### 🔍 Quick Reference for Machining Operations")
        
        # Create tabs for different reference charts
        ref_tab1, ref_tab2, ref_tab3, ref_tab4 = st.tabs([
            "🔩 Drill Charts", 
            "🔧 Threading Reference", 
            "📐 Machining Data", 
            "⚙️ Machine Specs"
        ])
        
        with ref_tab1:
            st.subheader("🔩 Standard Drill Size Charts")
            
            # Number drill sizes (most commonly used in machining)
            st.markdown("#### Number Drill Sizes (#80 to #1)")
            number_drill_data = [
                ["#80", "0.0135", "0.343"], ["#79", "0.0145", "0.368"], ["#78", "0.016", "0.406"], ["#77", "0.018", "0.457"],
                ["#76", "0.020", "0.508"], ["#75", "0.021", "0.533"], ["#74", "0.0225", "0.572"], ["#73", "0.024", "0.610"],
                ["#72", "0.025", "0.635"], ["#71", "0.026", "0.660"], ["#70", "0.028", "0.711"], ["#69", "0.0292", "0.742"],
                ["#68", "0.031", "0.787"], ["#67", "0.032", "0.813"], ["#66", "0.033", "0.838"], ["#65", "0.035", "0.889"],
                ["#64", "0.036", "0.914"], ["#63", "0.037", "0.940"], ["#62", "0.038", "0.965"], ["#61", "0.039", "0.991"],
                ["#60", "0.040", "1.016"], ["#59", "0.041", "1.041"], ["#58", "0.042", "1.067"], ["#57", "0.043", "1.092"],
                ["#56", "0.0465", "1.181"], ["#55", "0.052", "1.321"], ["#54", "0.055", "1.397"], ["#53", "0.0595", "1.511"],
                ["#52", "0.0635", "1.613"], ["#51", "0.067", "1.702"], ["#50", "0.070", "1.778"], ["#49", "0.073", "1.854"],
                ["#48", "0.076", "1.930"], ["#47", "0.0785", "1.994"], ["#46", "0.081", "2.057"], ["#45", "0.082", "2.083"],
                ["#44", "0.086", "2.184"], ["#43", "0.089", "2.261"], ["#42", "0.0935", "2.375"], ["#41", "0.096", "2.438"],
                ["#40", "0.098", "2.489"], ["#39", "0.0995", "2.527"], ["#38", "0.1015", "2.578"], ["#37", "0.104", "2.642"],
                ["#36", "0.1065", "2.705"], ["#35", "0.110", "2.794"], ["#34", "0.111", "2.819"], ["#33", "0.113", "2.870"],
                ["#32", "0.116", "2.946"], ["#31", "0.120", "3.048"], ["#30", "0.1285", "3.264"], ["#29", "0.136", "3.454"],
                ["#28", "0.1405", "3.569"], ["#27", "0.144", "3.658"], ["#26", "0.147", "3.734"], ["#25", "0.1495", "3.797"],
                ["#24", "0.152", "3.861"], ["#23", "0.154", "3.912"], ["#22", "0.157", "3.988"], ["#21", "0.159", "4.039"],
                ["#20", "0.161", "4.089"], ["#19", "0.166", "4.216"], ["#18", "0.1695", "4.305"], ["#17", "0.173", "4.394"],
                ["#16", "0.177", "4.496"], ["#15", "0.180", "4.572"], ["#14", "0.182", "4.623"], ["#13", "0.185", "4.699"],
                ["#12", "0.189", "4.801"], ["#11", "0.191", "4.851"], ["#10", "0.1935", "4.915"], ["#9", "0.196", "4.978"],
                ["#8", "0.199", "5.055"], ["#7", "0.201", "5.105"], ["#6", "0.204", "5.182"], ["#5", "0.2055", "5.220"],
                ["#4", "0.209", "5.309"], ["#3", "0.213", "5.410"], ["#2", "0.221", "5.613"], ["#1", "0.228", "5.791"]
            ]
            
            number_df = pd.DataFrame(number_drill_data, columns=["Number Size", "Decimal (in)", "Metric (mm)"])
            st.dataframe(number_df, hide_index=True, use_container_width=True)
            
            # Letter drill sizes
            st.markdown("#### Letter Drill Sizes (A to Z)")
            letter_drill_data = [
                ["A", "0.234", "5.944"], ["B", "0.238", "6.045"], ["C", "0.242", "6.147"], ["D", "0.246", "6.248"],
                ["E", "0.250", "6.350"], ["F", "0.257", "6.528"], ["G", "0.261", "6.629"], ["H", "0.266", "6.756"],
                ["I", "0.272", "6.909"], ["J", "0.277", "7.036"], ["K", "0.281", "7.137"], ["L", "0.290", "7.366"],
                ["M", "0.295", "7.493"], ["N", "0.302", "7.671"], ["O", "0.316", "8.026"], ["P", "0.323", "8.204"],
                ["Q", "0.332", "8.433"], ["R", "0.339", "8.611"], ["S", "0.348", "8.839"], ["T", "0.358", "9.093"],
                ["U", "0.368", "9.347"], ["V", "0.377", "9.576"], ["W", "0.386", "9.804"], ["X", "0.397", "10.08"],
                ["Y", "0.404", "10.26"], ["Z", "0.413", "10.49"]
            ]
            
            letter_df = pd.DataFrame(letter_drill_data, columns=["Letter Size", "Decimal (in)", "Metric (mm)"])
            st.dataframe(letter_df, hide_index=True, use_container_width=True)
            
            # Common fractional drill sizes
            st.markdown("#### Common Fractional Drill Sizes")
            fractional_drill_data = [
                ["1/64", "0.015625", "0.397"], ["1/32", "0.03125", "0.794"], ["3/64", "0.046875", "1.191"],
                ["1/16", "0.0625", "1.588"], ["5/64", "0.078125", "1.984"], ["3/32", "0.09375", "2.381"],
                ["7/64", "0.109375", "2.778"], ["1/8", "0.125", "3.175"], ["9/64", "0.140625", "3.572"],
                ["5/32", "0.15625", "3.969"], ["11/64", "0.171875", "4.366"], ["3/16", "0.1875", "4.763"],
                ["13/64", "0.203125", "5.159"], ["7/32", "0.21875", "5.556"], ["15/64", "0.234375", "5.953"],
                ["1/4", "0.250", "6.350"], ["17/64", "0.265625", "6.747"], ["9/32", "0.28125", "7.144"],
                ["19/64", "0.296875", "7.541"], ["5/16", "0.3125", "7.938"], ["21/64", "0.328125", "8.334"],
                ["11/32", "0.34375", "8.731"], ["23/64", "0.359375", "9.128"], ["3/8", "0.375", "9.525"],
                ["25/64", "0.390625", "9.922"], ["13/32", "0.40625", "10.319"], ["27/64", "0.421875", "10.716"],
                ["7/16", "0.4375", "11.113"], ["29/64", "0.453125", "11.509"], ["15/32", "0.46875", "11.906"],
                ["31/64", "0.484375", "12.303"], ["1/2", "0.500", "12.700"]
            ]
            
            fractional_df = pd.DataFrame(fractional_drill_data, columns=["Fraction", "Decimal (in)", "Metric (mm)"])
            st.dataframe(fractional_df, hide_index=True, use_container_width=True)
            
            # Search functionality
            st.markdown("#### 🔍 Quick Drill Size Lookup")
            search_size = st.text_input("Enter drill size (e.g., #7, 1/4, 0.250):", placeholder="Enter size to search...")
            
            if search_size:
                # Search through all drill sizes
                all_sizes = number_drill_data + letter_drill_data + fractional_drill_data
                results = []
                search_term = search_size.upper().strip()
                
                for size_data in all_sizes:
                    try:
                        if (search_term in size_data[0].upper() or 
                            search_term in size_data[1]):
                            results.append(size_data)
                        elif search_term.replace('#', '').replace('"', '').replace('.', '').isdigit():
                            search_val = float(search_term.replace('#', '').replace('"', ''))
                            if abs(float(size_data[1]) - search_val) < 0.001:
                                results.append(size_data)
                    except (ValueError, IndexError):
                        continue
                
                if results:
                    st.success(f"Found {len(results)} matching drill sizes:")
                    result_df = pd.DataFrame(results, columns=["Size", "Decimal (in)", "Metric (mm)"])
                    st.dataframe(result_df, hide_index=True, use_container_width=True)
                else:
                    st.warning("No matching drill sizes found.")
        
        with ref_tab2:
            st.subheader("🔧 Threading Reference")
            st.info("Threading charts and tap drill sizes will be added here")
            
            # Common thread tap drill sizes
            st.markdown("#### Common Thread Tap Drill Sizes")
            tap_drill_data = [
                ["#4-40", "#43", "0.089", "2.26"], ["#6-32", "#36", "0.1065", "2.71"], 
                ["#8-32", "#29", "0.136", "3.45"], ["#10-24", "#25", "0.1495", "3.80"],
                ["#10-32", "#21", "0.159", "4.04"], ["#12-24", "#16", "0.177", "4.50"],
                ["1/4-20", "#7", "0.201", "5.11"], ["1/4-28", "#3", "0.213", "5.41"],
                ["5/16-18", "F", "0.257", "6.53"], ["5/16-24", "I", "0.272", "6.91"],
                ["3/8-16", "5/16", "0.3125", "7.94"], ["3/8-24", "Q", "0.332", "8.43"],
                ["7/16-14", "U", "0.368", "9.35"], ["7/16-20", "25/64", "0.391", "9.92"],
                ["1/2-13", "27/64", "0.422", "10.72"], ["1/2-20", "29/64", "0.453", "11.51"]
            ]
            
            tap_df = pd.DataFrame(tap_drill_data, columns=["Thread Size", "Tap Drill", "Decimal (in)", "Metric (mm)"])
            st.dataframe(tap_df, hide_index=True, use_container_width=True)
            
        with ref_tab3:
            st.subheader("📐 Machining Reference Data")
            
            # SFM reference for common materials
            st.markdown("#### Surface Feet per Minute (SFM) Reference")
            sfm_data = [
                ["Mild Steel", "100-150", "200-300", "80-120"],
                ["Stainless Steel", "60-100", "150-250", "50-80"],
                ["Aluminum", "300-500", "600-1000", "250-400"],
                ["Brass", "200-300", "400-600", "150-250"],
                ["Cast Iron", "80-120", "150-250", "60-100"],
                ["Tool Steel", "40-80", "100-180", "30-60"],
                ["Titanium", "30-60", "80-150", "25-50"],
                ["Inconel", "20-40", "60-120", "15-30"]
            ]
            
            sfm_df = pd.DataFrame(sfm_data, columns=["Material", "Drilling SFM", "Turning SFM", "Threading SFM"])
            st.dataframe(sfm_df, hide_index=True, use_container_width=True)
            
            # Feed rate guidelines
            st.markdown("#### General Feed Rate Guidelines")
            feed_data = [
                ["Drilling", "0.002-0.010", "0.004-0.015", "0.001-0.005"],
                ["Reaming", "0.004-0.012", "0.008-0.020", "0.003-0.008"],
                ["Tapping", "Auto (pitch)", "Auto (pitch)", "Auto (pitch)"],
                ["Turning", "0.005-0.020", "0.010-0.030", "0.003-0.015"],
                ["Threading", "Auto (pitch)", "Auto (pitch)", "Auto (pitch)"],
                ["Cutoff", "0.001-0.005", "0.002-0.008", "0.001-0.003"]
            ]
            
            feed_df = pd.DataFrame(feed_data, columns=["Operation", "Steel (in/rev)", "Aluminum (in/rev)", "Stainless (in/rev)"])
            st.dataframe(feed_df, hide_index=True, use_container_width=True)
            
        with ref_tab4:
            st.subheader("⚙️ Davenport Machine Specifications")
            
            # Machine capacity data
            st.markdown("#### Davenport Model B Specifications")
            machine_specs = [
                ["Bar Capacity", "1/8\" to 1-5/8\"", "3.2mm to 41.3mm"],
                ["Bar Length", "Up to 12 feet", "Up to 3.66 meters"],
                ["Spindle Speed", "50-2000 RPM", "Variable speed"],
                ["Number of Spindles", "5 positions", "Standard configuration"],
                ["Collet Range", "1/8\" to 1-5/8\"", "Step collets available"],
                ["Threading Capability", "6:1, 4:1, 2:1", "Multiple ratios"],
                ["Cycle Rate", "45-75 CPM", "Depends on part complexity"],
                ["Power Requirements", "15-25 HP", "Main spindle motor"]
            ]
            
            specs_df = pd.DataFrame(machine_specs, columns=["Specification", "Imperial", "Notes/Metric"])
            st.dataframe(specs_df, hide_index=True, use_container_width=True)
            
            # Common collet sizes
            st.markdown("#### Standard Collet Sizes")
            collet_data = [
                ["1/8\"", "0.125", "3.18"], ["5/32\"", "0.156", "3.97"], ["3/16\"", "0.188", "4.76"],
                ["1/4\"", "0.250", "6.35"], ["5/16\"", "0.313", "7.94"], ["3/8\"", "0.375", "9.53"],
                ["7/16\"", "0.438", "11.11"], ["1/2\"", "0.500", "12.70"], ["9/16\"", "0.563", "14.29"],
                ["5/8\"", "0.625", "15.88"], ["11/16\"", "0.688", "17.46"], ["3/4\"", "0.750", "19.05"],
                ["13/16\"", "0.813", "20.64"], ["7/8\"", "0.875", "22.23"], ["15/16\"", "0.938", "23.81"],
                ["1\"", "1.000", "25.40"], ["1-1/8\"", "1.125", "28.58"], ["1-1/4\"", "1.250", "31.75"],
                ["1-3/8\"", "1.375", "34.93"], ["1-1/2\"", "1.500", "38.10"], ["1-5/8\"", "1.625", "41.28"]
            ]
            
            collet_df = pd.DataFrame(collet_data, columns=["Collet Size", "Decimal (in)", "Metric (mm)"])
            st.dataframe(collet_df, hide_index=True, use_container_width=True)
