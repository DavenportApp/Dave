# PyInstaller build script for CAM Assistant
# Run this with: python build_exe.py

import os
import sys
import subprocess

def build_exe():
    print("Building CAM Assistant executable...")
    
    # Create spec file content
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-
import streamlit as st
import os

block_cipher = None

# Get Streamlit path
streamlit_path = st.__path__[0]

a = Analysis(
    ['cam_assistant_REV18.py'],
    pathex=[],
    binaries=[],
    datas=[
        (streamlit_path, 'streamlit'),
        ('*.json', '.'),
        ('*.csv', '.'),
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli', 
        'streamlit.runtime',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.state',
        'altair',
        'plotly',
        'plotly.graph_objs',
        'pandas',
        'numpy',
        'openpyxl',
        'click',
        'tornado',
        'pympler',
        'validators',
        'watchdog',
        'blinker',
        'cachetools',
        'importlib_metadata',
        'packaging',
        'pillow',
        'protobuf',
        'pyarrow',
        'python_dateutil',
        'requests',
        'rich',
        'tenacity',
        'toml',
        'typing_extensions',
        'tzlocal',
        'gitpython'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CAM_Assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    cofile=None,
    icon=None,
)
'''
    
    # Write spec file
    with open('cam_assistant.spec', 'w') as f:
        f.write(spec_content)
    
    # Install PyInstaller if not present
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Build the executable
    print("Building executable (this may take 5-10 minutes)...")
    result = subprocess.run([
        sys.executable, '-m', 'PyInstaller', 
        '--clean', 'cam_assistant.spec'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Build successful!")
        print("📁 Executable location: dist/CAM_Assistant.exe")
        print("📏 File size: ~200-400 MB")
        print("⏱️  Startup time: 10-30 seconds")
    else:
        print("❌ Build failed:")
        print(result.stderr)

if __name__ == "__main__":
    build_exe()
