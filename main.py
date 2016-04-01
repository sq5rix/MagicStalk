from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from threading import Thread
import serial


class RootWidget(GridLayout):
    obj_cur_mst = ObjectProperty(None)
    obj_cur_temp = ObjectProperty(None)
    obj_adj_mst = ObjectProperty(None)
    obj_avg_mst = ObjectProperty(None)


class Flower(GridLayout):

    name = ''
    port = ''
    val = ''
    command = ''
    sp = serial.Serial()

    obj_cur_mst = ObjectProperty(None)
    obj_cur_temp = ObjectProperty(None)
    obj_adj_mst = ObjectProperty(None)
    obj_avg_mst = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Flower, self).__init__()
        self.cols = kwargs['cols']
        self.name = kwargs['name']
        self.port = kwargs['port']
        self.sp = serial.Serial(self.port, baudrate=38400)
        t = Thread(target=self.listener)
        t.start()

    def listener(self):
        c = ""
        while True:
            if c.isalpha():
                self.command = c
                num = ''
                c = str(self.sp.read(), encoding='UTF-8')
                while c.isdigit():
                    num += c
                    c = str(self.sp.read(), encoding='UTF-8')
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


class FlowerList:

    def __init__(self):
        self.flower_list = []

    def add_flower(self, name, port):
        flower = Flower(self, name, port)
        self.flower_list += flower
        flower.run()


class MagicStalkApp(App):

    def build(self):
        return Flower(cols=2, name='drosera', port='/dev/ttyUSB1' )


if __name__ == '__main__':
    MagicStalkApp().run()

