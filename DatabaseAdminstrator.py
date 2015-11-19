from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.uix.popup import Popup

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from Queue import Queue

from src.dbadmin.Translator import CSVTranslator, ExcelTranslator, ExternalDBTranslator
from src.dbadmin.DataBuffer import DataBuffer
from src.dbadmin.Writer import CSVWriter, ExcelWriter, TerminalWriter
from src.dbadmin.DataStream import DataStream
from src.dbadmin.Validator import Validator

import os.path
import platform

#------------------------------------------------------------
#----------------ORM-----------------------------------------
#------------------------------------------------------------

#Instantiate the Declarative Base Class
Base = declarative_base()
Logger.info('SQLAlchemy: Declaritive Base Instantiated')

#Store the base level key action
class KeyAction(Base):
    __tablename__ = 'keyaction'
    
    id = Column(Integer, primary_key=True)
    systemareaid = Column(Integer, ForeignKey('systemarea.id'))
    name = Column(String)
    description = Column(String)
    custom = Column(Boolean)
    
    sys = relationship("SystemArea", backref=backref('keyaction', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<Key Action: ID = '%s', System Area ID = '%s', Name = '%s', Description = '%s', Custom = '%s'>" % (self.id, self.systemareaid, self.name, self.description, self.custom)

#Store the base level system area
class SystemArea(Base):
    __tablename__ = 'systemarea'
    
    id = Column(Integer, primary_key=True)
    moduleid = Column(Integer, ForeignKey('module.id'))
    name = Column(String)
    
    mod = relationship("Module", backref=backref('systemarea', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<System Area: ID = '%s', Module ID = '%s', Name = '%s'>" % (self.id, self.moduleid, self.name)

#Store the base level module
class Module(Base):
    __tablename__ = 'module'
    
    id = Column(Integer, primary_key=True)
    productid = Column(Integer, ForeignKey('product.id'))
    name = Column(String)
    
    def __repr_(self):
        return "<Module: ID = '%s', Name = '%s', Product = %s>" % (self.id, self.name, self.productid)
    
#Store the base level product
class Product(Base):
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr_(self):
        return "<Product: ID = '%s', Name = '%s'>" % (self.id, self.name)

#Store the base level input parameter
class InputParameter(Base):
    __tablename__ = 'inputparameter'
    
    id = Column(Integer, primary_key=True)
    keyactionid = Column(Integer, ForeignKey('keyaction.id'))
    name = Column(String)
    
    act = relationship("KeyAction", backref=backref('inputparameter', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<Input Parameter: ID = '%s', Key Action ID = '%s', Name = '%s'>" % (self.id, self.keyactionid, self.name)
    
#Store the base level client
class Client(Base):
    __tablename__ = 'client'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr_(self):
        return "<Client: ID = '%s', Name = '%s'>" % (self.id, self.name)
    
#Store the base level project
class Project(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True)
    clientid = Column(Integer, ForeignKey('client.id'))
    name = Column(String)
    
    mod = relationship("Client", backref=backref('project', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<Project: ID = '%s', Client ID = '%s', Name = '%s'>" % (self.id, self.clientid, self.name)
    
#Store the base level system area
class TestScript(Base):
    __tablename__ = 'testscript'
    
    id = Column(Integer, primary_key=True)
    projectid = Column(Integer, ForeignKey('project.id'))
    name = Column(String)
    
    mod = relationship("Project", backref=backref('testscript', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<Test Script: ID = '%s', Project ID = '%s', Name = '%s'>" % (self.id, self.projectid, self.name)
    
#Store the base level system area
class Workflow(Base):
    __tablename__ = 'workflow'
    
    id = Column(Integer, primary_key=True)
    testscriptid = Column(Integer, ForeignKey('testscript.id'))
    name = Column(String)
    
    mod = relationship("TestScript", backref=backref('workflow', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<System Area: ID = '%s', Module ID = '%s', Name = '%s'>" % (self.id, self.moduleid, self.name)

class WorkflowAction(Base):
    __tablename__ = 'workflowaction'
    
    id = Column(Integer, primary_key=True)
    keyactionid = Column(Integer, ForeignKey('keyaction.id'))
    workflowid = Column(Integer, ForeignKey('workflow.id'))
    expectedresult = Column(String)
    notes = Column(String)
    fail = Column(Boolean)
    
    ka = relationship("KeyAction", backref=backref('workflowaction', order_by=id), single_parent=True)
    wf = relationship("Workflow", backref=backref('workflowaction', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<Workflow Action: ID = '%s', Key Action ID = '%s', Expected Results = '%s', Notes = '%s', Fail = '%s'>" % (self.id, self.keyactionid, self.expectedresult, self.notes, self.fail)
    
class WorkflowNextAction(Base):
    __tablename__ = 'workflownextaction'
    
    id = Column(Integer, primary_key=True)
    keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
    nextactionid = Column(Integer)
    
    act = relationship("WorkflowAction", backref=backref('workflownextaction', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<Workflow Next Action: ID = '%s', Key Action ID = '%s', Next Action ID = '%s'>" % (self.id, self.keyactionid, self.nextactionid)
    
class WorkflowParameter(Base):
    __tablename__ = 'workflowparam'
    
    id = Column(Integer, primary_key=True)
    inputparamid = Column(Integer, ForeignKey('inputparameter.id'))
    keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
    value = Column(String)
    
    act = relationship("WorkflowAction", backref=backref('workflowparam', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    ip = relationship("InputParameter", backref=backref('workflowparam', order_by=id), single_parent=True)
    
    def __repr_(self):
        return "<Workflow Parameter: ID = '%s', Input Parameter ID = '%s', Key Action ID = '%s', Value = '%s'>" % (self.id, self.inputparamid, self.keyactionid, self.value)

class FlowchartPosition(Base):
    __tablename__ = 'flowchart'
    
    id = Column(Integer, primary_key=True)
    keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
    row = Column(Integer)
    col = Column(Integer)
    
    act = relationship("WorkflowAction", backref=backref('flowchart', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)

#------------------------------------------------------------
#----------------SQLAlchemy Connections----------------------
#------------------------------------------------------------

#Figure out whether we are running on windows or unix
#Connect to the DB
#echo=True turns on query logging
#echo="debug" turns on query + result logging
#echo=False turns off query logging
if platform.system() == 'Windows':
    engine = create_engine('sqlite:///test.db', echo=True)
else:
    engine = create_engine('sqlite:///test.db', echo=True)

#Connect to the DB
#echo=True turns on query logging
#echo="debug" turns on query + result logging
#echo=False turns off query logging
engine = create_engine('sqlite:///test.db', echo="debug")
Logger.info('SQLAlchemy: Engine Created')

#Database analyzed & created if necessary
if not os.path.exists('test.db'):
    Base.metadata.create_all(engine)
Logger.info('SQLAlchemy: Database Analyzed and Created if Necessary')

#Create the Session Factory
Session = sessionmaker(bind=engine)
session = Session()
Logger.info('SQLAlchemy: Session Created')

#------------------------------------------------------------
#----------------Translator Classes--------------------------
#------------------------------------------------------------
                
class InternalDBTranslator(Translator):
    #Singleton
    #Use on one table at a time, finish, then call reset()
    
    def __init__(self):
        super(InternalDBTranslator, self).__init__(**kwargs)
    
    def reset(self):
        self.last_read = 0
    
    def process(data_type, table, output_stream, stream_size):
        rows = session.query(table).order_by(table.id)[self.last_read:self.last_read+stream_size]
        for row in rows:
            buf = DataBuffer()
            for col in row:
                buf.append(col)
            buf.type = data_type
            output_stream.put(buf)
       
#------------------------------------------------------------
#----------------DB Writer-----------------------------------
#------------------------------------------------------------

#Internal DB Writer catches the data stream and writes results to database

class DBWriter():
    
    def write(stream):
        while stream.result_stream.empty() == False:
            #Retrieve the top value from the queue
            data_buffer = stream.result_stream.get()
            
            #Write the data to the DB
            if data_buffer.type == 0:
                #The buffer data type is not assigned, perform no operations
                Logger.debug('Writer: Buffer Data Type not assigned')
            elif data_buffer.type == 1:
                Logger.debug('Writer: Key Action Export Initialized')
            elif data_buffer.type == 2:
                Logger.debug('Writer: System Area Export Initialized')
            elif data_buffer.type == 3:
                Logger.debug('Writer: Module Export Initialized')
            elif data_buffer.type == 4:
                Logger.debug('Writer: Product Export Initialized')
            elif data_buffer.type == 5:
                Logger.debug('Writer: Client Export Initialized')
            elif data_buffer.type == 6:
                Logger.debug('Writer: Project Export Initialized')
            elif data_buffer.type == 7:
                Logger.debug('Writer: Test Script Export Initialized')
            elif data_buffer.type == 8:
                Logger.debug('Writer: Workflow Export Initialized')
            elif data_buffer.type == 9:
                Logger.debug('Writer: Workflow Action Export Initialized')
            elif data_buffer.type == 10:
                Logger.debug('Writer: Input Parameter Export Initialized')
            elif data_buffer.type == 11:
                Logger.debug('Writer: Workflow Parameter Export Initialized')
            elif data_buffer.type == 12:
                Logger.debug('Writer: Workflow Next Action Export Initialized')
            elif data_buffer.type == 13:
                Logger.debug('Writer: Flowchart Export Initialized')
            
            #Finish with the data
            stream.result_stream.task_done()

#------------------------------------------------------------
#----------------Main App------------------------------------
#------------------------------------------------------------
    
Builder.load_file('kv/DBAdministrator.kv')
Builder.load_file('kv/FileChooserPopup.kv')

class FileChooserPopup(BoxLayout):
    text_input = ObjectProperty(None)
    file_chooser = ObjectProperty(None)
    app = ObjectProperty(None)
    
class DestinationFileChooserPopup(BoxLayout):
    text_input = ObjectProperty(None)
    file_chooser = ObjectProperty(None)
    app = ObjectProperty(None)

class DatabaseWidget(BoxLayout):
    pop_up = ObjectProperty(None)

class DatabaseApp(App):
    def build(self):
         return DatabaseWidget()
     
    def FindSourcePopup(self, *args):
         Logger.debug('Find Source Popup')
         popup = Popup(title='Source', content=FileChooserPopup(app=self), size_hint=(0.5, 0.75))
         self.root.pop_up = popup
         popup.open()
         
    def FillInput(self, *args):
        Logger.debug('Fill Source Popup')
        selected_file = self.root.pop_up.content.file_chooser.selection[0]
        self.root.ids.source_input.text = selected_file
        self.root.pop_up.dismiss()
    
    def FillDestinationInput(self, *args):
        Logger.debug('Fill Destination Popup')
        selected_file = self.root.pop_up.content.file_chooser.selection[0]
        self.root.ids.destination_input.text = selected_file
        self.root.pop_up.dismiss()
     
    def FindDestinationPopup(self, *args):
         Logger.debug('Find Destination Popup')
         popup = Popup(title='Destination', content=DestinationFileChooserPopup(app=self), size_hint=(0.5, 0.75))
         self.root.pop_up = popup
         popup.open()
     
    def RunMigration(self, *args):
         Logger.debug('Run Migration')
         
         #Create Data Stream
         stream = DataStream()
         
         #Create Translators & Writers
         
         #If the direction is 'Import', assign the writer to the Internal DB Writer
         #If it's 'Export', assign the importer to the Internal DB Importer
         if self.root.ids.direction_spinner.text == 'Import':
             writer = DBWriter()
             
             #Find the importer
             if self.root.ids.translator_spinner.text == 'CSV':
                 importer = CSVTranslator(input_file=self.root.ids.source_input.text)
             elif self.root.ids.translator_spinner.text == 'Excel':
                 importer = ExcelTranslator(input_file=self.root.ids.source_input.text)
             elif self.root.ids.translator_spinner.text == 'DB':
                 importer = ExternalDBTranslator(db_path=self.root.ids.source_input.text)
             else:
                 Logger.debug('Nothing Selected')
                 return True
                 #Nothing selected
         elif self.root.ids.direction_spinner.text == 'Export':
             importer = InternalDBTranslator()
             
             #Find the writer
             if self.root.ids.translator_spinner.text == 'CSV':
                 writer = CSVWriter()
             elif self.root.ids.translator_spinner.text == 'Excel':
                 writer = ExcelWriter()
             else:
                 Logger.debug('Nothing Selected')
                 return True
                 #Nothing selected
                 
         else:
             #No direction selected
             Logger.debug('Nothing Selected')
             return True
        
         log_writer = TerminalWriter()

         #TO-DO: How do we know when to stop

         #Single Iteration
         #Run Translations
         importer.translate()
         
         #Run Validations
         stream.stream()
         
         #Run Writer
         writer.write(stream)
         
         #Run Error Writer
         log_writer.write(stream)
         
    def UpdateDirection(self, *args):
         Logger.debug('Update Direction')
         if self.root.ids.direction_spinner.text == 'Import':
             self.root.ids.destination_input.text = 'test.db'
             self.root.ids.source_input.text = ''
         else:
             self.root.ids.source_input.text = 'test.db'
             self.root.ids.destination_input.text = ''

if __name__ == '__main__':
    DatabaseApp().run()
