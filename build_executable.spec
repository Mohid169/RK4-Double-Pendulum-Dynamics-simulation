# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/demos/Demo.gif', 'assets/demos/'),
        ('docs/physics_derivation', 'docs/'),
    ],
    hiddenimports=[
        'pygame',
        'numpy',
        'imageio',
        'imageio.plugins',
        'imageio.plugins.ffmpeg',
        'imageio_ffmpeg',
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
    name='DoublePendulumArt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

# Create a .app bundle on macOS
app = BUNDLE(
    exe,
    name='DoublePendulumArt.app',
    icon=None,
    bundle_identifier='com.doublependulum.art',
    info_plist={
        'CFBundleDisplayName': 'Double Pendulum Art',
        'CFBundleGetInfoString': 'Interactive Double Pendulum Physics Art',
        'CFBundleIdentifier': 'com.doublependulum.art',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': 'True',
    },
) 