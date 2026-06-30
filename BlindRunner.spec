# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['blindrunner\\__main__.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('blindrunner/assets', 'assets'),
        ('blindrunner/ingame_levels', 'ingame_levels'),
        ('blindrunner/backup_levels', 'backup_levels'),
        ('blindrunner/player_levels', 'player_levels')
    ],
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
    name='BlindRunner1',
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
    icon='blindrunner/assets/icon.ico'
)
