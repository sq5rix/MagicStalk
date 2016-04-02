import serial
from threading import Thread


class SerialInterface:
    """ serial interface opener """
    def __init__(self, name, port):
        self.name = name
        self.port = port
        try:
            self.sp = serial.Serial(self.port, baudrate=38400)
        except:
            pass

    def read(self):
        try:
            c = str(self.sp.read(), encoding='UTF-8')
            return c
        except:
            return ''

    def write(self, c):
        try:
            str(self.sp.write(c), encoding='UTF-8')
        except:
            pass


class Parser(SerialInterface):
    """ simple uart parser - format 'X9292992 ', where X - any letter, any number follows """
    val = ''
    command = ''

    def __init__(self, **kwargs):
        super(Parser, self).__init__(**kwargs)
        try:
            t = Thread(target=self.listener)
            t.start()
        except:
            pass

    def parse(self):
        """ parse, event on change will send command and value """
        c = ''
        while True:
            if c.isalpha():
                self.command = c
                num = ''
                c = self.read()
                while c.isdigit():
                    num += c
                    c = self.read()
                if num.__sizeof__() > 0:
                    self.val = num
                    '''TODO how to pass args from here to kivy, Event !! '''
                else:
                    pass
            else:
                c = self.read()