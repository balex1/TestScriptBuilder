from openpyxl import Workbook
import os.path

class ExcelReader:
		
	def GetKeyActionPage(self, workbook):
		#Workbook Name
		self.workbook_name = workbook
		
		#If the workbook exists, connect to it.  Otherwise, throw an exception.
		if not os.path.exists(self.workbook_name):
			raise KeyError('Workbook does not exist')
		else:
			wb = load_workbook(self.workbook_name)
			
		#Load the First Worksheet
		ws = wb.get_sheet_by_name('Key_Actions')
		
		i = 0
		result = []
		
		#While the Key Action Name is not blank, iterate through the list
		while ws["C%s" % i] != '':
			result.append(["A%s" % i])
			result.append(["B%s" % i])
			result.append(["C%s" % i])
			result.append(["D%s" % i])
			result.append(["E%s" % i])
			result.append(["F%s" % i])
			i += 1
			
		return result