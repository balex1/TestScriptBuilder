# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 23:30:27 2015

@author: alex
"""

def coordinate_from_string(coord_string):
    
    temp_string = ""
    num_string = ""
    
    for c in coord_string:
        if c.isdigit() == False:
            temp_string+=c
        else:
            num_string+=c
        
    new_tuple = (temp_string, num_string)
    return new_tuple

def column_index_from_string(str_col):
    
    temp_string = ""
    col_index = 0
    
    for c in coord_string:
        number = ord(c) - 96
        col_index+=number
        
    return col_index

def get_column_letter(index):
    letter_count=0
    while index > 26:
        letter_count+=1
        index-=26
    new_string = ""
    while letter_count > 0:
        new_string.append('A')
        letter_count-=1    
    new_string.append(chr(index + 96))
    return new_string