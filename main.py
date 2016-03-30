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
        try:
            self.sp = serial.Serial(self.port, 38400, timeout=30)
        except:
            print('Error: no port')

    def run(self):
        while True:
            if c.isaplha():
                self.command = c
                num = ''
                c = self.sp.read()
                while c.isdigit():
                    num += c
                    c = self.sp.read()
                if num.__sizeof__() > 0:
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
            else:
                c = self.sp.read()


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

