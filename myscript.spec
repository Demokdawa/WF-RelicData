# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'ducat.png', '.' ),
         ( 'plat.png', '.' ),
		 ( 'icon.png', '.' ),
		 ( 'my_screenshot.png', '.' ),
		 ( 'theme_source.png', '.' ),
		 ( 'ref_fr.txt', '.' ),
		 ( 'relic_pb2.py', '.' ),
		 ( 'relic_pb2_grpc.py', '.' ),
		 ( 'Tesseract-OCR', 'Tesseract-OCR' ),
		 ( 'tessdata', 'tessdata' )
         ]

a = Analysis(['main.py'],
             pathex=['C:\\Users\\aprieto\\Documents\\GitHub\\WF-RelicData'],
             binaries=[],
             datas=added_files,
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='RelicScanner',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
