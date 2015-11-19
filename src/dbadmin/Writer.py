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
                Logger.debug('Writer: Buffer Data Type not assigned')
            elif data_buffer.type == 1:
                Logger.debug('Writer: Key Action Export Initialized')
            elif data_buffer.type == 2:
                Logger.debug('Writer: System Area Export Initialized')
            elif data_buffer.type == 3:
                Logger.debug('Writer: Module Export Initialized')
            elif data_buffer.type == 4:
                Logger.debug('Writer: Product Export Initialized')
            elif data_buffer.type == 5:
                Logger.debug('Writer: Client Export Initialized')
            elif data_buffer.type == 6:
                Logger.debug('Writer: Project Export Initialized')
            elif data_buffer.type == 7:
                Logger.debug('Writer: Test Script Export Initialized')
            elif data_buffer.type == 8:
                Logger.debug('Writer: Workflow Export Initialized')
            elif data_buffer.type == 9:
                Logger.debug('Writer: Workflow Action Export Initialized')
            elif data_buffer.type == 10:
                Logger.debug('Writer: Input Parameter Export Initialized')
            elif data_buffer.type == 11:
                Logger.debug('Writer: Workflow Parameter Export Initialized')
            elif data_buffer.type == 12:
                Logger.debug('Writer: Workflow Next Action Export Initialized')
            elif data_buffer.type == 13:
                Logger.debug('Writer: Flowchart Export Initialized')
            
            #Finish with the data
            stream.result_stream.task_done()

class TerminalWriter():
    #The error logger
    
    def write(stream):
        while stream.error_stream.empty() == False:
            #Retrieve the top value from the queue
            data = stream.error_stream.get()
            
            #Write the data to the Terminal
            if data_buffer.type == 0:
                #The buffer data type is not assigned, perform no operations
                Logger.debug('Writer: Buffer Data Type not assigned')
            elif data_buffer.type == 1:
                Logger.debug('Writer: Key Action Export Initialized')
            elif data_buffer.type == 2:
                Logger.debug('Writer: System Area Export Initialized')
            elif data_buffer.type == 3:
                Logger.debug('Writer: Module Export Initialized')
            elif data_buffer.type == 4:
                Logger.debug('Writer: Product Export Initialized')
            elif data_buffer.type == 5:
                Logger.debug('Writer: Client Export Initialized')
            elif data_buffer.type == 6:
                Logger.debug('Writer: Project Export Initialized')
            elif data_buffer.type == 7:
                Logger.debug('Writer: Test Script Export Initialized')
            elif data_buffer.type == 8:
                Logger.debug('Writer: Workflow Export Initialized')
            elif data_buffer.type == 9:
                Logger.debug('Writer: Workflow Action Export Initialized')
            elif data_buffer.type == 10:
                Logger.debug('Writer: Input Parameter Export Initialized')
            elif data_buffer.type == 11:
                Logger.debug('Writer: Workflow Parameter Export Initialized')
            elif data_buffer.type == 12:
                Logger.debug('Writer: Workflow Next Action Export Initialized')
            elif data_buffer.type == 13:
                Logger.debug('Writer: Flowchart Export Initialized')
            
            #Finish with the data
            stream.error_stream.task_done()
    
class CSVWriter():
    
    def __init__(self, inp_file):
        self.input_file=inp_file
    
    def write(stream):
        while stream.result_stream.empty() == False:
            #Retrieve the top value from the queue
            data = stream.result_stream.get()
            
            #Write the data to the CSV File
            if data_buffer.type == 0:
                #The buffer data type is not assigned, perform no operations
                Logger.debug('Writer: Buffer Data Type not assigned')
            elif data_buffer.type == 1:
                Logger.debug('Writer: Key Action Export Initialized')
            elif data_buffer.type == 2:
                Logger.debug('Writer: System Area Export Initialized')
            elif data_buffer.type == 3:
                Logger.debug('Writer: Module Export Initialized')
            elif data_buffer.type == 4:
                Logger.debug('Writer: Product Export Initialized')
            elif data_buffer.type == 5:
                Logger.debug('Writer: Client Export Initialized')
            elif data_buffer.type == 6:
                Logger.debug('Writer: Project Export Initialized')
            elif data_buffer.type == 7:
                Logger.debug('Writer: Test Script Export Initialized')
            elif data_buffer.type == 8:
                Logger.debug('Writer: Workflow Export Initialized')
            elif data_buffer.type == 9:
                Logger.debug('Writer: Workflow Action Export Initialized')
            elif data_buffer.type == 10:
                Logger.debug('Writer: Input Parameter Export Initialized')
            elif data_buffer.type == 11:
                Logger.debug('Writer: Workflow Parameter Export Initialized')
            elif data_buffer.type == 12:
                Logger.debug('Writer: Workflow Next Action Export Initialized')
            elif data_buffer.type == 13:
                Logger.debug('Writer: Flowchart Export Initialized')
            
            #Finish with the data
            stream.result_stream.task_done()