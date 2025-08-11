import sys
from pathlib import Path

# Add SRC directory to path
src_path = Path(__file__).parent / "SRC"
sys.path.insert(0, str(src_path))

print(f"Looking for modules in: {src_path}")
print(f"SRC directory exists: {src_path.exists()}")

if src_path.exists():
    print(f"Files in SRC directory:")
    for file in src_path.iterdir():
        print(f"  - {file.name}")

# Test each import individually
modules = [
    ('data_loader', 'load_data_files'),
    ('utils', 'JobSetup'),
    ('cam_operations', 'cam_operations'),
    ('thread_calculator', 'thread_calculator'),
    ('quote_builder', 'quote_builder'),
    ('simulation', 'simulation_system'),
    ('reference_charts', 'reference_charts')
]

for module_name, object_name in modules:
    try:
        module = __import__(module_name)
        obj = getattr(module, object_name)
        print(f"✅ {module_name}.{object_name} - SUCCESS")
    except ImportError as e:
        print(f"❌ {module_name} - IMPORT FAILED: {e}")
    except AttributeError as e:
        print(f"⚠️ {module_name} - MODULE OK, but missing {object_name}: {e}")
    except Exception as e:
        print(f"❌ {module_name} - OTHER ERROR: {e}")