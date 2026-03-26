# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# Python DLL 자동 탐지
python_dir = os.path.dirname(sys.executable)
python_version = f"{sys.version_info.major}{sys.version_info.minor}"
dll_name = f"python{python_version}.dll"
dll_path = os.path.join(python_dir, dll_name)

binaries_list = []
if os.path.exists(dll_path):
    binaries_list.append((dll_path, '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries_list,
    datas=[('shipbuilding_dict.db', '.')] if os.path.exists('shipbuilding_dict.db') else [],
    hiddenimports=[],
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
    a.binaries,       # 추가
    a.zipfiles,       # 추가
    a.datas,          # 추가
    exclude_binaries=False,  # True → False
    name='ShipbuildingDictionary',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='./assets/icon.ico' if os.path.exists('./assets/icon.ico') else None,
)
