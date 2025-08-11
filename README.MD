# 🔧 Davenport CAM Assistant REV21

**Professional CAM Programming & Production Analysis Tool for Davenport Multi-Spindle Screw Machines**

![Version](https://img.shields.io/badge/version-REV21--1.0.0-blue)
![Status](https://img.shields.io/badge/status-Production%20Ready-green)
![Manual](https://img.shields.io/badge/manual-REV21%20Compliant-orange)

## 📋 Overview

The Davenport CAM Assistant REV21 is a comprehensive, professional-grade tool designed specifically for programming and optimizing Davenport multi-spindle screw machine operations. Built with REV21 Davenport manual compliance, this application provides advanced CAM programming capabilities, threading calculations, and comprehensive cost analysis.

## ✨ Key Features

### 🏭 **Professional CAM Programming**
- Complete spindle position configuration (5-position standard)
- Professional tool library integration
- Advanced operation parameter calculations
- Real-time cycle time analysis with critical path detection
- Material-specific speed and feed recommendations

### 🔩 **REV21 Threading Calculator**
- Complete Davenport REV21 manual compliance
- Professional threading methods (6:1, 4:1, 2:1)
- Advanced thread parameter calculations
- Tool life estimation and surface finish prediction
- Comprehensive threading optimization recommendations

### 💰 **Comprehensive Quote Builder**
- Multi-tier pricing (Prototype, Production, Annual)
- Advanced cost breakdown analysis
- Material cost calculations with overhead
- Professional quote generation and export
- Volume analysis and cost optimization

### 📊 **Advanced Analytics**
- Real-time performance monitoring
- Production rate calculations
- Optimization recommendations
- Professional reporting and export capabilities

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Web browser (Chrome, Firefox, Safari, or Edge)

### Quick Start
1. **Download and Extract**
   ```bash
   # Download the application files
   # Extract to your desired directory
   cd "C:\Your\Directory\_CAM ASSISTANT"
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Application**
   ```bash
   streamlit run main.py
   ```

4. **Access Interface**
   - Open your web browser to `http://localhost:8501`
   - The application will launch automatically

## 📁 Project Structure

```
_CAM ASSISTANT/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                  # This documentation
├── src/                       # Source code directory
│   ├── config.py              # Configuration and constants
│   ├── data_loader.py         # Data management system
│   ├── utils.py               # Utility functions and classes
│   ├── quote_builder.py       # Quote generation and cost analysis
│   ├── cam_operations.py      # CAM operations and spindle configuration
│   └── threading_calculator.py # REV21 threading calculations
└── data/                      # Data files directory
    ├── tool_libraries/        # Tool library data
    ├── materials/            # Material specifications
    ├── threading_data/       # Threading method data
    └── cost_data/           # Cost calculation data
```

## 🎯 Usage Guide

### 1. **Job Setup**
- Enter job name, customer, and part number
- Specify workpiece dimensions (diameter, length)
- Select material type from professional library
- Configure machine RPM and settings
- System validates inputs and provides recommendations

### 2. **CAM Operations Configuration**
- Configure each spindle position (1-5)
- Select operations (Drill, Ream, Tap, Knurl, etc.)
- Choose professional tools from integrated library
- Set operation parameters with smart recommendations
- Analyze cycle time and critical path

### 3. **Threading Calculator**
- Select REV21 Davenport threading method
- Configure thread specifications (diameter, TPI, length)
- Calculate threading parameters and times
- Receive professional optimization recommendations
- Compare all available threading methods

### 4. **Quote Generation**
- Generate quotes for multiple quantities
- Analyze cost breakdown and margins
- Export professional quotes and analysis
- Compare volume pricing scenarios

## 🔧 Professional Features

### **REV21 Manual Compliance**
- Exact threading method implementations
- Proper gear ratio calculations
- Authentic RPM formulas and cam space specifications
- Professional tool and material recommendations

### **Advanced Calculations**
- Surface speed calculations with material factors
- Tool life estimation based on industry standards
- Threading force and time calculations
- Comprehensive cycle time analysis

### **Professional Interface**
- Enterprise-grade user interface
- Real-time validation and error handling
- Comprehensive system monitoring
- Professional export capabilities

### **Data Management**
- Session save/restore functionality
- Professional quote export formats
- Comprehensive error reporting
- System status monitoring

## ⚙️ System Requirements

### **Minimum Requirements**
- **OS:** Windows 10, macOS 10.15, or Linux Ubuntu 18.04+
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 500MB available space
- **Network:** Internet connection for initial setup

### **Recommended Configuration**
- **OS:** Windows 11 or macOS 12+
- **RAM:** 16GB or more
- **Storage:** 1GB+ available space
- **Display:** 1920x1080 or higher resolution

## 🛠️ Configuration Options

### **Machine Configuration**
- Support for 5, 6, and 8-spindle machines
- CPM settings (75, 60, 45)
- Custom spindle position configurations

### **Material Library**
- Steel, Stainless Steel, Brass, Bronze
- Aluminum, Cast Iron, Tool Steel
- Custom material property definitions

### **Tool Library**
- Comprehensive end-working tools
- Complete side-working tool sets
- Professional tool specifications and recommendations

## 📈 Performance & Optimization

### **Real-time Analysis**
- Cycle time calculations with critical path analysis
- Production rate estimates
- Machine utilization metrics
- Optimization recommendations

### **Professional Recommendations**
- Material-specific speed and feed suggestions
- Tool life optimization strategies
- Threading method selection guidance
- Cost optimization opportunities

## 🔍 Troubleshooting

### **Common Issues**

**Application won't start:**
- Verify Python installation and version
- Check all dependencies are installed: `pip install -r requirements.txt`
- Ensure no other application is using port 8501

**Data files not loading:**
- Verify data/ directory structure
- Check file permissions
- Review error messages in system status

**Performance issues:**
- Close unnecessary browser tabs
- Restart the application
- Check system resources and memory usage

### **Error Reporting**
- Use built-in error reporting system
- Export error reports for technical support
- Check system status in sidebar for diagnostics

## 🆘 Support & Documentation

### **Getting Help**
- Built-in help system in application sidebar
- Comprehensive tooltips and guidance throughout interface
- Professional documentation and examples

### **Technical Support**
- Error reporting system with detailed diagnostics
- Session export/import for troubleshooting
- Comprehensive system status monitoring

## 📝 Version History

### **REV21-1.0.0 (Current)**
- Complete REV21 Davenport manual compliance
- Professional threading calculator implementation
- Advanced CAM operations with critical path analysis
- Comprehensive quote builder with multi-tier pricing
- Enterprise-grade user interface and error handling

## 🔧 Development & Customization

### **Extending the Application**
- Modular architecture allows easy feature additions
- Professional configuration system
- Comprehensive utility functions for calculations
- Standardized data formats and interfaces

### **Custom Tool Libraries**
- JSON-based tool library format
- Easy addition of custom tools and specifications
- Professional tool recommendation system
- Material-specific tool suggestions

## ⚖️ Legal & Compliance

### **REV21 Manual Compliance**
This application is designed to be fully compliant with Davenport REV21 manual specifications, including:
- Exact threading method implementations
- Proper gear ratio and RPM calculations
- Authentic cam space specifications
- Professional machining parameter recommendations

### **Disclaimer**
This software is provided as a programming aid and analysis tool. Users are responsible for verifying all calculations and recommendations against current Davenport manual specifications and safety requirements. Always consult official Davenport documentation and qualified machinists for critical applications.

---

## 🎯 **Quick Reference**

| Feature | Location | Key Benefits |
|---------|----------|--------------|
| **Job Setup** | Tab 1 | Professional validation, smart recommendations |
| **CAM Operations** | Tab 2 | Complete spindle configuration, cycle time analysis |
| **Threading** | Tab 3 | REV21 compliance, method comparison, optimization |
| **Quote Builder** | Tab 4 | Multi-tier pricing, comprehensive cost analysis |

---

**⚙️ Davenport CAM Assistant REV21 - Professional CAM Programming Made Simple**

*For technical support or feature requests, use the built-in error reporting system or contact your system administrator.*