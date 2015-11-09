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
    
    #Internal Object Properties
    name_in = ObjectProperty(None)
    er_in = ObjectProperty(None)
    ipgrid_in = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(WFCarouselItem, self).__init__(**kwargs)
        
        #Layout the basic elements of the element
        self.orientation='vertical'
        ipgrid = GridLayout(rows=3, size_hint=(1, 0.55))
        self.ipgrid_in = ipgrid
        
        nametext = Label(size_hint=(1, 0.1))
        self.name_in = nametext
        ertext = TextInput(hint_text='Expected Results', size_hint=(1, 0.35))
        self.er_in = ertext
        
        #Bind the Properties
        self.bind(name=self.SetNameText)
        self.bind(er=self.SetErText)
        
        #Put the widgets together
        
        #Base Layout
        self.add_widget(nametext)
        self.add_widget(ertext)
        self.add_widget(ipgrid)
            
    def SetErText(self, *args):
        self.er_in.text = self.er
    def SetNameText(self, *args):
        self.name_in.text = self.name