# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Gui_Excel_CSV.py'],
             pathex=['C:\\Users\\nhuan.nguyen\\AppData\\Roaming\\pyRevit\\Extensions\\PySteelFraming.extension\\PySteelFraming.tab\\GetDataFromColumnAndFraming.panel\\TestDataToExcel.pushbutton\\Data_CSV\\CodeDataCSV'],
             binaries=[],
             datas=[('C:\\Users\\nhuan.nguyen\\AppData\\Roaming\\pyRevit\\Extensions\\PySteelFraming.extension\\PySteelFraming.tab\\GetDataFromColumnAndFraming.panel\\TestDataToExcel.pushbutton\\Data_CSV\\CodeDataCSV\\*.xlsx', 'Data' )],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Test11',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Test_Test')
