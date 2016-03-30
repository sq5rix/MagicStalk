from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import threading
import serial


class Flower(threading.Thread):

    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.val = ''
        self.command = ''

    def set_name(self, name):
        self.name = name

    def set_port(self, port):
        self.port = port

    def get_data(self):
        while True:
            c = sp.read()
            if c.isaplha():
                self.command = c
                num = ''
                c = sp.read()
                while c.isdigit():
                    num += c
                    c = sp.read()
                self.val = num
                if self.command == 'A':
                    MagicStalkLayout.ids('avg_mst').text = self.val
                elif self.command == 'M':
                    MagicStalkLayout.ids('cur_mst').text = self.val
                elif self.command == 'T':
                    MagicStalkLayout.ids('cur_temp').text = self.val
                elif self.command == 'C':
                    MagicStalkLayout.ids('adj_mst').text = self.val
                else:
                    pass

    def run(self):
        try:
            sp = serial.Serial(self.port, 38400, timeout=30)
            sp.flush()
            self.get_data(self)
        except:
            print('no connection on '+port)


class FlowerList(Flower):

    def __init__(self):
        self.flower_list = []

    def add_flower(self, name, port):
        flower = Flower(self, name, port)
        self.flower_list += flower
        flower.run()


class MagicStalkLayout(GridLayout):
    pass


class MagicStalkApp(App):
    def build(self):
        return MagicStalkLayout(cols=2)


if __name__ == '__main__':
    MagicStalkApp().run()

