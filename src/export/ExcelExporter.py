# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:06:25 2015

@author: Alex
"""

import xml.etree.ElementTree as ET
from openpyxl import Workbook
import openpyxl.utils as Utils
import sqlite3 as lite
import os

class TemplateReader():
    #Read the XML Template and generate SQL Queries based on it
    #Pass to the writer each segment individually

    def __init__(self, db_path):
        self.wb = Workbook()
        orig_sheet = self.wb.get_active_sheet()
        self.wb.create_sheet('Header', 0)
        self.wb.remove_sheet(orig_sheet)
        self.db_path=db_path
        
    def select_files_in_folder(self, dir, ext):
        for file in os.listdir(dir):
            if file.endswith('.%s' % ext):
                yield os.path.join(dir, file)
    
    def translate_template(self, xml_path):
        
        #Connect to the DB
        self.con = lite.connect(self.db_path)
        self.cur = self.con.cursor()
        
        with self.con:
        
            #Read the XML Template
            self.tree = ET.parse(xml_path)
            self.root = self.tree.getroot()
            header_ws = self.wb.get_sheet_by_name('Header')
            for child in self.root:
                if child.tag == 'Header':
                    for row in child:
                        #Process each header row
                        for element in row:
                            #Process each element
                            #We expect two property values:
                            #cell, the first cell of the merge
                            #end_cell, the last cell in the merge
                            header_ws[element.attrib['start_cell']] = element.text
                            header_ws.merge_cells('%s:%s' % (element.attrib['start_cell'], element.attrib['end_cell']))
                            print('Header element placed')
                elif child.tag == 'Body':
                    #Process the body segment
                    for page in child:
                        #Process each page
                        body_ws = self.wb.create_sheet(page.attrib['name'])
                        for segment in page:
                            for child in segment:
                                if child.tag == 'Title':
                                    body_ws[segment.attrib['cell']] = child.text
                                    print('Data Title element %s placed in cell %s' % (child.text, segment.attrib['cell']))
                                elif child.tag == 'Header':
                                    i=0
                                    for column in child:
                                        #Place the column header for each query column
                                        #TO-DO: Ensure header column moves down for each segment correctly
                                        cell = Utils.coordinate_from_string(segment.attrib['cell'])
                                        col = Utils.column_index_from_string(cell[0])
                                        body_ws['%s%s' % (Utils.get_column_letter(col+i), 2)] = column.text
                                        print('Data Header element %s placed in cell %s%s' % (column.text, Utils.get_column_letter(col+i), 2))
                                        i+=1
                                elif child.tag == 'Query':
                                    #Execute the query and place the results into the page
                                    self.cur.execute(child.text)
                                    data = self.cur.fetchall()
                                    print('query %s executed' % (child.text))
                                    i=3
                                    for row in data:
                                        j=0
                                        #Place the data into the report
                                        for e in row:
                                            cell = Utils.coordinate_from_string(segment.attrib['cell'])
                                            col = Utils.column_index_from_string(cell[0])
                                            body_ws['%s%s' % (Utils.get_column_letter(col+j), i)] = e
                                            print('Data Element %s placed in column %s%s' % (e, Utils.get_column_letter(col+i), j))
                                            j+=1
                                        i+=1
            self.wb.save('Export.xlsx')