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
            print('Error in port')

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


class AvrParser(SerialInterface):
    """ simple uart parser - format 'X9292992 ', where X - any letter, any number follows """
    result = ['', '']

    def __init__(self, **kwargs):
        super(AvrParser, self).__init__(**kwargs)
        try:
            t = Thread(target=self.parse, name='thread')
            t.start()
            print(t.name)
        except:
            pass
        self.val = ''
        self.command = ''

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
                    self.result = [self.command, self.val]
                    '''TODO how to pass args from here to kivy, Event !! '''
                else:
                    pass
            else:
                c = self.read()