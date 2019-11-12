import csv
def ReturnDataAllRowByIndexpath (path,NumberRow):
        with open(path) as csvFile:
            readcsv =csv.reader(csvFile, delimiter=';')
            readcsv = list(readcsv)
            RowNumber = readcsv[NumberRow]
        csvFile.close()
        RowNumber.pop(0)
        return RowNumber