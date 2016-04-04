from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from interface import AvrParser
from magicfiles import MagicFileWriter
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition


class Flower:

    def __init__(self, **kwargs):
        # self.cols = kwargs['cols']
        self.name = kwargs['name']
        self.port = kwargs['port']
        self._f = MagicFileWriter(self.name)
        self.listen = AvrParser(name=self.name, port=self.port)
        self.listen.bind(result=self.listener)  # result is ListProperty in Flower

    def listener(self, _, val):
        if val[0] == 'A':
            self.obj_avg_mst.text = val[1]
            self._f.write_serial_line(str(val[1]), ', ')
        elif val[0] == 'M':
            self.obj_cur_mst.text = val[1]
        elif val[0] == 'T':
            self.obj_cur_temp.text = val[1]
            self._f.write_serial_line(str(val[1]), ', ')
        elif val[0] == 'C':
            self.obj_adj_mst.text = val[1]
            self._f.write_serial_line(str(val[1]), '\n' )
        else:
            pass


class FlowerScreen(Flower, Screen):
    """ screen with detailed flower data, connected, or small
    """
    def __init__(self, **kwargs):
        super(FlowerScreen, self).__init__(**kwargs)
        self.obj_cur_mst = ObjectProperty(None)
        self.obj_cur_temp = ObjectProperty(None)
        self.obj_adj_mst = ObjectProperty(None)
        self.obj_avg_mst = ObjectProperty(None)


class FlowerList:
    """ List of flowers, on main screen
    """
    def __init__(self):
        self.flower_list = []

    def add_flower(self, name, port):
        """ creates a new flower in the list
        :param name: name of flower
        :param port: USB port or future UDP port
        """
        self.flower_list += Flower(self, name, port)
        # Flower(cols=2, name='drosera', port='/dev/ttyUSB1')


class Manager(ScreenManager):
    def __init__(self):
        self.transition = WipeTransition()
        self.main_screen = ObjectProperty(None)
        self.flower_screen = ObjectProperty(None)
        self.settings_screen = ObjectProperty(None)


class MagicStalkApp(App):
    """ main app, will change - create a list and main screen
    """
    def build(self):
        return Manager()


if __name__ == '__main__':
    MagicStalkApp().run()

