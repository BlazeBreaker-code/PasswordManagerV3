# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],  # Ensure this points to 'main.py' instead of 'password_manager.py'
    pathex=[],
    binaries=[],
    datas=[('resources/styles.qss', 'resources'), ('C:\\Users\\Suraj\\source\\repos\\PasswordManagerV3\\PasswordManagerV3\\data\\Key.key', 'data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='password_manager',
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
    codesign_identity=None,
    entitlements_file=None,
)
