from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from ConnectorNode import ConnectorNode
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.uix.image import Image
from kivy.uix.button import Button

#This class defines the line drawn between two nodes
class Connector(Widget):
	
	#Front and Back vertices, the line is drawn in between
	#2 Entry Lists
	front = ListProperty([0, 0])
	back = ListProperty([1, 1])
	
	#The color of the lines
	#3 Entry Lists
	line_color = ListProperty([1, 1, 1])
	
	ellipse_diameter = NumericProperty(20)
	
	def __init__(self, **kwargs):
		super(Connector, self).__init__(**kwargs)
		self.bind(front=self.set_front, back=self.set_back, line_color=self.set_color)
	
	def set_front(self, *args):
		self.canvas.clear()
		with self.canvas:
			Color(self.line_color[0], self.line_color[1], self.line_color[2])
			Line(points=[self.front[0], self.front[1], self.back[0], self.back[1]])
	
	def set_back(self, *args):
		self.canvas.clear()
		with self.canvas:
			Color(self.line_color[0], self.line_color[1], self.line_color[2])
			Line(points=[self.front[0], self.front[1], self.back[0], self.back[1]])
	
	def set_color(self, *args):
		self.canvas.clear()
		with self.canvas:
			Color(self.line_color[0], self.line_color[1], self.line_color[2])
			Line(points=[self.front[0], self.front[1], self.back[0], self.back[1]])
	
#This represents a connector with two connector node's
class ConnectorWidget(Widget):
	
	moveback = BooleanProperty(False)
	releaseback = BooleanProperty(False)
	pressfront = BooleanProperty(False)
	
	front = ObjectProperty(None)
	back = ObjectProperty(None)
	connect = ObjectProperty(None)
	
	app = ObjectProperty(None)
	
	def __init__(self, **kwargs):
		super(ConnectorWidget, self).__init__(**kwargs)
		#image = Image(source='image/press_node.png')
		front_node = Button(background_normal='image/press_node.png')
		front_node.bind(pos=self.set_front, on_press=self.press_front)
		self.front = front_node
		self.add_widget(front_node)
		
	def set_front(self, *args):
		self.connect.front = self.front.pos
		
	def set_back(self, *args):
		self.connect.back = self.back.pos
		
	def press_front(self, *args):
		#Add the back node and connector to the widget
		image2 = Image(source='image/drag_node.png')
		back_node = ConnectorNode(img=image2, app=self.app, is_draggable=True)
		connector = Connector()
		back_node.bind(pos=self.set_back, on_move=self.move_back, on_release=self.release_back)
		self.back = back_node
		self.connect = connector
		self.add_widget(connector)
		self.add_widget(back_node)
		if self.pressfront:
			self.pressfront = False
		else:
			self.pressfront = True
		
	def move_back(self, *args):
		if self.moveback:
			self.moveback = False
		else:
			self.moveback = True
	
	def release_back(self, *args):
		#Snap the back button to the nearest node
		if self.releaseback:
			self.releaseback = False
		else:
			self.releaseback = True