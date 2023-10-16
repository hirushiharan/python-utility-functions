import xlsxwriter

# Class to contain the Write to excel functions
class writeToExcel:

	# Initialize function
	def __init__(self, workbook) -> None:
		self.workbook = workbook

	# Function to create a new excel workbook
	def	createWorkbook(self):
		file = xlsxwriter.Workbook(self.workbook)
		return file
	
	# Function to close the opend workbook
	def closeWorkbook(self, workbook):
		workbook.close()

	# Function to create a new worksheet
	def createWorksheet(self, workbook, sheet):
		worksheet = workbook.add_worksheet(sheet)
		return worksheet
	
	# Function to define the initial row & column
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
	
