# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
    ('src/data/dialogues/*.*',           'data/dialogues'),
    ('src/data/fonts/*.*',               'data/fonts'),
    ('src/data/images/*.*',              'data/images'),
    ('src/data/images/portraits/*.*',    'data/images/portraits'),
    ('src/data/images/spritesheets/*.*', 'data/images/spritesheets'),
    ('src/data/maps/*.*',                'data/maps'),
    ('src/data/maps/tsx/*.*',            'data/maps/tsx'),
    ('src/data/music/*.*',               'data/music'),
    ('src/data/sounds/*.*',              'data/sounds')
    ]

a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=added_files,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Unnamed',
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
    icon='src/data/images/icondefault.ico'
)
