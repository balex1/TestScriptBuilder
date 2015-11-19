from openpyxl import Workbook
from openpyxl import load_workbook
import csv
import sqlite3 as lite
from DataBuffer import DataBuffer

#Translator classes accept an external file as an output and
#creates data buffers to be processed in batches & writes the
#buffers to queues on the data stream

class Translator():
    #Translator base class that the other translators inherit from
    #One translator per file

    #The user should override the process and next_section methods for the
    #individual translator classes.  These are pulled into the translate method
    #which is called by the end user

    #File type = 0 is Key Action
    #File type = 1 is Workflow
    
    def __init__(self, inp_file, file_type, output_stream, stream_size):
        #Internal variables based on input
        self.input_file = inp_file
        self.type = file_type
        self.output_queue = output_stream
        self.stream_size = stream_size
        
        #Internal variables not visible to user
        self.last_read = 0
        self.sections = []
        self.last_section = -1
        self.section_finished = False
        self.translation_finished= False
        
        #Create Sections based on data buffer types
        if file_type == 0:
            self.sections = [4, 3, 2, 1, 10]
        elif file_type == 1:
            self.sections = [5, 6, 7, 8, 9, 11, 12, 13]
        
    #Should be called at beginning of overwritten method
    def next_section(self):
        if self.last_section < len(self.sections) - 1:
            self.last_section+=1
        else:
            self.translation_finished = True
            return True
        
    #Should be called at beginning of overwritten method
    #In the method the user should control the section_finished flag
    def process(self):
        if self.section_finished == True:
            self.next_section()
        #User should implement the rest of this method for each individual translator
    
    def translate(self):
        self.process()
        

class CSVTranslator(Translator):
    
    def __init__(self, inp_file, file_type, output_stream, stream_size):
        super(CSVTranslator, self).__init__(**kwargs)
        #Each entry on the CSV List will start with an integer from 1-13
        #corresponding to the type of the data buffer created
        self.current_type = 0
        self.reader = csv.reader(inp_file, delimiter=',', quotechar='|')
        
    def next_section(self):
        super(CSVTranslator, self).next_section(**kwargs)
    
    def process(self):
        with open(self.input_file, 'rb') as csvfile:
            j=0
            i=self.last_read
            for row in self.reader:
                super(CSVTranslator, self).process(**kwargs)
                if j - i < self.stream_size and j >= i:
                    #Check for the type of the data buffer
                    if row[0] != self.current_type:
                        self.next_section()
                        self.current_type = row[0]

                    #Create the data buffer
                    buf = DataBuffer()
                    for col in row:
                        buf.append(col)
                    buf.type = self.current_type
                    self.output_queue.put(buf)
                    j+=1
            self.last_read+=self.stream_size
    
class ExcelTranslator(Translator):
    
    def __init__(self, inp_file, file_type, output_stream, stream_size):
        super(ExcelTranslator, self).__init__(**kwargs)
        self.wb = load_workbook(filename = self.input_file)
        self.alphabet_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.current_sheet = 0
        self.sheets = self.wb.get_sheet_names()
        self.sheet_name = self.sheets[self.current_sheet]
        
    def next_section(self):
        super(ExcelTranslator, self).next_section(**kwargs)
        self.last_read = 0
        
        #Move to the next excel sheet
        self.current_sheet+=1
        self.sheet_name = self.sheets[self.current_sheet]
    
    def process(self):
        reader = self.wb.get_sheet_by_name(self.sheet_name)
        i = self.last_read
        j = 0
        for i in range(self.last_read, self.last_read+self.stream_size):
            super(ExcelTranslator, self).process(**kwargs)
            buf = DataBuffer()
            start_element = reader['%s1' % (self.alphabet_list[i])]
            
            #TO-DO: Calculate Data Length
            data_length = 0
            
            if start_element != '':
                for j in range(0, data_length):
                    buf.append(reader['%s%s' % (self.alphabet_list[i], j))
            else:
                self.section_finished = True
            buf.type = self.type
            self.output_stream.put(buf)
    
class ExternalDBTranslator(Translator):
    
    def __init__(self, inp_file, file_type, output_stream, stream_size):
        super(ExternalDBTranslator, self).__init__(**kwargs)
        self.con = lite.connect(self.input_file)
        #Key Action
        if self.type == 0:
            self.tables = ['Product', 'Module', 'SystemArea', 'KeyAction', 'InputParameter']
        else:
            self.tables = ['Client', 'Project', 'TestScript', 'Workflow', 'WorkflowAction', 'WorkflowNextAction', 'WorkflowParameter', 'Flowchart']
        self.current_table = 0
        self.table_name = self.tables[self.current_table]

    def next_section(self):
        super(ExternalDBTranslator, self).next_section(**kwargs)
        self.last_read=0
        
        #Move to the next table
        self.current_table+=1
        self.table_name = self.tables[self.current_table]
    
    def process(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM ? ORDER_BY Id LIMIT ? OFFSET ?", (self.table_name, stream_size, self.last_read))
            rows = cur.fetchall()
            if rows is None:
                self.section_finished = True
            else:
                for row in rows:
                    buf = DataBuffer()
                    for col in row:
                        buf.append(col)
                    buf.type = data_type
                    output_stream.put(buf)