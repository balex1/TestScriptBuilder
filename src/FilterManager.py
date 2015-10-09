from ORM import KeyAction, SystemArea, Module, InputParameter, WorkflowAction, WorkflowSequence, WorkflowNextAction, WorkflowParameter, SubflowSequence, SubflowNextAction, SubflowParameter
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class FilterManager():
	#TO-DO: Add Custom Filtering
	#Update Page Length

	def __init__(self, Engine, Session):
		self.page = 1
		self.numPages = 999
		self.pageLength = 5

	def NextPage(self):
		self.page = self.page + 1
		if self.page > self.numPages:
			self.page = 1

	def PrevPage(self):
		self.page = self.page - 1
		if self.page == 0:
			self.page = self.numPages
			
	def FirstPage(self):
		self.page = 1

	def ApplyFilter(self, module, sysarea, keyaction, custom):
		#Instantiate a session each time we need to connect to the DB
		session = Session()
		self.pageLength = 20
		limit = self.pageLength
		offset = self.page * (self.pageLength - 1)
		if module == "" and sysarea == "" and keyaction == "":
			results = session.query(KeyAction).filter(KeyAction.custom == custom).\
				order_by(KeyAction.id)[limit:offset]
		elif module == "" and sysarea == "":
			results = session.query(KeyAction).\
				filter(KeyAction.name.like("'%s'" % (keyaction))).\
					filter(KeyAction.custom == custom).\
						order_by(KeyAction.id)[limit:offset]
		elif module == "" and keyaction == "":
			results = session.query(KeyAction).join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
				filter(SystemArea.name.like("'%s'" % (sysarea))).\
					filter(KeyAction.custom == custom).\
						order_by(KeyAction.id)[limit:offset]
		elif sysarea == "" and keyaction == "":
			results = session.query(KeyAction).join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
				join(Module, SystemArea.moduleid == Module.id).\
					filter(Module.name.like("'%s'" % (module))).\
						filter(KeyAction.custom == custom).\
							order_by(KeyAction.id)[limit:offset]
		elif module == "":
			results = session.query(KeyAction).join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
				filter(KeyAction.name.like("'%s'" % (keyaction))).\
					filter(SystemArea.name.like("'%s'" % (sysarea))).\
						filter(KeyAction.custom == custom).\
							order_by(KeyAction.id)[limit:offset]
		elif sysarea == "":
			results = session.query(KeyAction).join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
				join(Module, SystemArea.moduleid == Module.id).\
					filter(KeyAction.name.like("'%s'" % (keyaction))).\
						filter(Module.name.like("'%s'" % (module))).\
							filter(KeyAction.custom == custom).\
								order_by(KeyAction.id)[limit:offset]
		elif keyaction == "":
			results = session.query(KeyAction).join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
				join(Module, SystemArea.moduleid == Module.id).\
					filter(SystemArea.name.like("'%s'" % (sysarea))).\
						filter(Module.name.like("'%s'" % (module))).\
							filter(KeyAction.custom == custom).\
								order_by(KeyAction.id)[limit:offset]
		else:
			results = session.query(KeyAction).join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
				join(Module, SystemArea.moduleid == Module.id).\
					filter(KeyAction.name.like("'%s'" % (keyaction))).\
						filter(SystemArea.name.like("'%s'" % (sysarea))).\
							filter(Module.name.like("'%s'" % (module))).\
								filter(KeyAction.custom == custom).\
									order_by(KeyAction.id)[limit:offset]
	
	def ApplyWorkflowFilter(self, workflow, module, sysarea, keyaction, custom):
		
		#Instantiate a session each time we need to connect to the DB
		session = Session()
		self.pageLength = 10
		limit = self.pageLength
		offset = self.page * (self.pageLength - 1)
		
		#Apply the filter
		if module == "" and sysarea == "" and keyaction == "" and workflow == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				filter(KeyAction.custom == custom).\
					order_by(WorkflowAction.id)[limit:offset]
		elif module == "" and sysarea == "" and keyaction == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				filter(KeyAction.custom == custom).\
					filter(WorkflowSequence.name.like("'%s'" % (workflow))).\
						order_by(WorkflowAction.id)[limit:offset]
		elif workflow == "" and module == "" and sysarea == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					filter(KeyAction.name.like("'%s'" % (keyaction))).\
						filter(KeyAction.custom == custom).\
							order_by(WorkflowAction.id)[limit:offset]
		elif module == "" and workflow == "" and keyaction == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						filter(SystemArea.name.like("'%s'" % (sysarea))).\
							filter(KeyAction.custom == custom).\
								order_by(WorkflowAction.id)[limit:offset]
		elif workflow == "" and sysarea == "" and keyaction == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						join(Module, SystemArea.moduleid == Module.id).\
							filter(Module.name.like("'%s'" % (module))).\
								filter(KeyAction.custom == custom).\
									order_by(WorkflowAction.id)[limit:offset]
		elif module == "" and workflow == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						filter(KeyAction.name.like("'%s'" % (keyaction))).\
							filter(SystemArea.name.like("'%s'" % (sysarea))).\
								filter(KeyAction.custom == custom).\
									order_by(WorkflowAction.id)[limit:offset]
		elif module == "" and keyaction == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						filter(SystemArea.name.like("'%s'" % (sysarea))).\
							filter(KeyAction.custom == custom).\
								filter(WorkflowSequence.name.like("'%s'" % (workflow))).\
									order_by(WorkflowAction.id)[limit:offset]
		elif module == "" and systemarea == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					filter(KeyAction.name.like("'%s'" % (keyaction))).\
						filter(KeyAction.custom == custom).\
							filter(WorkflowSequence.name.like("'%s'" % (workflow))).\
								order_by(WorkflowAction.id)[limit:offset]
		elif systemarea == "" and workflow == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						join(Module, SystemArea.moduleid == Module.id).\
							filter(KeyAction.name.like("'%s'" % (keyaction))).\
								filter(Module.name.like("'%s'" % (module))).\
									filter(KeyAction.custom == custom).\
										order_by(WorkflowAction.id)[limit:offset]
		elif systemarea == "" and keyaction == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						join(Module, SystemArea.moduleid == Module.id).\
							filter(Module.name.like("'%s'" % (module))).\
								filter(KeyAction.custom == custom).\
									filter(WorkflowSequence.name.like("'%s'" % (workflow))).\
										order_by(WorkflowAction.id)[limit:offset]
		elif keyaction == "" and workflow == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						join(Module, SystemArea.moduleid == Module.id).\
							filter(SystemArea.name.like("'%s'" % (sysarea))).\
								filter(Module.name.like("'%s'" % (module))).\
									filter(KeyAction.custom == custom).\
										order_by(WorkflowAction.id)[limit:offset]
		elif module == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						join(Module, SystemArea.moduleid == Module.id).\
							filter(KeyAction.name.like("'%s'" % (keyaction))).\
								filter(SystemArea.name.like("'%s'" % (sysarea))).\
									filter(KeyAction.custom == custom).\
										filter(WorkflowSequence.name.like("'%s'" % (workflow))).\
											order_by(WorkflowAction.id)[limit:offset]
		elif systemarea == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						join(Module, SystemArea.moduleid == Module.id).\
							filter(KeyAction.name.like("'%s'" % (keyaction))).\
								filter(Module.name.like("'%s'" % (module))).\
									filter(KeyAction.custom == custom).\
										filter(WorkflowSequence.name.like("'%s'" % (workflow))).\
											order_by(WorkflowAction.id)[limit:offset]
		elif keyaction == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						join(Module, SystemArea.moduleid == Module.id).\
							filter(SystemArea.name.like("'%s'" % (sysarea))).\
								filter(Module.name.like("'%s'" % (module))).\
									filter(KeyAction.custom == custom).\
										filter(WorkflowSequence.name.like("'%s'" % (workflow))).\
											order_by(WorkflowAction.id)[limit:offset]
		elif workflow == "":
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						join(Module, SystemArea.moduleid == Module.id).\
							filter(KeyAction.name.like("'%s'" % (keyaction))).\
								filter(SystemArea.name.like("'%s'" % (sysarea))).\
									filter(Module.name.like("'%s'" % (module))).\
										filter(KeyAction.custom == custom).\
											order_by(WorkflowAction.id)[limit:offset]
		else:
			results = session.query(WorkflowAction).join(WorkflowSequence, WorkflowSequence.keyactionid == WorkflowAction.id).\
				join(KeyAction, WorkflowAction.keyactionid == KeyAction.id).\
					join(SystemArea, KeyAction.systemareaid == SystemArea.id).\
						join(Module, SystemArea.moduleid == Module.id).\
							filter(KeyAction.name.like("'%s'" % (keyaction))).\
								filter(SystemArea.name.like("'%s'" % (sysarea))).\
									filter(Module.name.like("'%s'" % (module))).\
										filter(KeyAction.custom == custom).\
											filter(WorkflowSequence.name.like("'%s'" % (workflow))).\
												order_by(WorkflowAction.id)[limit:offset]
		return results

	def GetCurrentPage(self):
		return self.page
	
	def NumPages(self):
		return self.numPages
	
	def GetPageLength(self):
		return self.pageLength
	
	def SetPageLength(self, newLength):
		self.pageLength = newLength