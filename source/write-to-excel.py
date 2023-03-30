# pip install xlsxwriter 

import xlsxwriter

workbook = xlsxwriter.Workbook('example.xlsx')

# Define worksheet name
worksheet = workbook.add_worksheet("My sheet")

# Some data we want to write to the worksheet.
scores = (
	['ankit', 1000],
	['rahul', 100],
	['priya', 300],
	['harshita', 50],
)

# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

# Iterate over the data and write it out row by row.
for name, score in (scores):
	worksheet.write(row, col, name)
	worksheet.write(row, col + 1, score)
	row += 1

workbook.close()
