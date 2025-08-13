"""
Data loading and management functions for the Davenport CAM Assistant
Handles job data, material data, and file operations
"""

import json
import os
import pandas as pd
from datetime import datetime
from config import TOOL_DEFINITIONS, CONFIG

def load_job_data():
    """Load job data from Excel or JSON files"""
    job_data = {}
    
    # Try to load from Excel first
    try:
        if os.path.exists("job_data.xlsx"):
            df = pd.read_excel("job_data.xlsx")
            for _, row in df.iterrows():
                job_number = str(row.get('Job Number', ''))
                if job_number:
                    job_data[job_number] = {
                        'customer': row.get('Customer', ''),
                        'part_number': row.get('Part Number', ''),
                        'description': row.get('Description', ''),
                        'material': row.get('Material', ''),
                        'quantity': row.get('Quantity', 0),
                        'due_date': row.get('Due Date', ''),
                        'setup_time': row.get('Setup Time', 0),
                        'cycle_time': row.get('Cycle Time', 0)
                    }
    except Exception as e:
        print(f"Could not load Excel file: {e}")
    
    # Fallback to JSON
    if not job_data:
        try:
            with open("job_data.json", "r") as f:
                job_data = json.load(f)
        except FileNotFoundError:
            job_data = {}
    
    return job_data

def save_job_data(job_data):
    """Save job data to JSON file"""
    try:
        with open("job_data.json", "w") as f:
            json.dump(job_data, f, indent=4, default=str)
        return True
    except Exception as e:
        print(f"Error saving job data: {e}")
        return False

def load_material_data():
    """Load material properties and cutting data"""
    try:
        with open("material_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Default material data
        return {
            "12L14": {
                "type": "Free Machining Steel",
                "hardness": "150-200 HB",
                "sfm_range": (200, 400),
                "feed_range": (0.005, 0.020),
                "description": "Excellent machinability, good for high production"
            },
            "1018": {
                "type": "Low Carbon Steel", 
                "hardness": "120-170 HB",
                "sfm_range": (150, 300),
                "feed_range": (0.005, 0.015),
                "description": "Good machinability, weldable"
            },
            "303SS": {
                "type": "Stainless Steel",
                "hardness": "150-200 HB", 
                "sfm_range": (100, 200),
                "feed_range": (0.003, 0.012),
                "description": "Free machining stainless, good corrosion resistance"
            },
            "6061-T6": {
                "type": "Aluminum",
                "hardness": "95 HB",
                "sfm_range": (400, 800),
                "feed_range": (0.008, 0.025),
                "description": "Heat treatable, good strength-to-weight ratio"
            },
            "360 Brass": {
                "type": "Brass",
                "hardness": "65-85 HB",
                "sfm_range": (300, 600),
                "feed_range": (0.008, 0.020),
                "description": "Excellent machinability, good corrosion resistance"
            }
        }

def load_quote_templates():
    """Load quote templates and pricing data"""
    try:
        with open("quote_templates.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Default quote template
        return {
            "standard": {
                "setup_rate": 85.00,
                "machine_rate": 65.00,
                "material_markup": 1.25,
                "tooling_markup": 1.15,
                "overhead_percentage": 0.15,
                "profit_margin": 0.20
            },
            "rush": {
                "setup_rate": 100.00,
                "machine_rate": 75.00,
                "material_markup": 1.30,
                "tooling_markup": 1.20,
                "overhead_percentage": 0.18,
                "profit_margin": 0.25
            }
        }

def save_quote_data(quote_data, job_number):
    """Save quote data with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quote_{job_number}_{timestamp}.json"
    
    try:
        # Create quotes directory if it doesn't exist
        os.makedirs("quotes", exist_ok=True)
        
        with open(f"quotes/{filename}", "w") as f:
            json.dump(quote_data, f, indent=4, default=str)
        return filename
    except Exception as e:
        print(f"Error saving quote: {e}")
        return None

def load_setup_library():
    """Load saved setups and configurations"""
    try:
        with open("setup_library.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_setup_to_library(setup_name, setup_data):
    """Save current setup to library for reuse"""
    try:
        library = load_setup_library()
        library[setup_name] = {
            **setup_data,
            "created_date": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        with open("setup_library.json", "w") as f:
            json.dump(library, f, indent=4, default=str)
        return True
    except Exception as e:
        print(f"Error saving setup: {e}")
        return False

def export_data_to_excel(data_dict, filename):
    """Export data dictionary to Excel file"""
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for sheet_name, data in data_dict.items():
                if isinstance(data, dict):
                    # Convert dict to DataFrame
                    df = pd.DataFrame.from_dict(data, orient='index')
                elif isinstance(data, list):
                    # Convert list to DataFrame
                    df = pd.DataFrame(data)
                else:
                    continue
                
                df.to_excel(writer, sheet_name=sheet_name)
        return True
    except Exception as e:
        print(f"Error exporting to Excel: {e}")
        return False

def backup_data():
    """Create backup of all data files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
        
        files_to_backup = [
            "job_data.json",
            "material_data.json", 
            "quote_templates.json",
            "setup_library.json",
            "config.json",
            "tool_definitions.json"
        ]
        
        for file in files_to_backup:
            if os.path.exists(file):
                with open(file, 'r') as src:
                    with open(f"{backup_dir}/{file}", 'w') as dst:
                        dst.write(src.read())
        
        return backup_dir
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None