from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.uix.button import Button
import flower


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.add_flower()
        # self.bind(result=self.add_flower)

    def add_flower(self):
        b = Button(text='Hello world', font_size=12)
        # self.id.grid.add_button(button)


class FlowerScreen(Screen):
    """ screen with detailed flower data, connected, or small
    """
    pass
    obj_cur_mst = ObjectProperty(None)
    obj_cur_temp = ObjectProperty(None)
    obj_adj_mst = ObjectProperty(None)
    obj_avg_mst = ObjectProperty(None)


class SettingsScreen(Screen):
    pass


class Manager(ScreenManager):
    # self.transition = WipeTransition()
    main_screen = ObjectProperty(None)
    flower_screen = ObjectProperty(None)
    settings_screen = ObjectProperty(None)


class MagicStalkApp(App):
    """ main app, will change - create a list and main screen
    """
    def build(self):
        m = Manager(transition=WipeTransition())
        b = Button(text='Hello world', font_size=10)
        m.main_screen.ids.grid.add_widget(b)
        return m


if __name__ == '__main__':
    MagicStalkApp().run()

