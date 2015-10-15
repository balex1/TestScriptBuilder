from kivy.widget import widget
from kivy.graphics import Color, Line
from ConnectorNode import ConnectorNode
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty

#This class defines the line drawn between two nodes
class Connector(Widget):
	
	#Front and Back vertices, the line is drawn in between
	#2 Entry Lists
	front = ListProperty([])
	back = ListProperty([])
	
	#The color of the lines
	#3 Entry Lists
	line_color = ListProperty([])
	
	ellipse_diameter = NumericProperty(20)
	
	def __init__(self, **kwargs):
		super(Connector, self).__init__(**kwargs)
		self.bind(front=self.set_front, back=self.set_back, color=self.set_color)
	
	def set_front(self, *args):
		self.canvas.clear()
		with self.canvas:
			Color(line_color[0], line_color[1], line_color[2])
			Line(points=[front[0], front[1], back[0], back[1]])
	
	def set_back(self, *args):
		self.canvas.clear()
		with self.canvas:
			Color(line_color[0], line_color[1], line_color[2])
			Line(points=[front[0], front[1], back[0], back[1]])
	
	def set_color(self, *args):
		self.canvas.clear()
		with self.canvas:
			Color(line_color[0], line_color[1], line_color[2])
			Line(points=[front[0], front[1], back[0], back[1]])
	
#This represents a connector with two connector node's
class ConnectorWidget(Widget):
	
	moveback = BooleanProperty(False)
	releaseback = BooleanProperty(False)
	pressfront = BooleanProperty(False)
	
	front = ObjectProperty(None)
	back = ListProperty([])
	connections = ListProperty([])
	
	app = ObjectProperty(None)
	
	def __init__(self, **kwargs):
		super(Connector, self).__init__(**kwargs)
		image = Image(source='image/press_node.png')
		front_node = ConnectorNode(img=image, app=self.app, is_draggable=False)
		front_node.bind(pos=set_front, on_press=press_front)
		front = front_node
		self.add_widget(front_node)
		
	def set_front(self, *args):
		connector.front = front_node.pos
		
	def set_back(self, *args):
		connector.back = back_node.pos
		
	def press_front(self, *args):
		#Add the back node and connector to the widget
		image2 = Image(source='image/drag_node.png')
		back_node = ConnectorNode(img=image2, app=self.app, is_draggable=True)
		connector = Connector()
		back_node.bind(pos=set_back, on_move=move_back, on_release=release_back)
		back.append(back_node)
		connections.append(connector)
		self.add_widget(connector)
		self.add_widget(back_node)
		if pressfront:
			pressfront = False
		else:
			pressfront = True
		
	def move_back(self, *args):
		if moveback:
			moveback = False
		else:
			moveback = True
	
	def release_back(self, *args):
		#Snap the back button to the nearest node
		if releaseback:
			releaseback = False
		else:
			releaseback = True