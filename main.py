from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.uix.button import Button
import flower


class MainScreen(Screen):
    pass


class FlowerScreen(Screen):
    """ screen with detailed flower data, connected, or small
    """
    obj_cur_mst = ObjectProperty(None)
    obj_cur_temp = ObjectProperty(None)
    obj_adj_mst = ObjectProperty(None)
    obj_avg_mst = ObjectProperty(None)


class SettingsScreen(Screen):
    pass


class NextFlower(Screen):
    pass


class Manager(ScreenManager):

    main_screen = ObjectProperty(None)
    flower_screen = ObjectProperty(None)
    settings_screen = ObjectProperty(None)
    flower_name = StringProperty('')

    main_flower_list = flower.FlowerList()

    def on_flower_name(self, instance, value):
        b = Button(text=value, size_hint=(0.2, 0.2))
        self.main_screen.ids.stack.add_widget(b)
        #self.main_flower_list.add_flower(value)


class MagicStalkApp(App):
    """ main app, will change - create a list and main screen
    """
    def build(self):
        m = Manager(transition=WipeTransition())
        return m


if __name__ == '__main__':
    MagicStalkApp().run()

