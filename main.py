from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.uix.button import Button
from flower import FlowerList, Flower


class MainScreen(Screen):
    pass


class Manager(ScreenManager):

    main_screen = ObjectProperty(None)
    flower_screen = ObjectProperty(None)
    flower_name = StringProperty('')

    main_flower_list = FlowerList()

    def add_button_to_main(self, f):
        b = Button(text=f.name, size_hint=(0.2, 0.2))
        b.bind(on_release=self.bind_screen_button)
        self.main_screen.ids.stack.add_widget(b)
        f.populate_ports()
        f.set_button(b)
        self.main_flower_list.add_flower(f)
        self.add_widget(f)

    def remove_button_from_main(self, data):
        pass

    def populate_flower_list(self):
        for i in self.main_flower_list.flower_list:
            self.add_button_to_main(i)

    def on_flower_name(self, ins, nm):
        """ Event - on creating new flower
        :param ins: ignored
        :param nm: name of newly created screen
        :return: none
        """
        f = Flower(name=nm, port=None)
        self.add_button_to_main(f)

    def bind_screen_button(self, ins):
        self.current = ins.text
        self.current_screen.ids.text_input.text = ins.text
        self.current_screen.ids.text_input.readonly = True


class MagicStalkApp(App):
    """ main app, will change - create a list and main screen
    """
    def build(self):
        self.title = 'MagicStalk'
        m = Manager(transition=WipeTransition())
        m.populate_flower_list()
        return m


if __name__ == '__main__':
    MagicStalkApp().run()

