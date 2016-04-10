from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from flower import FlowerManager


class Manager(ScreenManager):

    main_screen = ObjectProperty(None)
    flower_screen = ObjectProperty(None)
    flower_name = StringProperty('')

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.main_flower_list = FlowerManager(self)

    def on_flower_name(self, ins, nm):
        """ Event - on creating new flower
        :param ins: manager name
        :param nm: ignored
        :return: none
        """
        self.main_flower_list.add_flower(name=nm)


class MagicStalkApp(App):
    """ main app, will change - create a list and main screen
    """
    def build(self):
        self.title = 'MagicStalk'
        m = Manager(transition=WipeTransition())
        return m


if __name__ == '__main__':
    MagicStalkApp().run()

