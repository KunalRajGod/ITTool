# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('gui/*.css', 'gui'),
        ('database/*.py', 'database'),
        ('modules/*.py', 'modules'),
        ('security/*.py', 'security'),
        ('assets/*', 'assets'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'psutil',
        'bcrypt',
        'speedtest_cli',
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
    [],
    exclude_binaries=True,
    name='PC Repair Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulator=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='PCRepairTool.icns'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PC Repair Tool'
)

app = BUNDLE(
    coll,
    name='PC Repair Tool.app',
    icon='PCRepairTool.icns',
    bundle_identifier='com.pcrepair.tool',
    version='1.0.0',
    info_plist={
        'CFBundleName': 'PC Repair Tool',
        'CFBundleDisplayName': 'PC Repair Tool',
        'CFBundleGetInfoString': 'PC and Mac repair utility',
        'CFBundleIdentifier': 'com.pcrepair.tool',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
        'NSRequiresAquaSystemAppearance': False,
        'LSApplicationCategoryType': 'public.app-category.utilities',
        'NSAppleEventsUsageDescription': 'This app requires access to perform system repairs',
        'NSSystemAdministrationUsageDescription': 'This app requires admin privileges to repair system issues',
    },
)