from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, StringProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
from kivy.properties import ListProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

class KeyActionCarouselItem(BoxLayout):

    #Event Properties
    validate = BooleanProperty(False)
    
    #Value Properties
    module = StringProperty('')
    systemarea = StringProperty('')
    keyaction = StringProperty('')
    description = StringProperty('')
    custom = BooleanProperty(False)
    
    #List of Input Params
    iplist = ListProperty([])
    
    #App property
    app = ObjectProperty(None)
    
    #Name & ID List
    name_list = ListProperty([])
    id_list = ListProperty([])
    
    #Internal Object Properties
    module_in = ObjectProperty(None)
    sa_in = ObjectProperty(None)
    ka_in = ObjectProperty(None)
    desc_in = ObjectProperty(None)
    ipgrid_in = ObjectProperty(None)
    ipbutton_in = ObjectProperty(None)
    custom_in = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(KeyActionCarouselItem, self).__init__(**kwargs)
        
        #Layout the basic elements of the element
        self.orientation='vertical'
        topgrid = GridLayout(cols=2, size_hint=(1, 0.1))
        ipgrid = GridLayout(rows=3, size_hint=(1, 0.5))
        self.ipgrid_in = ipgrid
        bottomgrid = GridLayout(cols=2, size_hint=(1, 0.1))
        customgrid = GridLayout(cols=2, size_hint=(0.5, 1))
        modtext = TextInput(hint_text='Module')
        self.module_in = modtext
        satext = TextInput(hint_text='System Area')
        self.sa_in = satext
        katext = TextInput(hint_text='Key Action', size_hint=(1, 0.1))
        self.ka_in = katext
        desctext = TextInput(hint_text='Description', size_hint=(1, 0.2))
        self.desc_in = desctext
        custlabel = Label(text='Custom')
        custcheck = CheckBox()
        self.custom_in = custcheck
        ipbutton = Button(text='Add Input Parameter', on_press=self.app.AddInputParamToGrid)
        self.ipbutton_in = ipbutton
        
        #Bind the Properties
        self.bind(module=self.SetModText)
        self.bind(systemarea=self.SetSAText)
        self.bind(keyaction=self.SetKAText)
        self.bind(description=self.SetDescText)
        self.bind(custom=self.SetCustCheck)
        
        #Put the widgets together
        
        #Custom Grid
        customgrid.add_widget(custlabel)
        customgrid.add_widget(custcheck)
  
        bottomgrid.add_widget(customgrid)
        bottomgrid.add_widget(ipbutton)
        
        #Top Grid
        topgrid.add_widget(modtext)
        topgrid.add_widget(satext)
        
        #Base Layout
        self.add_widget(topgrid)
        self.add_widget(katext)
        self.add_widget(desctext)
        self.add_widget(bottomgrid)
        self.add_widget(ipgrid)
            
    def SetModText(self, *args):
        self.module_in.text = self.module
    def SetSAText(self, *args):
        self.sa_in.text = self.systemarea
    def SetKAText(self, *args):
        self.ka_in.text = self.keyaction
    def SetDescText(self, *args):
        self.desc_in.text = self.description
    def SetCustCheck(self, *args):
        self.custom_in.active = self.custom