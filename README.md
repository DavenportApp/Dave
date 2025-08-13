# CAM Assistant REV8

A comprehensive Streamlit application for Davenport multi-spindle CAM machine setup and programming.

## Features

- **Job Setup & Quoting**: Material selection, machine configuration, and production time calculations
- **CAM Operations**: Spindle setup with tool selection and cam recommendations
- **Threading Calculator**: Precise threading calculations with gear recommendations
- **3D Simulation**: Visual representation of machining operations
- **Setup Sheet Generation**: Excel export for machine setup documentation

## Quick Start

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:

   ```bash
   streamlit run cam_assistant_REV8.py
   ```

3. **Open in browser**: The app will automatically open at `http://localhost:8501`

## Project Structure

```
cam-assistant/
├── cam_assistant_REV8.py      # Main Streamlit application
├── requirements.txt           # Python dependencies
├── config.json               # Machine configurations
├── materials.json            # Material properties database
├── davenport_cams.json       # Davenport cam specifications
├── tool_definitions.json     # Tool library definitions
└── *.json                    # Various data files and configurations
```

## Recent Updates (REV8)

✅ **Threading Calculator Improvements**:

- Corrected threading calculations to match Davenport manual
- Added threading method recommendations based on cycle time
- Fixed session state persistence across tabs

✅ **Data Persistence**:

- Thread calculator inputs now persist when switching tabs
- CAM operations data preserved during navigation
- Improved user experience with consistent data retention

✅ **Smart Recommendations**:

- Automatic threading method suggestions based on cycle time
- Threading gear recommendations with TPI calculations
- Cam suggestions based on rise requirements

## Threading Methods

- **6:1 Threading**: Best for precision, slower cutting (> 6 sec cycles)
- **2:1 Threading**: General purpose, moderate speed (< 3 sec cycles)
- **4:1 Threading**: Balanced performance (3-6 sec cycles)

## Usage Tips

1. **Start with Job Setup**: Configure your material, dimensions, and machine settings
2. **Set Up CAM Operations**: Define tools and operations for each spindle position
3. **Calculate Threading**: Use the threading calculator for precise gear and cam selection
4. **Review Simulation**: Check the 3D visualization before final setup
5. **Generate Setup Sheet**: Export complete documentation for the machine operator

## Support

This application is specifically designed for Davenport Model B multi-spindle machines with 5 positions. All calculations follow Davenport engineering guidelines and manual specifications.

## Development

- Built with Streamlit for interactive web interface
- Uses Plotly for 3D visualizations
- Pandas for data management
- OpenpyXL for Excel export functionality
