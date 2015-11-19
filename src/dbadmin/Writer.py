#------------------------------------------------------------
#----------------Export Writers------------------------------
#------------------------------------------------------------

#Export Writers catch the data stream and write results out to external files

class ExcelWriter():
    
    def __init__(self, inp_file):
        self.input_file=inp_file
    
    def write(stream):
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
    
    def write(stream):
        while stream.error_stream.empty() == False:
            #Retrieve the top value from the queue
            data_buffer = stream.error_stream.get()
            
            #Write the data to the Terminal
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
            stream.error_stream.task_done()
    
class CSVWriter():
    
    def __init__(self, inp_file):
        self.input_file=inp_file
    
    def write(stream):
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