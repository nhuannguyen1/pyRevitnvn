from tkinter import *
import TextGetDataFromExcel
import TextGetDataFromExcel_ReadExcel
root  = Tk ()
#write title on widget
root.title ("Data Processing")
frame  = Frame (root)
frame.pack()

bottomframe = Frame(root)

bottomframe.pack( side = BOTTOM )

# function to export excel
def ExportToExcel():
    TextGetDataFromExcel.CreateFileExcel()
#Function to export Csv
def ExportToCsv():
    TextGetDataFromExcel_ReadExcel.CreateFileCSV()
def CreateWWidget():
    # Create buttom from Csv to get data 
    Buttom_ExportToCSV  = Button (frame,text = "ExportToCSV",command = ExportToCsv)
    #pack to widget 
    Buttom_ExportToCSV.pack(side = LEFT, expand = True, fill = BOTH)
    # Create buttom from excel to get data 
    Buttom_ExportToExcel  = Button (frame,text = "ExportToExcel",command = ExportToExcel)
    #pack to widget 
    Buttom_ExportToExcel.pack(side = LEFT, expand = True, fill = BOTH)
    # quit widget 
    buttom_quit = Button (bottomframe,text = "Exit",command = root.quit)
    #pack to widget 
    buttom_quit.pack(side = BOTTOM)
    root.mainloop()
CreateWWidget()