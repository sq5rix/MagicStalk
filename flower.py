from interface import AvrParser
from magicfiles import MagicFileWriter
from magicerror import MagicError
from json import dumps, loads
from kivy.properties import ObjectProperty
import os


class Flower:
    """
    flower class to keep single sensor group and flower data
    """
    def __init__(self, **kwargs):
        self._f = None
        self._listen = None
        self.param_dict = {}
        self.update_flower(**kwargs)
        self.scr = ObjectProperty(None)
        self.but = ObjectProperty(None)

    def update_flower(self, **kwargs):
        self.param_dict = {}
        for i in kwargs:
            self.param_dict[i] = kwargs[i]
        if self.param_dict['port'] != 'None':
            self._f = MagicFileWriter(self.name)
            self._listen = AvrParser(name=self.name, port=self.port)
            self._listen.bind(result=self.listener)  # result is ListProperty in Flower
        else:
            if self._f is None :
                self._listen.remove()
                self._f.remove()
        return self.param_dict

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

    def set_screen(self, b):
        self.scr = b

    def get_screen(self):
        return self.scr

    def set_button(self, b):
        self.but = b

    def get_button(self, b):
        return self.but


class FlowerList:
    """ List of flowers, on main screen
    """
    def __init__(self):
        self.flower_list = []
        self.get_list()

    def add_flower(self, **kwargs):
        """ add flower to the list
        :param li: flower properties list
        :return:  none
        """
        self.flower_list.append(dump_kwargs(**kwargs))
        self.write_list_to_file()

    def remove_flower(self, name):
        """ remove flower from the list
        :param name: flower name
        :return:  none
        """
        self.flower_list.remove(get_dict_from_key(name))
        self.write_list_to_file()

    def write_list_to_file(self):
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

    def get_list(self):
        try:
            f = open('data/all.json')
            json_data = f.read()
            f.close()
            self.flower_list = loads(json_data)
        except:
            self.flower_list = []


def dump_kwargs(**kwargs):
    _dict = {}
    for i in kwargs:
        _dict[i] = kwargs[i]
    return _dict


def get_dict_from_key(d, name):
    _dict = d.get(name)
    return _dict

