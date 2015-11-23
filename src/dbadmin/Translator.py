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

    #Stream Size is approximate - each translator implements it differently but uses
    #the input value as a guideline
    
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
            self.sections = [1, 2, 3, 4, 5]
        elif file_type == 1:
            self.sections = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
            
        print('Translator base initialized')
        
    #Should be called at beginning of overwritten method
    def next_section(self):
        if self.last_section < len(self.sections) - 1:
            self.last_section+=1
        else:
            self.translation_finished = True
            return True
            
        self.section_finished = False
            
        print('Translator base Next Section Called')
        
    #Should be called at beginning of overwritten method
    #In the method the user should control the section_finished flag
    def process(self):
        if self.section_finished == True:
            self.next_section()
        #User should implement the rest of this method for each individual translator
        print('Translator base Process called')
    
    def translate(self):
        print('Translator base Translate called')
        self.process()
        

class CSVTranslator(Translator):
    
    def __init__(self, inp_file, file_type, output_stream, stream_size):
        Translator.__init__(self, inp_file, file_type, output_stream, stream_size)
        #Each entry on the CSV List will start with an integer from 1-13
        #corresponding to the type of the data buffer created
        self.current_type = 0
        print('CSVTranslator Intialized')
        
    def next_section(self):
        print('CSVTranslator Next Section Called')
        Translator.next_section(self)
    
    def process(self):
        print('CSVTranslator Process Called')
        with open(self.input_file, 'rb') as csvfile:
            self.reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            #Counter to reset on next section
            k=0
            
            #Process Counter
            j=0
            
            #Last Read
            i=self.last_read
            
            
            for row in self.reader:
                
                if j - i < self.stream_size and j >= i:
                    #Check for the type of the data buffer
                    if row[0] != self.current_type:
                        self.next_section()
                        self.current_type = row[0]
                        print('Current Type set to %s' % (self.current_type))
                        k=0
                    else:
                        k+=1
                        
                        #Create the data buffer
                        buf = DataBuffer()
                        print('Data buffer initialized')
                        skipfirst = 0
                        for col in row:
                            if skipfirst != 0:
                                buf.append(col)
                                print('%s appended to data buffer' % (col))
                            skipfirst+=1
                        buf.type = self.current_type
                        #The buffer has been translated
                        buf.next_status()
                        print('Buffer type set to %s' % (self.current_type))
                        self.output_queue.put(buf)
                        print('Buffer written to queue')
                j+=1
            self.last_read+=self.stream_size
            print('Last read set to %s' % (self.last_read))
    
class ExcelTranslator(Translator):
    
    def __init__(self, inp_file, file_type, output_stream, stream_size):
        Translator.__init__(self, inp_file, file_type, output_stream, stream_size)
        self.wb = load_workbook(filename = self.input_file)
        self.alphabet_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.current_sheet = 0
        self.sheets = self.wb.get_sheet_names()
        self.sheet_name = self.sheets[self.current_sheet]
        self.last_read = 1
        
    def next_section(self):
        Translator.next_section(self)
        self.last_read = 2
        
        #Move to the next excel sheet
        if self.type == 0:
            sheet_limit = 4
        else:
            sheet_limit = 8
        if self.current_sheet < sheet_limit:
            self.current_sheet+=1
            self.sheet_name = self.sheets[self.current_sheet]
        else:
            self.translation_finished = True
    
    def process(self):
        counter=0
        while counter < self.stream_size and self.translation_finished == False:
            Translator.process(self)
            reader = self.wb.get_sheet_by_name(self.sheet_name)
            skipfirst = 0
            for row in reader.rows:
                if skipfirst != 0:
                    buf = DataBuffer()
                    start_element = row[0].value
                    
                    #If the row is not empty, populate and push the data buffer
                    if start_element != '' and start_element is not None:
                        for col in row:
                            if col.value != '' and col.value is not None:
                                buf.append(col.value)
                            if self.type == 0:
                                buf.type = self.current_sheet+1
                            else:
                                but.type = self.current_sheet+6
                        buf.next_status()
                        self.output_queue.put(buf)
                    #If the row is empty, flip the section finished flag
                    else:
                        self.section_finished = True
                    counter+=1
                skipfirst+=1
            self.last_read+=self.stream_size
            self.section_finished = True
    
class ExternalDBTranslator(Translator):
    
    def __init__(self, inp_file, file_type, output_stream, stream_size):
        Translator.__init__(self, inp_file, file_type, output_stream, stream_size)
        #Key Action
        if self.type == 0:
            self.tables = ['Product', 'Module', 'SystemArea', 'KeyAction', 'InputParameter']
        else:
            self.tables = ['Product', 'Module', 'SystemArea', 'KeyAction', 'InputParameter', 'Client', 'Project', 'TestScript', 'Workflow', 'WorkflowAction', 'WorkflowNextAction', 'WorkflowParam', 'Flowchart']
        self.current_table = 0
        self.table_name = self.tables[self.current_table]

    def next_section(self):
        Translator.next_section(self)
        self.last_read=0
        
        #Move to the next table
        if self.type == 0:
            table_limit = 4
        else:
            table_limit = 12
        if self.current_table < table_limit:
            self.current_table+=1
            self.table_name = self.tables[self.current_table]
        else:
            self.translation_finished = True
    
    def process(self):
        self.con = lite.connect(self.input_file)
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM {} LIMIT ? OFFSET ?".format(self.table_name), (self.stream_size, self.last_read))
            rows = cur.fetchall()
            self.last_read+=len(rows)
            if len(rows) < self.stream_size:
                self.section_finished = True
            if rows is not None and len(rows) != 0:
                for row in rows:
                    buf = DataBuffer()
                    for col in row:
                        buf.append(col)
                    if self.type == 0:
                        buf.type = self.current_table+1
                    else:
                        buf.type = self.current_table+1
                    buf.next_status()
                    self.output_queue.put(buf)
            Translator.process(self)