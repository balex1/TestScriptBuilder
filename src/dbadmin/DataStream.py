from queue import Queue
from Validator import Validator

#------------------------------------------------------------
#----------------Data Stream---------------------------------
#------------------------------------------------------------

#The data stream contains a queue and applies validations to the
#top data buffer in the queue until it's empty
#This uses Batches

class DataStream():
    def __init__(self):
        self.buffer_stream = Queue(maxsize=0)
        self.error_stream = Queue(maxsize=0)
        self.result_stream = Queue(maxsize=0)
        self.val = Validator()
    
    def stream(self):
        while self.buffer_stream.empty() == False:
            
            #Retrieve the top value from the queue
            data = self.buffer_stream.get()
            
            #Validate the buffer
            self.val.validate(self.buffer_stream, data)
            
            #If there is an error on the buffer, move it to the error stream
            if data.status==4:
                self.error_stream.put(data)
            #Else, put it to the result stream
            else:
                self.result_stream.put(data)