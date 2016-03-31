from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from threading import Thread
import serial


class Flower(GridLayout):

    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.val = ''
        self.command = ''
        self.sp = serial.Serial(self.port, baudrate=38400)
        super(Flower, self).__init__(cols=2)

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
                        self.ids.avg_mst.text = self.val
                    elif self.command == 'M':
                        self.ids.cur_mst.text = self.val
                    elif self.command == 'T':
                        self.ids.cur_temp.text = self.val
                    elif self.command == 'C':
                        self.ids.adj_mst.text = self.val
                    else:
                        pass
            else:
                c = str(self.sp.read(), encoding='UTF-8')
                print(c)

    def run(self):
        try:
            t = Thread(target=self.listener())
            t.start()
        except:
            print("Error: unable to start thread")


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

    #f = Flower('drosera', '/dev/ttyUSB1')

    def build(self):
        return RootWidget(cols=2)


if __name__ == '__main__':
    MagicStalkApp().run()

