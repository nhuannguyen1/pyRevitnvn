"""
import os
import cx_Freeze
import sys
import pandas
import openpyxl
import numpy
base = None
if sys.platform == 'win32':
    base = "Win32GUI"
executables = [cx_Freeze.Executable("Gui_Excel_CSV.py", base=base, icon="clienticon.ico")]
cx_Freeze.setup(
    name = "SeaofBTC-Client",
    options = {"build_exe": {"packages":["tkinter","pandas","openpyxl"], "include_files":["clienticon.ico"]}},
    version = "0.01",
    description = "Sea of BTC trading application",
    executables = executables
    )
"""
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["tkinter","pandas","openpyxl"],"include_files":["clienticon.ico"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "guifoo",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Gui_Excel_CSV.py", base=base,icon="clienticon.ico")])
