from interface import AvrParser
from magicfiles import MagicFileWriter
from magicerror import MagicError
from json import dumps, loads
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
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
        self.port_list = populate_ports()
        super(FlowerScreen, self).__init__(**kwargs)

    def on_delete_flower(self, ins, val):
        self.delete_flower = True


class Flower:
    """
    flower class to keep single sensor group and flower data
    """
    def __init__(self, my_manager, **kwargs):
        # super(Flower, self).__init__(**kwargs)

        self.my_manager = my_manager

        self.name = kwargs['name']
        self._listen = None
        self._f = None
        self.scr = FlowerScreen(name=self.name)
        self.scr.bind(delete_flower=self.delete_this_flower)
        self.scr.bind(chosen_port=self.connect_flower_to_sensor)
        self.port = kwargs['port']
        self.but = self.add_button_to_main()

    def connect_flower_to_sensor(self, ins, val):
        print('port in Flower = ' + val)
        self.port = val
        self.scr.chosen_port = val
        if self.port != 'None':
            self._f = MagicFileWriter(self.name)
            self._listen = AvrParser(name=self.name, port=self.port)
            self._listen.bind(result=self.listener)  # result is ListProperty in Flower

    def delete_this_flower(self, ins, val):
        self.name = ''
        self.port = 'None'
        self.scr.remove_widget(self.but)
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
            self.scr.avg_mst.text = val[1]
        elif val[0] == 'M':
            self.scr.cur_mst.text = val[1]
        elif val[0] == 'T':
            self.scr.cur_temp.text = val[1]
        elif val[0] == 'C':
            self.scr.adj_mst.text = val[1]
            self._f.write_serial_line(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d, %H:%M, '))
            self._f.write_serial_line(
                        self.scr.cur_temp.text, ', ',
                        self.scr.avg_mst.text, ', ',
                        self.scr.cur_mst.text, '\n')

    def add_button_to_main(self):
        b = Button(text=self.name, size_hint=(0.2, 0.2))
        b.bind(on_release=self.bind_screen_button)
        self.my_manager.main_screen.ids.stack.add_widget(b)
        self.scr.ids.text_input.text = self.name
        self.scr.ids.text_input.readonly = True
        self.my_manager.add_widget(self.scr)
        return b

    def bind_screen_button(self, val):
        self.my_manager.current = val.text

    def set_button(self, b):
        self.but = b

    def get_button(self, b):
        return self.but

    def dump_flower(self):
        return {'name': self.name, 'port': self.port}


class FlowerManager:
    """ List of flowers, on main screen
    """
    DATA = 'data/all.json'

    def __init__(self, my_manager):
        self.flower_list = []
        self.my_mgr = my_manager
        self.get_flower_list()

    def add_flower(self, **kwargs):
        """ add flower to the list """
        f = Flower(self.my_mgr, **kwargs)
        self.flower_list.append(f)
        self.write_list_to_file()
        return f

    def remove_flower(self, fl):
        """ remove flower from the list
        :param fl: flower object
        :return:  none
        """
        self.flower_list.remove(fl)
        del fl
        self.write_list_to_file()

    def write_list_to_file(self):
        d = os.path.dirname(self.DATA)
        try:
            os.stat(d)
        except:
            os.mkdir(d)
        # try:
        with open(self.DATA, 'w') as f:
            f.write(dumps(self.create_flower_list()))
        # except:
        #     MagicError('cannot open file '+self.DATA)

    def get_flower_list(self):
        # try:
        with open(self.DATA) as f:
            json_data = f.read()
        self.load_flowers(loads(json_data))
        #     print(loads(json_data))
        #     self.load_flowers(loads(json_data))
        # except:
        #     self.flower_list = []

    def create_flower_list(self):
        return [i.dump_flower() for i in self.flower_list]

    def load_flowers(self, data):
        x = [self.add_flower(name=i['name'], port=i['port']) for i in data]
        return x


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

