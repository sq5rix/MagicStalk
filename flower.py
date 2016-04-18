from magicerror import MagicError
from json import dumps, loads
import os
import csv

from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.uix.widget import Widget

from interface import populate_ports
from interface import AvrParser


class FlowerScreen(Screen):
    """ screen with detailed flower data, connected, or small
    """
    port_list = ListProperty()
    chosen_port = StringProperty()
    delete_flower = BooleanProperty(False)  # simple flag to delete object

    def __init__(self, **kwargs):

        self.cur_mst = ObjectProperty(None)
        self.cur_temp = ObjectProperty(None)
        self.adj_mst = ObjectProperty(None)
        self.avg_mst = ObjectProperty(None)

        self.port_list = populate_ports()
        super(FlowerScreen, self).__init__(**kwargs)


class GraphWindow(Widget):

    grid_points = ListProperty([])

    def __init__(self, **kwargs):
        super(GraphWindow, self).__init__(**kwargs)
        self.last_hour = '00'
        self.name = 'orchid'
        self.line_elem = []
        self.time_elem = []
        l = []
        with self.canvas:
            for i in range(10):
                l += [self.pos[0]+1, int(self.pos[1]+i*self.size[1]/10),
                      self.width+1, int(self.pos[1]+i*self.size[1]/10)]
            self.grid_points = l

    @staticmethod
    def in_hour(time):
        return time.partition(':')[0]

    def get_moisture_from_file(self):
        # date, time, temp, moist, corr_moist
        # self.x, self.y, self.width, self.height
        mp = []
        self.line_elem = []
        self.time_elem = []
        with open('log/{}.csv'.format(self.name), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                mp += ([row[i].strip() for i in range(4)])
        e = index = day = 0
        while e < len(mp)-4:
            x = [mp[e+i] for i in range(4)]
            hour = self.in_hour(x[1])
            if (hour > self.last_hour) or (hour == '00'):
                if hour == '00':
                    day += 1
                self.line_elem += [self.pos[0]+index, self.pos[1]+self.height*int(x[3])/1000]
                self.time_elem += [day, hour]
                self.last_hour = hour
                index += 1
            e += 4


class Flower(FlowerScreen):
    """
    flower class to keep single sensor group and flower data
    """
    def __init__(self, my_manager, name, port):

        super(Flower, self).__init__()

        self.my_manager = my_manager
        self.name = name
        self.port = port

        self.small_label = ObjectProperty(None)
        self.anchor = ObjectProperty(None)
        self.but = ObjectProperty(None)

        if self.port == '':
            self.port = 'None'
        self.chosen_port = self.port
        self.ids.usb_port.text = self.chosen_port
        self.bind(chosen_port=self.connect_flower_to_sensor)
        self.bind(delete_flower=self.delete_this_flower)
        self.add_button_to_main()

        self.graph_window = GraphWindow()

        self.communicator = AvrParser(self.name)
        self.communicator.bind(result=self.communicator.listener)  # result from serial is ListProperty[command, val]
        self.communicator.bind(passed_value=self.on_passed_value)  # result from parser is ListProperty[M, T, A, C]
        self.communicator.change_port(self.port)

    def connect_flower_to_sensor(self, _, val):
        """ on event - change position in spinner - connect flower to sensor
        :param _: ignore
        :param val: port name
        """
        self.port = val
        self.communicator.change_port(val)
        self.my_manager.main_flower_list.write_list_to_file()

    def on_passed_value(self, _, val):
        self.ids.cur_mst.text = self.small_label.text = val[0]
        self.ids.cur_temp.text = val[1]
        self.ids.avg_mst.text = val[2]
        self.ids.adj_mst.text = val[3]

    def add_button_to_main(self):
        """
        adds a button so that it is in Layout, otherwise it is in the 0,0
        """
        self.anchor = AnchorLayout(id='anchor', size_hint=(0.2, 0.2))  # anchor in the stack layout in main screen
        self.my_manager.main_screen.ids.stack.add_widget(self.anchor)  # add anchor to manager.main_screen

        self.but = Button()
        self.but.bind(on_release=self.bind_screen_button)
        self.anchor.add_widget(self.but)

        box = BoxLayout(orientation='vertical')
        self.anchor.add_widget(box)
        box.add_widget(Label(text=self.name))
        self.small_label = Label(id='small_moisture', text=self.ids.cur_mst.text)
        box.add_widget(self.small_label)

        self.ids.text_input.text = self.name
        self.ids.usb_port.text = self.chosen_port
        self.ids.text_input.readonly = True
        self.my_manager.add_widget(self)

    def delete_this_flower(self, _, val):
        print('delete_this_flower: ', self.name)
        self.name = ''
        self.port = 'None'
        self.my_manager.main_screen.ids.stack.remove_widget(self.anchor)
        self.my_manager.remove_widget(self)
        self.my_manager.main_flower_list.remove_flower(self)
        self.my_manager.current = 'Main Screen'

    def bind_screen_button(self, _):
        self.my_manager.current = self.name

    def set_button(self, b):
        self.but = b

    def get_button(self):
        return self.but

    def dump_flower(self):
        return {'name': self.name, 'port': self.port}


class FlowerManager:
    """ List of flowers, on main screen
    """
    DATA = 'data/all.json'

    def __init__(self, my_manager):
        self.flower_list = []
        self.my_manager = my_manager  # creator of this object, normally a screen manager
        self.get_flower_list()  # get list from ini file

    def add_flower(self, **kwargs):
        """ add flower to the list """
        f = Flower(self.my_manager, **kwargs)
        self.flower_list.append(f)
        self.write_list_to_file()
        return f

    def remove_flower(self, fl):
        """ remove flower from the list
        :param fl: flower object
        """
        self.flower_list.remove(fl)
        del fl.but
        del fl
        self.write_list_to_file()

    def write_list_to_file(self):
        d = os.path.dirname(self.DATA)
        try:
            os.stat(d)
        except:
            os.mkdir(d)
        try:
            with open(self.DATA, 'w') as f:
                f.write(dumps(self.create_flower_list()))
        except FileNotFoundError:
            MagicError('cannot open file '+self.DATA)

    def get_flower_list(self):
        try:
            with open(self.DATA) as f:
                json_data = f.read()
            self.load_flowers(loads(json_data))
        except FileNotFoundError:
            self.flower_list = []

    def create_flower_list(self):
        return [i.dump_flower() for i in self.flower_list]

    def load_flowers(self, data):
        x = [self.add_flower(name=i['name'], port=i['port']) for i in data]
        return x
