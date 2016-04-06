from interface import AvrParser
from magicfiles import MagicFileWriter
from kivy.uix.screenmanager import Screen, ScreenManager


class Flower:
    """
    flower class to keep single sensor group and flower data
    """
    def __init__(self, name, port, prop):
        self.name = name
        self.port = port
        self.property = prop
        self._f = MagicFileWriter(self.name)
        self.listen = AvrParser(name=self.name, port=self.port)
        self.listen.bind(result=self.listener)  # result is ListProperty in Flower

    def listener(self, _, val):
        """ push data from serial port to flower display
        :param _: ignored
        :param val: value from sensor
        :return: none
        """
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

    def add_flower(self, name, port, prop):
        """
        :param name: name of flower
        :param port: connection port, serial, TODO udp
        :param prop: button on screen property
        :return: none
        """
        self.flower_list.append(Flower(name, port, prop))


# class FlowerScreen(FlowerList, Screen):
#
#     def add_set_flower(self):
#         pass
