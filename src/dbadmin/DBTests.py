# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:09:30 2015

DB Admin Tests

@author: Alex
"""

from Translator import CSVTranslator, ExcelTranslator, ExternalDBTranslator
from DataBuffer import DataBuffer
from Writer import CSVWriter, ExcelWriter, TerminalWriter
from DataStream import DataStream

class Tester():
    
    def test_buffer(self):
        buf = DataBuffer()
        
        #Append
        buf.append(1)
        assert(buf.data[0] == 1)
        
        buf.append(2)
        assert(buf.data[0] == 1)
        assert(buf.data[1] == 2)
        
        buf.append(3)
        
        #Remove
        buf.remove(1)
        assert(buf.data[0] == 2)
        
        #Clear
        buf.clear()
        assert(buf.length() == 0)
        
        #Next Status
        assert(buf.status == 0)
        buf.next_status()
        assert(buf.status == 1)
        buf.next_status()
        assert(buf.status == 2)
        buf.next_status()
        assert(buf.status == 3)
        buf.next_status()
        assert(buf.status == 3)
        
        #Add Error
        buf.add_error('Test')
        assert(buf.error[0] == 'Test')
        buf.add_error('Test2')
        assert(buf.error[0] == 'Test')
        assert(buf.error[1] == 'Test2')
        
        #Clear Erros
        buf.clear_error()
        assert(len(buf.error) == 0)
    
    def test_stream(self):
        buf = DataBuffer()
        buf2 = DataBuffer()
        buf3 = DataBuffer()
        stream = DataStream()
        stream.buffer_stream.put(buf)
        stream.buffer_stream.put(buf2)
        stream.buffer_stream.put(buf3)
        stream.stream()
        assert(stream.result_stream.get() == buf)
        assert(stream.result_stream.empty() == False)
        stream.result_stream.task_done()
        assert(stream.result_stream.get() == buf2)
        assert(stream.result_stream.empty() == False)
        stream.result_stream.task_done()
        assert(stream.result_stream.get() == buf3)
        assert(stream.result_stream.empty() == True)
        stream.result_stream.task_done()
        assert(stream.result_stream.empty() == True)
        
    def test_csv_translator(self):
        
        #The Data Stream
        stream = DataStream()
        
        #The CSV Translator
        #Input File = test.csv
        #File Type = 0 (Key Action Dataloader)
        #Result Stream = stream.buffer_stream
        #Stream Size = 2
        translator = CSVTranslator('test.csv', 0, stream.buffer_stream, 10)
        print('Translator Created')
        
        #Pull Results from the CSV Files into the data stream
        translator.translate()
        print('Translation Done')
        
        #Pull the data buffers through the data stream
        stream.stream()
        print('Stream Pushed')
        
        #Pull the buffers off the result stream for validation (later, for writing)
        
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '1')
        assert(buf.data[1] == 'TMS')
        assert(buf.type == '1')
        stream.result_stream.task_done()
        print('Buffer 3 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '2')
        assert(buf.data[1] == 'WMOS')
        assert(buf.type == '1')
        stream.result_stream.task_done()
        print('Buffer 4 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '3')
        assert(buf.data[1] == 'MIF')
        assert(buf.type == '1')
        stream.result_stream.task_done()
        print('Buffer 5 checked')
        
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '1')
        assert(buf.data[1] == '1')
        assert(buf.data[2] == 'TP&E')
        assert(buf.type == '2')
        stream.result_stream.task_done()
        print('Buffer 7 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '2')
        assert(buf.data[1] == '1')
        assert(buf.data[2] == 'FAP')
        assert(buf.type == '2')
        stream.result_stream.task_done()
        print('Buffer 8 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '3')
        assert(buf.data[1] == '1')
        assert(buf.data[2] == 'Order Management')
        assert(buf.type == '2')
        stream.result_stream.task_done()
        print('Buffer 9 checked')
        
        #Pull Results from the CSV Files into the data stream
        translator.translate()
        print('Translation Done')
        
        #Pull the data buffers through the data stream
        stream.stream()
        print('Stream Pushed')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '1')
        assert(buf.data[1] == '1')
        assert(buf.data[2] == 'Cons4.0')
        assert(buf.type == '3')
        stream.result_stream.task_done()
        print('Buffer 11 checked')
        
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '2')
        assert(buf.data[1] == '2')
        assert(buf.data[2] == 'Freight Invoicing')
        assert(buf.type == '3')
        stream.result_stream.task_done()
        print('Buffer 12 checked')
        
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '3')
        assert(buf.data[1] == '3')
        assert(buf.data[2] == 'RTS')
        assert(buf.type == '3')
        stream.result_stream.task_done()
        print('Buffer 13 checked')
        
    def test_excel_translator(self):
        
        #The Data Stream
        stream = DataStream()
        
        #The CSV Translator
        #Input File = test.csv
        #File Type = 0 (Key Action Dataloader)
        #Result Stream = stream.buffer_stream
        #Stream Size = 2
        translator = ExcelTranslator('test.xlsx', 0, stream.buffer_stream, 10)
        print('Translator Created')
        
        #Pull Results from the CSV Files into the data stream
        translator.translate()
        print('Translation Done')
        
        #Pull the data buffers through the data stream
        stream.stream()
        print('Stream Pushed')
        
        #Pull the buffers off the result stream for validation (later, for writing)
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 1)
        assert(buf.data[1] == 'TMS')
        assert(buf.type == 1)
        stream.result_stream.task_done()
        print('Buffer 1 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 2)
        assert(buf.data[1] == 'WMOS')
        assert(buf.type == 1)
        stream.result_stream.task_done()
        print('Buffer 2 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 3)
        assert(buf.data[1] == 'MIF')
        assert(buf.type == 1)
        stream.result_stream.task_done()
        print('Buffer 3 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 1)
        assert(buf.data[1] == 1)
        assert(buf.data[2] == 'TP&E')
        assert(buf.type == 2)
        stream.result_stream.task_done()
        print('Buffer 4 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 2)
        assert(buf.data[1] == 1)
        assert(buf.data[2] == 'FAP')
        assert(buf.type == 2)
        stream.result_stream.task_done()
        print('Buffer 5 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 3)
        assert(buf.data[1] == 1)
        assert(buf.data[2] == 'Order Management')
        assert(buf.type == 2)
        stream.result_stream.task_done()
        print('Buffer 6 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 1)
        assert(buf.data[1] == 1)
        assert(buf.data[2] == 'Cons4.0')
        assert(buf.type == 3)
        stream.result_stream.task_done()
        print('Buffer 7 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 2)
        assert(buf.data[1] == 2)
        assert(buf.data[2] == 'Freight Invoicing')
        assert(buf.type == 3)
        stream.result_stream.task_done()
        print('Buffer 8 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 3)
        assert(buf.data[1] == 3)
        assert(buf.data[2] == 'RTS')
        assert(buf.type == 3)
        stream.result_stream.task_done()
        print('Buffer 9 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 1)
        assert(buf.data[1] == 1)
        assert(buf.data[2] == 'Start Engine Run')
        assert(buf.data[3] == 'Start an Engine Run')
        assert(buf.data[4] == 0)
        assert(buf.type == 4)
        stream.result_stream.task_done()
        print('Buffer 10 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 2)
        assert(buf.data[1] == 2)
        assert(buf.data[2] == 'Create Invoice')
        assert(buf.data[3] == 'Create a Freight Invoice')
        assert(buf.data[4] == 0)
        assert(buf.type == 4)
        stream.result_stream.task_done()
        print('Buffer 11 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 3)
        assert(buf.data[1] == 3)
        assert(buf.data[2] == 'Create RTS')
        assert(buf.data[3] == 'Create an RTS')
        assert(buf.data[4] == 0)
        assert(buf.type == 4)
        stream.result_stream.task_done()
        print('Buffer 12 checked')
        
        #Pull Results from the CSV Files into the data stream
        translator.translate()
        print('Translation Done')
        
        #Pull the data buffers through the data stream
        stream.stream()
        print('Stream Pushed')
        
        #Pull the buffers off the result stream for validation (later, for writing)
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 1)
        assert(buf.data[1] == 1)
        assert(buf.data[2] == 'Parameter Set')
        assert(buf.type == 5)
        stream.result_stream.task_done()
        print('Buffer 13 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 2)
        assert(buf.data[1] == 1)
        assert(buf.data[2] == 'Order Filter')
        assert(buf.type == 5)
        stream.result_stream.task_done()
        print('Buffer 14 checked')
        
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == 3)
        assert(buf.data[1] == 1)
        assert(buf.data[2] == 'Shipment Filter')
        assert(buf.type == 5)
        stream.result_stream.task_done()
        print('Buffer 15 checked')
        
        assert(stream.result_stream.empty() == False)
        
    def test_odf_translator(self):
        
        #The Data Stream
        stream = DataStream()
        
        #The CSV Translator
        #Input File = test.csv
        #File Type = 0 (Key Action Dataloader)
        #Result Stream = stream.buffer_stream
        #Stream Size = 2
        translator = ExcelTranslator('test.ods', 0, stream.buffer_stream, 10)
        print('Translator Created')
        
        #Pull Results from the CSV Files into the data stream
        translator.translate()
        print('Translation Done')
        
        #Pull the data buffers through the data stream
        stream.stream()
        print('Stream Pushed')
        
        #Pull the buffers off the result stream for validation (later, for writing)
        assert(stream.result_stream.empty() == False)
        buf = stream.result_stream.get()
        for d in buf.data:
            print(d)
        assert(buf.data[0] == '1')
        assert(buf.data[1] == 'TMS')
        assert(buf.type == '1')
        stream.result_stream.task_done()
        print('Buffer 1 checked')
        
    def test_db_translator(self):
        #The Data Stream
        stream = DataStream()
        
        translator = ExternalDBTranslator('test.db', 0, stream.buffer_stream, 10)
        
        #Pull Results from the CSV Files into the data stream
        translator.translate()
        print('Translation Done')
        
        #Pull the data buffers through the data stream
        stream.stream()
        print('Stream Pushed')
        
        #Pull the buffers off the result stream for validation (later, for writing)
    
    def run_tests(self):
        
        #Pass
        self.test_buffer()
        
        #Pass
        self.test_stream()
        
        #Pass
        self.test_csv_translator()
        
        #Pass
        self.test_excel_translator()
        
        #Fail
        #self.test_odf_translator()
        
        #TO-DO
        #self.test_db_translator()

if __name__ == '__main__':
    Tester().run_tests()