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


class Manager(ScreenManager):

    main_screen = ObjectProperty(None)
    flower_screen = ObjectProperty(None)
    flower_name = StringProperty('')
    main_flower_list = flower.FlowerList()

    def add_button_to_main(self, value):
        b = Button(text=value, size_hint=(0.2, 0.2))
        b.bind(on_release=self.bind_screen_button)
        self.main_screen.ids.stack.add_widget(b)
        self.add_widget(FlowerScreen(name=value))

    def populate_flower_list(self):
        for i in self.main_flower_list.flower_list:
            self.add_button_to_main(i[0])

    def on_flower_name(self, ins, value):
        self.main_flower_list.add_flower(value, None)
        self.add_button_to_main(value)

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

