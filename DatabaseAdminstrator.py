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

from src.dbadmin.Translator import CSVTranslator, ExcelTranslator, ExternalDBTranslator, Translator
from src.dbadmin.DataBuffer import DataBuffer
from src.dbadmin.Writer import CSVWriter, ExcelWriter, TerminalWriter
from src.dbadmin.DataStream import DataStream

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

class KeyActionImport(Base):
    __tablename__ = 'keyaction_import'
    
    id = Column(Integer, primary_key=True) 
    keyactionid = Column(Integer, ForeignKey('keyaction.id'))
    importid = Column(Integer)
    
    act = relationship("KeyAction", backref=backref('keyaction_import', order_by=id))
    
    def __repr_(self):
        return "<Key Action: ID = '%s'>" % (self.id)

#Store the base level system area
class SystemArea(Base):
    __tablename__ = 'systemarea'
    
    id = Column(Integer, primary_key=True)
    moduleid = Column(Integer, ForeignKey('module.id'))
    name = Column(String)
    
    mod = relationship("Module", backref=backref('systemarea', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<System Area: ID = '%s', Module ID = '%s', Name = '%s'>" % (self.id, self.moduleid, self.name)

class SystemAreaImport(Base):
    __tablename__ = 'systemarea_import'
    
    id = Column(Integer, primary_key=True) 
    systemareaid = Column(Integer, ForeignKey('systemarea.id'))
    importid = Column(Integer)
    
    act = relationship("SystemArea", backref=backref('systemarea_import', order_by=id))
    
    def __repr_(self):
        return "<System Area: ID = '%s'>" % (self.id)

#Store the base level module
class Module(Base):
    __tablename__ = 'module'
    
    id = Column(Integer, primary_key=True)
    productid = Column(Integer, ForeignKey('product.id'))
    name = Column(String)
    
    mod = relationship("Product", backref=backref('module', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<Module: ID = '%s', Name = '%s', Product = %s>" % (self.id, self.name, self.productid)
        
class ModuleImport(Base):
    __tablename__ = 'module_import'
    
    id = Column(Integer, primary_key=True) 
    moduleid = Column(Integer, ForeignKey('module.id'))
    importid = Column(Integer)
    
    act = relationship("Module", backref=backref('module_import', order_by=id))
    
    def __repr_(self):
        return "<Module: ID = '%s'>" % (self.id)
    
#Store the base level product
class Product(Base):
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr_(self):
        return "<Product: ID = '%s', Name = '%s'>" % (self.id, self.name)
        
class ProductImport(Base):
    __tablename__ = 'product_import'
    
    id = Column(Integer, primary_key=True) 
    productid = Column(Integer, ForeignKey('product.id'))
    importid = Column(Integer)
    
    act = relationship("Product", backref=backref('product_import', order_by=id))
    
    def __repr_(self):
        return "<Product: ID = '%s'>" % (self.id)

#Store the base level input parameter
class InputParameter(Base):
    __tablename__ = 'inputparameter'
    
    id = Column(Integer, primary_key=True)
    keyactionid = Column(Integer, ForeignKey('keyaction.id'))
    name = Column(String)
    
    act = relationship("KeyAction", backref=backref('inputparameter', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
    
    def __repr_(self):
        return "<Input Parameter: ID = '%s', Key Action ID = '%s', Name = '%s'>" % (self.id, self.keyactionid, self.name)
    
class InputParameterImport(Base):
    __tablename__ = 'inputparameter_import'
    
    id = Column(Integer, primary_key=True) 
    inputparameterid = Column(Integer, ForeignKey('inputparameter.id'))
    importid = Column(Integer)
    
    act = relationship("InputParameter", backref=backref('inputparameter_import', order_by=id))
    
    def __repr_(self):
        return "<Input Parameter: ID = '%s'>" % (self.id)
    
#Store the base level client
class Client(Base):
    __tablename__ = 'client'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr_(self):
        return "<Client: ID = '%s', Name = '%s'>" % (self.id, self.name)
        
class ClientImport(Base):
    __tablename__ = 'client_import'
    
    id = Column(Integer, primary_key=True) 
    clientid = Column(Integer, ForeignKey('client.id'))
    importid = Column(Integer)
    
    act = relationship("Client", backref=backref('client_import', order_by=id))
    
    def __repr_(self):
        return "<Client: ID = '%s'>" % (self.id)
    
#Store the base level project
class Project(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True)
    clientid = Column(Integer, ForeignKey('client.id'))
    name = Column(String)
    
    mod = relationship("Client", backref=backref('project', order_by=id))
    
    def __repr_(self):
        return "<Project: ID = '%s', Client ID = '%s', Name = '%s'>" % (self.id, self.clientid, self.name)
        
class ProjectImport(Base):
    __tablename__ = 'project_import'
    
    id = Column(Integer, primary_key=True) 
    projectid = Column(Integer, ForeignKey('project.id'))
    importid = Column(Integer)
    
    act = relationship("Project", backref=backref('project_import', order_by=id))
    
    def __repr_(self):
        return "<Project: ID = '%s'>" % (self.id)
    
#Store the base level system area
class TestScript(Base):
    __tablename__ = 'testscript'
    
    id = Column(Integer, primary_key=True)
    projectid = Column(Integer, ForeignKey('project.id'))
    name = Column(String)
    
    mod = relationship("Project", backref=backref('testscript', order_by=id))
    
    def __repr_(self):
        return "<Test Script: ID = '%s', Project ID = '%s', Name = '%s'>" % (self.id, self.projectid, self.name)
    
class TestScriptImport(Base):
    __tablename__ = 'testscript_import'
    
    id = Column(Integer, primary_key=True) 
    testscriptid = Column(Integer, ForeignKey('testscript.id'))
    importid = Column(Integer)
    
    act = relationship("TestScript", backref=backref('testscript_import', order_by=id))
    
    def __repr_(self):
        return "<Test Script: ID = '%s'>" % (self.id)    
    
#Store the base level system area
class Workflow(Base):
    __tablename__ = 'workflow'
    
    id = Column(Integer, primary_key=True)
    testscriptid = Column(Integer, ForeignKey('testscript.id'))
    name = Column(String)
    
    mod = relationship("TestScript", backref=backref('workflow', order_by=id))
    
    def __repr_(self):
        return "<System Area: ID = '%s', Module ID = '%s', Name = '%s'>" % (self.id, self.moduleid, self.name)

class WorkflowImport(Base):
    __tablename__ = 'workflow_import'
    
    id = Column(Integer, primary_key=True) 
    workflowid = Column(Integer, ForeignKey('workflow.id'))
    importid = Column(Integer)
    
    act = relationship("Workflow", backref=backref('workflow_import', order_by=id))
    
    def __repr_(self):
        return "<Workflow: ID = '%s'>" % (self.id)    

class WorkflowAction(Base):
    __tablename__ = 'workflowaction'
    
    id = Column(Integer, primary_key=True)
    keyactionid = Column(Integer, ForeignKey('keyaction.id'))
    workflowid = Column(Integer, ForeignKey('workflow.id'))
    expectedresult = Column(String)
    notes = Column(String)
    fail = Column(Boolean)
    
    ka = relationship("KeyAction", backref=backref('workflowaction', order_by=id), single_parent=True)
    wf = relationship("Workflow", backref=backref('workflowaction', order_by=id))
    
    def __repr_(self):
        return "<Workflow Action: ID = '%s', Key Action ID = '%s', Expected Results = '%s', Notes = '%s', Fail = '%s'>" % (self.id, self.keyactionid, self.expectedresult, self.notes, self.fail)
    
class WorkflowActionImport(Base):
    __tablename__ = 'workflowaction_import'
    
    id = Column(Integer, primary_key=True) 
    workflowactionid = Column(Integer, ForeignKey('workflowaction.id'))
    importid = Column(Integer)
    
    act = relationship("WorkflowAction", backref=backref('workflowaction_import', order_by=id))
    
    def __repr_(self):
        return "<Workflow Action: ID = '%s'>" % (self.id)      
    
class WorkflowNextAction(Base):
    __tablename__ = 'workflownextaction'
    
    id = Column(Integer, primary_key=True)
    keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
    nextactionid = Column(Integer)
    
    act = relationship("WorkflowAction", backref=backref('workflownextaction', order_by=id))
    
    def __repr_(self):
        return "<Workflow Next Action: ID = '%s', Key Action ID = '%s', Next Action ID = '%s'>" % (self.id, self.keyactionid, self.nextactionid)
    
class WorkflowNextActionImport(Base):
    __tablename__ = 'workflownextaction_import'
    
    id = Column(Integer, primary_key=True) 
    workflownextactionid = Column(Integer, ForeignKey('workflownextaction.id'))
    importid = Column(Integer)
    
    act = relationship("WorkflowNextAction", backref=backref('workflownextaction_import', order_by=id))
    
    def __repr_(self):
        return "<Workflow Next Action: ID = '%s'>" % (self.id)      
    
class WorkflowParameter(Base):
    __tablename__ = 'workflowparam'
    
    id = Column(Integer, primary_key=True)
    inputparamid = Column(Integer, ForeignKey('inputparameter.id'))
    keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
    value = Column(String)
    
    act = relationship("WorkflowAction", backref=backref('workflowparam', order_by=id))
    ip = relationship("InputParameter", backref=backref('workflowparam', order_by=id), single_parent=True)
    
    def __repr_(self):
        return "<Workflow Parameter: ID = '%s', Input Parameter ID = '%s', Key Action ID = '%s', Value = '%s'>" % (self.id, self.inputparamid, self.keyactionid, self.value)

class WorkflowParameterImport(Base):
    __tablename__ = 'workflowparam_import'
    
    id = Column(Integer, primary_key=True) 
    workflowparameterid = Column(Integer, ForeignKey('workflowparam.id'))
    importid = Column(Integer)
    
    act = relationship("WorkflowParameter", backref=backref('workflowparam_import', order_by=id))
    
    def __repr_(self):
        return "<Workflow Parameter: ID = '%s'>" % (self.id)  

class FlowchartPosition(Base):
    __tablename__ = 'flowchart'
    
    id = Column(Integer, primary_key=True)
    keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
    row = Column(Integer)
    col = Column(Integer)
    
    act = relationship("WorkflowAction", backref=backref('flowchart', order_by=id))

class FlowchartPositionImport(Base):
    __tablename__ = 'flowchart_import'
    
    id = Column(Integer, primary_key=True) 
    flowchartpositionid = Column(Integer, ForeignKey('flowchart.id'))
    importid = Column(Integer)
    
    act = relationship("FlowchartPosition", backref=backref('flowchart_import', order_by=id))
    
    def __repr_(self):
        return "<Flowchart: ID = '%s'>" % (self.id)  

#------------------------------------------------------------
#----------------SQLAlchemy Connections----------------------
#------------------------------------------------------------

engine_path = 'sqlite:///test.db'
engine_name = 'test.db'

#Figure out whether we are running on windows or unix
#Connect to the DB
#echo=True turns on query logging
#echo="debug" turns on query + result logging
#echo=False turns off query logging
if platform.system() == 'Windows':
    engine = create_engine(engine_path, echo="debug")
else:
    engine = create_engine(engine_path, echo="debug")

#Connect to the DB
#echo=True turns on query logging
#echo="debug" turns on query + result logging
#echo=False turns off query logging
#engine = create_engine(engine_path, echo="debug")
Logger.info('SQLAlchemy: Engine Created')

#Database analyzed & created if necessary
if not os.path.exists(engine_name):
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
    
    def write(self, stream):
        while stream.result_stream.empty() == False:
            #Retrieve the top value from the queue
            data_buffer = stream.result_stream.get()
            
            #Write the data to the DB
            if data_buffer.type == 0:
                #The buffer data type is not assigned, perform no operations
                Logger.debug('Writer: Buffer Data Type not assigned')
                
            elif data_buffer.type == 1:
                
                Logger.debug('Writer: Product Export Initialized')
                
                #Create an Import Product object
                imp = ProductImport()
                imp.importid = data_buffer.data[0]
                
                #Does the product already exist in the DB?
                result = session.query(Product).filter(Product.name == '%s' % (data_buffer.data[1])).all()
                
                if result is not None and len(result) != 0:
                    imp.productid = result[0].id
                else:
                    #Make a new product
                    prod = Product()
                    prod.name = data_buffer.data[1]
                    session.add(prod)
                    session.commit()
                    imp.productid = prod.id
                
                session.add(imp)
                session.commit()
                    
            elif data_buffer.type == 2:
                
                Logger.debug('Writer: Module Export Initialized')
                
                #Create an Import Module object
                imp = ModuleImport()
                imp.importid = data_buffer.data[0]
                
                #Does the module already exist in the DB?
                result = session.query(Module).join(Product).join(ProductImport).\
                    filter(Module.name == '%s' % (data_buffer.data[2])).\
                        filter(ProductImport.importid == data_buffer.data[1]).all()
                        
                if result is not None and len(result) != 0:
                    imp.moduleid = result[0].id
                else:
                    #Find the product for the new module
                    prod = session.query(Product).join(ProductImport).\
                        filter(ProductImport.importid == data_buffer.data[1]).all()
                        
                    if prod is not None and len(prod) != 0:
                        
                        #Make a new module
                        mod = Module()
                        mod.name = data_buffer.data[2]
                        mod.productid = prod[0].id
                        session.add(mod)
                        session.commit()
                        imp.moduleid = mod.id
                    
                    else:
                        #If the product import can't be found, then the buffer should be
                        #added to the error queue and the method exited
                        data_buffer.add_error('Import Product not found in DB')
                        stream.error_stream.put(data_buffer)
                        return True
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 3:
                
                Logger.debug('Writer: System Area Export Initialized')
                
                #Create an Import System Area object
                imp = SystemAreaImport()
                imp.importid = data_buffer.data[0]
                
                #Does the system area already exist in the DB?
                result = session.query(SystemArea).join(Module).join(ModuleImport).\
                    filter(SystemArea.name == '%s' % (data_buffer.data[2])).\
                        filter(ModuleImport.importid == data_buffer.data[1]).all()
                        
                if result is not None and len(result) != 0:
                    imp.systemareaid = result[0].id
                else:
                    #Find the module for the new system area
                    mod = session.query(Module).join(ModuleImport).\
                        filter(ModuleImport.importid == data_buffer.data[1]).all()
                        
                    if mod is not None and len(mod) != 0:
                        
                        #Make a new system area
                        sa = SystemArea()
                        sa.name = data_buffer.data[2]
                        sa.moduleid = mod[0].id
                        session.add(sa)
                        session.commit()
                        imp.systemareaid = sa.id
                    else:
                        #If the module import can't be found, then the buffer should be
                        #added to the error queue and the method exited
                        data_buffer.add_error('Import Module not found in DB')
                        stream.error_stream.put(data_buffer)
                        return True
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 4:
                
                Logger.debug('Writer: Key Action Export Initialized')
                
                #Create an Import Key Action object
                imp = KeyActionImport()
                imp.importid = data_buffer.data[0]
                
                #Does the key action already exist in the DB?
                result = session.query(KeyAction).join(SystemArea).join(SystemAreaImport).\
                    filter(KeyAction.name == '%s' % (data_buffer.data[2])).\
                        filter(SystemAreaImport.importid == data_buffer.data[1]).all()
                        
                if result is not None and len(result) != 0:
                    imp.keyactionid = result[0].id
                    result[0].name = data_buffer.data[2]
                    result[0].description = data_buffer.data[3]
                    if data_buffer.data[4] == 0 or data_buffer.data[4] == '0'\
                        or data_buffer.data[4] == False or data_buffer.data[4] == 'False'\
                            or data_buffer.data[4] is None or data_buffer.data[4] == '':
                                
                        result[0].custom = False
                    else:
                        result[0].custom = True
                else:
                    #Find the system area for the new key action
                    sa = session.query(SystemArea).join(SystemAreaImport).\
                        filter(SystemAreaImport.importid == data_buffer.data[1]).all()
                        
                    if sa is not None and len(sa) != 0:
                        
                        #Make a new key action
                        ka = KeyAction()
                        ka.name = data_buffer.data[2]
                        ka.systemareaid = sa[0].id
                        ka.name = data_buffer.data[2]
                        ka.description = data_buffer.data[3]
                        if data_buffer.data[4] == 0 or data_buffer.data[4] == '0'\
                            or data_buffer.data[4] == False or data_buffer.data[4] == 'False'\
                                or data_buffer.data[4] is None or data_buffer.data[4] == '':
                                    
                            ka.custom = False
                        else:
                            ka.custom = True
                        session.add(ka)
                        session.commit()
                        imp.keyactionid = ka.id
                        
                    else:
                        #If the system area import can't be found, then the buffer should be
                        #added to the error queue and the method exited
                        data_buffer.add_error('Import System Area not found in DB')
                        stream.error_stream.put(data_buffer)
                        return True
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 5:
                
                Logger.debug('Writer: Input Parameter Export Initialized')
                
                #Create an Import Key Action object
                imp = InputParameterImport()
                imp.importid = data_buffer.data[0]
                
                #Does the input parameter already exist in the DB?
                result = session.query(InputParameter).join(KeyAction).join(KeyActionImport).\
                    filter(InputParameter.name == '%s' % (data_buffer.data[2])).\
                        filter(KeyActionImport.importid == data_buffer.data[1]).all()
                        
                if result is not None and len(result) != 0:
                    imp.inputparameterid = result[0].id
                else:
                    #Find the key action for the new input parameter
                    ka = session.query(KeyAction).join(KeyActionImport).\
                        filter(KeyActionImport.importid == data_buffer.data[1]).all()
                        
                    if ka is not None and len(ka) != 0:
                        
                        #Make a new input paramter
                        ip = InputParameter()
                        ip.name = data_buffer.data[2]
                        ip.keyactionid = ka[0].id
                        session.add(ip)
                        session.commit()
                        imp.keyactionid = ip.id
                        
                    else:
                        #If the key action import can't be found, then the buffer should be
                        #added to the error queue and the method exited
                        data_buffer.add_error('Import Key Action not found in DB')
                        stream.error_stream.put(data_buffer)
                        return True
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 6:
                
                Logger.debug('Writer: Client Export Initialized')
                
                #Create an Import Client object
                imp = ClientImport()
                imp.importid = data_buffer.data[0]
                
                #Does the client already exist in the DB?
                result = session.query(Client).filter(Client.name == '%s' % (data_buffer.data[1])).all()
                
                if result is not None and len(result) != 0:
                    imp.clientid = result[0].id
                else:
                    #Make a new client
                    client = Client()
                    client.name = data_buffer.data[1]
                    session.add(client)
                    session.commit()
                    imp.clientid = client.id
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 7:
                
                Logger.debug('Writer: Project Export Initialized')
                
                #Create an Import Project object
                imp = ProjectImport()
                imp.importid = data_buffer.data[0]
                
                #Does the system area already exist in the DB?
                result = session.query(Project).join(Client).join(ClientImport).\
                    filter(Project.name == '%s' % (data_buffer.data[2])).\
                        filter(ClientImport.importid == data_buffer.data[1]).all()
                        
                if result is not None and len(result) != 0:
                    imp.projectid = result[0].id
                else:
                    #Find the client for the new project
                    cl = session.query(Client).join(ClientImport).\
                        filter(ClientImport.importid == data_buffer.data[1]).all()
                        
                    if cl is not None and len(cl) != 0:
                        
                        #Make a new project
                        pr = Project()
                        pr.name = data_buffer.data[2]
                        pr.clientid = cl[0].id
                        session.add(pr)
                        session.commit()
                        imp.projectid = pr.id
                    else:
                        #If the client import can't be found, then the buffer should be
                        #added to the error queue and the method exited
                        data_buffer.add_error('Import Client not found in DB')
                        stream.error_stream.put(data_buffer)
                        return True
                
                session.add(imp)
                session.commit()
            elif data_buffer.type == 8:
                
                Logger.debug('Writer: Test Script Export Initialized')
                
                #Create an Import Test Script object
                imp = TestScriptImport()
                imp.importid = data_buffer.data[0]
                
                #Does the test script already exist in the DB?
                result = session.query(TestScript).join(Project).join(ProjectImport).\
                    filter(TestScript.name == '%s' % (data_buffer.data[2])).\
                        filter(ProjectImport.importid == data_buffer.data[1]).all()
                        
                if result is not None and len(result) != 0:
                    imp.testscriptid = result[0].id
                else:
                    #Find the project for the new test script
                    pr = session.query(Project).join(ProjectImport).\
                        filter(ProjectImport.importid == data_buffer.data[1]).all()
                        
                    if pr is not None and len(pr) != 0:
                        
                        #Make a new test script
                        ts = TestScript()
                        ts.name = data_buffer.data[2]
                        ts.projectid = pr[0].id
                        session.add(ts)
                        session.commit()
                        imp.testscriptid = ts.id
                    else:
                        #If the project import can't be found, then the buffer should be
                        #added to the error queue and the method exited
                        data_buffer.add_error('Import Project not found in DB')
                        stream.error_stream.put(data_buffer)
                        return True
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 9:
                
                Logger.debug('Writer: Workflow Export Initialized')
                
                #Create an Import Workflow object
                imp = WorkflowImport()
                imp.importid = data_buffer.data[0]
                
                #Does the workflow already exist in the DB?
                result = session.query(Workflow).join(TestScript).join(TestScriptImport).\
                    filter(Workflow.name == '%s' % (data_buffer.data[2])).\
                        filter(TestScriptImport.importid == data_buffer.data[1]).all()
                        
                if result is not None and len(result) != 0:
                    imp.workflowid = result[0].id
                    #Remove the workflow actions from the workflow and replace them
                    wfas = session.query(WorkflowAction).join(Workflow).filter(Workflow.id == result[0].id)
                    for wfa in wfas:
                    
                        #Clear the next actions, flowchart positions, and workflow parameters from the workflow action
                        #This allows for a full replace when doing dataloaders of these
                        #lower level objects while updating on matches with higher level
                        #objects
                        
                        na = session.query(WorkflowNextAction).join(WorkflowAction).filter(WorkflowAction.id == wfa.id)
                        fc = session.query(FlowchartPosition).join(WorkflowAction).filter(WorkflowAction.id == wfa.id)
                        wp = session.query(WorkflowParameter).join(WorkflowAction).filter(WorkflowAction.id == wfa.id)
                        
                        for n in na:
                            session.delete(n)
                        for f in fc:
                            session.delete(f)
                        for w in wp:
                            session.delete(w)
                        session.delete(wfa)
                    session.commit()
                else:
                    #Find the test script for the new workflow
                    ts = session.query(TestScript).join(TestScriptImport).\
                        filter(TestScriptImport.importid == data_buffer.data[1]).all()
                        
                    if ts is not None and len(ts) != 0:
                        
                        #Make a new workflow
                        wf = Workflow()
                        wf.name = data_buffer.data[2]
                        wf.testscriptid = ts[0].id
                        session.add(wf)
                        session.commit()
                        imp.workflowid = wf.id
                    else:
                        #If the Test Script import can't be found, then the buffer should be
                        #added to the error queue and the method exited
                        data_buffer.add_error('Import Test Script not found in DB')
                        stream.error_stream.put(data_buffer)
                        return True
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 10:
                
                Logger.debug('Writer: Workflow Action Export Initialized')
                
                #Create an Import Workflow Action object
                imp = WorkflowActionImport()
                imp.importid = data_buffer.data[0]
                
                #Does the workflow action already exist in the DB? No

                #Find the workfow for the new workflow action
                wf = session.query(Workflow).join(WorkflowImport).\
                    filter(WorkflowImport.importid == data_buffer.data[2]).all()
                    
                #Find the key action for the new workflow action
                ka = session.query(KeyAction).join(KeyActionImport).\
                    filter(KeyActionImport.importid == data_buffer.data[1]).all()
                    
                if wf is not None and len(wf) != 0:
                    if ka is not None and len(ka) != 0:
                    
                        #Make a new workflow action
                        wfa = WorkflowAction()
                        wfa.keyactionid = ka[0].id
                        wfa.workflowid = wf[0].id
                        wfa.expectedresult = data_buffer.data[3]
                        wfa.notes = data_buffer.data[4]
                        wfa.fail = data_buffer.data[5]
                        session.add(wfa)
                        session.commit()
                        imp.workflowactionid = wfa.id
                    else:
                        #If the key action import can't be found, then the buffer should be
                        #added to the error queue and the method exited
                        data_buffer.add_error('Import Key Action not found in DB')
                        stream.error_stream.put(data_buffer)
                        return True
                else:
                    #If the Workflow import can't be found, then the buffer should be
                    #added to the error queue and the method exited
                    data_buffer.add_error('Import Workflow not found in DB')
                    stream.error_stream.put(data_buffer)
                    return True
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 11:
                
                Logger.debug('Writer: Workflow Next Action Export Initialized')
                
                #Create an Import WorkflowNext Action object
                imp = WorkflowNextActionImport()
                imp.importid = data_buffer.data[0]
                
                #Does the workflow next action already exist in the DB?
                #We can assume no, and clear the workflow next actions & replce them

                #Find the workfow action for the new workflow next action
                wfa = session.query(WorkflowAction).join(WorkflowActionImport).\
                    filter(WorkflowActionImport.importid == data_buffer.data[1]).all()
                    
                #Find the next workflow id for the new workflow next action
                wfa2 = session.query(WorkflowAction).join(WorkflowActionImport).\
                    filter(WorkflowActionImport.importid == data_buffer.data[2]).all()
                    
                if wfa is not None and len(wfa) != 0:
                    if wfa2 is not None and len(wfa2) != 0:
                    
                        #Make a new workflow next action
                        wfna = WorkflowNextAction()
                        wfna.keyactionid = wfa[0].id
                        wfna.nextactionid = wfa2[0].id
                        session.add(wfna)
                        session.commit()
                        imp.workflownextactionid = wfna.id
                        
                    else:
                        #If the first workflow action import can't be found, then the buffer should be
                        #added to the error queue and the method exited
                        data_buffer.add_error('First Import Workflow Action not found in DB')
                        stream.error_stream.put(data_buffer)
                        return True
                else:
                    #If the second workflow action import can't be found, then the buffer should be
                    #added to the error queue and the method exited
                    data_buffer.add_error('Second Import Workflow Action not found in DB')
                    stream.error_stream.put(data_buffer)
                    return True
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 12:
                
                Logger.debug('Writer: Workflow Parameter Export Initialized')
                
                #Create an Import Workflow Parameter object
                imp = WorkflowParameterImport()
                imp.importid = data_buffer.data[0]
                
                ips = session.query(InputParameter).join(InputParameterImport).\
                    filter(InputParameterImport.importid == data_buffer.data[2]).all()
                
                if len(ips) != 0 and ips is not None:
                    ip = ips[0]
                else:
                    #If the workflow parameter import can't be found, then the buffer should be
                    #added to the error queue and the method exited
                    data_buffer.add_error('Import Workflow Parameter not found in DB')
                    stream.error_stream.put(data_buffer)
                    return True
                    
                    #Does the workflow parameter already exist in the DB?
                    #We can assume no, and clear the workflow next actions & replce them

                    #Find the workfow action for the new workflow parameter
                wfas = session.query(WorkflowAction).join(WorkflowActionImport).\
                    filter(WorkflowActionImport.importid == data_buffer.data[1]).all()
                    
                if wfas is not None and len(wfa) != 0:
                    wfa = wfas[0]
                else:
                    #If the product import can't be found, then the buffer should be
                    #added to the error queue and the method exited
                    data_buffer.add_error('Import Product not found in DB')
                    stream.error_stream.put(data_buffer)
                    return True
                    
                #Make a new workflow parameter
                wfp = WorkflowNextAction()
                wfp.keyactionid = wfa.id
                wfp.inputparameterid = ip.id
                wfp.value = data_buffer.data[3]
                session.add(wfp)
                session.commit()
                imp.workflowparameterid = wfp.id
                
                session.add(imp)
                session.commit()
                
            elif data_buffer.type == 13:
                Logger.debug('Writer: Flowchart Export Initialized')
                
                #Create an Import Flowchart object
                imp = FlowchartPositionImport()
                imp.importid = data_buffer.data[0]
                
                #Does the workflow parameter already exist in the DB?
                #We can assume no, and clear the workflow next actions & replce them

                #Find the workfow action for the new flowchart position
                wfa = session.query(WorkflowAction).join(WorkflowActionImport).\
                    filter(WorkflowActionImport.importid == data_buffer.data[1]).all()
                    
                if wfa is not None and len(wfa) != 0:
                    
                    #Make a new flowchart position
                    fp = FlowchartPosition()
                    fp.keyactionid = wfa[0].id
                    fp.row = data_buffer.data[2]
                    fp.col = data_buffer.data[3]
                    session.add(fp)
                    session.commit()
                    imp.flowchartpositionid = fp.id
                else:
                    #If the workflow action import can't be found, then the buffer should be
                    #added to the error queue and the method exited
                    data_buffer.add_error('Import Workflow Action not found in DB')
                    stream.error_stream.put(data_buffer)
                    return True
                
                session.add(imp)
                session.commit()
            
            #Finish with the data
            data_buffer.next_status()
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
         
         #Read the data type
         if self.root.ids.type_spinner.text == 'Key Action':
             import_type = 0
         elif self.root.ids.type_spinner.text == 'Workflow':
             import_type = 1
         elif self.root.ids.type_spinner.text == 'Test Script':
             import_type = 2
         else:
             import_type = 3
             Logger.debug('Import Type Unresolved')
             
         #If the direction is 'Import', assign the writer to the Internal DB Writer
         #If it's 'Export', assign the importer to the Internal DB Importer
         if self.root.ids.direction_spinner.text == 'Import':
             writer = DBWriter()
             
             #Find the importer
             if self.root.ids.translator_spinner.text == 'CSV':
                 importer = CSVTranslator(self.root.ids.source_input.text, import_type, stream.buffer_stream, 10)
             elif self.root.ids.translator_spinner.text == 'Excel':
                 importer = ExcelTranslator(self.root.ids.source_input.text, import_type, stream.buffer_stream, 10)
             elif self.root.ids.translator_spinner.text == 'DB':
                 importer = ExternalDBTranslator(self.root.ids.source_input.text, import_type, stream.buffer_stream, 10)
             else:
                 Logger.debug('Nothing Selected')
                 return True
                 #Nothing selected
         elif self.root.ids.direction_spinner.text == 'Export':
             importer = InternalDBTranslator()
             
             #Find the writer
             if self.root.ids.translator_spinner.text == 'Excel':
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

         while importer.translation_finished == False:

             #Single Iteration
             #Run Translations
             importer.translate()
             
             #Run Validations
             stream.stream()
             
             #Run Writer
             writer.write(stream)
             
         #Run Error Writer
         log_writer.write(stream)
             
         #DB Cleanup
             
         if self.root.ids.direction_spinner.text == 'Import':
             
             if import_type == 0:
             
                 #Delete everything from the key action import tables
                 imp = session.query(InputParameterImport).all()
                 for i in imp:
                     session.delete(i)
                     
                 ka = session.query(KeyActionImport).all()
                 for i in ka:
                     session.delete(i)
                     
                 sa = session.query(SystemAreaImport).all()
                 for i in sa:
                     session.delete(i)
                     
                 mod = session.query(ModuleImport).all()
                 for i in mod:
                     session.delete(i)
                     
                 prod = session.query(ProductImport).all()
                 for i in prod:
                     session.delete(i)
                     
             else:
                 
                 #Delete everything from the key action import tables
                 imp = session.query(InputParameterImport).all()
                 for i in imp:
                     session.delete(i)
                     
                 ka = session.query(KeyActionImport).all()
                 for i in ka:
                     session.delete(i)
                     
                 sa = session.query(SystemAreaImport).all()
                 for i in sa:
                     session.delete(i)
                     
                 mod = session.query(ModuleImport).all()
                 for i in mod:
                     session.delete(i)
                     
                 prod = session.query(ProductImport).all()
                 for i in prod:
                     session.delete(i)
                     
                 #Delete everything from the workflow import tables
                     
                 cl = session.query(ClientImport).all()
                 for c in cl:
                     session.delete(c)
                     
                 pr = session.query(ProjectImport).all()
                 for p in pr:
                     session.delete(p)
                     
                 ts = session.query(TestScriptImport).all()
                 for t in ts:
                     session.delete(t)
                     
                 wf = session.query(WorkflowImport).all()
                 for w in wf:
                     session.delete(w)
                     
                 wfa = session.query(WorkflowActionImport).all()
                 for a in wfa:
                     session.delete(a)
                     
                 wfna = session.query(WorkflowNextActionImport).all()
                 for na in wfna:
                     session.delete(na)
                     
                 wfp = session.query(WorkflowParameterImport).all()
                 for p in wfp:
                     session.delete(p)
                     
                 fl = session.query(FlowchartPositionImport).all()
                 for l in fl:
                     session.delete(l)
             
             session.commit()
         
    def UpdateDirection(self, *args):
         Logger.debug('Update Direction')
         if self.root.ids.direction_spinner.text == 'Import':
             self.root.ids.destination_input.text = 'test.db'
             self.root.ids.source_input.text = ''
             
             del self.root.ids.translator_spinner.values[:]
             self.root.ids.translator_spinner.values.append('CSV')
             self.root.ids.translator_spinner.values.append('Excel')
             self.root.ids.translator_spinner.values.append('DB')
             self.root.ids.translator_spinner.text = ''
             self.root.ids.type_spinner.text = ''
         else:
             self.root.ids.source_input.text = 'test.db'
             self.root.ids.destination_input.text = ''
             
             del self.root.ids.translator_spinner.values[:]
             self.root.ids.translator_spinner.values.append('Excel')
             self.root.ids.translator_spinner.text = 'Excel'
             
             del self.root.ids.type_spinner.values[:]
             self.root.ids.type_spinner.values.append('Test Script')
             self.root.ids.type_spinner.text = 'Test Script'
             
    def UpdateTranslator(self, *args):
         Logger.debug('Update Translator')
         if self.root.ids.direction_spinner.text == 'Import':

             if self.root.ids.translator_spinner.text =='CSV':
                 del self.root.ids.type_spinner.values[:]
                 self.root.ids.type_spinner.values.append('Key Action')
                 self.root.ids.type_spinner.text = 'Key Action'
             elif self.root.ids.translator_spinner.text == 'Excel':
                 del self.root.ids.type_spinner.values[:]
                 self.root.ids.type_spinner.values.append('Key Action')
                 self.root.ids.type_spinner.text = 'Key Action'
             elif self.root.ids.translator_spinner.text == 'DB':
                 del self.root.ids.type_spinner.values[:]
                 self.root.ids.type_spinner.values.append('Workflow')
                 self.root.ids.type_spinner.text = 'Workflow'


if __name__ == '__main__':
    DatabaseApp().run()
