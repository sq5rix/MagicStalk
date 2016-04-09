from interface import AvrParser
from magicfiles import MagicFileWriter
from magicerror import MagicError
from json import dumps, loads
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
import interface
import os
import datetime


class FlowerScreen(Screen):
    """ screen with detailed flower data, connected, or small
    """
    delete_flower = BooleanProperty(False)  # simple flag to delete object
    port_list = ListProperty()
    chosen_port = StringProperty()

    cur_mst = ObjectProperty(None)
    cur_temp = ObjectProperty(None)
    adj_mst = ObjectProperty(None)
    avg_mst = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FlowerScreen, self).__init__(**kwargs)
        self.port_list = populate_ports()
        # FlowerList.add_flower()

    def on_delete_flower(self, ins, val):
        self.delete_flower = True


class Flower(FlowerScreen):
    """
    flower class to keep single sensor group and flower data
    """
    def __init__(self, **kwargs):
        super(Flower, self).__init__()
        self._f = None
        self._listen = None
        self.name = kwargs['name']
        self.port = kwargs['port']
        self.scr = ObjectProperty(None)
        self.but = ObjectProperty(None)
        self.bind(chosen_port=self.connect_flower_to_sensor)
        self.bind(delete_flower=self.delete_this_flower)

    def connect_flower_to_sensor(self, ins, val):
        print('port in Flower = ' + val)
        self.port = val
        if self.port != 'None':
            self._f = MagicFileWriter(self.name)
            self._listen = AvrParser(name=self.name, port=self.port)
            self._listen.bind(result=self.listener)  # result is ListProperty in Flower

    def delete_this_flower(self, ins, val):
        self.name = ''
        self.port = 'None'
        self.remove_widget(self.but)
        if self._f:
            self._f.remove()
        if self._listen:
            self._listen.remove()

    def listener(self, _, val):
        """ push data from serial port to flower display
        :param _: ignored
        :param val: value from sensor
        :return: none
        """
        if val[0] == 'A':
            self.avg_mst.text = val[1]
        elif val[0] == 'M':
            self.cur_mst.text = val[1]
        elif val[0] == 'T':
            self.cur_temp.text = val[1]
        elif val[0] == 'C':
            self.adj_mst.text = val[1]
            self._f.write_serial_line(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d, %H:%M, '))
            self._f.write_serial_line(
                        self.cur_temp.text, ', ',
                        self.avg_mst.text, ', ',
                        self.cur_mst.text, '\n')

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

    def add_flower(self, f):
        """ add flower to the list """
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
            with open('data/all.json') as f:
                json_data = f.read()
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


def populate_ports():
    x = interface.list_serial_ports()
    x.append('None')
    return x


def dump_kwargs(**kwargs):
    _dict = {}
    for i in kwargs:
        _dict[i] = kwargs[i]
    return _dict


def get_dict_from_key(d, name):
    _dict = d.get(name)
    return _dict

