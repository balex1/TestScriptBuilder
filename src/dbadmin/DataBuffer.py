
#------------------------------------------------------------
#----------------Data Pipeline Buffer------------------------
#------------------------------------------------------------

#This class stores data that will be put through the import/export pipeline
class DataBuffer():
    
    #List of data to be processed
    data = []
    
    #Error list
    error = []
    
    #Status of the data buffer
    #0 = Unprocessed
    #1 = Translated
    #2 = Validated
    #3 = Written
    #4 = Error
    status = 0
    
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
    type = 0
    
    def append(self, val):
        data.append(val)
        
    def remove(self, val):
        data.remove(val)
        
    def clear(self):
        del data[:]
        
    def next_status(self):
        if status < 3:
            status+=1
            
    def set_error(self, error_message):
        self.error = error_message
        self.status = 4
		
	def add_error(self, error_message):
		self.error.append(error_message)
		self.status = 4
        
    def clear_error(self):
        del self.error[:]
        self.status = 0