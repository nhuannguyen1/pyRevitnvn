from tkinter import *
from tkinter import filedialog
import TextGetDataFromExcel
import TextGetDataFromExcel_ReadExcel
import os
import sys
# function to export excel
def ExportToExcel():
    TextGetDataFromExcel.CreateFileExcel()
#function to define file open 
def mfileopen():
    files = filedialog.askopenfile()
    #label = Label(text = files).pack(side = BOTTOM )
    output.insert(END,files)
    output.pack()
#Function to export Csv
def ExportToCsv():
    TextGetDataFromExcel_ReadExcel.CreateFileCSV()
def CreateWWidget():
    root  = Tk ()
    #write title on widget
    root.title ("Data Processing")
    frame  = Frame (root)
    frame.pack()
    bottomframe = Frame(root)
    bottomframe.pack(side = BOTTOM )
    # Create buttom from Csv to get data 
    Buttom_ExportToCSV  = Button (frame,\
                                text = "ExportToCSV",\
                                command = ExportToCsv)
    #pack to widget 
    Buttom_ExportToCSV.pack(side = LEFT,\
                             expand = True,
                              fill = BOTH)
    # Create buttom from excel to get data 
    Buttom_ExportToExcel  = Button (frame,
                                    text = "ExportToExcel",\
                                    command = ExportToExcel)
    #pack to widget 
    Buttom_ExportToExcel.pack(side = LEFT,
                             expand = True,
                              fill = BOTH)
    # quit widget 
    buttom_quit = Button (bottomframe,
                        text = "Exit",
                        command = root.quit)
    #pack to widget 
    buttom_quit.pack(side = BOTTOM)
    # create buttom
    output = Text(bottomframe,
                    width = 70,
                    height = 3,
                    wrap = WORD,
                    background = "white").pack()
    button = Button(text = "open file",
                        width = 30, 
                        command = mfileopen).\
                        pack()
    root.mainloop()
CreateWWidget()
