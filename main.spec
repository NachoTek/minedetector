# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Minedetector game application.

This configuration creates a Windows executable using onedir mode (faster for development).
For production single-file build, use: python -m PyInstaller --onefile --windowed --name=Minedetector --clean main.py
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include the entire src directory
        ('src', 'src'),
    ],
    hiddenimports=[
        # Tkinter and related modules
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        # Application modules (ensure all are included)
        'src.ui.main_window',
        'src.ui.game_grid',
        'src.ui.mine_counter',
        'src.ui.reset_button',
        'src.ui.timer',
        'src.game.board',
        'src.game.adjacent_counter',
        'src.game.chording',
        'src.game.flood_fill',
        'src.game.mine_placement',
        'src.models.cell',
        'src.models.game_state',
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
    name='Minedetector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Critical: Hide console window for Tkinter GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
