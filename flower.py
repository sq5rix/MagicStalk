from interface import AvrParser
from magicfiles import MagicFileWriter


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
        self.flower_list += Flower(self, name=name, port=port)
        # Flower(cols=2, name='drosera', port='/dev/ttyUSB1')