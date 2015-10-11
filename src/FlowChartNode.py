from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, StringProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.DraggableImage import DraggableImage

#This widget contains a central button and two toggle buttons
class NodeWidget(BoxLayout):

	#We expose events:
	#on_press when the central button is pressed
	#on_release when the central button is released
	#on_press_right when the right button is pressed
	#on_press_left when the left button is pressed
	press = BooleanProperty(False)
	release = BooleanProperty(False)
	press_right = BooleanProperty(False)
	press_left = BooleanProperty(False)
	release_right = BooleanProperty(False)
	release_left = BooleanProperty(False)
	
	#Properties exposed to set internal properties
	title = StringProperty('')
	left_background_normal = StringProperty('Left_Up.png')
	left_background_down = StringProperty('Left_Down.png')
	center_background_normal = StringProperty('Center_Button_Up.png')
	center_background_down = StringProperty('Center_Button_Down.png')
	right_background_normal = StringProperty('Right_Up.png')
	right_background_down = StringProperty('Right_Down.png')
	font_name = StringProperty('Roboto')
	markup = BooleanProperty(True)
	padding_x = NumericProperty(0)
	padding_y = NumericProperty(0)
	
	#Which node is active
	active_left = BooleanProperty(False)
	active_right = BooleanProperty(False)
	
	#Object Properties for internal elements
	left_button = ObjectProperty(None)
	center_button = ObjectProperty(None)
	right_button = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(NodeWidget, self).__init__(**kwargs)
		center = DraggableImage()
		left = ToggleButton()
		right = ToggleButton()
		left.size_hint = (0.10345, 1)
		center.size_hint = (0.801724, 1)
		right.size_hint = (0.094827, 1)
		left.background_normal = 'Left_Up.png'
		left.background_down = 'Left_Down.png'
		center.background_normal = 'Center_Button_Up.png'
		center.background_down = 'Center_Button_Down.png'
		right.background_normal = 'Right_Up.png'
		right.background_down = 'Right_Down.png'
		left.group = 'ends'
		right.group = 'ends'
		left.bind(on_press=self.ActivateNode_Left)
		left.bind(on_release=self.ReleaseNode_Left)
		right.bind(on_press=self.ActivateNode_Right)
		right.bind(on_release=self.ReleaseNode_Right)
		center.bind(on_press=self.PressNode)
		center.bind(on_release=self.ReleaseNode)
		self.left_button = left
		self.center_button = center
		self.right_button = right
		self.bind(title=self.SetTitle)
		self.bind(left_background_normal=self.SetLeftBackgroundNormal)
		self.bind(left_background_down=self.SetLeftBackgroundDown)
		self.bind(center_background_normal=self.SetCenterBackgroundNormal)
		self.bind(center_background_down=self.SetCenterBackgroundDown)
		self.bind(right_background_normal=self.SetRightBackgroundNormal)
		self.bind(right_background_down=self.SetRightBackgroundDown)
		self.bind(font_name=self.SetFontName)
		self.bind(markup=self.SetMarkup)
		self.bind(padding_x=self.SetPaddingX)
		self.bind(padding_y=self.SetPaddingY)
		self.add_widget(left)
		self.add_widget(center)
		self.add_widget(right)

	def ActivateNode_Left(self, *args):
		if self.active_left == False:
			self.active_left = True
			self.active_right = False
		else:
			self.active_left = False
			self.active_right = True
		if self.press_left == True:
			self.press_left = False
		else:
			self.press_left = True

	def ActivateNode_Right(self, *args):
		if self.active_right == False:
			self.active_right = True
			self.active_left = False
		else:
			self.active_right = False
			self.active_left = True
		if self.press_right == True:
			self.press_right = False
		else:
			self.press_right = True
			
	def ReleaseNode_Left(self, *args):
		if self.release_left == True:
			self.release_left == False
		else:
			self.release_left == True
			
	def ReleaseNode_Right(self, *args):
		if self.release_right == True:
			self.release_right == False
		else:
			self.release_right == True

	def PressNode(self, *args):
		if self.press == True:
			self.press = False
		else:
			self.press = True

	def ReleaseNode(self, *args):
		if self.release == True:
			self.release = False
		else:
			self.release = True

	def SetTitle(self, *args):
		self.center_button.text = self.title

	def SetLeftBackgroundDown(self, *args):
		self.left_button.background_down = self.left_background_down
	
	def SetLeftBackgroundNormal(self, *args):
		self.left_button.background_normal = self.left_background_normal
		
	def SetCenterBackgroundDown(self, *args):
		self.center_button.background_down = self.center_background_down
		
	def SetCenterBackgroundNormal(self, *args):
		self.center_button.background_normal = self.center_background_normal
		
	def SetRightBackgroundDown(self, *args):
		self.right_button.background_down = self.right_background_down
		
	def SetRightBackgroundNormal(self, *args):
		self.right_button.background_normal = self.right_background_normal
		
	def SetFontName(self, *args):
		self.center_button.font_name = self.font_name
		
	def SetMarkup(self, *args):
		self.center_button.markup = self.markup
		
	def SetPaddingX(self, *args):
		self.center_button.padding_x = self.padding_x
		
	def SetPaddingY(self, *args):
		self.center_button.padding_y = self.padding_y
