
#------------------------------------------------------------
#----------------Data Pipeline Buffer------------------------
#------------------------------------------------------------

#This class stores data that will be put through the import/export pipeline
class DataBuffer():
    
    def __init__(self):
        
        #List of data to be processed
        self.data = []
        
        #Error list
        self.error = []
        
        #Status of the data buffer
        #0 = Unprocessed
        #1 = Translated
        #2 = Validated
        #3 = Written
        #4 = Error
        self.status = 0
        
        #The type of the data buffer
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
        self.type = 0
    
    def append(self, val):
        self.data.append(val)
        
    def remove(self, val):
        self.data.remove(val)
        
    def clear(self):
        del self.data[:]
        
    def length(self):
        return len(self.data)
        
    def next_status(self):
        if self.status < 3:
            self.status+=1

    def add_error(self, error_message):
        self.error.append(error_message)
        self.status = 4
        
    def clear_error(self):
        del self.error[:]
        self.status = 0