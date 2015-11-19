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

	def validate(buffer_stream, data_buffer):
		#Run validations
		if data_buffer.type == 0:
			#The buffer data type is not assigned, perform no operations
			Logger.debug('Validations: Buffer Data Type not assigned')
		elif data_buffer.type == 1:
			Logger.debug('Validations: Key Action Validation Initialized')
		elif data_buffer.type == 2:
			Logger.debug('Validations: System Area Validation Initialized')
		elif data_buffer.type == 3:
			Logger.debug('Validations: Module Validation Initialized')
		elif data_buffer.type == 4:
			Logger.debug('Validations: Product Validation Initialized')
		elif data_buffer.type == 5:
			Logger.debug('Validations: Client Validation Initialized')
		elif data_buffer.type == 6:
			Logger.debug('Validations: Project Validation Initialized')
		elif data_buffer.type == 7:
			Logger.debug('Validations: Test Script Validation Initialized')
		elif data_buffer.type == 8:
			Logger.debug('Validations: Workflow Validation Initialized')
		elif data_buffer.type == 9:
			Logger.debug('Validations: Workflow Action Validation Initialized')
		elif data_buffer.type == 10:
			Logger.debug('Validations: Input Parameter Validation Initialized')
		elif data_buffer.type == 11:
			Logger.debug('Validations: Workflow Parameter Validation Initialized')
		elif data_buffer.type == 12:
			Logger.debug('Validations: Workflow Next Action Validation Initialized')
		elif data_buffer.type == 13:
			Logger.debug('Validations: Flowchart Validation Initialized')
			
		buffer_stream.task_done()