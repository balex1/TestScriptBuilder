# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 12:19:56 2015

@author: alex
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, StringProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
from kivy.properties import ListProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

class KeyActionPopup(BoxLayout):

    #Event Properties
    validate = BooleanProperty(False)
    
    #Value Properties
    module = StringProperty('')
    systemarea = StringProperty('')
    keyaction = StringProperty('')
    description = StringProperty('')
    ips = ListProperty([])
    custom = BooleanProperty(False)
    
    #Internal Object Properties
    module_in = ObjectProperty(None)
    sa_in = ObjectProperty(None)
    ka_in = ObjectProperty(None)
    desc_in = ObjectProperty(None)
    custom_in = ObjectProperty(None)
    ipgrid_in = ObjectProperty(None)
 
    #App
    app=ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(KeyActionPopup, self).__init__(**kwargs)
        
        #Layout the basic elements of the element
        self.orientation='vertical'
        topgrid = GridLayout(cols=2, size_hint=(1, 0.1))
        ipgrid = GridLayout(rows=3, size_hint=(1, 0.5))
        self.ipgrid_in = ipgrid
        bottomgrid = GridLayout(cols=2, size_hint=(1, 0.1))
        customgrid = GridLayout(cols=2, size_hint=(0.5, 1))
        modtext = TextInput(hint_text='Module')
        self.module_in = modtext
        satext = TextInput(hint_text='System Area')
        self.sa_in = satext
        katext = TextInput(hint_text='Key Action', size_hint=(1, 0.1))
        self.ka_in = katext
        desctext = TextInput(hint_text='Description', size_hint=(1, 0.2))
        self.desc_in = desctext
        custlabel = Label(text='Custom')
        custcheck = CheckBox()
        self.custom_in = custcheck
        addip_button = Button(text='Add IP', on_press=self.app.add_ip_to_popup)
  
        save = Button(text='Save', size_hint=(1, 0.1))
        save.bind(on_press=self.app.WFSaveQuickActionPopup)
        
        #Bind the save button and text validations
        modtext.bind(on_text_validate=self.Validate)
        satext.bind(on_text_validate=self.Validate)
        katext.bind(on_text_validate=self.Validate)
        desctext.bind(on_text_validate=self.Validate)
        
        #Bind the Properties
        self.bind(module=self.SetModText)
        self.bind(systemarea=self.SetSAText)
        self.bind(keyaction=self.SetKAText)
        self.bind(description=self.SetDescText)
        self.bind(custom=self.SetCustCheck)
        
        #Put the widgets together
        
        #Custom Grid
        customgrid.add_widget(custlabel)
        customgrid.add_widget(custcheck)
        bottomgrid.add_widget(customgrid)
        bottomgrid.add_widget(addip_button)
        
        #Top Grid
        topgrid.add_widget(modtext)
        topgrid.add_widget(satext)
        
        #Base Layout
        self.add_widget(topgrid)
        self.add_widget(katext)
        self.add_widget(desctext)
        self.add_widget(bottomgrid)
        self.add_widget(ipgrid)
        self.add_widget(save)
            
    def Validate(self, *args):
        if self.validate == False:
            self.validate = True
        else:
            self.validate = False
            
    def SetModText(self, *args):
        self.module_in.text = self.module
    def SetSAText(self, *args):
        self.sa_in.text = self.systemarea
    def SetKAText(self, *args):
        self.ka_in.text = self.keyaction
    def SetDescText(self, *args):
        self.desc_in.text = self.description
    def SetIPText(self, *args):
        self.ip_in.text = self.ip1
    def SetIP2Text(self, *args):
        self.ip2_in.text = self.ip2
    def SetIP3Text(self, *args):
        self.ip3_in.text = self.ip3
    def SetCustCheck(self, *args):
        self.custom_in.active = self.custom