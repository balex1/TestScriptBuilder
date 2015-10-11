from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.label import Label

class WFCarouselItem(BoxLayout):

	#Event Properties
	validate = BooleanProperty(False)
	
	#Value Properties
	name = StringProperty('')
	er = StringProperty('')
	ip1 = StringProperty('')
	ip2 = StringProperty('')
	ip3 = StringProperty('')
	
	#Internal Object Properties
	name_in = ObjectProperty(None)
	er_in = ObjectProperty(None)
	ip_in = ObjectProperty(None)
	ip2_in = ObjectProperty(None)
	ip3_in = ObjectProperty(None)
	
	def __init__(self, **kwargs):
		super(WFCarouselItem, self).__init__(**kwargs)
		
		#Layout the basic elements of the element
		self.orientation='vertical'
		ipgrid = GridLayout(rows=3, size_hint=(1, 0.55))
		
		nametext = Label(size_hint=(1, 0.1))
		self.name_in = nametext
		ertext = TextInput(hint_text='Expected Results', size_hint=(1, 0.35))
		self.desc_in = desctext
		iptext = TextInput()
		self.ip_in = iptext
		ip2text = TextInput()
		self.ip2_in = ip2text
		ip3text = TextInput()
		self.ip3_in = ip3text
		
		#Bind the save button and text validations
		ertext.bind(on_text_validate=self.Validate)
		iptext.bind(on_text_validate=self.Validate)
		ip2text.bind(on_text_validate=self.Validate)
		ip3text.bind(on_text_validate=self.Validate)
		
		#Bind the Properties
		self.bind(name=self.SetNameText)
		self.bind(er=self.SetErText)
		self.bind(ip1=self.SetIPText)
		self.bind(ip2=self.SetIP2Text)
		self.bind(ip3=self.SetIP3Text)
		
		#Put the widgets together
		
		#Input Parameter Grid
		ipgrid.add_widget(iptext)
		ipgrid.add_widget(ip2text)
		ipgrid.add_widget(ip3text)
		
		#Base Layout
		self.add_widget(nametext)
		self.add_widget(ertext)
		self.add_widget(ipgrid)
			
	def Validate(self, *args):
		if self.validate == False:
			self.validate = True
		else:
			self.validate = False
			
	def SetErText(self, *args):
		self.er_in.text = self.er
	def SetNameText(self, *args):
		self.name_in.text = self.name
	def SetIPText(self, *args):
		self.ip_in.text = self.ip1
	def SetIP2Text(self, *args):
		self.ip2_in.text = self.ip2
	def SetIP3Text(self, *args):
		self.ip3_in.text = self.ip3