# pip install xlsxwriter 

import xlsxwriter

class writeToExcel:

	def __init__(self, workbook) -> None:
		self.workbook = workbook

	def	createWorkbook(self):
		file = xlsxwriter.Workbook(self.workbook)

		return file
	
	def closeWorkbook(self, workbook):
		workbook.close()

	def createWorksheet(self, workbook, sheet):
		worksheet = workbook.add_worksheet(sheet)

		return worksheet
	
	def defineRowColumn(self, rowNum, columnNum):
		row = rowNum
		col = columnNum

		return row, col

excel = writeToExcel("example.xlsx")
file = excel.createWorkbook()
sheet = excel.createWorksheet(file, "my_sheet")
row, col = excel.defineRowColumn(0,0)

# Data
scores = (
	['ankit', 1000],
	['rahul', 100],
	['priya', 300],
	['harshita', 50],
)

# Iterate over the data and write it out row by row.
for name, score in (scores):
	sheet.write(row, col, name)
	sheet.write(row, col + 1, score)
	row += 1

excel.closeWorkbook(file)
	
