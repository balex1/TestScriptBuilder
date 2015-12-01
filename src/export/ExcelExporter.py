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
    
    #Takes in the XML path of the template file
    #params is a list of the input parameters for the template
    #TO-DO: Look for '?' in the xml values and replace it with the next up param
    def translate_template(self, xml_path, params):
        
        #Counter for the input parameters
        param_counter = 0
        
        #Counter for the segments within pages
        segment_counter = 0
        
        #Wild Card Counter
        wc_counter = 0
        
        sn = self.wb.get_sheet_names()
        for s in sn:
            self.wb.remove_sheet(self.wb.get_sheet_by_name(s))
        self.wb.create_sheet('Header', 0)
        
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
                            if '?' not in element.text or element.text != '?':
                                header_ws[element.attrib['start_cell']] = element.text
                            #If a wildcard is encountered, we need to replace it with the
                            #correct parameter
                            else:
                                text = list(element.text)
                                wc_counter = 0
                                for i in text:
                                    if i == '?':
                                        text[wc_counter] = params[param_counter]
                                        print('Parameter %s used' % (params[param_counter]))
                                        param_counter+=1
                                    wc_counter+=1
                                header_ws[element.attrib['start_cell']] = ''.join(text)
                            header_ws.merge_cells('%s:%s' % (element.attrib['start_cell'], element.attrib['end_cell']))
                            print('Header element placed')
                elif child.tag == 'Body':
                    #Process the body segment
                    for page in child:
                        #Process each page
                        segment_counter = 0
                        body_ws = self.wb.create_sheet(page.attrib['name'])
                        for segment in page:
                            for child in segment:
                                if child.tag == 'Title':
                                    if '?' not in child.text or child.text != '?':
                                        body_ws[segment.attrib['cell']] = child.text
                                    #If a wildcard is encountered, we need to replace it with the
                                    #correct parameter
                                    else:
                                        text = list(child.text)
                                        wc_counter = 0
                                        for i in text:
                                            if i == '?':
                                                text[wc_counter] = params[param_counter]
                                                print('Parameter %s used' % (params[param_counter]))
                                                param_counter+=1
                                            wc_counter+=1
                                        body_ws[segment.attrib['cell']] = ''.join(text)
                                    print('Data Title element %s placed in cell %s' % (child.text, segment.attrib['cell']))
                                    segment_counter+=1
                                elif child.tag == 'Header':
                                    i=0
                                    for column in child:
                                        #Place the column header for each query column
                                        cell = Utils.coordinate_from_string(segment.attrib['cell'])
                                        col = Utils.column_index_from_string(cell[0])
                                        body_ws['%s%s' % (Utils.get_column_letter(col+i), 1 + segment_counter)] = column.text
                                        print('Data Header element %s placed in cell %s%s' % (column.text, Utils.get_column_letter(col+i), 2))
                                        i+=1
                                    segment_counter+=1
                                elif child.tag == 'Query':
                                    #Execute the query and place the results into the page
                                    if '?' not in child.text:
                                        self.cur.execute(child.text)
                                    #If a wildcard is encountered, we need to replace it with the
                                    #correct parameter
                                    else:
                                        text = list(child.text)
                                        wc_counter = 0
                                        for i in text:
                                            if i == '?':
                                                text[wc_counter] = params[param_counter]
                                                print('Parameter %s used' % (params[param_counter]))
                                                param_counter+=1
                                            wc_counter+=1
                                        self.cur.execute(''.join(text))
                                    data = self.cur.fetchall()
                                    print('query %s executed' % (child.text))
                                    i=3
                                    for row in data:
                                        j=0
                                        segment_counter+=1
                                        #Place the data into the report
                                        for e in row:
                                            cell = Utils.coordinate_from_string(segment.attrib['cell'])
                                            col = Utils.column_index_from_string(cell[0])
                                            body_ws['%s%s' % (Utils.get_column_letter(col+j), i)] = e
                                            print('Data Element %s placed in column %s%s' % (e, Utils.get_column_letter(col+i), j))
                                            j+=1
                                        i+=1
            self.wb.save('Export.xlsx')