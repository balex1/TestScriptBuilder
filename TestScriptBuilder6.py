from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ListProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.actionbar import ActionBar, ActionView, ActionButton, ActionGroup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from src.KeyActionCarouselItem import KeyActionCarouselItem
from src.WFCarouselItem import WFCarouselItem

from src.flowcharts.DragGrid import DragGrid, DragGridCell
from src.flowcharts.FlowChartNode2 import FlowChartNode, DraggableImage
from src.flowcharts.DraggableOption import DraggableOption

import os.path

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

#Connect to the DB
engine = create_engine('sqlite:///test.db', echo=True)
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
#----------------Filter Manager------------------------------
#------------------------------------------------------------


class FilterManager():
    #TO-DO: Add Optional Custom Filtering

    def __init__(self):
        self.page = 1
        self.pageLength = 5
        self.customEnabled = False
        Logger.info('Filter: Filter Manager Created')
    
    #Getters & Setters
    def GetCurrentPage(self):
        return self.page
    
    def GetPageLength(self):
        return self.pageLength
    
    def SetPageLength(self, newLength):
        self.pageLength = newLength
        Logger.debug('Filter: Page Length Set')
        
    def isCustomFilteringEnabled(self):
        return self.customEnabled
        
    def setCustomFilteringEnabled(self, newcust):
        self.customEnabled = newcust

    #Pagination
    def NextPage_KA(self, module, sysarea, keyaction, custom):
        Logger.debug('Filter: Next Page')
        self.page = self.page + 1
        limit = ((self.page - 1) * self.pageLength)
        offset = self.pageLength + ((self.page - 1) * self.pageLength)
        res = self.GetKeyActionResults(module, sysarea, keyaction, custom, limit, offset)
        Logger.debug('Filter: Filter Applied')
        if len(res) == 0:
            self.page = 1
            limit = ((self.page - 1) * self.pageLength)
            offset = self.pageLength + ((self.page - 1) * self.pageLength)
            return self.GetKeyActionResults(module, sysarea, keyaction, custom, limit, offset)
        else:
            return res

    def PrevPage_KA(self, module, sysarea, keyaction, custom):
        Logger.debug('Filter: Previous Page')
        if self.page != 1:
            self.page = self.page - 1
        limit = ((self.page - 1) * self.pageLength)
        offset = self.pageLength + ((self.page - 1) * self.pageLength)
        return self.GetKeyActionResults(module, sysarea, keyaction, custom, limit, offset)
    
    def NextPage_WF(self, workflow, module, sysarea, keyaction, custom):
        Logger.debug('Filter: Next Page')
        self.page = self.page + 1
        limit = ((self.page - 1) * self.pageLength)
        offset = self.pageLength + ((self.page - 1) * self.pageLength)
        res = self.GetWorkflowResults(workflow, module, sysarea, keyaction, custom, limit, offset)
        Logger.debug('Filter: Filter Applied')
        if len(res) == 0:
            self.page = 1
            limit = ((self.page - 1) * self.pageLength)
            offset = self.pageLength + ((self.page - 1) * self.pageLength)
            return self.GetWorkflowResults(workflow, module, sysarea, keyaction, custom, limit, offset)
        else:
            return res

    def PrevPage_WF(self, workflow, module, sysarea, keyaction, custom):
        Logger.debug('Filter: Previous Page')
        if self.page != 1:
            self.page = self.page - 1
        limit = ((self.page - 1) * self.pageLength)
        offset = self.pageLength + ((self.page - 1) * self.pageLength)
        return self.GetWorkflowResults(workflow, module, sysarea, keyaction, custom, limit, offset)
            
    #Utility Method
    def FirstPage(self):
        self.page = 1
        Logger.debug('Filter: First Page')

    #Filtering
    def ApplyFilter(self, module, sysarea, keyaction, custom):
        #Instantiate a session each time we need to connect to the DB
        self.pageLength = 20
        limit = ((self.page - 1) * self.pageLength)
        offset = self.pageLength + ((self.page - 1) * self.pageLength)
        Logger.debug('Filter: Key Action Filter Applied')
        return self.GetKeyActionResults(module, sysarea, keyaction, custom, limit, offset)
    
    def SimpleFilter(self):
        limit = ((self.page - 1) * self.pageLength)
        offset = self.pageLength + ((self.page - 1) * self.pageLength)
        return session.query(KeyAction).order_by(KeyAction.id)[limit:offset]
        
    def ApplyWorkflowFilter(self, workflow, module, sysarea, keyaction, custom):
        
        #Instantiate a session each time we need to connect to the DB
        self.pageLength = 10
        limit = ((self.page - 1) * self.pageLength)
        offset = self.pageLength + ((self.page - 1) * self.pageLength)
        
        #Apply the filter
        Logger.debug('Filter: Workflow Filter Applied')
        return self.GetWorkflowResults(workflow, module, sysarea, keyaction, custom, limit, offset)
        
    def FindTestScripts(self, workflow, testscript, client, project, limit, offset):
        if (workflow == "" or workflow is None) and (testscript == "" or testscript is None) and (project == "" or project is None) and (client == "" or client is None):
            results = session.query(TestScript).\
                order_by(TestScript.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (testscript == "" or testscript is None) and (project == "" or project is None):
            results = session.query(TestScript).join(Workflow).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).order_by(TestScript.id)[limit:offset]
                
        elif (testscript == "" or testscript is None) and (project == "" or project is None) and (client == "" or client is None):
            results = session.query(TestScript).join(Workflow).filter(Workflow.name.like('%' + str(workflow) + '%')).\
                order_by(TestScript.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (testscript == "" or testscript is None) and (client == "" or client is None):
            results = session.query(TestScript).join(Workflow).join(Project).\
                filter(Project.name.like('%' + str(project) + '%')).order_by(TestScript.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (project == "" or project is None) and (client == "" or client is None):
            results = session.query(TestScript).\
                filter(TestScript.name.like('%' + str(testscript) + '%')).order_by(TestScript.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (testscript == "" or testscript is None):
            results = session.query(TestScript).join(Workflow).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    order_by(TestScript.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (project == "" or project is None):
            results = session.query(TestScript).join(Workflow).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(TestScript.name.like('%' + str(testscript) + '%')).\
                    order_by(TestScript.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (client == "" or client is None):
            results = session.query(TestScript).join(Workflow).join(Project).\
                filter(TestScript.name.like('%' + str(testscript) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    order_by(TestScript.id)[limit:offset]
                    
        elif (testscript == "" or testscript is None) and (project == "" or project is None):
            results = session.query(TestScript).join(Workflow).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Workflow.name.like('%' + str(workflow) + '%')).\
                    order_by(TestScript.id)[limit:offset]
                    
        elif (testscript == "" or testscript is None) and (client == "" or client is None):
            results = session.query(TestScript).join(Workflow).join(Project).\
                filter(Workflow.name.like('%' + str(workflow) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    order_by(TestScript.id)[limit:offset]
                    
        elif (project == "" or project is None) and (client == "" or client is None):
            results = session.query(TestScript).join(Workflow).\
                filter(Workflow.name.like('%' + str(workflow) + '%')).filter(TestScript.name.like('%' + str(testscript) + '%')).\
                    order_by(TestScript.id)[limit:offset]
                    
        elif (workflow == "" or workflow is None):
            results = session.query(TestScript).join(Workflow).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).order_by(TestScript.id)[limit:offset]
                    
        elif (testscript == "" or testscript is None):
            results = session.query(TestScript).join(Workflow).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    filter(Workflow.name.like('%' + str(workflow) + '%')).order_by(TestScript.id)[limit:offset]
                    
        elif (project == "" or project is None):
            results = session.query(TestScript).join(Workflow).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Workflow.name.like('%' + str(workflow) + '%')).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).order_by(TestScript.id)[limit:offset]
                    
        elif (client == "" or client is None):
            results = session.query(TestScript).join(Workflow).join(Project).join(Client).\
                filter(Workflow.name.like('%' + str(workflow) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).order_by(TestScript.id)[limit:offset]
                    
        else:
            results = session.query(TestScript).join(Workflow).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).filter(Workflow.name.like('%' + str(workflow) + '%')).\
                        order_by(TestScript.id)[limit:offset]
            
        return results
            
        
    def FindWorkflows(self, workflow, testscript, client, project, limit, offset):
        if (workflow == "" or workflow is None) and (testscript == "" or testscript is None) and (project == "" or project is None) and (client == "" or client is None):
            results = session.query(Workflow).\
                order_by(Workflow.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (testscript == "" or testscript is None) and (project == "" or project is None):
            results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).order_by(Workflow.id)[limit:offset]
                
        elif (testscript == "" or testscript is None) and (project == "" or project is None) and (client == "" or client is None):
            results = session.query(Workflow).filter(Workflow.name.like('%' + str(workflow) + '%')).\
                order_by(Workflow.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (testscript == "" or testscript is None) and (client == "" or client is None):
            results = session.query(Workflow).join(TestScript).join(Project).\
                filter(Project.name.like('%' + str(project) + '%')).order_by(Workflow.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (project == "" or project is None) and (client == "" or client is None):
            results = session.query(Workflow).join(TestScript).\
                filter(TestScript.name.like('%' + str(testscript) + '%')).order_by(Workflow.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (testscript == "" or testscript is None):
            results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    order_by(Workflow.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (project == "" or project is None):
            results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(TestScript.name.like('%' + str(testscript) + '%')).\
                    order_by(Workflow.id)[limit:offset]
                
        elif (workflow == "" or workflow is None) and (client == "" or client is None):
            results = session.query(Workflow).join(TestScript).join(Project).\
                filter(TestScript.name.like('%' + str(testscript) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    order_by(Workflow.id)[limit:offset]
                    
        elif (testscript == "" or testscript is None) and (project == "" or project is None):
            results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Workflow.name.like('%' + str(workflow) + '%')).\
                    order_by(Workflow.id)[limit:offset]
                    
        elif (testscript == "" or testscript is None) and (client == "" or client is None):
            results = session.query(Workflow).join(TestScript).join(Project).\
                filter(Workflow.name.like('%' + str(workflow) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    order_by(Workflow.id)[limit:offset]
                    
        elif (project == "" or project is None) and (client == "" or client is None):
            results = session.query(Workflow).join(TestScript).\
                filter(Workflow.name.like('%' + str(workflow) + '%')).filter(TestScript.name.like('%' + str(testscript) + '%')).\
                    order_by(Workflow.id)[limit:offset]
                    
        elif (workflow == "" or workflow is None):
            results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).order_by(Workflow.id)[limit:offset]
                    
        elif (testscript == "" or testscript is None):
            results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    filter(Workflow.name.like('%' + str(workflow) + '%')).order_by(Workflow.id)[limit:offset]
                    
        elif (project == "" or project is None):
            results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Workflow.name.like('%' + str(workflow) + '%')).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).order_by(Workflow.id)[limit:offset]
                    
        elif (client == "" or client is None):
            results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
                filter(Workflow.name.like('%' + str(workflow) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).order_by(Workflow.id)[limit:offset]
                    
        else:
            results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
                filter(Client.name.like('%' + str(client) + '%')).filter(Project.name.like('%' + str(project) + '%')).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).filter(Workflow.name.like('%' + str(workflow) + '%')).\
                        order_by(Workflow.id)[limit:offset]
            
        return results
        
    def GetKeyActionResults(self, module, sysarea, keyaction, cust, limit, offset):
        if self.customEnabled == True:
            if cust == 'False' or cust == False or cust == 0:
                custom = 0
            else:
                custom = 1
            if (module == "" or module is None) and (sysarea == "" or sysarea is None) and (keyaction == "" or keyaction is None):
                results = session.query(KeyAction).filter(KeyAction.custom == custom).order_by(KeyAction.id)[limit:offset]
                
            elif (module == "" or module is None) and (sysarea == "" or sysarea is None):
                results = session.query(KeyAction).filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
                    filter(KeyAction.custom == custom).order_by(KeyAction.id)[limit:offset]
                    
            elif (module == "" or module is None) and (keyaction == "" or keyaction is None):
                results = session.query(KeyAction).join(SystemArea).filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
                    filter(KeyAction.custom == custom).order_by(KeyAction.id)[limit:offset]
                    
            elif (sysarea == "" or sysarea is None) and (keyaction == "" or keyaction is None):
                results = session.query(KeyAction).join(SystemArea).join(Module).filter(Module.name.like('%' + str(module) + '%')).\
                    filter(KeyAction.custom == custom).order_by(KeyAction.id)[limit:offset]
                
            elif (module == "" or module is None):
                results = session.query(KeyAction).join(SystemArea).filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
                    filter(SystemArea.name.like('%' + str(sysarea) + '%')).filter(KeyAction.custom == custom).order_by(KeyAction.id)[limit:offset]
                
            elif (sysarea == "" or sysarea is None):
                results = session.query(KeyAction).join(SystemArea).join(Module).filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
                    filter(Module.name.like('%' + str(module) + '%')).filter(KeyAction.custom == custom).order_by(KeyAction.id)[limit:offset]
                
            elif (keyaction == "" or keyaction is None):
                results = session.query(KeyAction).join(SystemArea).join(Module).filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
                    filter(Module.name.like('%' + str(module) + '%')).filter(KeyAction.custom == custom).order_by(KeyAction.id)[limit:offset]
                
            else:
                results = session.query(KeyAction).join(SystemArea).join(Module).filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
                    filter(SystemArea.name.like('%' + str(sysarea) + '%')).filter(Module.name.like('%' + str(module) + '%')).\
                        filter(KeyAction.custom == custom).order_by(KeyAction.id)[limit:offset]
        else:
            if (module == "" or module is None) and (sysarea == "" or sysarea is None) and (keyaction == "" or keyaction is None):
                results = session.query(KeyAction).order_by(KeyAction.id)[limit:offset]
                
            elif (module == "" or module is None) and (sysarea == "" or sysarea is None):
                results = session.query(KeyAction).filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
                    order_by(KeyAction.id)[limit:offset]
                    
            elif (module == "" or module is None) and (keyaction == "" or keyaction is None):
                results = session.query(KeyAction).join(SystemArea).filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
                    order_by(KeyAction.id)[limit:offset]
                    
            elif (sysarea == "" or sysarea is None) and (keyaction == "" or keyaction is None):
                results = session.query(KeyAction).join(SystemArea).join(Module).filter(Module.name.like('%' + str(module) + '%')).\
                    order_by(KeyAction.id)[limit:offset]
                
            elif (module == "" or module is None):
                results = session.query(KeyAction).join(SystemArea).filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
                    filter(SystemArea.name.like('%' + str(sysarea) + '%')).order_by(KeyAction.id)[limit:offset]
                
            elif (sysarea == "" or sysarea is None):
                results = session.query(KeyAction).join(SystemArea).join(Module).filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
                    filter(Module.name.like('%' + str(module) + '%')).order_by(KeyAction.id)[limit:offset]
                
            elif (keyaction == "" or keyaction is None):
                results = session.query(KeyAction).join(SystemArea).join(Module).filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
                    filter(Module.name.like('%' + str(module) + '%')).order_by(KeyAction.id)[limit:offset]
                
            else:
                results = session.query(KeyAction).join(SystemArea).join(Module).filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
                    filter(SystemArea.name.like('%' + str(sysarea) + '%')).filter(Module.name.like('%' + str(module) + '%')).\
                        order_by(KeyAction.id)[limit:offset]
        return results
    
     #TO-DO: Update Query
    def GetWorkflowResults(self, workflow, testscript, project, client, limit, offset):

        if (testscript == "" or testscript is None) and (project == "" or project is None) and (client == "" or client is None) and (workflow == "" or workflow is None):
            results = session.query(WorkflowAction).\
                order_by(WorkflowAction.id)[limit:offset]
                    
        elif (testscript == "" or testscript is None) and (project == "" or project is None) and (client == "" or client is None):
            results = session.query(Workflow).join(WorkflowAction).\
                filter(Workflow.name.like('%' + str(workflow) + '%')).\
                    order_by(WorkflowAction.id)[limit:offset]
                        
        elif (workflow == "" or workflow is None) and (testscript == "" or testscript is None) and (project == "" or project is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Client.name.like('%' + str(client) + '%')).\
                        order_by(WorkflowAction.id)[limit:offset]
                    
        elif (workflow == "" or workflow is None) and (testscript == "" or testscript is None) and (client == "" or client is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Project.name.like('%' + str(project) + '%')).\
                        order_by(WorkflowAction.id)[limit:offset]
                            
        elif (workflow == "" or workflow is None) and (project == "" or project is None) and (client == "" or client is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).\
                        order_by(WorkflowAction.id)[limit:offset]
                        
        elif (workflow == "" or workflow is None) and (testscript == "" or testscript is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Client.name.like('%' + str(client) + '%')).\
                        filter(Project.name.like('%' + str(project) + '%')).\
                            order_by(WorkflowAction.id)[limit:offset]
                                    
        elif (testscript == "" or testscript is None) and (client == "" or client is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Project.name.like('%' + str(project) + '%')).\
                        filter(Workflow.name.like('%' + str(workflow) + '%')).\
                            order_by(WorkflowAction.id)[limit:offset]
                                    
        elif (testscript == "" or testscript is None) and (project == "" or project is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Client.name.like("'%s'" % (client))).\
                            filter(Workflow.name.like('%' + str(workflow) + '%')).\
                                order_by(WorkflowAction.id)[limit:offset]
                                
        elif (workflow == "" or workflow is None) and (project == "" or project is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Client.name.like('%' + str(client) + '%')).\
                        filter(TestScript.name.like('%' + str(testscript) + '%')).\
                            order_by(WorkflowAction.id)[limit:offset]
                                        
        elif (project == "" or project is None) and (client == "" or client is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(TestScript.name.like('%' + str(testscript) + '%')).\
                        filter(Workflow.name.like('%' + str(workflow) + '%')).\
                            order_by(WorkflowAction.id)[limit:offset]
                                        
        elif (workflow == "" or workflow is None) and (client == "" or client is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Project.name.like('%' + str(project) + '%')).\
                        filter(TestScript.name.like('%' + str(testscript) + '%')).\
                            order_by(WorkflowAction.id)[limit:offset]
                                        
        elif (testscript == "" or testscript is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Client.name.like('%' + str(client) + '%')).\
                        filter(Project.name.like('%' + str(project) + '%')).\
                            filter(Workflow.name.like('%' + str(workflow) + '%')).\
                                order_by(WorkflowAction.id)[limit:offset]
                                            
        elif (project == "" or project is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Client.name.like('%' + str(client) + '%')).\
                        filter(TestScript.name.like('%' + str(testscript) + '%')).\
                            filter(Workflow.name.like('%' + str(workflow) + '%')).\
                                order_by(WorkflowAction.id)[limit:offset]
                                            
        elif (client == "" or client is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Project.name.like('%' + str(project) + '%')).\
                        filter(TestScript.name.like('%' + str(testscript) + '%')).\
                            filter(Workflow.name.like('%' + str(workflow) + '%')).\
                                order_by(WorkflowAction.id)[limit:offset]
                                
        elif (workflow == "" or workflow is None):
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Client.name.like('%' + str(client) + '%')).\
                        filter(Project.name.like('%' + str(project) + '%')).\
                            filter(TestScript.name.like('%' + str(testscript) + '%')).\
                                order_by(WorkflowAction.id)[limit:offset]
                                            
        else:
            results = session.query(Workflow).join(WorkflowAction).\
                join(TestScript).join(Project).join(Client).\
                    filter(Client.name.like('%' + str(client) + '%')).\
                        filter(Project.name.like('%' + str(project) + '%')).\
                            filter(TestScript.name.like('%' + str(testscript) + '%')).\
                                filter(Workflow.name.like('%' + str(workflow) + '%')).\
                                    order_by(WorkflowAction.id)[limit:offset]
                                                
        return results

#------------------------------------------------------------
#----------------Main App------------------------------------
#------------------------------------------------------------

#Load the .kv file
Builder.load_file('kv/TestScriptOptionsPopup.kv')
Builder.load_file('kv/AddToWorkflowPopup.kv')
Builder.load_file('kv/CreateWorkflowPopup.kv')
Builder.load_file('kv/KeyActionGroupScreen.kv')
Builder.load_file('kv/KeyActionsTabbedPanel.kv')
Builder.load_file('kv/LoadWorkflowPopup.kv')
Builder.load_file('kv/SelectableButton.kv')
Builder.load_file('kv/WorkflowScreen.kv')
Logger.info('KV: KV File Loaded')

#Create the filter manager
filter = FilterManager()
current_product = 'Default'
current_client = 'Default'
current_project = 'Default'
current_script = 'Default'

#Create the Selection List
selected = []

#Create the list of selected key action id's to allow updating names
selected_ids = []

class KeyActionGroupScreen(Screen):
    pop_up=ObjectProperty(None)

class WorkflowScreen(Screen):
    drag_grid=ObjectProperty(None)
    grid_layout=ObjectProperty(None)
    float_layout=ObjectProperty(None)

class SelectableGrid(GridLayout):
    pass

class ProductPanel(BoxLayout):
    pass

class ConnectionsPanel(BoxLayout):
    pass

class KeyActionAdvancedOptionsPopup(BoxLayout):
    pass

class KeyActionTabbedPanel(TabbedPanel):
    pass

class TestScriptOptionsPopup(BoxLayout):
    pass

class ExportPopup(BoxLayout):
    pass

class AddToWorkflowPopup(BoxLayout):
    spinner=ObjectProperty(None)
    atwp_workflow=ObjectProperty(None)
    atwp_testscript=ObjectProperty(None)
    atwp_client=ObjectProperty(None)
    atwp_project=ObjectProperty(None)
    
class LoadWorkflowPopup(BoxLayout):
    spinner=ObjectProperty(None)
    lwp_workflow=ObjectProperty(None)
    lwp_testscript=ObjectProperty(None)
    lwp_client=ObjectProperty(None)
    lwp_project=ObjectProperty(None)
    
class CreateWorkflowPopup(BoxLayout):
    new_flow=ObjectProperty(None)
    spinner=ObjectProperty(None)
    cwp_workflow=ObjectProperty(None)
    cwp_testscript=ObjectProperty(None)
    cwp_client=ObjectProperty(None)
    cwp_project=ObjectProperty(None)

class SelectableButton(ToggleButton):
    #Exposes on_selection event
    selection = BooleanProperty(False)
    #Internal, for the Grid Layout to control the selection

    #Assumes button starts with selection = False
    def SelectButton(self, *args):
        if self.selection == False:
            self.selection = True
            selected.append(self.text)
        else:
            self.selection = False
            selected.remove(self.text)

#Create the Screenmanager and add the Screens
sm = ScreenManager()
sm.add_widget(KeyActionGroupScreen(name='keyactiongroup'))
sm.add_widget(WorkflowScreen(name='workflow'))
Logger.info('Kivy: Screens added to Screen Manager')

#App Definition
class TestScriptBuilderApp(App):

    #Initialization function
    #Set the first screen and return the screen manager
    def build(self):
        Logger.debug('Kivy: Set current Screen and return the ScreenManager')
        #Set the current page to key action and run a default filter
        sm.current = 'keyactiongroup'
        filter.FirstPage()
        prod_rows = session.query(Product).filter(Product.name == current_product).all()
        if len(prod_rows) == 0:
            prod = Product(name=current_product)
            session.add(prod)
            session.commit()

        return sm
    
#----------------------------------------------------------
#------------------WF Callbacks----------------------------
#----------------------------------------------------------

    def AdvancedOptionsPopup_WF(self, *args):
        Logger.debug('WF: Advanced Options Popup')
        #This popup should allow for loading a script configuration file (HTML & SQL)
        #It should also allow for exporting the script and choosing export format
        popup = Popup(title='Export Options', content=ExportPopup(), size_hint=(0.5, 0.75))
        popup.open()
        
    def WFQuickActionPopup(self, *args):
        Logger.debug('WF: Quick Action Popup')
        popup = Popup(title='Quick Key Action', content=KeyActionCarouselItem(), size_hint=(0.5, 0.75))
        popup.bind(on_dismiss=self.WFSaveQuickActionPopup)
        popup.open()
        
    def WFLoadActionPopup(self, *args):
        Logger.debug('WF: Load Action Popup')
        
    def WFSaveQuickActionPopup(self, *args):
        Logger.debug('WF: Save Action Popup')
        
    def TestScriptPopup_WF(self, *args):
        Logger.debug('WF: Test Script Popup')
        popup = Popup(title='Test Script Options', content=TestScriptOptionsPopup(), size_hint=(0.5, 0.75))
        popup.open()
        
    def SaveTestScriptPopup(self, *args):
        Logger.debug('WF: Save Test Script Popup')
        
    def UpdateWorkflowName(self, *args):
        Logger.debug('WF: Update Workflow Name')
        
    def SaveWorkflow(self, *args):
        Logger.debug('WF: Save Workflow')
        
    def SaveAction(self, *args):
        Logger.debug('WF: Save Action')
    
    def CreateNewSubflow(self, *args):
        Logger.debug('WF: Create New Subflow')
        
    def SaveConnectionsPanel(self, *args):
        Logger.debug('Save Connections Panel')
        
    def SaveConnectionsPanelDefaults(self, *args):
        Logger.debug('Save Connections Panel Defaults')
  
    #This is a critical method as it is called when a draggable is released on
    #the flowchart, to add a flowchart node.  This takes the label from the original
    #Draggable, puts it into a new draggable wrapper and then into the flowchart node  
    def add_flowchart_node(self, cell, image):
        Logger.debug('Add flowchart node with image %s and cell %s' % (image, cell))
        drag_label = DraggableImage(img=image, app=self, grid=self.root.get_screen('workflow').drag_grid, cell=cell)
        drag = FlowChartNode(app=self, grid=self.root.get_screen('workflow').drag_grid, cell=cell, label=drag_label)
        drag_label.node = drag
        #Bind the double press to load the key action into the side editor
        drag_label.bind(on_double_press=self.LoadSideEditor)
        cell.add_widget(drag)
        cell.nodes.append(drag)
        self.root.get_screen('workflow').drag_grid.nodes.append(drag)
        
    def LoadSideEditor(self, node):
        #Loop through the nodes in the grid and find the one that has been double pressed
        Logger.debug('Load Side Editor with action %s' % (node.img.text))
        #for node in self.root.get_screen('workflow').drag_grid.nodes:
            #if node.label.is_double_pressed:
    
        #Query the DB for the details of the action with the name from the label
        ka = session.query(KeyAction).filter(KeyAction.name==node.img.text).one()
        ips = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == node.img.text).all()
        wfa = session.query(WorkflowAction).join(KeyAction).filter(KeyAction.name == node.img.text).one()
        wps = session.query(WorkflowParameter).join(WorkflowAction).join(KeyAction).filter(KeyAction.name == node.img.text).all()
        #Load the double clicked node into the side editor
        self.root.get_screen('workflow').ids.wf_carousel.name = node.img.text
        if wfa.expectedresult is not None:
            self.root.get_screen('workflow').ids.wf_carousel.er = wfa.expectedresult
            
        if len(ips) == 0:
            ip1 = InputParameter(keyactionid=ka.id)
            ip2 = InputParameter(keyactionid=ka.id)
            ip3 = InputParameter(keyactionid=ka.id)
            session.add(ip1)
            session.add(ip2)
            session.add(ip3)
            session.commit()
        elif len(ips) == 1:
            ip1 = InputParameter(keyactionid=ka.id)
            ip2 = InputParameter(keyactionid=ka.id)
            ip3 = ips[0]
            session.add(ip1)
            session.add(ip2)
            session.commit()
        elif len(ips) == 2:
            ip1 = InputParameter(keyactionid=ka.id)
            ip2 = ips[0]
            ip3 = ips[1]
            session.add(ip1)
            session.commit()
        else:
            ip1 = ips[0]
            ip2 = ips[1]
            ip3 = ips[2]
            
        if ip1.name is not None:
            self.root.get_screen('workflow').ids.wf_carousel.ip1_name = ip1.name
        if ip2.name is not None:
            self.root.get_screen('workflow').ids.wf_carousel.ip2_name = ip2.name
        if ip3.name is not None:
            self.root.get_screen('workflow').ids.wf_carousel.ip3_name = ip3.name
            
        if len(wps) == 0:
            wp1 = WorkflowParameter(keyactionid=wfa.id)
            wp2 = WorkflowParameter(keyactionid=wfa.id)
            wp3 = WorkflowParameter(keyactionid=wfa.id)
            session.add(wp1)
            session.add(wp2)
            session.add(wp3)
            session.commit()
        elif len(wps) == 1:
            wp1 = WorkflowParameter(keyactionid=wfa.id)
            wp2 = WorkflowParameter(keyactionid=wfa.id)
            wp3 = wps[0]
            session.add(wp1)
            session.add(wp2)
            session.commit()
        elif len(wps) == 2:
            wp1 = WorkflowParameter(keyactionid=wfa.id)
            wp2 = wps[0]
            wp3 = wps[1]
            session.add(wp1)
            session.commit()
        else:
            wp1 = wps[0]
            wp2 = wps[1]
            wp3 = wps[2]
            
        if wp1.value is not None:
            self.root.get_screen('workflow').ids.wf_carousel.ip = wp1.value
        if wp2.value is not None:
            self.root.get_screen('workflow').ids.wf_carousel.ip2 = wp2.value
        if wp3.value is not None:
            self.root.get_screen('workflow').ids.wf_carousel.ip3 = wp3.value
        
    def ApplyLoadWorkflowPopupFilter(self, *args):
        Logger.debug('Apply workflow filter popup')
        
        #Clear the Spinner
        for value in self.root.get_screen('keyactiongroup').pop_up.content.spinner.values:
            self.root.get_screen('keyactiongroup').pop_up.content.spinner.values.remove(value)
        
        #Get Filter Values
        wf = self.root.get_screen('keyactiongroup').pop_up.content.lwp_workflow.text
        ts = self.root.get_screen('keyactiongroup').pop_up.content.lwp_testscript.text
        cl = self.root.get_screen('keyactiongroup').pop_up.content.lwp_client.text
        pr = self.root.get_screen('keyactiongroup').pop_up.content.lwp_project.text
        
        #Get Result Set from Filter Manager
        num_flows = session.query(Workflow).count()
        if num_flows - 5 < 0:
            num_flows = 0
        else:
            num_flows = num_flows - 5
        results = filter.FindWorkflows(wf, ts, cl, pr, 5, num_flows)
        
        #Load Result Set Into Spinner
        for result in results:
            self.root.get_screen('keyactiongroup').pop_up.content.spinner.values.append(result.name)
            
    def LoadWorkflowPopup(self, *args):
        Logger.debug('WF: Load Workflow Popup')
        popup = Popup(title='Load Workflow', content=LoadWorkflowPopup(), size_hint=(0.4, 0.5))
        popup.open()
        self.root.get_screen('keyactiongroup').pop_up = popup
        
        #Populate the latest 5 workflows into the spinner
        num_flows = session.query(Workflow).count()
        if num_flows - 5 < 0:
            num_flows = 0
        else:
            num_flows = num_flows - 5
        results = session.query(Workflow).order_by(Workflow.id)[num_flows:num_flows+5]
        
        #Populate values in spinner
        for result in results:
            popup.content.spinner.values.append(result.name)
            
    def LoadFlow(self, *args):
        Logger.debug('Add To Workflow')
        
        current_workflow=self.root.get_screen('keyactiongroup').pop_up.content.spinner.text
        
        #Load the Key Actions for the flow
        keyactions = session.query(KeyAction).join(WorkflowAction).\
            join(Workflow).filter(Workflow.name==current_workflow).all()
        
        #Put each element into the draggable list
        for action in keyactions:
            lbl = Label(text=action.name)
            
            drag_option = DraggableOption(img=lbl, app=self,\
                grid=self.root.get_screen('workflow').drag_grid,\
                    grid_layout=self.root.get_screen('workflow').grid_layout,\
                        float_layout=self.root.get_screen('workflow').float_layout)
                        
            self.root.get_screen('workflow').grid_layout.add_widget(drag_option)
            
        self.root.get_screen('keyactiongroup').pop_up.dismiss()
        self.root.get_screen('workflow').ids.current_wf.text = current_workflow
        
            
#----------------------------------------------------------
#-------------------Key Action Page Callbacks--------------
#----------------------------------------------------------
    
    def CreateFlow(self, *args):
        Logger.debug('Create New Flow')
        
        current_script=self.root.get_screen('keyactiongroup').pop_up.content.spinner.text
        
        test_script=session.query(TestScript).filter(TestScript.name==current_script).one()
        
        workflow = Workflow(testscriptid=test_script.id, name=self.root.get_screen('keyactiongroup').pop_up.content.new_flow.text)
        session.add(workflow)
        session.commit()
        for option in selected:
            keyaction = session.query(KeyAction).filter(KeyAction.name==option).one()
            wfa = WorkflowAction(workflowid=workflow.id, keyactionid=keyaction.id)
            session.add(wfa)
        session.commit()
        
    def AddToFlow(self, *args):
        Logger.debug('Add To Workflow')
        
        current_workflow=self.root.get_screen('keyactiongroup').pop_up.content.spinner.text
        
        workflow = session.query(Workflow).filter(Workflow.name==current_workflow).one()
        for option in selected:
            keyaction = session.query(KeyAction).filter(KeyAction.name==option).one()
            wfa = WorkflowAction(workflowid=workflow.id, keyactionid=keyaction.id)
            session.add(wfa)
        session.commit()

    def SaveProductPanel(self, *args):
        Logger.debug('Update Product Panel')
        
    def SaveProductPanelDefaults(self, *args):
        Logger.debug('Update Product Panel Defaults')
        
    def FindDatabaseFile(self, *args):
        Logger.debug('Update Product Panel Defaults')
        
    def LoadDatabase(self, *args):
        Logger.debug('Update Product Panel Defaults')
        
    def FindExcelLoader(self, *args):
        Logger.debug('Update Product Panel Defaults')
        
    def ApplyWorkflowPopupFilter(self, *args):
        Logger.debug('Apply workflow filter popup')
        
        #Clear the Spinner
        for value in self.root.get_screen('keyactiongroup').pop_up.content.spinner.values:
            self.root.get_screen('keyactiongroup').pop_up.content.spinner.values.remove(value)
        
        #Get Filter Values
        wf = self.root.get_screen('keyactiongroup').pop_up.content.atwp_workflow.text
        ts = self.root.get_screen('keyactiongroup').pop_up.content.atwp_testscript.text
        cl = self.root.get_screen('keyactiongroup').pop_up.content.atwp_client.text
        pr = self.root.get_screen('keyactiongroup').pop_up.content.atwp_project.text
        
        #Get Result Set from Filter Manager
        num_flows = session.query(Workflow).count()
        if num_flows - 5 < 0:
            num_flows = 0
        else:
            num_flows = num_flows - 5
        results = filter.FindWorkflows(wf, ts, cl, pr, 5, num_flows)
        
        #Load Result Set Into Spinner
        for result in results:
            self.root.get_screen('keyactiongroup').pop_up.content.spinner.values.append(result.name)
        
    def ApplyCreateWorkflowPopupFilter(self, *args):
        Logger.debug('Apply workflow filter popup')
        
        #Clear the Spinner
        if len(self.root.get_screen('keyactiongroup').pop_up.content.spinner.values) != 0:
            for value in self.root.get_screen('keyactiongroup').pop_up.content.spinner.values:
                self.root.get_screen('keyactiongroup').pop_up.content.spinner.values.remove(value)
        
        #Get Filter Values
        wf = self.root.get_screen('keyactiongroup').pop_up.content.cwp_workflow.text
        ts = self.root.get_screen('keyactiongroup').pop_up.content.cwp_testscript.text
        cl = self.root.get_screen('keyactiongroup').pop_up.content.cwp_client.text
        pr = self.root.get_screen('keyactiongroup').pop_up.content.cwp_project.text
        
        #Get Result Set from Filter Manager
        num_scripts = session.query(TestScript).count()
        if num_scripts - 5 < 0:
            num_scripts = 0
        else:
            num_scripts = num_scripts - 5
        results = filter.FindTestScripts(wf, ts, cl, pr, num_scripts, num_scripts + 5)
        
        #Load Result Set Into Spinner
        for result in results:
            self.root.get_screen('keyactiongroup').pop_up.content.spinner.values.append(result.name)
        
    def AddToWorkflowPopup(self, *args):
        Logger.debug('WF: Add to Workflow Popup')
        popup = Popup(title='Add To Workflow', content=AddToWorkflowPopup(), size_hint=(0.4, 0.5))
        popup.open()
        self.root.get_screen('keyactiongroup').pop_up = popup
        
        #Populate the latest 5 workflows into the spinner
        num_flows = session.query(Workflow).count()
        if num_flows - 5 < 0:
            num_flows = 0
        else:
            num_flows = num_flows - 5
        results = session.query(Workflow).order_by(Workflow.id)[num_flows:num_flows+5]
        
        #Populate values in spinner
        for result in results:
            popup.content.spinner.values.append(result.name)
        
    def CreateWorkflowPopup(self, *args):
        Logger.debug('WF: Add to Workflow Popup')
        popup = Popup(title='Create Workflow', content=CreateWorkflowPopup(), size_hint=(0.4, 0.5))
        popup.open()
        self.root.get_screen('keyactiongroup').pop_up = popup
        
        #Get the latest 5 Test Scripts
        num_scripts = session.query(TestScript).count()
        Logger.debug('Num Scripts %s' % (num_scripts))
        if num_scripts - 5 < 0:
            num_scripts = 0
        else:
            num_scripts = num_scripts - 5
        results = session.query(TestScript).order_by(TestScript.id)[num_scripts:num_scripts+5]
        Logger.debug('Num Results %s' % (len(results)))
        
        #Populate values in spinner
        for result in results:
           popup.content.spinner.values.append(result.name)
           Logger.debug('Result %s appended' % (result.name))
    
    #----------------------------------------------------------
    #-------------------Filtering Methods----------------------
    
    #Load the next page for the Key Action Group Screen
    def LoadNextPageKAG(self, *args):
        Logger.debug('Load Next KAG Filter Page')
        self.root.get_screen('keyactiongroup').ids.selection_layout.clear_widgets()
        mod = self.root.get_screen('keyactiongroup').ids.modulefilter_kag.text
        sa = self.root.get_screen('keyactiongroup').ids.safilter_kag.text
        ka = self.root.get_screen('keyactiongroup').ids.kafilter_kag.text
        cust = self.root.get_screen('keyactiongroup').ids.customfilter.active
        filter.setCustomFilteringEnabled(self.root.get_screen('keyactiongroup').ids.custswitch.active)
        
        for i in selected_ids:
            selected_ids.remove(i)
        
        for j in selected:
            selected.remove(j)
        
        results = filter.NextPage_KA(str(mod), str(sa), str(ka), str(cust))
        i = 0
        for i in range(0, len(results)):
            sel = SelectableButton(text=str(results[i].name))
            #sel.bind(on_press.SelectButton)
            self.root.get_screen('keyactiongroup').ids.selection_layout.add_widget(sel)
    
    #Load the previous page for the Key Action Group Screen
    def LoadPrevPageKAG(self, *args):
        Logger.debug('Load Prev KAG Filter Page')
        self.root.get_screen('keyactiongroup').ids.selection_layout.clear_widgets()
        mod = self.root.get_screen('keyactiongroup').ids.modulefilter_kag.text
        sa = self.root.get_screen('keyactiongroup').ids.safilter_kag.text
        ka = self.root.get_screen('keyactiongroup').ids.kafilter_kag.text
        cust = self.root.get_screen('keyactiongroup').ids.customfilter.active
        filter.setCustomFilteringEnabled(self.root.get_screen('keyactiongroup').ids.custswitch.active)
        
        for i in selected_ids:
            selected_ids.remove(i)
        
        for j in selected:
            selected.remove(j)
        
        results = filter.PrevPage_KA(str(mod), str(sa), str(ka), str(cust))
        i = 0
        for i in range(0, len(results)):
            sel = SelectableButton(text=str(results[i].name))
            #sel.bind(on_press.SelectButton)
            self.root.get_screen('keyactiongroup').ids.selection_layout.add_widget(sel)
            
    #Load the next page for the Key Action Group Screen
    def ApplyFilterKAG(self, *args):
        Logger.debug('Apply KAG Filter')
        filter.FirstPage()
        self.root.get_screen('keyactiongroup').ids.selection_layout.clear_widgets()
        mod = self.root.get_screen('keyactiongroup').ids.modulefilter_kag.text
        sa = self.root.get_screen('keyactiongroup').ids.safilter_kag.text
        ka = self.root.get_screen('keyactiongroup').ids.kafilter_kag.text
        cust = self.root.get_screen('keyactiongroup').ids.customfilter.active
        filter.setCustomFilteringEnabled(self.root.get_screen('keyactiongroup').ids.custswitch.active)
        
        for i in selected_ids:
            selected_ids.remove(i)
        
        for j in selected:
            selected.remove(j)
        
        results = filter.ApplyFilter(str(mod), str(sa), str(ka), str(cust))
        i = 0
        for i in range(0, len(results)):
            sel = SelectableButton(text=str(results[i].name))
            #sel.bind(on_press= self.SelectButton)
            self.root.get_screen('keyactiongroup').ids.selection_layout.add_widget(sel)
            
    #Clear the filter in t he Key Action Group Screen
    def ClearFilterKAG(self, *args):
        Logger.debug('Clear KAG Filter')
        self.root.get_screen('keyactiongroup').ids.modulefilter_kag.text = ''
        self.root.get_screen('keyactiongroup').ids.safilter_kag.text = ''
        self.root.get_screen('keyactiongroup').ids.kafilter_kag.text = ''
        self.root.get_screen('keyactiongroup').ids.custswitch.active = False
        filter.setCustomFilteringEnabled(self.root.get_screen('keyactiongroup').ids.custswitch.active)
        self.ApplyFilterKAG(args)
        
    def SetCustom(self, *args):
        Logger.debug('Set Custom')
        
    def EnableCustomFiltering(self, *args):
        Logger.debug('Set Custom Filtering')
        
    def DisableCustomFiltering(self, *args):
        Logger.debug('Set Custom Filtering')
        
    #----------------------------------------------------------
    #-------------------Action Bar Methods---------------------
    
    def AdvancedOptionsPopup_KAG(self, *args):
        Logger.debug('Advanced Options')
        popup = Popup(title='Advanced Options', content=KeyActionTabbedPanel(), size_hint=(0.75, 0.75))
        popup.open()
        
    def ImportKeyActions(self, *args):
        Logger.debug('DB Import')
        
    def ImportWorkflows(self, *args):
        Logger.debug('DB Import')
        
    def Quit(self, *args):
        Logger.debug('Graceful Exit')
        
    def GoToWorkflowPage(self, *args):
        Logger.debug('Go To Workflow Page')
        sm.current='workflow'

    def GoToAnalysisPage(self, *args):
        Logger.debug('Go To Analysis Page')
        
    def GoToKeyActionGroupPage(self, *args):
        Logger.debug('Go To Key Action Page')
        sm.current = 'keyactiongroup'
        
    def DuplicateKeyAction(self, *args):
        Logger.debug('Duplicate Key Action')
        #Duplicate the selected key actions
        
        self.root.get_screen('keyactiongroup').ids.carousel_ka.clear_widgets()
        numSelected = len(selected)
        
        if numSelected > 1:
            for action in selected:
                #Create the Key Action Carousel Item
                keyaction = KeyActionCarouselItem()
                    
                #Set the Module & System Area
                sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                keyaction.systemarea = sa_rows[0].name
                mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                keyaction.module = mod_rows[0].name
                
                #Create a new Key Action
                ka = KeyAction()
                session.add(ka)
                
                rows = session.query(KeyAction).filter(KeyAction.name == action)
                
                #Set the Key Action attributes
                keyaction.keyaction = "New %s" % (rows[0].name)
                ka.name = "New %s" % (rows[0].name)
                keyaction.description = rows[0].description
                ka.description = rows[0].description
                keyaction.custom = rows[0].custom
                ka.custom = rows[0].custom
                ka.systemareaid = rows[0].systemareaid
                session.commit()
                    
                #Set the Input Parameters
                ip_rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == action).all()
                if len(ip_rows) >= 3:
                    keyaction.ip1 = ip_rows[0].name
                    keyaction.ip2 = ip_rows[1].name
                    keyaction.ip3 = ip_rows[2].name
                    
                    ip_a = InputParameter()
                    session.add(ip_a)
                    ip_a.name = ip_rows[0].name
                    ip_a.keyactionid = ka.id
                    
                    ip_b = InputParameter()
                    session.add(ip_b)
                    ip_b.name = ip_rows[1].name
                    ip_b.keyactionid = ka.id
                    
                    ip_c = InputParameter()
                    session.add(ip_c)
                    ip_c.name = ip_rows[2].name
                    ip_b.keyactionid = ka.id
                    
                elif len(ip_rows) == 2:
                    keyaction.ip1 = ip_rows[0].name
                    keyaction.ip2 = ip_rows[1].name
                    ip_a = InputParameter()
                    session.add(ip_a)
                    ip_a.name = ip_rows[0].name
                    ip_a.keyactionid = ka.id
                    
                    ip_b = InputParameter()
                    session.add(ip_b)
                    ip_b.name = ip_rows[1].name
                    ip_b.keyactionid = ka.id
                    
                elif len(ip_rows) == 1:
                    keyaction.ip1 = ip_rows[0].name
                    ip_a = InputParameter()
                    session.add(ip_a)
                    ip_a.name = ip_rows[0].name
                    ip_a.keyactionid = ka.id
                    
                keyaction.bind(on_save=self.SaveQuickKeyAction)
                keyaction.bind(on_validate=self.ValidateQuickKeyAction)
        
                #Add the base widget to the screen in the carousel
                self.root.get_screen('keyactiongroup').ids.carousel_ka.add_widget(keyaction)
        elif numSelected == 1:
            action = selected[0]
            #Create the Key Action Carousel Item
            keyaction = KeyActionCarouselItem()
                
            #Set the Module & System Area
            sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.name == action)
            keyaction.systemarea = sa_rows[0].name
            mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.name == action)
            keyaction.module = mod_rows[0].name
            
            #Create a new Key Action
            ka = KeyAction()
            session.add(ka)
            
            rows = session.query(KeyAction).filter(KeyAction.name == action)
            
            #Set the Key Action attributes
            keyaction.keyaction = "New %s" % (rows[0].name)
            ka.name = "New %s" % (rows[0].name)
            keyaction.description = rows[0].description
            ka.description = rows[0].description
            keyaction.custom = rows[0].custom
            ka.custom = rows[0].custom
            ka.systemareaid = rows[0].systemareaid
            session.commit()
                
            #Set the Input Parameters
            ip_rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == action).all()
            if len(ip_rows) >= 3:
                keyaction.ip1 = ip_rows[0].name
                keyaction.ip2 = ip_rows[1].name
                keyaction.ip3 = ip_rows[2].name
                
                ip_a = InputParameter()
                session.add(ip_a)
                ip_a.name = ip_rows[0].name
                ip_a.keyactionid = ka.id
                
                ip_b = InputParameter()
                session.add(ip_b)
                ip_b.name = ip_rows[1].name
                ip_b.keyactionid = ka.id
                
                ip_c = InputParameter()
                session.add(ip_c)
                ip_c.name = ip_rows[2].name
                ip_b.keyactionid = ka.id
                
            elif len(ip_rows) == 2:
                keyaction.ip1 = ip_rows[0].name
                keyaction.ip2 = ip_rows[1].name
                ip_a = InputParameter()
                session.add(ip_a)
                ip_a.name = ip_rows[0].name
                ip_a.keyactionid = ka.id
                    
                ip_b = InputParameter()
                session.add(ip_b)
                ip_b.name = ip_rows[1].name
                ip_b.keyactionid = ka.id
                
            elif len(ip_rows) == 1:
                keyaction.ip1 = ip_rows[0].name
                ip_a = InputParameter()
                session.add(ip_a)
                ip_a.name = ip_rows[0].name
                ip_a.keyactionid = ka.id
            session.commit()
            keyaction.bind(on_save=self.SaveQuickKeyAction)
            keyaction.bind(on_validate=self.ValidateQuickKeyAction)
    
            #Add the base widget to the screen in the carousel
            self.root.get_screen('keyactiongroup').ids.carousel_ka.add_widget(keyaction)
            self.ApplyFilterKAG(args)
    
    def DeleteKeyAction(self, *args):
        Logger.debug('Delete Key Action')
        numSelected = len(selected)
        
        if numSelected > 1:
            for action in selected:
                results = session.query(KeyAction).filter(KeyAction.name == action).all()
                if len(results) > 1:
                    raise KeyError('Business Key Violation in table key action')
                elif len(results) == 1:
                    result = results[0]
                    session.add(result)
                    session.delete(result)
        elif numSelected == 1:
            action = selected[0]
            results = session.query(KeyAction).filter(KeyAction.name == action).all()
            if len(results) > 1:
                raise KeyError('Business Key Violation in table key action')
            elif len(results) == 1:
                result = results[0]
                session.add(result)
                session.delete(result)
                session.commit()
        self.ApplyFilterKAG(args)
                
    #----------------------------------------------------------
    #-------------------Grid Methods---------------------------
                
    def SelectButton(self, *args):
        Logger.debug('Select Button')
                
    def AddWorkflow(self, *args):
        Logger.debug('Add Workflow')
        
    #----------------------------------------------------------
    #-------------------Quick Key Action Methods---------------
    
    def ClearQuickAction(self, *args):
        Logger.debug('QKA: Clear Quick Action')
        
        #Remove all selected id's from the master list
        for item in selected_ids:
            selected_ids.remove(item)
        
        self.root.get_screen('keyactiongroup').ids.carousel_ka.clear_widgets()
        keyaction = KeyActionCarouselItem()
        keyaction.bind(on_validate=self.ValidateQuickKeyAction)
        
        #Add the base widget to the screen in the carousel
        self.root.get_screen('keyactiongroup').ids.carousel_ka.add_widget(keyaction)
        
    def ValidateQuickKeyAction(self, *args):
        pass
    
    def SaveQuickKeyAction(self, *args):
        Logger.debug('QKA: Save Quick Key Action Frame')
        i = 0
        #Loop through the children of the carousel and save each one
        if len(selected_ids)>1:
            Logger.debug('QKA: Selected IDs Length %s' % (len(selected_ids)))
            for child in self.root.get_screen('keyactiongroup').ids.carousel_ka.slides:
                
                keyactions = self.SaveKeyAction(child, i)
                self.SaveInputParameters(child, keyactions, i)
                i += 1
                
        #If there is only one child, save it
        elif len(selected_ids) == 1:
            Logger.debug('QKA: Selected IDs Length 1')
            child = self.root.get_screen('keyactiongroup').ids.carousel_ka.slides[0]

            keyactions = self.SaveKeyAction(child, i)
            self.SaveInputParameters(child, keyactions, i)
        else:
            #Save the key action as a new key action
            Logger.debug('QKA: Selected IDs Length 0')
            if len(self.root.get_screen('keyactiongroup').ids.carousel_ka.slides) != 0:
            
                #Only execute if there are elements in the carousel
                Logger.debug('QKA: Elements exist in the carousel')
                child = self.root.get_screen('keyactiongroup').ids.carousel_ka.slides[0]
                
                #Module
                prod_rows = session.query(Product).filter(Product.name == current_product).all()
                rows = session.query(Module).filter(Module.name == child.module_in.text).all()
                if len(rows) > 1:
                    raise KeyError('Business Key Violation in table module')
                elif len(rows) != 1:
                    mod = Module()
                    mod.name = child.module_in.text
                    mod.productid = prod_rows[0].id
                    session.add(mod)
                session.commit()
                Logger.debug('QKA: Module Committed %s' % (child.module_in.text))
                
                #System Area
                sa_rows = session.query(SystemArea).filter(SystemArea.name == child.sa_in.text).all()
                if len(sa_rows) > 1:
                    raise KeyError('Business Key Violation in table system area')
                elif len(sa_rows) == 1:
                    sa_rows[0].name == child.sa_in.text
                    if len(rows) == 1:
                        sa_rows[0].moduleid = rows[0].id
                    else:
                        sa_rows[0].moduleid = mod.id
                else:
                    sys = SystemArea()
                    sys.name = child.sa_in.text
                    session.add(sys)
                    if len(rows) == 1:
                        sys.moduleid = rows[0].id
                    else:
                        sys.moduleid = mod.id
                session.commit()
                Logger.debug('QKA: System Area Committed %s' % (child.sa_in.text))
            
                #Key Action
                kaName = child.ka_in.text
                keyaction = KeyAction(name=kaName)
                session.add(keyaction)
                if len(sa_rows) == 1:
                    keyaction.systemareaid = sa_rows[0].id
                else:
                    keyaction.systemareaid = sys.id
                keyaction.description = child.desc_in.text
                keyaction.custom = child.custom_in.active
                session.commit()
                Logger.debug('QKA: Key Action Committed %s' % (child.ka_in.text))
                
                #Input Parameters
                if child.ip_in.text != '' and child.ip_in.text is not None:
                    inpparam = InputParameter(name=child.ip_in.text)
                    session.add(inpparam)
                    inpparam.keyactionid = keyaction.id
                    Logger.debug('QKA: Input Parameter Committed %s' % (child.ip_in.text))
                if child.ip2_in.text != '' and child.ip2_in.text is not None:
                    inpparam2 = InputParameter(name=child.ip2_in.text)
                    session.add(inpparam2)
                    inpparam2.keyactionid = keyaction.id
                    Logger.debug('QKA: Input Parameter Committed %s' % (child.ip2_in.text))
                if child.ip3_in.text != '' and child.ip3_in.text is not None:
                    inpparam3 = InputParameter(name=child.ip3_in.text)
                    session.add(inpparam3)
                    inpparam3.keyactionid = keyaction.id
                    Logger.debug('QKA: Input Parameter Committed %s' % (child.ip3_in.text))
                session.commit()
        self.ApplyFilterKAG(args)
            
    def LoadQuickAction(self, *args):
        Logger.debug('Load Quick Action')
        self.root.get_screen('keyactiongroup').ids.carousel_ka.clear_widgets()
        numSelected = len(selected)
        
        for item in selected_ids:
            selected_ids.remove(item)
        
        if numSelected > 1:
            for action in selected:
                rows = session.query(KeyAction).\
                    filter_by(name=action).all()
                if len(rows) > 1:
                    #More than one business key is found
                    raise KeyError('Business Key Violation in table key action')
                elif len(rows) == 1:
                    #Exactly one business key is found
                    
                    #Add the key action to the list of id's in the carousel
                    selected_ids.append(rows[0].id)
                    
                    #Create the Key Action Carousel Item
                    keyaction = KeyActionCarouselItem()
                    
                    #Set the Module & System Area
                    sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                    keyaction.systemarea = sa_rows[0].name
                    mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                    keyaction.module = mod_rows[0].name
                    
                    #Set the Key Action attributes
                    keyaction.keyaction = rows[0].name
                    keyaction.description = rows[0].description
                    keyaction.custom = rows[0].custom
                    
                    #Set the Input Parameters
                    ip_rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == action).all()
                    if len(ip_rows) >= 3:
                        keyaction.ip1 = ip_rows[0].name
                        keyaction.ip2 = ip_rows[1].name
                        keyaction.ip3 = ip_rows[2].name
                    elif len(ip_rows) == 2:
                        keyaction.ip1 = ip_rows[0].name
                        keyaction.ip2 = ip_rows[1].name
                    elif len(ip_rows) == 1:
                        keyaction.ip1 = ip_rows[0].name
                    keyaction.bind(on_validate=self.ValidateQuickKeyAction)
        
                    #Add the base widget to the screen in the carousel
                    self.root.get_screen('keyactiongroup').ids.carousel_ka.add_widget(keyaction)
                else:
                    #No matching business keys are found
                    raise KeyError('Business Key Called from UI that does not exist in DB')
            
        elif numSelected == 1:
            action = selected[0]
            rows = session.query(KeyAction).filter_by(name=action).all()
            if len(rows) > 1:
                #More than one business key is found
                raise KeyError('Business Key Violation in table key action')
            elif len(rows) == 1:
                #Exactly one business key is found
                keyaction = KeyActionCarouselItem()
                
                #Add the key action to the list of id's in the carousel
                selected_ids.append(rows[0].id)
                
                #Set the Module & System Area
                sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                keyaction.systemarea = sa_rows[0].name
                mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                keyaction.module = mod_rows[0].name
                
                #Set the Key Action attributes
                keyaction.keyaction = rows[0].name
                keyaction.description = rows[0].description
                keyaction.custom = rows[0].custom
                
                #Set the Input Parameters
                ip_rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == action).all()
                if len(ip_rows) >= 3:
                    keyaction.ip1 = ip_rows[0].name
                    keyaction.ip2 = ip_rows[1].name
                    keyaction.ip3 = ip_rows[2].name
                elif len(ip_rows) == 2:
                    keyaction.ip1 = ip_rows[0].name
                    keyaction.ip2 = ip_rows[1].name
                elif len(ip_rows) == 1:
                    keyaction.ip1 = ip_rows[0].name
                keyaction.bind(on_validate=self.ValidateQuickKeyAction)
    
                #Add the base widget to the screen in the carousel
                self.root.get_screen('keyactiongroup').ids.carousel_ka.add_widget(keyaction)
            else:
                #No matching business keys are found
                raise KeyError('Business Key Called from UI that does not exist in DB')
    
    #----------------------------------------------------------
    #----------------Internal Methods for Saving---------------
    #----------called in the SaveQuickKeyAction method---------
    
    def SaveKeyAction(self, child, i):
        #Module
        rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.id == selected_ids[i]).all()
        if len(rows) > 1:
            raise KeyError('Business Key Violation in table module')
        elif len(rows) == 1:
            rows[0].name = child.module_in.text
        session.commit()
        Logger.debug('QKA: Module Committed %s' % (child.module_in.text))
        
        #System Area
        sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.id == selected_ids[i]).all()
        if len(sa_rows) > 1:
            raise KeyError('Business Key Violation in table system area')
        elif len(sa_rows) == 1:
            sa_rows[0].name == child.sa_in.text
        sa_rows[0].moduleid = rows[0].id
        session.commit()
        Logger.debug('QKA: System Area Committed %s' % (child.sa_in.text))

        #Key Action
        ka_rows = session.query(KeyAction).filter(KeyAction.id == selected_ids[i]).all()
        if len(ka_rows) > 1:
            raise KeyError('Business Key Violation in table key action')
        elif len(ka_rows) == 1:
                ka_rows[0].id == child.ka_in.text
        ka_rows[0].systemareaid = sa_rows[0].id
        ka_rows[0].description = child.desc_in.text
        ka_rows[0].custom = child.custom_in.active
        session.commit()
        Logger.debug('QKA: Key Action Committed %s' % (child.ka_in.text))
        return ka_rows
        
    def SaveInputParameters(self, child, ka_rows, i):
        #Input Parameters
            
        rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.id == selected_ids[i]).all()
                
        #No existing input parameters for key action
        if len(rows) == 0:
            inpparam = InputParameter(name=child.ip_in.text)
            session.add(inpparam)
            inpparam.keyactionid = ka_rows[0].id
            inpparam2 = InputParameter(name=child.ip2_in.text)
            session.add(inpparam2)
            inpparam2.keyactionid = ka_rows[0].id
            inpparam3 = InputParameter(name=child.ip3_in.text)
            session.add(inpparam3)
            inpparam3.keyactionid = ka_rows[0].id
            session.commit()
            Logger.debug('QKA: No existing input parameters for key action')
                    
        #Single Existing input parameter for key action
        elif len(rows) == 1:
            Logger.debug('QKA: Single existing input parameter for key action')
            if rows[0].name == child.ip_in.text:
                Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                inpparam2 = InputParameter(name=child.ip2_in.text)
                session.add(inpparam2)
                inpparam2.keyactionid = ka_rows[0].id
                inpparam3 = InputParameter(name=child.ip3_in.text)
                session.add(inpparam3)
                inpparam3.keyactionid = ka_rows[0].id
            elif rows[0].name == child.ip2_in.text:
                Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                inpparam = InputParameter(name=child.ip_in.text)
                session.add(inpparam)
                inpparam.keyactionid = ka_rows[0].id
                inpparam3 = InputParameter(name=child.ip3_in.text)
                session.add(inpparam3)
                inpparam3.keyactionid = ka_rows[0].id
            elif rows[0].name == child.ip3_in.text:
                Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                inpparam = InputParameter(name=child.ip_in.text)
                session.add(inpparam)
                inpparam.keyactionid = ka_rows[0].id
                inpparam2 = InputParameter(name=child.ip2_in.text)
                session.add(inpparam2)
                inpparam2.keyactionid = ka_rows[0].id
            else:
                Logger.debug('QKA: No match encountered')
                rows[0].name = child.ip_in.text
                inpparam2 = InputParameter(name=child.ip2_in.text)
                session.add(inpparam2)
                inpparam2.keyactionid = ka_rows[0].id
                inpparam3 = InputParameter(name=child.ip3_in.text)
                session.add(inpparam3)
                inpparam3.keyactionid = ka_rows[0].id
                    
            session.commit()
                    
        #2 Existing input parameters for key action
        elif len(rows) == 2:
            Logger.debug('QKA: Two existing input parameters for key action')
            if rows[0].name == child.ip_in.text:
                Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                if rows[1].name == child.ip2_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                    if child.ip3_in.text != '' and child.ip3_in.text is not None:
                        inpparam3 = InputParameter(name=child.ip3_in.text)
                        session.add(inpparam3)
                        inpparam3.keyactionid = ka_rows[0].id
                elif rows[1].name == child.ip3_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                    if child.ip2_in.text != '' and child.ip2_in.text is not None:
                        inpparam2 = InputParameter(name=child.ip2_in.text)
                        session.add(inpparam2)
                        inpparam2.keyactionid = ka_rows[0].id
                else:
                    Logger.debug('QKA: The parameters in the UI dont match those in the DB')
                    #The input parameters in the UI don't match those in the DB
                    rows[1].name=child.ip2_in.text
                    if child.ip3_in.text != '' and child.ip3_in.text is not None:
                        inpparam3 = InputParameter(name=child.ip3_in.text)
                        session.add(inpparam3)
                        inpparam3.keyactionid = ka_rows[0].id
                        
            elif rows[0].name == child.ip2_in.text:
                Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                if rows[1].name == child.ip_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                    if child.ip3_in.text != '' and child.ip3_in.text is not None:
                        inpparam3 = InputParameter(name=child.ip3_in.text)
                        session.add(inpparam3)
                        inpparam3.keyactionid = ka_rows[0].id
                elif rows[1].name == child.ip3_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                    if child.ip2_in.text != '' and child.ip2_in.text is not None:
                        inpparam1 = InputParameter(name=child.ip_in.text)
                        session.add(inpparam1)
                        inpparam1.keyactionid = ka_rows[0].id
                else:
                    #The input parameters in the UI don't match those in the DB
                    Logger.debug('QKA: The input parameters in the UI dont match those in the DB')
                    inpparam1 = InputParameter(name=child.ip_in.text)
                    session.add(inpparam1)
                    inpparam1.keyactionid = ka_rows[0].id
                    rows[1].name=child.ip3_in.text
                    
            elif rows[0].name == child.ip3_in.text:
                Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                if rows[1].name == child.ip2_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                    if child.ip_in.text != '' and child.ip_in.text is not None:
                        inpparam2 = InputParameter(name=child.ip_in.text)
                        session.add(inpparam2)
                        inpparam2.keyactionid = ka_rows[0].id
                elif rows[1].name == child.ip_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                    if child.ip2_in.text != '' and child.ip2_in.text is not None:
                        inpparam2 = InputParameter(name=child.ip2_in.text)
                        session.add(inpparam2)
                        inpparam2.keyactionid = ka_rows[0].id
                else:
                    Logger.debug('QKA: The input parameters in the UI dont match those in the DB')
                    #The input parameters in the UI don't match those in the DB
                    rows[1].name=child.ip_in.text
                    inpparam2 = InputParameter(name=child.ip2_in.text)
                    session.add(inpparam2)
                    inpparam2.keyactionid = ka_rows[0].id
                    
            else:
                Logger.debug('QKA: The input parameters dont match those in the DB')
                #The input parameters in the UI don't match those in the DB
                rows[0].name=child.ip_in.text
                rows[1].name=child.ip2_in.text
                if child.ip3_in.text != '' and child.ip3_in.text is not None:
                    inpparam3 = InputParameter(name=child.ip3_in.text)
                    session.add(inpparam3)
                    inpparam3.keyactionid = ka_rows[0].id
                        
            session.commit()
                    
        #3 or more Existing Input Parameters for Key Action
        else:
            Logger.debug('QKA: Three existing input parameters for key action')
            if rows[0].name == child.ip_in.text:
                Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                if rows[1].name == child.ip2_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                    if rows[2].name != child.ip3_in.text and child.ip3_in.text != '' and child.ip3_in.text is not None:
                        Logger.debug('QKA: No match on %s' % (child.ip3_in.text))
                        rows[2].name=child.ip3_in.text
                elif rows[1].name == child.ip3_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                    if rows[2].name != child.ip2_in.text and child.ip2_in.text != '' and child.ip2_in.text is not None:
                        Logger.debug('QKA: No match on %s' % (child.ip2_in.text))
                        rows[2].name=child.ip2_in.text
                elif rows[2].name == child.ip2_in.text and child.ip3_in.text != '' and child.ip3_in.text is not None:
                    Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                    rows[1].name=child.ip3_in.text
                elif rows[2].name == child.ip3_in.text and child.ip2_in.text != '' and child.ip2_in.text is not None:
                    Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                    rows[1].name=child.ip2_in.text
                else:
                    Logger.debug('QKA: No match')
                    rows[1].name=child.ip2_in.text
                    rows[2].name=child.ip3_in.text
            elif rows[0].name == child.ip2_in.text:
                Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                if rows[1].name == child.ip_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                    if rows[2].name != child.ip3_in.text and child.ip3_in.text != '' and child.ip3_in.text is not None:
                        Logger.debug('QKA: No match on %s' % (child.ip3_in.text))
                        rows[2].name=child.ip3_in.text
                elif rows[1].name == child.ip3_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                    if rows[2].name != child.ip_in.text and child.ip_in.text != '' and child.ip_in.text is not None:
                        Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                        rows[2].name=child.ip_in.text
                elif rows[2].name == child.ip_in.text and child.ip3_in.text != '' and child.ip3_in.text is not None:
                    Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                    rows[1].name=child.ip3_in.text
                elif rows[2].name == child.ip3_in.text and child.ip_in.text != '' and child.ip_in.text is not None:
                    Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                    rows[1].name=child.ip_in.text
                else:
                    Logger.debug('QKA: No match')
                    rows[1].name=child.ip_in.text
                    rows[2].name=child.ip3_in.text
            elif rows[0].name == child.ip3_in.text:
                Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                if rows[1].name == child.ip2_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                    if rows[2].name != child.ip_in.text and child.ip_in.text != '' and child.ip_in.text is not None:
                        Logger.debug('QKA: No match on %s' % (child.ip_in.text))
                        rows[2].name=child.ip_in.text
                elif rows[1].name == child.ip_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                    if rows[2].name != child.ip2_in.text and child.ip2_in.text != '' and child.ip2_in.text is not None:
                        Logger.debug('QKA: No match on %s' % (child.ip2_in.text))
                        rows[2].name=child.ip2_in.text
                elif rows[2].name == child.ip2_in.text and child.ip_in.text != '' and child.ip_in.text is not None:
                    Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                    rows[1].name=child.ip_in.text
                elif rows[2].name == child.ip_in.text and child.ip_in.text != '' and child.ip_in.text is not None:
                    Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                    rows[1].name=child.ip2_in.text
                else:
                    Logger.debug('QKA: No match')
                    rows[1].name=child.ip_in.text
                    rows[2].name=child.ip2_in.text
            else:
                Logger.debug('QKA: No match on first result')
                if rows[1].name == child.ip_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                    if rows[2].name == child.ip2_in.text and child.ip3_in.text != '' and child.ip3_in.text is not None:
                        Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                        rows[0].name=child.ip3_in.text
                    elif rows[2].name == child.ip3_in.text and child.ip2_in.text != '' and child.ip2_in.text is not None:
                        Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                        rows[0].name=child.ip2_in.text
                    else:
                        Logger.debug('QKA: No match')
                        rows[0].name=child.ip2_in.text
                        rows[2].name=child.ip3_in.text
                elif rows[2].name == child.ip_in.text:
                    Logger.debug('QKA: Match on %s' % (child.ip_in.text))
                    if rows[1].name == child.ip2_in.text and child.ip3_in.text != '' and child.ip3_in.text is not None:
                        Logger.debug('QKA: Match on %s' % (child.ip2_in.text))
                        rows[0].name=child.ip3_in.text
                    elif rows[1].name == child.ip3_in.text and child.ip2_in.text != '' and child.ip2_in.text is not None:
                        Logger.debug('QKA: Match on %s' % (child.ip3_in.text))
                        rows[0].name=child.ip2_in.text
                    else:
                        Logger.debug('QKA: No match')
                        rows[0].name=child.ip2_in.text
                        rows[1].name=child.ip3_in.text
                else:
                    Logger.debug('QKA: All parameters replaced')
                    rows[0].name=child.ip_in.text
                    rows[1].name=child.ip2_in.text
                    rows[2].name=child.ip3_in.text
    
if __name__ == '__main__':
    TestScriptBuilderApp().run()