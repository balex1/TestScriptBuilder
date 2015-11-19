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
        
    
    
    def run_tests(self):
        self.test_buffer()
        self.test_stream()

if __name__ == '__main__':
    Tester().run_tests()