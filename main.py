from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from interface import AvrParser
from magicfiles import MagicFileWriter


class Flower(GridLayout):

    name = ''
    port = ''

    obj_cur_mst = ObjectProperty(None)
    obj_cur_temp = ObjectProperty(None)
    obj_adj_mst = ObjectProperty(None)
    obj_avg_mst = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Flower, self).__init__()
        self.cols = kwargs['cols']
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


class FlowerList:

    def __init__(self):
        self.flower_list = []

    def add_flower(self, name, port):
        """ creates a new flower in the list
        :param name: name of flower
        :param port: USB port or future UDP port
        """
        self.flower_list += Flower(self, name, port)


class MagicStalkApp(App):
    """ main app, will change - create a list and main screen
    """
    def build(self):
        return Flower(cols=2, name='drosera', port='/dev/ttyUSB1')


if __name__ == '__main__':
    MagicStalkApp().run()

