# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 23:17:39 2016

Class files to store workflow information

@author: alex
"""

class _Workflow():
    def __init__(self):
        self.name = ''
        self.id = 0
        self.keyactions = []
        
    def add_keyaction(self, new_action):
        self.keyactions.append(new_action)
        
    def remove_keyaction(self, action):
        self.keyactions.remove(action)
        
    def clear_keyactions(self):
        del self.keyactions[:]
        
    def numRows(self):
        num_rows = 0
        for action in self.keyactions:
            num_rows+=action.numParams()
        
class _KeyAction():
    def __init__(self):
        self.name = ''
        self.description = ''
        self.systemarea = ''
        self.module = ''
        self.custom = False
        self.id = 0
        self.expected_result = ''
        self.notes = ''
        self.input_parameters = []
        
    def add_inputparameter(self, new_ip):
        self.input_parameters.append(new_ip)
        
    def remove_inputparameter(self, ip):
        self.input_parameters.remove(ip)
        
    def clear_inputparameters(self):
        del self.input_parameters[:]
        
    def numParams(self):
        num_params = 0
        for param in self.input_parameters:
            num_params+=1
        return num_params
        
class _InputParameter():
    def __init__(self):
        self.name = ''
        self.id = 0
        self.value = ''