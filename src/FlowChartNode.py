from ConnectorWidget import ConnectorWidget
from DraggableImage import DraggableImage
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.Image import Image

class FlowChartNode(FloatLayout):
	
	app = ObjectProperty(None)
	bot_con = ObjectProperty(None)
	top_con = ObjectProperty(None)
	left_con = ObjectProperty(None)
	right_con = ObjectProperty(None)
	
	def __init__(self, **kwargs):
		super(FlowChartNode, self).__init__(**kwargs)
		
    		image = Image(source='image/central_node.png')
    		central_node = DraggableImage(img=image, app=self.app, pos=self.pos)
    		central_node.bind(pos=self.set_center_position, drag=self.drag_center, up=self.up_center, down=self.down_center)
    		self.add_widget(central_node)
    		
    		bottom_connector = ConnectorWidget(app=self.app)
    		top_connector = ConnectorWidget(app=self.app)
    		left_connector = ConnectorWidget(app=self.app)
    		right_connector = ConnectorWidget(app=self.app)
      
    		self.bot_con = bottom_connector
    		self.top_con = top_connector 
    		self.left_con = left_connector 
    		self.right_con = right_connector 
      
    		self.add_widget(bottom_connector)
    		self.add_widget(top_connector)
    		self.add_widget(left_connector)
    		self.add_widget(right_connector)
    		
    		bottom_connector.bind(pressfront=self.press_bottom)
    		top_connector.bind(pressfront=self.press_top)
    		left_connector.bind(pressfront=self.press_left)
    		right_connector.bind(pressfront=self.press_right)
    		
    		bottom_connector.bind(moveback=self.move_bottom)
    		top_connector.bind(moveback=self.move_top)
    		left_connector.bind(moveback=self.move_left)
    		right_connector.bind(moveback=self.move_right)
    		
    		bottom_connector.bind(releaseback=self.release_bottom)
    		top_connector.bind(releaseback=self.release_top)
    		left_connector.bind(releaseback=self.release_left)
    		right_connector.bind(releaseback=self.release_right)
		
def set_center_position(self, *args):
	self.central_node.pos = self.pos
	Logger.debug('Set Center Position')
	
def down_center(self, *args):
	Logger.debug('Down Center')
	self.remove_widget(self.bot_con)
	self.remove_widget(self.top_con)
	self.remove_widget(self.left_con)
	self.remove_widget(self.right_con)
	
def drag_center(self, *args):
	Logger.debug('Drag Center')
	
def up_center(self, *args):
	Logger.debug('Up Center')
	self.add_widget(self.bot_con)
	self.add_widget(self.top_con)
	self.add_widget(self.left_con)
	self.add_widget(self.right_con)
	
def press_bottom(self, *args):
	Logger.debug('Press Bottom')
	
def press_top(self, *args):
	Logger.debug('Press Top')
	
def press_left(self, *args):
	Logger.debug('Press Left')
	
def press_right(self, *args):
	Logger.debug('Press Right')
	
def move_bottom(self, *args):
	Logger.debug('Move Bottom')
	
def move_top(self, *args):
	Logger.debug('Move Top')
	
def move_left(self, *args):
	Logger.debug('Move Left')
	
def move_right(self, *args):
	Logger.debug('Move Right')
	
def release_bottom(self, *args):
	Logger.debug('Release Bottom')
	
def release_top(self, *args):
	Logger.debug('Release Top')
	
def release_left(self, *args):
	Logger.debug('Release Left')
	
def release_right(self, *args):
	Logger.debug('Release Right')