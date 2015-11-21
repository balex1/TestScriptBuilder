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
			pass
		elif data_buffer.type == 2:
			pass
		elif data_buffer.type == 3:
			pass
		elif data_buffer.type == 4:
			pass
		elif data_buffer.type == 5:
			pass
		elif data_buffer.type == 6:
			pass
		elif data_buffer.type == 7:
			pass
		elif data_buffer.type == 8:
			pass
		elif data_buffer.type == 9:
			pass
		elif data_buffer.type == 10:
			pass
		elif data_buffer.type == 11:
			pass
		elif data_buffer.type == 12:
			pass
		elif data_buffer.type == 13:
			pass
			
		buffer_stream.task_done()