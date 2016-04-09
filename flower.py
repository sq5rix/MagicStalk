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
        self.name = kwargs['name']
        self.port = kwargs['port']
        self.scr = ObjectProperty(None)
        self.but = ObjectProperty(None)

    def update_flower(self):
        if self.port != 'None':
            self._f = MagicFileWriter(self.name)
            self._listen = AvrParser(name=self.name, port=self.port)
            self._listen.bind(result=self.listener)  # result is ListProperty in Flower
        else:
            if self._f is None :
                self._listen.remove()
                self._f.remove()
        return

    def listener(self, _, val):
        """ push data from serial port to flower display
        :param _: ignored
        :param val: value from sensor
        :return: none
        """
        if val[0] == 'A':
            self.scr.obj_avg_mst.text = val[1]
            self._f.write_serial_line(str(val[1]), ', ')
        elif val[0] == 'M':
            self.scr.obj_cur_mst.text = val[1]
        elif val[0] == 'T':
            self.scr.obj_cur_temp.text = val[1]
            self._f.write_serial_line(str(val[1]), ', ')
        elif val[0] == 'C':
            self.scr.obj_adj_mst.text = val[1]
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
        """ add flower to the list"""
        f = Flower(**kwargs)
        self.flower_list.append(f)
        self.write_list_to_file()
        return f

    def remove_flower(self, fl):
        """ remove flower from the list
        :param fl: flower object
        :return:  none
        """
        self.flower_list.remove(fl)
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
            f.write(dumps(self.save_flower_list()))
            f.close()
        except:
            MagicError('write_file_to_list: cannot open file')

    def get_list(self):
        try:
            f = open('data/all.json')
            json_data = f.read()
            f.close()
            self.load_flower_list(loads(json_data))
        except:
            self.flower_list = []

    def save_flower_list(self):
        l = []
        d = {}
        for i in self.flower_list:
            d['name'] = i.name
            d['port'] = i.port
            l.append(d)
        print(l)
        return l

    def load_flower_list(self, json_data):
        print(json_data)
        for i in json_data:
            self.flower_list.append(Flower(name=i['name'], port=i['port']))


def dump_kwargs(**kwargs):
    _dict = {}
    for i in kwargs:
        _dict[i] = kwargs[i]
    return _dict


def get_dict_from_key(d, name):
    _dict = d.get(name)
    return _dict

