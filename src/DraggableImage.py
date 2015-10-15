from Magnet import Magnet
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.clock import Clock

#This class defines a draggable object which will be
#added to the layout it's dropped on.  This allows for
#a sortable list that can be dragged into the flow node_editor
#The is_draggable property is exposed to allow for a button-like 
#functionality when it is off, and a dragable functionality when
#it is on.  This means we can have a connection mode to create
#connections between the nodes
class DraggableImage(Magnet):
    img = ObjectProperty(None, allownone=True)
    app = ObjectProperty(None)
    press = BooleanProperty(False)
    release = BooleanProperty(False)
    is_draggable = BooleanProperty(True)
    
    down = BooleanProperty(False)
    drag = BooleanProperty(False)
    up = BooleanProperty(False)

    def on_img(self, *args):
        self.clear_widgets()

        if self.img:
            Clock.schedule_once(lambda *x: self.add_widget(self.img), 0)

    def on_touch_down(self, touch, *args):
        if self.down:
            self.down = False
        else:
            self.down = True
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

        return super(DraggableImage, self).on_touch_down(touch, *args)

    def on_touch_move(self, touch, *args):
        grid_layout = self.app.root.get_screen('workflow').ids.grid_layout
        float_layout = self.app.root.get_screen('workflow').ids.float_layout
        box_layout = self.app.root.get_screen('workflow').ids.box_layout
        node_editor = self.app.root.get_screen('workflow').ids.node_editor

        if touch.grab_current == self:
            self.img.center = touch.pos
            if grid_layout.collide_point(*touch.pos):
                grid_layout.remove_widget(self)
                float_layout.remove_widget(self)

                for i, c in enumerate(grid_layout.children):
                    #We need to keep things in the floatlayout longer
                    if c.collision_point(*touch.pos):
                        grid_layout.add_widget(self, i+1)
                        break
                else:
                    grid_layout.add_widget(self)
            elif box_layout.collision_point(*touch.pos):
                if self.parent == grid_layout:
                    grid_layout.remove_widget(self)
                    float_layout.add_widget(self)
            elif node_editor.collision_point(*touch.pos):
                if self.parent == grid_layout:
                    grid_layout.remove_widget(self)
                    node_editor.add_widget(self)
                elif self.parent == float_layout:
                    float_layout.remove_widget(self)
                    node_editor.add_widget(self)

                self.center = touch.pos
        if self.drag:
            self.drag = False
        else:
            self.drag = True
        return super(DraggableImage, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch, *args):
        if self.is_draggable:
            if touch.grab_current == self:
                self.app.root.get_screen('workflow').remove_widget(self.img)
                self.add_widget(self.img)
                touch.ungrab(self)
                return True
        else:
            if self.release:
                self.release = False
            else:
                self.release = True
            return True
        if self.up:
            self.up = False
        else:
            self.up = True

        return super(DraggableImage, self).on_touch_up(touch, *args)

    def collision_point(self, x, y):
        x_left = self.center_x - (self.width / 1.5)
        x_right = self.center_x + (self.width / 1.5)
        y_bottom = self.center_y - (self.height / 1.5)
        y_top = self.center_y + (self.height / 1.5)
        return x_left <= x <= x_right and y_bottom <= y <= y_top