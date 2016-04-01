from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from threading import Thread
import serial


class Flower:

    obj_cur_mst = ObjectProperty(None)
    obj_cur_temp = ObjectProperty(None)
    obj_adj_mst = ObjectProperty(None)
    obj_avg_mst = ObjectProperty(None)

    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.val = ''
        self.command = ''
        self.sp = serial.Serial(self.port, baudrate=38400)

    def listener(self):
        c = ""
        while True:
            if c.isalpha():
                self.command = c
                num = ''
                c = str(self.sp.read(), encoding='UTF-8')
                print(c)
                while c.isdigit():
                    num += c
                    c = str(self.sp.read(), encoding='UTF-8')
                    print(c)
                if num.__sizeof__() > 0:
                    self.val = num
                    if self.command == 'A':
                        self.obj_avg_mst.text = self.val
                    elif self.command == 'M':
                        self.obj_cur_mst.text = self.val
                    elif self.command == 'T':
                        self.obj_cur_temp.text = self.val
                    elif self.command == 'C':
                        self.obj_adj_mst.text = self.val
                    else:
                        pass
            else:
                c = str(self.sp.read(), encoding='UTF-8')
                print(c)


class FlowerList:

    def __init__(self):
        self.flower_list = []

    def add_flower(self, name, port):
        flower = Flower(self, name, port)
        self.flower_list += flower
        flower.run()


class RootWidget(GridLayout):
    pass


class MagicStalkApp(App):

    def build(self):
        f = Flower('drosera', '/dev/ttyUSB1')
        t = Thread(target=f.listener)
        t.start()
        return RootWidget(cols=2)

if __name__ == '__main__':
    MagicStalkApp().run()

