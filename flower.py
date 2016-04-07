from interface import AvrParser
from magicfiles import MagicFileWriter
from magicerror import MagicError
from json import dumps, loads
import os


class Flower:
    """
    flower class to keep single sensor group and flower data
    """
    def __init__(self, name, port):
        self.name = name
        self.port = port
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
        self.get_list()

    def get_list(self):
        try:
            f = open('data/all.json')
            json_data = f.read()
            f.close()
            self.flower_list = loads(json_data)
        except:
            self.flower_list = []

    def add_flower(self, name, port):
        """
        :param name: name of flower
        :param port: connection port, serial, TODO udp
        :param prop: button on screen property
        :return: none
        """
        self.flower_list.append([name, port])
        filename = "data/all.json"
        d = os.path.dirname(filename)
        try:
            os.stat(d)
        except:
            os.mkdir(d)
        try:
            f = open(filename, 'w')
            f.write(dumps(self.flower_list))
            f.close()
        except:
            MagicError('cannot open file')
