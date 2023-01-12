# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['VISROC_2.0.py'],
    pathex=['/folder/to/path/'],
    binaries=[],
    datas=[
    ( '/folder/to/path/LOGO_VISROC_75x75.png', '.' ),
    ( '/folder/to/path/LOGO_VISROC_75x75.icns', '.' ),
    ( '/folder/to/path/graph_interpretation.png', '.'),
    ( '/folder/to/path/Help.html', '.' )],
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
a.datas += [('LOGO_VISROC_75x75.ico', '/folder/to/path/LOGO_VISROC_75x75.icns', 'DATA'),
	    ('LOGO_VISROC_75x75.jpg', '/folder/to/path/LOGO_VISROC_75x75.png', 'DATA'),
	    ('Help.png', '/folder/to/path/graph_interpretation.png', 'DATA'),
	    ('Help.html', '/folder/to/path/Help.html', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VISROC_2.0',
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
    manifest='XML',
)
app = BUNDLE(
    exe,
    name='VISROC_2.0.app',
    icon='/folder/to/path/LOGO_VISROC_75x75.icns',
    bundle_identifier='VISROC_2.0',
    info_plist={'NSRequiresAquaSystemAppearance': True},
)
