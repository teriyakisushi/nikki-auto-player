# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('core', 'core'), ('utils', 'utils'), ('logs', 'logs'), ('lang', 'lang'), ('score', 'score'), ('trans', 'trans'), ('config.yaml', '.')],
    hiddenimports=['cn', 'config', 'en', 'loguru', 'map', 'melody', 'melody_deal', 'ref', 'rich', 'score_parse', 'score_reader', 'tools', 'win32api', 'win32con', 'yaml'],
    excludes=[
        'matplotlib', 'tkinter', 'cv2', 'numpy',
        'PIL', 'PIL._imagingtk', 'PIL._tkinter_finder',
        'scipy', 'pandas', 'pyautogui'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NikkiAutoPlayer',
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
    icon='asset/violin.ico',
    version_info={
    'fileversion': (1, 0, 0, 0),
    'productversion': (1, 0, 0, 0),
    'CompanyName': 'SleepFox',
    'FileDescription': 'Infinity Nikki Auto Player for Musical Instrument',
    'ProductName': 'NikkiAutoPlayer',
    'OriginalFilename': 'NikkiAutoPlayer.exe'
    },
    options={
        'encoding': 'utf-8'
    }
)
