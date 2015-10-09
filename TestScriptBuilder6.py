from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ListProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.actionbar import ActionBar, ActionView, ActionButton, ActionGroup
from kivy.uix.togglebutton import ToggleButton
from NodeWidget6 import NodeWidget
from DraggableImage import DraggableImage
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from KeyActionCarouselItem import KeyActionCarouselItem
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
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
	name = Column(String)
	
	def __repr_(self):
		return "<Module: ID = '%s', Name = '%s'>" % (self.id, self.name)

#Store the base level input parameter
class InputParameter(Base):
	__tablename__ = 'inputparameter'
	
	id = Column(Integer, primary_key=True)
	keyactionid = Column(Integer, ForeignKey('keyaction.id'))
	name = Column(String)
	
	act = relationship("KeyAction", backref=backref('inputparameter', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
	
	def __repr_(self):
		return "<Input Parameter: ID = '%s', Key Action ID = '%s', Name = '%s'>" % (self.id, self.keyactionid, self.name)

class WorkflowAction(Base):
	__tablename__ = 'workflowaction'
	
	id = Column(Integer, primary_key=True)
	keyactionid = Column(Integer)
	expectedresult = Column(String)
	notes = Column(String)
	fail = Column(Boolean)
	
	def __repr_(self):
		return "<Workflow Action: ID = '%s', Key Action ID = '%s', Expected Results = '%s', Notes = '%s', Fail = '%s'>" % (self.id, self.keyactionid, self.expectedresult, self.notes, self.fail)

class WorkflowSequence(Base):
	__tablename__ = 'workflowseq'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	workflowid = Column(Integer)
	workflowdesc = Column(String)
	keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
	
	act = relationship("WorkflowAction", backref=backref('workflowseq', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
	
	def __repr_(self):
		return "<Workflow Sequence: ID = '%s', Name = '%s', Key Action ID = '%s'>" % (self.id, self.name, self.keyactionid)
	
class WorkflowNextAction(Base):
	__tablename__ = 'workflownextaction'
	
	id = Column(Integer, primary_key=True)
	keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
	nextactionid = Column(Integer)
	
	act = relationship("WorkflowAction", backref=backref('workflownextaction', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
	
	def __repr_(self):
		return "<Workflow Next Action: ID = '%s', Key Action ID = '%s', Next Action ID = '%s'>" % (self.id, self.keyactionid, self.nextactionid)

class SubflowAction(Base):
	__tablename__ = 'subflowaction'
	
	id = Column(Integer, primary_key=True)
	keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
	expectedresult = Column(String)
	notes = Column(String)
	fail = Column(Boolean)
	
	act = relationship("WorkflowAction", backref=backref('subflowaction', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
	
	def __repr_(self):
		return "<Workflow Action: ID = '%s', Key Action ID = '%s', Expected Results = '%s', Notes = '%s', Fail = '%s'>" % (self.id, self.keyactionid, self.expectedresult, self.notes, self.fail)

class SubflowSequence(Base):
	__tablename__ = 'subflowseq'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	keyactionid = Column(Integer, ForeignKey('subflowaction.id'))
	parentid = Column(Integer)
	subflowid = Column(Integer)
	
	act = relationship("SubflowAction", backref=backref('subflowseq', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
	
	def __repr_(self):
		return "<Subflow Sequence: ID = '%s', Name = '%s', Key Action ID = '%s', Parent Workflow ID = '%s'>" % (self.id, self.name, self.keyactionid, self.parentid)

class SubflowNextAction(Base):
	__tablename__ = 'subflownextaction'
	
	id = Column(Integer, primary_key=True)
	keyactionid = Column(Integer, ForeignKey('subflowaction.id'))
	nextactionid = Column(Integer)
	
	act = relationship("SubflowAction", backref=backref('subflownextaction', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
	
	def __repr_(self):
		return "<Subflow Next Action: ID = '%s', Key Action ID = '%s', Next Action ID = '%s'>" % (self.id, self.keyactionid, self.nextactionid)

class WorkflowParameter(Base):
	__tablename__ = 'workflowparam'
	
	id = Column(Integer, primary_key=True)
	inputparamid = Column(Integer)
	keyactionid = Column(Integer, ForeignKey('workflowaction.id'))
	value = Column(String)
	
	act = relationship("WorkflowAction", backref=backref('workflowparam', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
	
	def __repr_(self):
		return "<Workflow Parameter: ID = '%s', Input Parameter ID = '%s', Key Action ID = '%s', Value = '%s'>" % (self.id, self.inputparamid, self.keyactionid, self.value)

class SubflowParameter(Base):
	__tablename__ = 'subflowparam'
	
	id = Column(Integer, primary_key=True)
	inputparamid = Column(Integer, ForeignKey('workflowparam.id'))
	keyactionid = Column(Integer, ForeignKey('subflowaction.id'))
	value = Column(String)
	
	act = relationship("SubflowAction", backref=backref('subflowparam', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
	param = relationship("WorkflowParameter", backref=backref('subflowparam', order_by=id), cascade="all, delete, delete-orphan", single_parent=True)
	
	def __repr_(self):
		return "<Subflow Parameter: ID = '%s', Input Parameter ID = '%s', Key Action ID = '%s', Value = '%s'>" % (self.id, self.inputparamid, self.keyactionid, self.value)

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
	
	def GetWorkflowResults(self, workflow, module, sysarea, keyaction, limit, offset):

		if (module == "" or module is None) and (sysarea == "" or sysarea is None) and (keyaction == "" or keyaction is None) and (workflow == "" or workflow is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				order_by(WorkflowAction.id)[limit:offset]
					
		elif (module == "" or module is None) and (sysarea == "" or sysarea is None) and (keyaction == "" or keyaction is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				filter(WorkflowSequence.name.like('%' + str(workflow) + '%')).\
					order_by(WorkflowAction.id)[limit:offset]
						
		elif (workflow == "" or workflow is None) and (module == "" or module is None) and (sysarea == "" or sysarea is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
					order_by(WorkflowAction.id)[limit:offset]
					
		elif (workflow == "" or workflow is None) and (module == "" or module is None) and (keyaction == "" or keyaction is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).\
					filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
						order_by(WorkflowAction.id)[limit:offset]
							
		elif (workflow == "" or workflow is None) and (sysarea == "" or sysarea is None) and (keyaction == "" or keyaction is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).join(Module).\
					filter(Module.name.like('%' + str(module) + '%')).\
						order_by(WorkflowAction.id)[limit:offset]
						
		elif (workflow == "" or workflow is None) and (module == "" or module is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).\
					filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
						filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
							order_by(WorkflowAction.id)[limit:offset]
									
		elif (module == "" or module is None) and (keyaction == "" or keyaction is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).\
					filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
						filter(WorkflowSequence.name.like('%' + str(workflow) + '%')).\
							order_by(WorkflowAction.id)[limit:offset]
									
		elif (module == "" or module is None) and (sysarea == "" or sysarea is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).join(KeyAction).\
					filter(KeyAction.name.like("'%s'" % (keyaction))).\
							filter(WorkflowSequence.name.like('%' + str(workflow) + '%')).\
								order_by(WorkflowAction.id)[limit:offset]
								
		elif (workflow == "" or workflow is None) and (sysarea == "" or sysarea is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).join(Module).\
					filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
						filter(Module.name.like('%' + str(module) + '%')).\
							order_by(WorkflowAction.id)[limit:offset]
										
		elif (sysarea == "" or sysarea is None) and (keyaction == "" or keyaction is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).join(Module).\
					filter(Module.name.like('%' + str(module) + '%')).\
						filter(WorkflowSequence.name.like('%' + str(workflow) + '%')).\
							order_by(WorkflowAction.id)[limit:offset]
										
		elif (workflow == "" or workflow is None) and (keyaction == "" or keyaction is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).join(Module).\
					filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
						filter(Module.name.like('%' + str(module) + '%')).\
							order_by(WorkflowAction.id)[limit:offset]
										
		elif (module == "" or module is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).join(Module).\
					filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
						filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
							filter(WorkflowSequence.name.like('%' + str(workflow) + '%')).\
								order_by(WorkflowAction.id)[limit:offset]
											
		elif (sysarea == "" or sysarea is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).join(Module).\
					filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
						filter(Module.name.like('%' + str(module) + '%')).\
							filter(WorkflowSequence.name.like('%' + str(workflow) + '%')).\
								order_by(WorkflowAction.id)[limit:offset]
											
		elif (keyaction == "" or keyaction is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).join(Module).\
					filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
						filter(Module.name.like('%' + str(module) + '%')).\
							filter(WorkflowSequence.name.like('%' + str(workflow) + '%')).\
								order_by(WorkflowAction.id)[limit:offset]
								
		elif (workflow == "" or workflow is None):
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).join(Module).\
					filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
						filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
							filter(Module.name.like('%' + str(module) + '%')).\
								order_by(WorkflowAction.id)[limit:offset]
											
		else:
			results = session.query(WorkflowAction).join(WorkflowSequence).\
				join(KeyAction).join(SystemArea).join(Module).\
					filter(KeyAction.name.like('%' + str(keyaction) + '%')).\
						filter(SystemArea.name.like('%' + str(sysarea) + '%')).\
							filter(Module.name.like('%' + str(module) + '%')).\
								filter(WorkflowSequence.name.like('%' + str(workflow) + '%')).\
									order_by(WorkflowAction.id)[limit:offset]
												
		return results

#------------------------------------------------------------
#----------------Main App------------------------------------
#------------------------------------------------------------

#Load the .kv file
Builder.load_file('testscriptbuilder_v3.kv')
Logger.info('KV: KV File Loaded')

#Create the filter manager
filter = FilterManager()

#Create the Selection List
selected = []

#Create the list of selected key action id's to allow updating names
selected_ids = []

class WorkflowScreen(Screen):
	pass

class KeyActionGroupScreen(Screen):
	pass

class SelectableGrid(GridLayout):
	pass

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
		return sm
#----------------------------------------------------------
#-------------------Key Action Page Callbacks--------------
#----------------------------------------------------------
	
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
		
	def SetCustom(self, *args):
		Logger.debug('Set Custom')
		
	def EnableCustomFiltering(self, *args):
		Logger.debug('Set Custom Filtering')
		
	def DisableCustomFiltering(self, *args):
		Logger.debug('Set Custom Filtering')
		
	#----------------------------------------------------------
	#-------------------Action Bar Methods---------------------
	
	def ImportKeyActions(self, *args):
		Logger.debug('DB Import')
	def ImportWorkflows(self, *args):
		Logger.debug('DB Import')
	def LoadDatabase(self, *args):
		Logger.debug('DB Import')
	def Quit(self, *args):
		Logger.debug('Graceful Exit')
	def GoToWorkflowPage(self, *args):
		
		Logger.debug('Go To Workflow Page')
		sm.current = 'workflow'
		self.root.get_screen('workflow').ids.grid_layout.clear_widgets()
		self.root.get_screen('workflow').ids.float_layout.clear_widgets()
		
		Logger.debug('Load Drag-n-Drop List')
		filter.FirstPage()
		
		Logger.debug('Apply Filter')
		results = filter.ApplyWorkflowFilter(self.root.get_screen('workflow').ids.workflowfilter_wf.text, self.root.get_screen('workflow').ids.modulefilter_wf.text, self.root.get_screen('workflow').ids.safilter_wf.text, self.root.get_screen('workflow').ids.kafilter_wf.text, self.root.get_screen('workflow').ids.customfilter_wf.active)
		
		Logger.debug('Create List Elements and add to grid layout')
		i = 0
		for i in range(0, len(results)):
			image = Label(text=results[i].name)
			draggable = DraggableImage(img=image, app=self)
			self.root.get_screen('workflow').ids.grid_layout.add_widget(draggable)

	def GoToAnalysisPage(self, *args):
		Logger.debug('Go To Analysis Page')
		
	def GoToKeyActionGroupPage(self, *args):
		Logger.debug('Go To Key Action Page')
		sm.current = 'keyactiongroup'
		#Set the FilterManager to page 1
		filter.FirstPage()
		self.root.get_screen('keyactiongroup').ids.selection_layout.clear_widgets()
		filter.setCustomFilteringEnabled(self.root.get_screen('keyactiongroup').ids.custswitch.active)
		results = filter.ApplyFilter(str(self.root.get_screen('workflow').ids.modulefilter_kag.text), str(self.root.get_screen('workflow').ids.safilter_kag.text), str(self.root.get_screen('workflow').ids.kafilter_kag.text), str(self.root.get_screen('workflow').ids.customfilter.active))
		i = 0
		for i in range(0, len(results)):
			sel = SelectableButton(text=str(results[i].name))
			sel.bind(on_press.SelectButton)
			self.root.get_screen('keyactiongroup').ids.selection_layout.add_widget(sel)
		
	def DuplicateKeyAction(self, *args):
		Logger.debug('Duplicate Key Action')
		#Duplicate the selected key actions
		
		self.root.get_screen('keyactiongroup').ids.carousel_ka.clear_widgets()
		numSelected = len(selected)
		
		if numSelected > 1:
			for action in selected_ids:
				#Create the Key Action Carousel Item
				keyaction = KeyActionCarouselItem()
					
				#Set the Module & System Area
				sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.id == action)
				keyaction.systemarea = sa_rows[0].name
				mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.id == action)
				keyaction.module = mod_rows[0].name
				
				#Create a new Key Action
				ka = KeyAction()
				session.add(ka)
				
				rows = session.query(KeyAction).filter(KeyAction.id == action)
				
				#Set the Key Action attributes
				keyaction.keyaction = "New %s" % (rows[0].name)
				ka.name = "New %s" % (rows[0].name)
				keyaction.description = rows[0].description
				ka.description = rows[0].description
				keyaction.custom = rows[0].custom
				ka.custom = rows[0].custom
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
			action = selected_ids[0]
			#Create the Key Action Carousel Item
			keyaction = KeyActionCarouselItem()
				
			#Set the Module & System Area
			sa_rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.id == action)
			keyaction.systemarea = sa_rows[0].name
			mod_rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.id == action)
			keyaction.module = mod_rows[0].name
			
			#Create a new Key Action
			ka = KeyAction()
			session.add(ka)
			
			rows = session.query(KeyAction).filter(KeyAction.id == action)
			
			#Set the Key Action attributes
			keyaction.keyaction = "New %s" % (rows[0].name)
			ka.name = "New %s" % (rows[0].name)
			keyaction.description = rows[0].description
			ka.description = rows[0].description
			keyaction.custom = rows[0].custom
			ka.custom = rows[0].custom
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
				
	#----------------------------------------------------------
	#-------------------Grid Methods---------------------------
				
	def SelectButton(self, *args):
		Logger.debug('Select Button')
				
	def AddWorkflow(self, *args):
		Logger.debug('Add Workflow')
		
	def AddToFlow(self, *args):
		Logger.debug('Add To Workflow')
		
	#----------------------------------------------------------
	#-------------------Quick Key Action Methods---------------
	
	def ClearQuickAction(self, *args):
		Logger.debug('Clear Quick Action')
		
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
		Logger.debug('Save Quick Key Action Frame')
		i = 0
		#TO-DO: Save based on ID's, not names
		#Loop through the children of the carousel and save each one
		if len(selected_ids)>1:
			for child in self.root.get_screen('keyactiongroup').ids.carousel_ka.slides:
				
				#Module
				modName = child.module
				module = Module(name=modName)
				session.add(module)
				rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.id == selected_ids[i]).all()
				if len(rows > 1):
					raise KeyError('Business Key Violation in table module')
				elif len(rows) == 1:
					module.id = rows[0].id
				session.commit()
				
				#System Area
				saName = child.systemarea
				systemarea = SystemArea(name=saName)
				session.add(systemarea)
				rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.id == selected_ids[i]).all()
				if len(rows > 1):
					raise KeyError('Business Key Violation in table system area')
				elif len(rows) == 1:
					systemarea.id = rows[0].id
				systemarea.moduleid = module.id
				session.commit()
		
				#Key Action
				kaName = child.keyaction
				keyaction = KeyAction(name=kaName)
				session.add(keyaction)
				rows = session.query(KeyAction).filter(KeyAction.id == selected_ids[i]).all()
				if len(rows) > 1:
					raise KeyError('Business Key Violation in table key action')
				elif len(rows) == 1:
					keyaction.id = rows[0].id
				keyaction.systemareaid = systemarea.id
				keyaction.description = child.description
				keyaction.custom = child.custom
				session.commit()
				
				#Input Parameters
				#TO-DO: Check if the parameter exists before adding
				inpparam = InputParameter(name=child.ip1)
				session.add(inpparam)
				inpparam.keyactionid = keyaction.id
				inpparam2 = InputParameter(name=child.ip2)
				session.add(inpparam2)
				inpparam2.keyactionid = keyaction.id
				inpparam3 = InputParameter(name=child.ip3)
				session.add(inpparam3)
				inpparam3.keyactionid = keyaction.id
				session.commit()
				i += 1
				
		#If there is only one child, save it
		elif len(selected_ids) == 1:
			child = self.root.get_screen('keyactiongroup').ids.carousel_ka.slides[0]

			#Module
			modName = child.module
			module = Module(name=modName)
			session.add(module)
			rows = session.query(Module).join(SystemArea).join(KeyAction).filter(KeyAction.id == selected_ids[i]).all()
			if len(rows) > 1:
				raise KeyError('Business Key Violation in table module')
			elif len(rows) == 1:
				module.id = rows[0].id
			session.commit()
			
			#System Area
			saName = child.systemarea
			systemarea = SystemArea(name=saName)
			session.add(systemarea)
			rows = session.query(SystemArea).join(KeyAction).filter(KeyAction.id == selected_ids[0]).all()
			if len(rows) > 1:
				raise KeyError('Business Key Violation in table system area')
			elif len(rows) == 1:
				systemarea.id = rows[0].id
			systemarea.moduleid = module.id
			session.commit()
	
			#Key Action
			kaName = child.keyaction
			keyaction = KeyAction(name=kaName)
			session.add(keyaction)
			rows = session.query(KeyAction).filter(KeyAction.id == selected_ids[0]).all()
			if len(rows) > 1:
				raise KeyError('Business Key Violation in table key action')
			elif len(rows) == 1:
				keyaction.id = rows[0].id
			keyaction.systemareaid = systemarea.id
			keyaction.description = child.description
			keyaction.custom = child.custom
			session.commit()
			
			#Input Parameters
			
			rows = session.query(InputParameter).join(KeyAction).filter(KeyAction.id == keyaction.id).all()
			#No existing input parameters for key action
			if len(rows) == 0:
				inpparam = InputParameter(name=child.ip1)
				session.add(inpparam)
				inpparam.keyactionid = keyaction.id
				inpparam2 = InputParameter(name=child.ip2)
				session.add(inpparam2)
				inpparam2.keyactionid = keyaction.id
				inpparam3 = InputParameter(name=child.ip3)
				session.add(inpparam3)
				inpparam3.keyactionid = keyaction.id
				session.commit()
				
			#Single Existing input parameter for key action
			elif len(rows) == 1:
				if rows[0].name == child.ip1:
					inpparam = InputParameter(name=child.ip1)
					inpparam.id = rows[0].id
					session.add(inpparam)
					inpparam.keyactionid = keyaction.id
					inpparam2 = InputParameter(name=child.ip2)
					session.add(inpparam2)
					inpparam2.keyactionid = keyaction.id
					inpparam3 = InputParameter(name=child.ip3)
					session.add(inpparam3)
					inpparam3.keyactionid = keyaction.id
				elif rows[0].name == child.ip2:
					inpparam = InputParameter(name=child.ip1)
					session.add(inpparam)
					inpparam.keyactionid = keyaction.id
					inpparam2 = InputParameter(name=child.ip2)
					inpparam2.id = rows[0].id
					session.add(inpparam2)
					inpparam2.keyactionid = keyaction.id
					inpparam3 = InputParameter(name=child.ip3)
					session.add(inpparam3)
					inpparam3.keyactionid = keyaction.id
				elif rows[0].name == child.ip3:
					inpparam = InputParameter(name=child.ip1)
					session.add(inpparam)
					inpparam.keyactionid = keyaction.id
					inpparam2 = InputParameter(name=child.ip2)
					session.add(inpparam2)
					inpparam2.keyactionid = keyaction.id
					inpparam3 = InputParameter(name=child.ip3)
					inpparam3.id = rows[0].id
					session.add(inpparam3)
					inpparam3.keyactionid = keyaction.id
				else:
					inpparam = InputParameter(name=child.ip1)
					session.add(inpparam)
					inpparam.keyactionid = keyaction.id
					inpparam2 = InputParameter(name=child.ip2)
					session.add(inpparam2)
					inpparam2.keyactionid = keyaction.id
					inpparam3 = InputParameter(name=child.ip3)
					session.add(inpparam3)
					inpparam3.keyactionid = keyaction.id
				
				session.commit()
				
			#2 Existing input parameters for key action
			elif len(rows) == 2:
				if rows[0].name == child.ip1:
					inpparam = InputParameter(name=child.ip1)
					inpparam.id = rows[0].id
					session.add(inpparam)
					inpparam.keyactionid = keyaction.id
					if rows[1].name == child.ip2:
						inpparam2 = InputParameter(name=child.ip2)
						inpparam2.id = rows[1].id
						session.add(inpparam2)
						inpparam2.keyactionid = keyaction.id
						inpparam3 = InputParameter(name=child.ip3)
						session.add(inpparam3)
						inpparam3.keyactionid = keyaction.id
					elif rows[1].name == child.ip3:
						inpparam2 = InputParameter(name=child.ip2)
						session.add(inpparam2)
						inpparam2.keyactionid = keyaction.id
						inpparam3 = InputParameter(name=child.ip3)
						inpparam3.id = rows[1].id
						session.add(inpparam3)
						inpparam3.keyactionid = keyaction.id
					else:
						#The input parameters in the UI don't match those in the DB
						inpparam2 = InputParameter(name=child.ip2)
						session.add(inpparam2)
						inpparam2.keyactionid = keyaction.id
						inpparam3 = InputParameter(name=child.ip3)
						session.add(inpparam3)
						inpparam3.keyactionid = keyaction.id
					
				elif rows[0].name == child.ip2:
					inpparam2 = InputParameter(name=child.ip2)
					inpparam2.id = rows[0].id
					session.add(inpparam2)
					inpparam2.keyactionid = keyaction.id
					if rows[1].name == child.ip1:
						inpparam1 = InputParameter(name=child.ip1)
						inpparam1.id = rows[1].id
						session.add(inpparam1)
						inpparam1.keyactionid = keyaction.id
						inpparam3 = InputParameter(name=child.ip3)
						session.add(inpparam3)
						inpparam3.keyactionid = keyaction.id
					elif rows[1].name == child.ip3:
						inpparam1 = InputParameter(name=child.ip1)
						session.add(inpparam1)
						inpparam1.keyactionid = keyaction.id
						inpparam3 = InputParameter(name=child.ip3)
						inpparam3.id = rows[1].id
						session.add(inpparam3)
						inpparam3.keyactionid = keyaction.id
					else:
						#The input parameters in the UI don't match those in the DB
						inpparam1 = InputParameter(name=child.ip1)
						session.add(inpparam1)
						inpparam1.keyactionid = keyaction.id
						inpparam3 = InputParameter(name=child.ip3)
						session.add(inpparam3)
						inpparam3.keyactionid = keyaction.id
					
				elif rows[0].name == child.ip3:
					inpparam3 = InputParameter(name=child.ip3)
					inpparam3.id = rows[0].id
					session.add(inpparam3)
					inpparam3.keyactionid = keyaction.id
					if rows[1].name == child.ip2:
						inpparam1 = InputParameter(name=child.ip1)
						inpparam1.id = rows[1].id
						session.add(inpparam1)
						inpparam1.keyactionid = keyaction.id
						inpparam2 = InputParameter(name=child.ip2)
						session.add(inpparam2)
						inpparam2.keyactionid = keyaction.id
					elif rows[1].name == child.ip1:
						inpparam1 = InputParameter(name=child.ip1)
						session.add(inpparam1)
						inpparam1.keyactionid = keyaction.id
						inpparam2 = InputParameter(name=child.ip2)
						inpparam2.id = rows[1].id
						session.add(inpparam2)
						inpparam2.keyactionid = keyaction.id
					else:
						#The input parameters in the UI don't match those in the DB
						inpparam1 = InputParameter(name=child.ip1)
						inpparam1.id = rows[1].id
						session.add(inpparam1)
						inpparam1.keyactionid = keyaction.id
						inpparam2 = InputParameter(name=child.ip2)
						session.add(inpparam2)
						inpparam2.keyactionid = keyaction.id
					
				else:
					#The input parameters in the UI don't match those in the DB
					inpparam = InputParameter(name=child.ip1)
					session.add(inpparam)
					inpparam.keyactionid = keyaction.id
					inpparam2 = InputParameter(name=child.ip2)
					session.add(inpparam2)
					inpparam2.keyactionid = keyaction.id
					inpparam3 = InputParameter(name=child.ip3)
					session.add(inpparam3)
					inpparam3.keyactionid = keyaction.id
					
				session.commit()
				
			#3 or more Existing Input Parameters for Key Action
			else:
				if rows[0].name == child.ip1:
					inpparam = InputParameter(name=child.ip1)
					inpparam.id = rows[0].id
					session.add(inpparam)
					inpparam.keyactionid = keyaction.id
					if rows[1].name == child.ip2 or rows[2].name == child.ip3:
						inpparam2 = InputParameter(name=child.ip2)
						inpparam2.id = rows[1].id
						session.add(inpparam2)
						inpparam2.keyactionid = keyaction.id
						inpparam3 = InputParameter(name=child.ip3)
						inpparam3.id = rows[2].id
						session.add(inpparam3)
						inpparam3.keyactionid = keyaction.id
					elif rows[1].name == child.ip3 or rows[2].name == child.ip2:
						inpparam2 = InputParameter(name=child.ip2)
						inpparam2.id = rows[2].id
						session.add(inpparam2)
						inpparam2.keyactionid = keyaction.id
						inpparam3 = InputParameter(name=child.ip3)
						inpparam3.id = rows[1].id
						session.add(inpparam3)
						inpparam3.keyactionid = keyaction.id
					else:
						pass
				elif rows[0].name == child.ip2:
					if rows[1].name == child.ip1:
						pass
					elif rows[1].name == child.ip3:
						pass
					elif rows[2].name == child.ip2:
						pass
					elif rows[2].name == child.ip3:
						pass
					else:
						pass
				elif rows[0].name == child.ip3:
					if rows[1].name == child.ip2:
						pass
					elif rows[1].name == child.ip1:
						pass
					elif rows[2].name == child.ip2:
						pass
					elif rows[2].name == child.ip3:
						pass
					else:
						pass
				else:
					pass
		else:
			#Save the key action as a new key action
			if len(self.root.get_screen('keyactiongroup').ids.carousel_ka.slides) != 0:
			
				#Only execute if there are elements in the carousel
				
				child = self.root.get_screen('keyactiongroup').ids.carousel_ka.slides[0]
				
				#Module
				modName = child.module
				module = Module(name=modName)
				session.add(module)
				rows = session.query(Module).filter(Module.name == modName).all()
				if len(rows) > 1:
					raise KeyError('Business Key Violation in table module')
				elif len(rows) == 1:
					module.id = rows[0].id
				session.commit()
				
				#System Area
				saName = child.systemarea
				systemarea = SystemArea(name=saName)
				session.add(systemarea)
				rows = session.query(SystemArea).filter(SystemArea.name == saName).all()
				if len(rows) > 1:
					raise KeyError('Business Key Violation in table system area')
				elif len(rows) == 1:
					systemarea.id = rows[0].id
				systemarea.moduleid = module.id
				session.commit()
			
				#Key Action
				kaName = child.keyaction
				keyaction = KeyAction(name=kaName)
				session.add(keyaction)
				keyaction.systemareaid = systemarea.id
				keyaction.description = child.description
				keyaction.custom = child.custom
				session.commit()
				
				#Input Parameters				
				inpparam = InputParameter(name=child.ip1)
				session.add(inpparam)
				inpparam.keyactionid = keyaction.id
				inpparam2 = InputParameter(name=child.ip2)
				session.add(inpparam2)
				inpparam2.keyactionid = keyaction.id
				inpparam3 = InputParameter(name=child.ip3)
				session.add(inpparam3)
				inpparam3.keyactionid = keyaction.id
				session.commit()
			
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
	
if __name__ == '__main__':
	TestScriptBuilderApp().run()