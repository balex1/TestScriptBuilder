# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:06:25 2015

@author: Alex
"""

import xml.etree.ElementTree as ET
from openpyxl import Workbook, Utils
import sqlite3 as lite

class TemplateReader():
    #Read the XML Template and generate SQL Queries based on it
    #Pass to the writer each segment individually

    def __init__(self, db_path):
        self.wb = Workbook()
        orig_sheet = self.wb.get_active_sheet()
        self.wb.create_sheet('Header', 0)
        self.wb.remove_sheet(orig_sheet)
    
    def translate_template(self, xml_path):
        
        #Connect to the DB
        self.con = lite.connect(db_path)
        self.cur = self.con.cursor()
        
        with con:
        
            #Read the XML Template
            self.tree = ET.parse(xml_path)
            self.root = self.tree.getroot()
            header_ws = self.wb.get_sheet_by_name('Header')
            for child in self.root.children:
                if child.tag == 'Header':
                    for row in child.children:
                        #Process each header row
                        for element in row.children:
                            #Process each element
                            #We expect two property values:
                            #cell, the first cell of the merge
                            #end_cell, the last cell in the merge
                            header_ws[element.properties['start_cell']] = element.text
                            header_ws.merge_cells('%s:%s' % (element.attrib['start_cell'], element.attrib['end_cell']))
                            
                elif child.tag == 'Body':
                    #Process the body segment
                    for page in child.children:
                        #Process each page
                        body_ws = self.wb.create_sheet(page.attrib['name'])
                        for segment in page.children:
                            for child in segment:
                                if child.tag == 'Title':
                                    body_ws[segment.attrib['cell']] = child.text
                                elif child.tag == 'Header':
                                    i=0
                                    for column in child.children:
                                        #Place the column header for each query column
                                        cell = Utils.coordinate_from_string(segment.attrib['cell'])
                                        col = Utils.column_index_from_string(cell[0])
                                        body_ws['%s%s' % (Utils.get_column_letter(col+i), 2)] = column.text
                                        i+=1
                                elif child.tag == 'Query':
                                    #Execute the query and place the results into the page
                                    self.cur.execute(child.text)
                                    data = self.cur.fetchall()
                                    i=0
                                    for row in data:
                                        j=2
                                        #Place the data into the report
                                        for e in row:
                                            cell = Utils.coordinate_from_string(segment.attrib['cell'])
                                            col = Utils.column_index_from_string(cell[0])
                                            body_ws['%s%s' % (Utils.get_column_letter(col+i), j)] = e
                                        