from Magnet import Magnet
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.clock import Clock

#This class defines a draggable, pressable object which will be
#added to the node editor it's dropped on.  
#This allows for a button-like functionality when it is off, 
#and a dragable functionality when it is on.  This means we 
#can have a connection mode to create connections between the nodes
class ConnectorNode(Magnet):
    img = ObjectProperty(None, allownone=True)
    app = ObjectProperty(None)
    press = BooleanProperty(False)
    release = BooleanProperty(False)
    move = BooleanProperty(False)
    is_draggable = BooleanProperty(True)
    
    node_editor = ObjectProperty(None)

    def on_img(self, *args):
        self.clear_widgets()

        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        if self.collide_point(*touch.pos):
            if self.is_draggable:
                touch.grab(self)
                self.remove_widget(self.img)
                self.app.root.get_screen('workflow').add_widget(self.img)
                self.center = touch.pos
                self.img.center = touch.pos
            else:
                if self.press:
                    self.press = False
                else:
                    self.press = True
            return True

        return super(ConnectorNode, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):
        self.node_editor = self.app.root.get_screen('workflow').ids.node_editor

        if touch.grab_current == self:
            self.img.center = touch.pos
            self.center = touch.pos
        if self.move:
            self.move = False
        else:
            self.move = True

        return super(ConnectorNode, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        self.node_editor = self.app.root.get_screen('workflow').ids.node_editor
        if self.is_draggable:
            if touch.grab_current == self:
                self.app.root.get_screen('workflow').remove_widget(self.img)
                self.add_widget(self.img)
                touch.ungrab(self)
                return True
            #if self.node_editor.collide_point(*touch.pos):
                #self.node_editor.add_widget(self)
        else:
            if self.release:
                self.release = False
            else:
                self.release = True
            return True

        return super(ConnectorNode, self).on_touch_up(touch, *args)

    def collision_point(self, x, y):
        x_left = self.center_x - (self.width / 1.5)
        x_right = self.center_x + (self.width / 1.5)
        y_bottom = self.center_y - (self.height / 1.5)
        y_top = self.center_y + (self.height / 1.5)
        return x_left <= x <= x_right and y_bottom <= y <= y_top