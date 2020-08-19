import clr
import xlsxwriter 
  
# Workbook() takes one, non-optional, argument  
# which is the filename that we want to create.
path = r"C:\Users\nhuan.nguyen\AppData\Roaming\pyRevit\Extensions\PySteelFraming.extension\PySteelFraming.tab\TestCode.panel\Rwp.pushbutton\ExcelTest - Copy.xlsx"

workbook = xlsxwriter.Workbook(path) 
  
# The workbook object is then used to add new  
# worksheet via the add_worksheet() method. 
worksheet = workbook.add_worksheet() 
  
row = 0
column = 0
  
content = ["ankit", "rahul", "priya", "harshita", 
                    "sumit", "neeraj", "shivam"] 
  
# iterating through content list 
for item in content : 
  
    # write operation perform 
    worksheet.write(row, column, item) 
  
    # incrementing the value of row by one 
    # with each iteratons. 
    row += 1
  
# Finally, close the Excel file 
# via the close() method. 
workbook.close() 