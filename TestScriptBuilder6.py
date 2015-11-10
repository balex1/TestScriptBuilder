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
from kivy.clock import Clock

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from src.KeyActionCarouselItem import KeyActionCarouselItem
from src.KeyActionPopup import KeyActionPopup
from src.WFCarouselItem import WFCarouselItem

from src.flowcharts.Connector import Connector
from src.flowcharts.DragGrid import DragGrid, DragGridCell
from src.flowcharts.FlowChartNode2 import FlowChartNode, DraggableImage
from src.flowcharts.DraggableOption import DraggableOption

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
#----------------DB Seed Scripts-----------------------------
#------------------------------------------------------------

#Find if the seed data already exists
seed_products = session.query(Product).filter(Product.name=='Default').all()
seed_clients = session.query(Client).filter(Client.name=='Default').all()
seed_projects = session.query(Project).filter(Project.name=='Default').all()
seed_testscripts = session.query(TestScript).filter(TestScript.name=='Default').all()
seed_workflows = session.query(Workflow).filter(Workflow.name=='Default').all()

#Add the seed data
if len(seed_products) == 0:
    seed_product = Product(name='Default')
    session.add(seed_product)
else:
    seed_product = seed_products[0]
    
if len(seed_clients) == 0:
    seed_client = Client(name='Default')
    session.add(seed_client)
else:
    seed_client = seed_clients[0]
    
session.commit()

if len(seed_projects) == 0:
    seed_project = Project(name='Default', clientid=seed_client.id)
    session.add(seed_project)
else:
    seed_project = seed_projects[0]
    
session.commit()
    
if len(seed_testscripts) == 0:
    seed_testscript = TestScript(name='Default', projectid=seed_project.id)
    session.add(seed_testscript)
else:
    seed_testscript = seed_testscripts[0]
    
session.commit()
    
if len(seed_workflows) == 0:
    seed_workflow = Workflow(name='Default', testscriptid=seed_testscript.id)
    session.add(seed_workflow)
else:
    seed_workflow = seed_workflows[0]

#------------------------------------------------------------
#----------------Filter Manager------------------------------
#------------------------------------------------------------


class FilterManager():
    #Class to manage filtering within the application

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
#----------------DB Writer-----------------------------------
#------------------------------------------------------------

class DatabaseWriter():
    #Class to abstract away saving of key objects to the database
    
    def __init__(self):
        Logger.info('DBWriter: Database Writer Created')
        
    def SaveInputParameter(self, ip_name, ka_name):
        #Check if the input parameter exists
        ip = session.query(InputParameter).join(KeyAction).filter(KeyAction.name==ka_name).filter(InputParameter.name==ip_name).all()
        if len(ip) == 0:
            keyaction = session.query(KeyAction).filter(KeyAction.name==ka_name).all()
            inputparameter = InputParameter(name=ip_name, keyactionid=keyaction[0].id)
            session.add(inputparameter)
        else:
            inputparameter = ip[0]
            
        session.commit()
        
    def SaveWorkflowParameter(self, ip_name, action_name, flow_name, param_value):
        ip = session.query(InputParameter).join(KeyAction).\
            filter(KeyAction.name==action_name).filter(InputParameter.name==ip_name).all()
            
        ka = session.query(KeyAction).filter(KeyAction.name==action_name).all()
        wf = session.query(Workflow).filter(Workflow.name==flow_name)
        
        wfp = session.query(WorkflowParameter).join(WorkflowAction).join(Workflow).\
            filter(Workflow.name==flow_name).filter(WorkflowParameter.inputparamid==ip[0].id).all()
            
        if len(wfp) == 0:
            param = WorkflowParameter(inputparamid=ip[0].id, keyactionid=ka[0].id, value = param_value)
            session.add(param)
        else:
            param = wfp[0]
            param.value = param_value
            
        session.commit()

    def SaveKeyAction(self, module, sysarea, name, desc, custom, ip_list):
        #Check if the module exists
        mod = session.query(Module).filter(Module.name==module).all()
        if len(mod) == 0:
            module = Module(name=module)
            session.add(module)
        else:
            module = mod[0]
        
        #Check if the system area exists
        sa = session.query(SystemArea).filter(SystemArea.name==sysarea).all()
        if len(sa) == 0:
            sysarea = SystemArea(name=sysarea)
            session.add(sysarea)
        else:
            sysarea = sa[0]
        
        #Check if the key action exists
        ka = session.query(KeyAction).filter(KeyAction.name==name).all()
        if len(ka) == 0:
            keyaction = KeyAction(name=name)
            session.add(keyaction)
        else:
            keyaction = ka[0]
            
        session.commit()
            
        #Assign the keyaction to the system area and module
        keyaction.systemareaid = sysarea.id
        sysarea.moduleid = module.id
        
        #Assign the description & custom
        keyaction.description = desc
        if custom == True or custom == 'True' or custom == 'true':
            keyaction.custom = True
        else:
            keyaction.custom = False
            
        #Input Parameters
        #Assumes that ip_list is passed in as a list of text inputs
        for ip in ip_list:
            self.SaveInputParameter(ip.text, keyaction.name)
            
        session.commit()
            
    def SaveWorkflowAction(self, action_name, flow_name, expected_results, ip_value_list):
        ka = session.query(KeyAction).filter(KeyAction.name==action_name).all()
        wf = session.query(Workflow).filter(Workflow.name==flow_name).one()
        ips = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == action_name).all()
        i = 0
        
        #Check if the workflow action exists
        wfa = session.query(WorkflowAction).join(Workflow).\
            filter(Workflow.name==flow_name).filter(WorkflowAction.keyactionid==ka[0].id).all()
        
        if len(wfa) == 0:
            action = WorkflowAction(keyactionid=ka[0].id, workflowid=wf.id, expectedresult=expected_results)
            session.add(action)
        else:
            action = wfa[0]
            action.expectedresult = expected_results
            
        for ip_value in ip_value_list:
            self.SaveWorkflowParameter(ips[i].name, action_name, flow_name, ip_value)
            i+=1
            
        session.commit()
            
    def SaveConnectionsList(self, con_list, workflow, testscript, project, client):
        start = con_list[0]
        end = con_list[1]
        i=0
        #Iterate through the lists
        for celement in con_list[0]:
            #A celement of index i from con_list[0] is the start connector
            #A celement of index i from con_list[1] is the end connector
            
            #Check if the next action exists within the workflow
            nxa = session.query(WorkflowNextAction).filter(WorkflowNextAction.keyactionid==celement.label.img.text).filter(WorkflowNextAction.nextactionid==end[i].label.img.text).all()
            
            if len(nxa) == 0:
                #Find the key action and next key action
                ka = session.query(WorkflowAction).join(KeyAction).filter(KeyAction.name==celement.label.img.text).all()
                na = session.query(WorkflowAction).join(KeyAction).filter(KeyAction.name==end[i].label.img.text).all()
                #Create a new workflow next action
                next_action = WorkflowNextAction(keyactionid=ka[0].id, nextactionid=na[0].id)
                session.add(next_action)
                session.commit()
            else:
                next_action = nxa
            i+=1
            
        session.commit()
        
    def SaveKeyActionByID(self, child, id):
        #Module
        rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.id == id).all()
        if len(rows) > 1:
            raise KeyError('Business Key Violation in table module')
        elif len(rows) == 1:
            rows[0].name = child.module_in.text
        session.commit()
        Logger.debug('QKA: Module Committed %s' % (child.module_in.text))
        
        #System Area
        sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.id == id).all()
        if len(sa_rows) > 1:
            raise KeyError('Business Key Violation in table system area')
        elif len(sa_rows) == 1:
            sa_rows[0].name == child.sa_in.text
        sa_rows[0].moduleid = rows[0].id
        session.commit()
        Logger.debug('QKA: System Area Committed %s' % (child.sa_in.text))

        #Key Action
        ka_rows = session.query(KeyAction).filter(KeyAction.id == id).all()
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
        
    def ValidateInputParameter(self, input_list, ip_list, id, orig_ip_list):
        #Input List gives a list of text inputs
        #IP List gives a list of IP Name Strings to check against
        #ID is the Key ActionID
        #Origin IP List gives a list of the input parameter ID's in the sameorder as the ip list

        #How many existing parameters do we have on the action?
        inputparams = session.query(InputParameter).join(KeyAction).filter(KeyAction.id == id).all()
        
        #Fill the existing parameters first
        i=0
        for param in inputparams:
            for i in range(0, len(orig_ip_list)):
                if param.id == orig_ip_list[i]:
                    param.name = ip_list[i]
                i+=1
            i=0
        
        #Add any new parameters
        for j in range(len(inputparams), len(input_list)):
            par = InputParameter(name=input_list[j].text, keyactionid=id)
            session.add(par)
            
        session.commit()
        
    def SaveInputParameters(self, child, ka_rows, id, orig_ip_list):
        #Input Parameters
        
        self.ValidateInputParameter(child.iplist, ka_rows, id, orig_ip_list)
        
    def SaveFlowchart(self, nodes_list):
        for node in nodes_list:
            wfa = session.query(WorkflowAction).join(KeyAction).join(Workflow).\
                join(TestScript).join(Project).join(Client).filter(KeyAction.name==node.label.img.text).\
                    filter(TestScript.name == current_script).filter(Project.name==current_project).\
                        filter(Client.name==current_client).all()
                        
            fl = session.query(FlowchartPosition).filter(FlowchartPosition.keyactionid == wfa[0].id).all()
            
            if len(fl) == 0:
                flow = FlowchartPosition(keyactionid=wfa[0].id, row=node.cell.row, col=node.cell.col)
                session.add(flow)
            else:
                flow = fl[0]
                flow.row = node.cell.row
                flow.col = node.cell.col
                
        session.commit()

#------------------------------------------------------------         
#------------------------------------------------------------
#----------------Main App------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------

#Load the .kv file
Builder.load_file('kv/TestScriptOptionsPopup.kv')
Builder.load_file('kv/AddToWorkflowPopup.kv')
Builder.load_file('kv/CreateWorkflowPopup.kv')
Builder.load_file('kv/KeyActionGroupScreen.kv')
Builder.load_file('kv/KeyActionsTabbedPanel.kv')
Builder.load_file('kv/LoadWorkflowPopup.kv')
Builder.load_file('kv/LoadSubflowPopup.kv')
Builder.load_file('kv/SelectableButton.kv')
Builder.load_file('kv/WorkflowScreen.kv')
Builder.load_file('kv/ForInPopup.kv')
Builder.load_file('kv/DeletePopup.kv')
Logger.info('KV: KV Files Loaded')

#Create the filter manager
filter = FilterManager()
#Create the DB Writer
writer = DatabaseWriter()
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
    pop_up=ObjectProperty(None)
    drag_grid=ObjectProperty(None)
    grid_layout=ObjectProperty(None)
    float_layout=ObjectProperty(None)
    current_wf=ObjectProperty(None)
    current_workflowname=StringProperty(None)
    current_script=StringProperty(None)
    current_project=StringProperty(None)
    current_client=StringProperty(None)

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

class ForInPopup(BoxLayout):
    app=ObjectProperty(None)
    keyaction_spinner=ObjectProperty(None)
    inputparameter_spinner=ObjectProperty(None)
    in_textinput=ObjectProperty(None)
    endaction_spinner=ObjectProperty(None)

class TestScriptOptionsPopup(BoxLayout):
    current_client = ObjectProperty(None)
    load_client = ObjectProperty(None)
    new_client = ObjectProperty(None)
    current_project = ObjectProperty(None)
    load_project = ObjectProperty(None)
    new_project = ObjectProperty(None)
    current_testscript = ObjectProperty(None)
    load_testscript = ObjectProperty(None)
    new_testscript = ObjectProperty(None)
    app = ObjectProperty(None)

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
    
class LoadSubflowPopup(BoxLayout):
    new_name=ObjectProperty(None)
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
    
class DeletePopup(BoxLayout):
    label=ObjectProperty(None)

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
    
    def add_ip_to_popup(self, *args):
        Logger.debug('WF: Add IP to Popup')
        ip = TextInput(hint_text='Input Parameter')
        self.root.get_screen('workflow').pop_up.content.ipgrid_in.add_widget(ip)
        self.root.get_screen('workflow').pop_up.content.ips.append(ip)
    
    def ClearWorkflow(self):
        #Clear the current workflow information and input box
        current_client = 'Default'
        current_project = 'Default'
        current_script = 'Default'
        self.root.get_screen('workflow').current_workflowname = 'Default'
        self.root.get_screen('workflow').current_wf.text = 'Default'
        
        #Clear the Drag Grid, Draggable List
        self.root.get_screen('workflow').drag_grid.clear_cells()
        self.root.get_screen('workflow').grid_layout.clear_widgets()
        self.root.get_screen('workflow').float_layout.clear_widgets()

    def CreateNewSubflow(self, *args):
        Logger.debug('WF: Create New Subflow')
        popup = Popup(title='Load Workflow', content=LoadSubflowPopup(), size_hint=(0.4, 0.5))
        popup.open()
        self.root.get_screen('workflow').pop_up = popup
        
        #Populate the latest 5 workflows into the spinner from the current testscript
        num_flows = session.query(Workflow).join(TestScript).join(Project).join(Client).\
            filter(TestScript.name == current_script).filter(Project.name==current_project).\
                filter(Client.name==current_client).count()
        if num_flows - 5 < 0:
            num_flows = 0
        else:
            num_flows = num_flows - 5
        results = session.query(Workflow).join(TestScript).join(Project).join(Client).\
            filter(TestScript.name == current_script).filter(Project.name==current_project).\
                filter(Client.name==current_client).order_by(Workflow.id)[num_flows:num_flows+5]
        
        #Populate values in spinner
        for result in results:
            popup.content.spinner.values.append(result.name)
            
    def LoadSubflow(self, *args):
        Logger.debug('Load Subflow')
        
        current_workflow=self.root.get_screen('workflow').pop_up.content.spinner.text
        new_workflow=self.root.get_screen('workflow').pop_up.content.new_name.text
        self.root.get_screen('workflow').pop_up.dismiss()
        #Copy the current workflow into a new workflow
        
        #Check if the new workflow already exists
        wf = session.query(Workflow).join(TestScript).join(Project).join(Client).\
            filter(TestScript.name == current_script).filter(Project.name==current_project).\
                filter(Client.name==current_client).filter(Workflow.name==new_workflow).all()
        if len(wf)==0:
            ts = session.query(TestScript).join(Project).join(Client).\
            filter(TestScript.name == current_script).filter(Project.name==current_project).\
                filter(Client.name==current_client).all()
            script = ts[0]
            flow = Workflow(name=new_workflow, testscriptid=script.id)
            session.add(flow)
            session.commit()
        else:
            flow = wf[0]
            
        #Copy the workflow actions
        actions = session.query(KeyAction).join(WorkflowAction).join(Workflow).\
            join(TestScript).join(Project).join(Client).filter(Workflow.name==current_workflow).\
                filter(TestScript.name == current_script).filter(Project.name==current_project).\
                    filter(Client.name==current_client).all()
        for action in actions:
            wfa = session.query(WorkflowAction).join(KeyAction).join(Workflow).join(TestScript).\
                join(Project).join(Client).filter(KeyAction.name==action.name).\
                    filter(TestScript.name == current_script).filter(Project.name==current_project).\
                        filter(Client.name==current_client).all()
            flowaction = wfa[0]
            ips = session.query(WorkflowParameter).join(WorkflowAction).filter(WorkflowAction.id==flowaction.id).all()
            ip_value_list = []
            for ip in ips:
                ip_value_list.append(ip.name)
            writer.SaveWorkflowAction(action.name, flow.name, flowaction.expectedresult, ip_value_list)
        
        #Clear the current elements in the UI
        self.ClearWorkflow()
        
        #Load the Key Actions from the new subflow into the editor
        keyactions = session.query(KeyAction).join(WorkflowAction).\
            join(Workflow).join(TestScript).join(Project).Client().\
                filter(Workflow.name==new_workflow).filter(TestScript.name == current_script).\
                    filter(Project.name==current_project).filter(Client.name==current_client).all()
        
        #Put each element into the draggable list
        for action in keyactions:
            lbl = Label(text=action.name)
            
            drag_option = DraggableOption(img=lbl, app=self,\
                grid=self.root.get_screen('workflow').drag_grid,\
                    grid_layout=self.root.get_screen('workflow').grid_layout,\
                        float_layout=self.root.get_screen('workflow').float_layout)
                        
            self.root.get_screen('workflow').grid_layout.add_widget(drag_option)
            
        self.root.get_screen('keyactiongroup').pop_up.dismiss()
        self.root.get_screen('workflow').ids.current_wf.text = new_workflow
        self.root.get_screen('workflow').current_workflowname = new_workflow
        
    def SaveConnectionsPanel(self, *args):
        Logger.debug('Save Connections Panel')
        #Phase 2
        
    def SaveConnectionsPanelDefaults(self, *args):
        Logger.debug('Save Connections Panel Defaults')
        #Phase 2

    def AddAndNode(self, *args):
        Logger.debug('WF: Add And Node')
        
        current_workflow=self.root.get_screen('workflow').current_workflowname
            
        #--UI--
        #Create a Label
        lbl = Label(text='AND')
            
        #Create an Add Option in the Draggable List
        drag_option = DraggableOption(img=lbl, app=self,\
            grid=self.root.get_screen('workflow').drag_grid,\
                grid_layout=self.root.get_screen('workflow').grid_layout,\
                    float_layout=self.root.get_screen('workflow').float_layout)
                        
        self.root.get_screen('workflow').grid_layout.add_widget(drag_option)
        
        #--DB--
        #Find a key action
        ka = session.query(KeyAction).filter(KeyAction.name=='AND').all()
        #Find the workflow
        wf = session.query(Workflow).join(TestScript).join(Project).join(Client).\
            filter(Workflow.name==current_workflow).filter(TestScript.name == current_script).\
                    filter(Project.name==current_project).filter(Client.name==current_client).one()
        if len(ka) == 0:
            keyaction = KeyAction(name='AND')
            session.add(keyaction)
            session.commit()
        else:
            keyaction = ka[0]
        #Add the workflow action
        wfa = WorkflowAction(keyactionid=keyaction.id, workflowid=wf.id)
        session.add(wfa)
        session.commit()
        
    def AddOrNode(self, *args):
        Logger.debug('WF: Add Or Node')
        
        current_workflow=self.root.get_screen('workflow').current_workflowname
        
        #--UI--
        #Create a Label
        lbl = Label(text='OR')
            
        #Create an Add Option in the Draggable List
        drag_option = DraggableOption(img=lbl, app=self,\
            grid=self.root.get_screen('workflow').drag_grid,\
                grid_layout=self.root.get_screen('workflow').grid_layout,\
                    float_layout=self.root.get_screen('workflow').float_layout)
                        
        self.root.get_screen('workflow').grid_layout.add_widget(drag_option)
        
        #--DB--
        #Find a key action
        ka = session.query(KeyAction).filter(KeyAction.name=='OR').all()
        #Find the workflow
        wf = session.query(Workflow).join(TestScript).join(Project).join(Client).\
            filter(Workflow.name==current_workflow).filter(TestScript.name == current_script).\
                    filter(Project.name==current_project).filter(Client.name==current_client).one()
        if len(ka) == 0:
            keyaction = KeyAction(name='OR')
            session.add(keyaction)
            session.commit()
        else:
            keyaction = ka[0]
        #Add the workflow action
        wfa = WorkflowAction(keyactionid=keyaction.id, workflowid=wf.id)
        session.add(wfa)
        session.commit()
        
    def ShowForPopup(self, *args):
        Logger.debug('WF: Show For Popup')
        current_workflow=self.root.get_screen('workflow').current_workflowname
        popup = Popup(title='For-In', content=ForInPopup(), size_hint=(0.5, 0.4))
        self.root.get_screen('workflow').pop_up = popup
        popup.open()
        
        #Load The Key Actions
        keyactions = session.query(KeyAction).join(WorkflowAction).join(Workflow).filter(Workflow.name==current_workflow).all()
        for action in keyactions:
            popup.content.keyaction_spinner.values.append(action.name)
            popup.content.endaction_spinner.values.append(action.name)
        
    def AddForNode(self, *args):
        Logger.debug('WF: Add For Node')
        popup=self.root.get_screen('workflow').pop_up
        current_workflow=self.root.get_screen('workflow').current_workflowname
        
        #--UI--
        #Create a Label
        lbl = Label(text='FOR')
            
        #Create an Add Option in the Draggable List
        drag_option = DraggableOption(img=lbl, app=self,\
            grid=self.root.get_screen('workflow').drag_grid,\
                grid_layout=self.root.get_screen('workflow').grid_layout,\
                    float_layout=self.root.get_screen('workflow').float_layout)
                        
        self.root.get_screen('workflow').grid_layout.add_widget(drag_option)
        
        #--DB--
        #Find a key action
        ka = session.query(KeyAction).filter(KeyAction.name=='FOR').all()
        #Find the workflow
        wf = session.query(Workflow).join(TestScript).join(Project).join(Client).\
            filter(Workflow.name==current_workflow).filter(TestScript.name == current_script).\
                    filter(Project.name==current_project).filter(Client.name==current_client).one()
        if len(ka) == 0:
            keyaction = KeyAction(name='FOR')
            session.add(keyaction)
            session.commit()
        else:
            keyaction = ka[0]
        #Add the workflow action
        wfa = WorkflowAction(keyactionid=keyaction.id, workflowid=wf.id)
        session.add(wfa)
        session.commit()
        
        #Add an input parameter
        ip = InputParameter(keyactionid=keyaction.id, name='In')
        session.add(ip)
        
        ip2 = InputParameter(keyactionid=keyaction.id, name='Final Key Action')
        session.add(ip2)
        session.commit()
        
        wp = WorkflowParameter(inputparamid=ip.id, keyactionid=wfa.id, value=popup.content.in_textinput.text)
        session.add(wp)
        
        wp = WorkflowParameter(inputparamid=ip2.id, keyactionid=wfa.id, value=popup.content.endaction_spinner.text)
        session.add(wp)
        session.commit()
        
        popup.dismiss()
        
    def UpdateIPSpinner(self, *args):
        Logger.debug('WF: Update IP Spinner')
        current_workflow=self.root.get_screen('workflow').current_wf.text
        popup=self.root.get_screen('workflow').pop_up
        
        #Clear the IP Spinner
        del popup.content.inputparameter_spinner.values[:]
            
        ips = session.query(InputParameter).join(KeyAction).filter(KeyAction.name==popup.content.keyaction_spinner.text).all()
        for ip in ips:
            popup.content.inputparameter_spinner.values.append(ip.name)
        
    def AdvancedOptionsPopup_WF(self, *args):
        Logger.debug('WF: Advanced Options Popup')
        popup = Popup(title='Export Options', content=ExportPopup(), size_hint=(0.5, 0.75))
        self.root.get_screen('workflow').pop_up = popup
        popup.open()
        
    def WFQuickActionPopup(self, *args):
        Logger.debug('WF: Quick Action Popup')
        popup = Popup(title='Quick Key Action', content=KeyActionPopup(app=self), size_hint=(0.5, 0.75))
        self.root.get_screen('workflow').pop_up = popup
        #popup.bind(on_dismiss=self.WFSaveQuickActionPopup)
        popup.open()
        
    def WFSaveQuickActionPopup(self, *args):
        Logger.debug('WF: Save Action Popup')
        
        popup = self.root.get_screen('workflow').pop_up
        
        #Custom
        if popup.content.custom_in.active:
            cust = True
        else:
            cust = False

        #Save Key Action
        writer.SaveKeyAction(popup.content.module_in.text, popup.content.sa_in.text,\
            popup.content.ka_in.text, popup.content.desc_in.text, cust, popup.content.ips)
            
        #Add to workflow
        ip = []
        writer.SaveWorkflowAction(popup.content.ka_in.text, self.root.get_screen('workflow').current_wf.text, '', ip)
        
        #Add node in list
        lbl = Label(text=popup.content.ka_in.text)
        
        drag_option = DraggableOption(img=lbl, app=self,\
            grid=self.root.get_screen('workflow').drag_grid,\
                grid_layout=self.root.get_screen('workflow').grid_layout,\
                    float_layout=self.root.get_screen('workflow').float_layout)
                        
        self.root.get_screen('workflow').grid_layout.add_widget(drag_option)
            
    #Load the Test Script Popup
    def TestScriptPopup_WF(self, *args):
        Logger.debug('WF: Test Script Popup')
        popup = Popup(title='Test Script Options', content=TestScriptOptionsPopup(app=self), size_hint=(0.5, 0.75))
        self.root.get_screen('workflow').pop_up = popup
        popup.open()
        
        #Populate the currently selected values into the popup
        popup.content.current_client = current_client
        popup.content.current_project = current_project
        popup.content.current_testscript = current_script
        
        #Populate the Spinners
        clients = session.query(Client).all()
        for client in clients:
            popup.content.load_client.values.append(client.name)
            
        projects = session.query(Project).all()
        for project in projects:
            popup.content.load_project.values.append(project.name)
            
        scripts = session.query(TestScript).all()
        for script in scripts:
            popup.content.load_testscript.values.append(script.name)
            
    #Update the project and test script spinners in the test script popup
    def UpdateProjectAndTestScript(self, *args):
        Logger.debug('WF: Test Script Popup')
        popup = self.root.get_screen('workflow').pop_up
        
        #Clear the spinners
        del popup.content.load_project.values[:]
        del popup.content.load_testscript.values[:]
        
        #Query based on the updated client
        projects = session.query(Project).join(Client).filter(Client.name == popup.content.load_client.text).all()
        for project in projects:
            popup.content.load_project.values.append(project.name)
            
        scripts = session.query(TestScript).join(Project).join(Client).\
            filter(Client.name == popup.content.load_client.text).all()
        for script in scripts:
            popup.content.load_testscript.values.append(script.name)
        
    #Update the test script spinner in the test script popup
    def UpdateTestScript(self, *args):
        Logger.debug('WF: Test Script Popup')
        popup = self.root.get_screen('workflow').pop_up
        
        del popup.content.load_testscript.values[:]
            
        scripts = session.query(TestScript).join(Project).join(Client).\
            filter(Client.name == popup.content.load_client.text).\
                filter(Project.name==popup.content.load_project.text).all()
        for script in scripts:
            popup.content.load_testscript.values.append(script.name)
        
    def SaveTestScriptPopup(self, *args):
        Logger.debug('WF: Save Test Script Popup')
        popup = self.root.get_screen('workflow').pop_up
        
        #If-Else Block to determine whether we're creating new values or using 
        #old ones, or a combination of the two
        
        #New client, project, and test script
        if (popup.content.new_client.text is not None and popup.content.new_client.text != "")\
            and (popup.content.new_project.text is not None and popup.content.new_project.text != "")\
                and (popup.content.new_testscript.text is not None and popup.content.new_testscript.text != ""):
            Logger.debug('WF: Save Test Script Popup - New Client, Project & Test Script')
            client = Client(name=popup.content.new_client.text)
            session.add(client)
            session.commit()
            
            project = Project(name=popup.content.new_project.text, clientid=client.id)
            session.add(project)
            session.commit()
            
            script = TestScript(name=popup.content.new_testscript.text, projectid=project.id)
            session.add(script)
            session.commit()
            
        #New client and project
        elif (popup.content.new_client.text is not None and popup.content.new_client.text != "")\
            and (popup.content.new_project.text is not None and popup.content.new_project.text != ""):
            Logger.debug('WF: Save Test Script Popup - New Client & Project')
            #Invalid
            
        #new project and test script
        elif (popup.content.new_project.text is not None and popup.content.new_project.text != "")\
            and (popup.content.new_testscript.text is not None and popup.content.new_testscript.text != ""):
            Logger.debug('WF: Save Test Script Popup - New Project & Test Script')
            
            cl = session.query(Client).filter(Client.name==popup.content.load_client.text).all()
            client = cl[0]
            
            project = Project(name=popup.content.new_project.text, clientid=client.id)
            session.add(project)
            session.commit()
            
            script = TestScript(name=popup.content.new_testscript.text, projectid=project.id)
            session.add(script)
            session.commit()
            
        #New client
        elif (popup.content.new_client.text is not None and popup.content.new_client.text != ""):
            Logger.debug('WF: Save Test Script Popup - New Client')
            #Invalid
            
        #New Project
        elif (popup.content.new_project.text is not None and popup.content.new_project.text != ""):
            Logger.debug('WF: Save Test Script Popup - New Project')
            #invalid
            
        #New Test Script
        elif (popup.content.new_testscript.text is not None and popup.content.new_testscript.text != ""):
            Logger.debug('WF: Save Test Script Popup - New Test Script')
            
            cl = session.query(Client).filter(Client.name==popup.content.load_client.text).all()
            client = cl[0]
            
            pj = session.query(Project).join(Client).filter(Project.name==popup.content.load_project.text).\
                filter(Client.name==popup.content.load_client.text).all()
            project = pj[0]
            
            script = TestScript(name=popup.content.new_testscript.text, projectid=project.id)
            session.add(script)
            session.commit()
            
        #Load All From DB
        else:
            Logger.debug('WF: Save Test Script Popup - Existing Client, Project, Test Script')
            
            cl = session.query(Client).filter(Client.name==popup.content.load_client.text).all()
            client = cl[0]
            
            pj = session.query(Project).join(Client).filter(Project.name==popup.content.load_project.text).\
                filter(Client.name==popup.content.load_client.text).all()
            project = pj[0]
            
            sc = session.query(TestScript).join(Project).join(Client).\
                filter(TestScript.name==popup.content.load_testscript.text).\
                    filter(Project.name==popup.content.load_project.text).\
                        filter(Client.name==popup.content.load_client.text).all()
            script = sc[0]
            
        #Clear the current elements in the UI
        self.ClearWorkflow()

        #Assign the current script        
        current_script = script.name
        current_project = project.name
        current_client = client.name
        
    def UpdateWorkflowName(self, *args):
        #When Enter is pressed on the current workflow text input, update the workflow name
        Logger.debug('WF: Update Workflow Name')
        wf = session.query(Workflow).join(TestScript).join(Project).join(Client).\
            filter(Workflow.name==self.root.get_screen('workflow').current_workflowname).\
                filter(TestScript.name == current_script).filter(Project.name==current_project).\
                    filter(Client.name==current_client).all()
        flow = wf[0]
        flow.name = self.root.get_screen('workflow').current_wf.text
        session.commit()
        
    def SaveWorkflow(self, *args):
        Logger.debug('WF: Save Workflow')
        
        writer.SaveConnectionsList(self.root.get_screen('workflow').drag_grid.connections,\
            self.root.get_screen('workflow').current_workflowname, self.root.get_screen('workflow').current_script,\
                self.root.get_screen('workflow').current_project, self.root.get_screen('workflow').current_client)
        
        writer.SaveFlowchart(self.root.get_screen('workflow').drag_grid.nodes)
        
    def SaveAction(self, *args):
        Logger.debug('WF: Save Action')
        #Pull side editor values
        action_name = self.root.get_screen('workflow').ids.wf_carousel.name_in.text
        flow_name = self.root.get_screen('workflow').current_workflowname
        expected_results = self.root.get_screen('workflow').ids.wf_carousel.er_in.text
        ip_value_list = []
        for child in self.root.get_screen('workflow').ids.wf_carousel.ipgrid_in.children:
            ip_value_list.append(child.text)
            
        #Write values to the DB
        writer.SaveWorkflowAction(action_name, flow_name, expected_results, ip_value_list)
  
    #This is a critical method as it is called when a draggable is released on
    #the flowchart, to add a flowchart node.  This takes the label from the original
    #Draggable, puts it into a new draggable wrapper and then into the flowchart node  
    def add_flowchart_node(self, cell, image):
        Logger.debug('Add flowchart node with image %s and cell %s' % (image, cell))
        drag_label = DraggableImage(img=image, app=self, grid=self.root.get_screen('workflow').drag_grid,\
            cell=cell, grid_layout=self.root.get_screen('workflow').grid_layout,\
                float_layout=self.root.get_screen('workflow').float_layout)
        drag = FlowChartNode(app=self, grid=self.root.get_screen('workflow').drag_grid, cell=cell, label=drag_label)
        drag_label.node = drag
        #Bind the double press to load the key action into the side editor
        drag_label.bind(on_double_press=self.LoadSideEditor)
        cell.add_widget(drag)
        cell.nodes.append(drag)
        self.root.get_screen('workflow').drag_grid.nodes.append(drag)
        
    def add_draggable_node(self, image):
        Logger.debug('Add draggable option to list')
        drag_option = DraggableOption(img=image, app=self,\
            grid=self.root.get_screen('workflow').drag_grid,\
                grid_layout=self.root.get_screen('workflow').grid_layout,\
                    float_layout=self.root.get_screen('workflow').float_layout)
        self.root.get_screen('workflow').grid_layout.add_widget(drag_option)
        
    def LoadSideEditor(self, node):
        #Loop through the nodes in the grid and find the one that has been double pressed
        Logger.debug('Load Side Editor with action %s' % (node.img.text))
        #for node in self.root.get_screen('workflow').drag_grid.nodes:
            #if node.label.is_double_pressed:
        
        #Clear the elements of the side editor
        self.root.get_screen('workflow').ids.wf_carousel.er_in.text = ''
        self.root.get_screen('workflow').ids.wf_carousel.ipgrid_in.clear_widgets()
    
        #Query the DB for the details of the action with the name from the label
        ka = session.query(KeyAction).filter(KeyAction.name==node.img.text).one()
        ips = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == node.img.text).all()
        w = session.query(WorkflowAction).join(Workflow).join(TestScript).join(Project).join(Client).\
            join(KeyAction).filter(KeyAction.name == node.img.text).\
                filter(Workflow.name==self.root.get_screen('workflow').current_workflowname).\
                    filter(TestScript.name == current_script).filter(Project.name==current_project).\
                        filter(Client.name==current_client).all()
        wfa = w[0]
        #Load the double clicked node into the side editor
        self.root.get_screen('workflow').ids.wf_carousel.name = node.img.text
        if wfa.expectedresult is not None:
            self.root.get_screen('workflow').ids.wf_carousel.er_in.text = wfa.expectedresult
            
        #Load the input parameters
        for ip in ips:
            wp = session.query(WorkflowParameter).join(InputParameter).join(WorkflowAction).\
                join(Workflow).join(TestScript).join(Project).join(Client).\
                    filter(InputParameter.id == ip.id).filter(Workflow.id == w[0].id).\
                        filter(TestScript.name == current_script).filter(Project.name==current_project).\
                            filter(Client.name==current_client).all()
            lbl = TextInput(hint_text=ip.name)
            if len(wp) != 0:
                lbl.text = wp[0].value
            self.root.get_screen('workflow').ids.wf_carousel.ipgrid_in.add_widget(lbl)
        
    def ApplyLoadWorkflowPopupFilter(self, *args):
        Logger.debug('Apply workflow filter popup')
        
        #Clear the Spinner
        del self.root.get_screen('keyactiongroup').pop_up.content.spinner.values[:]
        
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
        #TO-DO - Workflows with the same name in different testscripts/projects/clients
        Logger.debug('Add To Workflow')
        
        current_workflow=self.root.get_screen('keyactiongroup').pop_up.content.spinner.text
        
        #Clear the current elements in the UI
        self.ClearWorkflow()
        
        #Load the Key Actions for the flow
        keyactions = session.query(KeyAction).join(WorkflowAction).\
            join(Workflow).filter(Workflow.name==current_workflow).all()
            
        #Load the Key Actions for the flowchart
        flowchart_actions = session.query(KeyAction.name, FlowchartPosition.col, FlowchartPosition.row).select_from(FlowchartPosition).\
            join(WorkflowAction).join(Workflow).join(KeyAction).join(TestScript).join(Project).join(Client).\
                filter(Workflow.name==current_workflow).all()
        if len(flowchart_actions) != 0:            
            #Load the Next Key Actions for the flowchart
            next_actions = session.query(WorkflowNextAction).join(WorkflowAction).\
                join(Workflow).filter(Workflow.name==current_workflow).all()
                        
            #Identify the elements in the keyactions list that aren't in the flowchart_actions list
            for action in keyactions:
                for node in flowchart_actions:
                    if action.name == node.name:
                        keyactions.remove(action)
                        
            #Populate the flowchart
                        
            #Nodes
            for node in flowchart_actions:
                image = Label(text=node.name)
                self.add_flowchart_node(self.root.get_screen('workflow').drag_grid.get_cell(node.col, node.row), image)
            
            #Connections
            for action in next_actions:
                ka1 = session.query(KeyAction).join(WorkflowAction).filter(WorkflowAction.id == action.keyactionid).all()
                ka2 = session.query(KeyAction).join(WorkflowAction).filter(WorkflowAction.id == action.nextactionid).all()
                
                for node in self.root.get_screen('workflow').drag_grid.nodes:
                    #Find the cnnected node
                    for node2 in self.root.get_screen('workflow').drag_grid.nodes:
                        if ka2[0].name == node2.label.img.text:
                            connected_node = node2
                    #Add connections to the grid
                    if ka1[0].name == node.label.img.text:
                        connector = Connector(line_color=node.connector.connector_color)
                        node.connector.connections.append(connector)
                        node.connections.append(connected_node)
                        node.grid.connections[0].append(node)
                        node.grid.connections[1].append(connected_node)
        #Put each remaining element into the draggable list
        for action in keyactions:
            lbl = Label(text=action.name)
            
            drag_option = DraggableOption(img=lbl, app=self,\
                grid=self.root.get_screen('workflow').drag_grid,\
                    grid_layout=self.root.get_screen('workflow').grid_layout,\
                        float_layout=self.root.get_screen('workflow').float_layout)
                        
            self.root.get_screen('workflow').grid_layout.add_widget(drag_option)
            
        self.root.get_screen('keyactiongroup').pop_up.dismiss()
        self.root.get_screen('workflow').ids.current_wf.text = current_workflow
        self.root.get_screen('workflow').current_workflowname = current_workflow
        
            
#----------------------------------------------------------
#-------------------Key Action Page Callbacks--------------
#----------------------------------------------------------
            
    def AddInputParamToGrid(self, *args):
        Logger.debug('Add Input Parameter To Grid')
        ip_input = TextInput(hint_text='Input Parameter')
        self.root.get_screen('keyactiongroup').ids.carousel_ka.current_slide.ipgrid_in.add_widget(ip_input)
        self.root.get_screen('keyactiongroup').ids.carousel_ka.current_slide.iplist.append(ip_input)
    
    def CreateFlow(self, *args):
        Logger.debug('Create New Flow')
        
        new_script=self.root.get_screen('keyactiongroup').pop_up.content.spinner.text
        
        test_script=session.query(TestScript).filter(TestScript.name==new_script).one()
        
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
        del self.root.get_screen('keyactiongroup').pop_up.content.spinner.values[:]
        
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
        del self.root.get_screen('keyactiongroup').pop_up.content.spinner.values[:]
        
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
        
        del selected_ids[:]
        del selected[:]
        
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
        
        del selected_ids[:]
        del selected[:]
        
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
        
        del selected_ids[:]
        del selected[:]
        
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
                keyaction = KeyActionCarouselItem(app=self)
                    
                #Set the Module & System Area
                sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                keyaction.sa_in.text = sa_rows[0].name
                mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                keyaction.module_in.text = mod_rows[0].name
                
                #Create a new Key Action
                ka = KeyAction()
                session.add(ka)
                
                rows = session.query(KeyAction).filter(KeyAction.name == action)
                
                #Set the Key Action attributes
                keyaction.ka_in.text = "New %s" % (rows[0].name)
                ka.name = "New %s" % (rows[0].name)
                keyaction.desc_in.text = rows[0].description
                ka.description = rows[0].description
                keyaction.custom_in.active = rows[0].custom
                ka.custom = rows[0].custom
                ka.systemareaid = rows[0].systemareaid
                session.commit()
                    
                #Get the Input Parameters
                ip_rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == action).all()
                    
                #Add the base widget to the screen in the carousel
                self.root.get_screen('keyactiongroup').ids.carousel_ka.add_widget(keyaction)
                    
                #Add Text Inputs to IP Grid
                for ip in ip_rows:
                    ip_input = TextInput(hint_text='Input Parameter')
                    keyaction.ipgrid_in.add_widget(ip_input)
                    keyaction.iplist.append(ip_input)
                        
                #Set the IP attributes
                i=0
                for ip in ip_rows:
                    keyaction.name_list.append(ip.name)
                    keyaction.id_list.append(ip.id)
                    keyaction.iplist[i].text = ip.name
                    i+=1

        elif numSelected == 1:
            action = selected[0]
            #Create the Key Action Carousel Item
            keyaction = KeyActionCarouselItem(app=self)
                
            #Set the Module & System Area
            sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.name == action)
            keyaction.sa_in.text = sa_rows[0].name
            mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.name == action)
            keyaction.module_in.text = mod_rows[0].name
            
            #Create a new Key Action
            ka = KeyAction()
            session.add(ka)
            
            rows = session.query(KeyAction).filter(KeyAction.name == action)
            
            #Set the Key Action attributes
            keyaction.ka_in.text = "New %s" % (rows[0].name)
            ka.name = "New %s" % (rows[0].name)
            keyaction.desc_in.text = rows[0].description
            ka.description = rows[0].description
            keyaction.custom_in.active = rows[0].custom
            ka.custom = rows[0].custom
            ka.systemareaid = rows[0].systemareaid
            session.commit()
                
            #Get the Input Parameters
            ip_rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == action).all()
                    
            #Add the base widget to the screen in the carousel
            self.root.get_screen('keyactiongroup').ids.carousel_ka.add_widget(keyaction)
                    
            #Add Text Inputs to IP Grid
            for ip in ip_rows:
                ip_input = TextInput(hint_text='Input Parameter')
                keyaction.ipgrid_in.add_widget(ip_input)
                keyaction.iplist.append(ip_input)
                        
            #Set the IP attributes
            i=0
            for ip in ip_rows:
                keyaction.name_list.append(ip.name)
                keyaction.id_list.append(ip.id)
                keyaction.iplist[i].text = ip.name
                i+=1
                
    def DeleteKeyActionPopup(self, *args):
        Logger.debug('Delete Key Action Popup')
        popup = Popup(title='Delete Key Action', content=DeletePopup(), size_hint=(0.5, 0.4))
        self.root.get_screen('keyactiongroup').pop_up=popup
        popup.open()
    
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
        del selected_ids[:]
        
        self.root.get_screen('keyactiongroup').ids.carousel_ka.clear_widgets()
        keyaction = KeyActionCarouselItem(app=self)
        
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
            
                orig_id_list = child.id_list
                name_list = child.name_list
                
                keyactions = writer.SaveKeyActionByID(child, selected_ids[i])
                writer.SaveInputParameters(child, name_list, selected_ids[i], orig_id_list)
                i += 1
                
        #If there is only one child, save it
        elif len(selected_ids) == 1:
            Logger.debug('QKA: Selected IDs Length 1')
            child = self.root.get_screen('keyactiongroup').ids.carousel_ka.slides[0]
            orig_id_list = child.id_list
            name_list = child.name_list

            keyactions = writer.SaveKeyActionByID(child, selected_ids[i])
            writer.SaveInputParameters(child, name_list, selected_ids[i], orig_id_list)
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
                for input in child.iplist:
                    if input.text != '' and input.text is not None:
                        inpparam = InputParameter(name=input.text)
                        session.add(inpparam)
                        inpparam.keyactionid = keyaction.id
                session.commit()
        self.ApplyFilterKAG(args)
        del selected_ids[:]
        del selected[:]
        self.root.get_screen('keyactiongroup').ids.carousel_ka.clear_widgets()
            
    def LoadQuickAction(self, *args):
        Logger.debug('Load Quick Action')
        self.root.get_screen('keyactiongroup').ids.carousel_ka.clear_widgets()
        numSelected = len(selected)
        
        del selected_ids[:]
        
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
                    keyaction = KeyActionCarouselItem(app=self)
                    
                    #Set the Module & System Area
                    sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                    keyaction.sa_in.text = sa_rows[0].name
                    mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                    keyaction.module_in.text = mod_rows[0].name
                    
                    #Set the Key Action attributes
                    keyaction.ka_in.text = rows[0].name
                    keyaction.desc_in.text = rows[0].description
                    keyaction.custom_in.active = rows[0].custom
                    
                    #Get the Input Parameters
                    ip_rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == action).all()
                    
                    #Add the base widget to the screen in the carousel
                    self.root.get_screen('keyactiongroup').ids.carousel_ka.add_widget(keyaction)
                    
                    #Add Text Inputs to IP Grid
                    for ip in ip_rows:
                        ip_input = TextInput(hint_text='Input Parameter')
                        keyaction.ipgrid_in.add_widget(ip_input)
                        keyaction.iplist.append(ip_input)
                        
                    #Set the IP attributes
                    i=0
                    for ip in ip_rows:
                        keyaction.name_list.append(ip.name)
                        keyaction.id_list.append(ip.id)
                        keyaction.iplist[i].text = ip.name
                        i+=1
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
                keyaction = KeyActionCarouselItem(app=self)
                
                #Add the key action to the list of id's in the carousel
                selected_ids.append(rows[0].id)
                
                #Set the Module & System Area
                sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                keyaction.sa_in.text = sa_rows[0].name
                mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.name == action)
                keyaction.module_in.text = mod_rows[0].name
                
                #Set the Key Action attributes
                keyaction.ka_in.text = rows[0].name
                keyaction.desc_in.text = rows[0].description
                keyaction.custom_in.active = rows[0].custom
                    
                #Get the Input Parameters
                ip_rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.name == action).all()
                   
                #Add the base widget to the screen in the carousel
                self.root.get_screen('keyactiongroup').ids.carousel_ka.add_widget(keyaction)
                    
                #Add Text Inputs to IP Grid
                for ip in ip_rows:
                    ip_input = TextInput(hint_text='Input Parameter')
                    keyaction.ipgrid_in.add_widget(ip_input)
                    keyaction.iplist.append(ip_input)
                        
                #Set the IP attributes
                i=0
                for ip in ip_rows:
                    keyaction.name_list.append(ip.name)
                    keyaction.id_list.append(ip.id)
                    keyaction.iplist[i].text = ip.name
                    i+=1
                    
            else:
                #No matching business keys are found
                raise KeyError('Business Key Called from UI that does not exist in DB')
    
if __name__ == '__main__':
    TestScriptBuilderApp().run()