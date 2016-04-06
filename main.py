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

    flower_name = StringProperty('')

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        # self.bind(flower_name=self._flower_name)
        print('init')

    def on_flower_name(self, instance, value):
        b = Button(text=self.flower_name, font_size=10)
        self.add_widget(b)
        print('action')


class Manager(ScreenManager):

    main_screen = ObjectProperty(None)
    flower_screen = ObjectProperty(None)
    settings_screen = ObjectProperty(None)


class MagicStalkApp(App):
    """ main app, will change - create a list and main screen
    """
    def build(self):
        m = Manager(transition=WipeTransition())
        return m


if __name__ == '__main__':
    MagicStalkApp().run()

