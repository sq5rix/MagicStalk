from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.uix.button import Button
from flower import FlowerList
import interface


class MainScreen(Screen):
    pass


class FlowerScreen(Screen):
    """ screen with detailed flower data, connected, or small
    """
    obj_cur_mst = ObjectProperty(None)
    obj_cur_temp = ObjectProperty(None)
    obj_adj_mst = ObjectProperty(None)
    obj_avg_mst = ObjectProperty(None)
    port_list = ListProperty()
    chosen_port = StringProperty()

    def populate_ports(self):
        self.port_list = interface.list_serial_ports()
        self.port_list.append('None')
        print(self.port_list)

    def on_chosen_port(self, ins, val):
        pass


class Manager(ScreenManager):

    main_screen = ObjectProperty(None)
    flower_screen = ObjectProperty(None)
    flower_name = StringProperty('')

    main_flower_list = FlowerList()

    def add_button_to_main(self, data):
        b = Button(name=data['name'], size_hint=(0.2, 0.2))
        b.bind(on_release=self.bind_screen_button)
        self.main_screen.ids.stack.add_widget(b)
        m = FlowerScreen(name=data['name'])
        m.populate_ports()
        self.add_widget(m)

    def remove_button_from_main(self, value):
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
        if nm == '':
            self.main_flower_list.remove_flower(nm)
            self.remove_button_from_main(nm)
        else:
            self.main_flower_list.add_flower(name=nm, port=None)
            self.add_button_to_main(nm)

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

