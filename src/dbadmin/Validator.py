#------------------------------------------------------------
#----------------Validator-----------------------------------
#------------------------------------------------------------

#The validate function performs validations on the data buffers
#0 is not assigned
#1 is key action
#2 is system area
#3 is module
#4 is product
#5 is client
#6 is project
#7 is testscript
#8 is workflow
#9 is workflow action
#10 is input parameter
#11 is workflow parameter
#12 is workflow next action
#13 is flowchart
class Validator():

	def validate(self, buffer_stream, data_buffer):
		#Run validations
		if data_buffer.type == 0:
			#The buffer data type is not assigned, perform no operations
			print('Validations: Buffer Data Type not assigned')
		elif data_buffer.type == 1:
			print('Validations: Key Action Validation Initialized')
		elif data_buffer.type == 2:
			print('Validations: System Area Validation Initialized')
		elif data_buffer.type == 3:
			print('Validations: Module Validation Initialized')
		elif data_buffer.type == 4:
			print('Validations: Product Validation Initialized')
		elif data_buffer.type == 5:
			print('Validations: Client Validation Initialized')
		elif data_buffer.type == 6:
			print('Validations: Project Validation Initialized')
		elif data_buffer.type == 7:
			print('Validations: Test Script Validation Initialized')
		elif data_buffer.type == 8:
			print('Validations: Workflow Validation Initialized')
		elif data_buffer.type == 9:
			print('Validations: Workflow Action Validation Initialized')
		elif data_buffer.type == 10:
			print('Validations: Input Parameter Validation Initialized')
		elif data_buffer.type == 11:
			print('Validations: Workflow Parameter Validation Initialized')
		elif data_buffer.type == 12:
			print('Validations: Workflow Next Action Validation Initialized')
		elif data_buffer.type == 13:
			print('Validations: Flowchart Validation Initialized')
			
		buffer_stream.task_done()