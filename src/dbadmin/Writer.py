#------------------------------------------------------------
#----------------Export Writers------------------------------
#------------------------------------------------------------

#0 is not assigned
#1 is product
#2 is module
#3 is system area
#4 is key action
#5 is client
#6 is input parameter
#7 is project
#8 is testscript
#9 is workflow
#10 is workflow action
#11 is workflow next action
#12 is workflow parameter
#13 is flowchart

#Export Writers catch the data stream and write results out to external files

class ExcelWriter():
    
    def __init__(self, inp_file):
        self.input_file=inp_file
    
    def write(self, stream):
        while stream.result_stream.empty() == False:
            #Retrieve the top value from the queue
            data_buffer = stream.get()
            
            #Write the data to the Excel Sheet
            if data_buffer.type == 0:
                #The buffer data type is not assigned, perform no operations
                print('Writer: Buffer Data Type not assigned')
            elif data_buffer.type == 1:
                print('Writer: Key Action Export Initialized')
            elif data_buffer.type == 2:
                print('Writer: System Area Export Initialized')
            elif data_buffer.type == 3:
                print('Writer: Module Export Initialized')
            elif data_buffer.type == 4:
                print('Writer: Product Export Initialized')
            elif data_buffer.type == 5:
                print('Writer: Client Export Initialized')
            elif data_buffer.type == 6:
                print('Writer: Project Export Initialized')
            elif data_buffer.type == 7:
                print('Writer: Test Script Export Initialized')
            elif data_buffer.type == 8:
                print('Writer: Workflow Export Initialized')
            elif data_buffer.type == 9:
                print('Writer: Workflow Action Export Initialized')
            elif data_buffer.type == 10:
                print('Writer: Input Parameter Export Initialized')
            elif data_buffer.type == 11:
                print('Writer: Workflow Parameter Export Initialized')
            elif data_buffer.type == 12:
                print('Writer: Workflow Next Action Export Initialized')
            elif data_buffer.type == 13:
                print('Writer: Flowchart Export Initialized')
            
            #Finish with the data
            stream.result_stream.task_done()

class TerminalWriter():
    #The error logger
    
    def write(self, stream):
        while stream.error_stream.empty() == False:
            #Retrieve the top value from the queue
            data_buffer = stream.error_stream.get()
            
            #Write the data to the Terminal
            if data_buffer.type == 0:
                #The buffer data type is not assigned, perform no operations
                print('Writer: Buffer Data Type not assigned Error Encountered')
            elif data_buffer.type == 1:
                print('Writer: Product Error Encountered')
            elif data_buffer.type == 2:
                print('Writer: Module Error Encountered')
            elif data_buffer.type == 3:
                print('Writer: System Area Error Encountered')
            elif data_buffer.type == 4:
                print('Writer: Key Action Error Encountered')
            elif data_buffer.type == 5:
                print('Writer: Input Parameter Error Encountered')
            elif data_buffer.type == 6:
                print('Writer: Client Error Encountered')
            elif data_buffer.type == 7:
                print('Writer: Project Error Encountered')
            elif data_buffer.type == 8:
                print('Writer: Test Script Error Encountered')
            elif data_buffer.type == 9:
                print('Writer: Workflow Error Encountered')
            elif data_buffer.type == 10:
                print('Writer: Workflow Action Error Encountered')
            elif data_buffer.type == 11:
                print('Writer: Workflow Next Action Error Encountered')
            elif data_buffer.type == 12:
                print('Writer: Workflow Parameter Error Encountered')
            elif data_buffer.type == 13:
                print('Writer: Flowchart Error Encountered')
                
            for d in data_buffer.data:
                print('%s' % (d))
                
            for e in data_buffer.error:
                print('%s' % (e))
            
            #Finish with the data
            stream.error_stream.task_done()
    
class CSVWriter():
    
    def __init__(self, inp_file):
        self.input_file=inp_file
    
    def write(self, stream):
        while stream.result_stream.empty() == False:
            #Retrieve the top value from the queue
            data_buffer = stream.result_stream.get()
            
            #Write the data to the CSV File
            if data_buffer.type == 0:
                #The buffer data type is not assigned, perform no operations
                print('Writer: Buffer Data Type not assigned')
            elif data_buffer.type == 1:
                print('Writer: Key Action Export Initialized')
            elif data_buffer.type == 2:
                print('Writer: System Area Export Initialized')
            elif data_buffer.type == 3:
                print('Writer: Module Export Initialized')
            elif data_buffer.type == 4:
                print('Writer: Product Export Initialized')
            elif data_buffer.type == 5:
                print('Writer: Client Export Initialized')
            elif data_buffer.type == 6:
                print('Writer: Project Export Initialized')
            elif data_buffer.type == 7:
                print('Writer: Test Script Export Initialized')
            elif data_buffer.type == 8:
                print('Writer: Workflow Export Initialized')
            elif data_buffer.type == 9:
                print('Writer: Workflow Action Export Initialized')
            elif data_buffer.type == 10:
                print('Writer: Input Parameter Export Initialized')
            elif data_buffer.type == 11:
                print('Writer: Workflow Parameter Export Initialized')
            elif data_buffer.type == 12:
                print('Writer: Workflow Next Action Export Initialized')
            elif data_buffer.type == 13:
                print('Writer: Flowchart Export Initialized')
            
            #Finish with the data
            stream.result_stream.task_done()