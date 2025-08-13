
### Session State Management
- `setup_data` - Primary job setup information
- `cam_operations_data` - Spindle and tool configurations
- `thread_calc_results` - Threading calculation results
- `spindle_data` - Final machining operations data

---

## Features Overview

### Quote Builder
- **Machine Selection**: Davenport Model B configuration
- **Material Database**: Comprehensive material properties and SFM guidelines
- **Bar Specifications**: Diameter, length, shape, and stock calculations
- **Production Estimates**: Cycle time analysis and quantity pricing
- **Smart Suggestions**: Auto-recommend collets, feed fingers, and burr collects

### CAM Operations
- **5-Position Spindle Setup**: End-working and side-working tool configuration
- **Effective Revolutions Calculation**: Real-time cycle time analysis
- **Cam Recommendations**: Automatic cam selection based on rise requirements
- **Block Setting Validation**: Ensure proper cam engagement ranges
- **Feed Gear Lookup**: Manual-compliant gear selection for optimal production

### Threading Calculator
- **Manual Methodology**: Follows exact Davenport instruction manual procedures
- **Multiple Methods**: 6:1, 2:1, and 4:1 threading configurations
- **Rise Calculations**: Precise cam rise requirements based on thread specifications
- **Time Analysis**: Complete threading operation timing and cycle integration
- **Gear Recommendations**: Official Davenport manual gear configurations

### Knurling System (REV22)
- **Industry Standards**: TPI (12-40) and DP (64-160) specifications
- **Professional Methods**: Bump, Straddle, and End knurling techniques
- **Material Optimization**: Speed and feed recommendations for 7 materials
- **Penetration Calculations**: 50% tooth depth industry standard
- **Timing Analysis**: RPM-based cam space calculations for optimal engagement

---

## Manual Compliance Status

### 100% Compliant Systems:
- ✅ **Threading calculations** - Exact manual methodology
- ✅ **Threading gear recommendations** - Official manual configurations  
- ✅ **Feed gear lookup** - Manual-accurate gear tables
- ✅ **Cycle time data** - Manual cycle time charts
- ✅ **Index times** - Official CPM index specifications
- ✅ **Knurling specifications** - Industry standard compliant

### Data Sources:
- **Threading Gears**: Davenport Manual Pages 135-151
- **Feed Gears**: Official Davenport gear charts (75/60/45 CPM)
- **Cycle Times**: Manual cycle time and effective revolution charts
- **Index Times**: 75 CPM = 0.4s, 60 CPM = 0.5s, 45 CPM = 0.66s

---

## Threading System

### Calculation Methodology
The threading calculator follows the exact Davenport manual procedure:

1. **Input Parameters**:
   - Thread length (inches)
   - Threads per inch (TPI)
   - Work RPM
   - Cycle time
   - Machine cycle rate (CPM)

2. **Working Time Calculation**: