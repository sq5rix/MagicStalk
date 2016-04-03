import serial
from threading import Thread
from kivy.properties import ListProperty
from kivy.event import EventDispatcher
from magicerror import MagicError


class SerialInterface:
    """ serial interface opener """
    def __init__(self, name, port):
        self.name = name
        self.port = port
        try:
            self.sp = serial.Serial(self.port, baudrate=38400)
        except serial.serialutil.SerialException:
            MagicError('Could not open port')
            self.port = 'None'

    def read_char(self):
        try:
            c = str(self.sp.read(), encoding='UTF-8')
            return c
        except:
            MagicError('cannot read from port: '+self.port)
            return ''

    def write_char(self, c):
        try:
            str(self.sp.write(c), encoding='UTF-8')
        except:
            MagicError('cannot write to port: '+self.port)


class Parser(EventDispatcher):
    """ simple abstract parser - format 'X9292992 ', where X - any letter, any number follows """
    result = ListProperty(['', ''])

    def __init__(self, **kwargs):
        super(Parser, self).__init__(**kwargs)
        try:
            t = Thread(target=self.parse, name=kwargs['name'])
            t.daemon = True
            t.start()
            print(t.name)
        except:
            MagicError('cannot run thread: '+t.name)
        self.val = ''
        self.command = ''

    def parse(self):
        """ parse event on change will send command and value - abstract, works with interface """
        c = ''
        while True:
            if c.isalpha():
                self.command = c
                num = ''
                c = self.read_char()
                while c.isdigit():
                    num += c
                    c = self.read_char()
                if num.__sizeof__() > 0:
                    self.val = num
                    self.result = [self.command, self.val]
                    print(self.result)
                else:
                    pass
            else:
                c = self.read_char()


class AvrParser(Parser, SerialInterface):
    """ simple uart parser - format 'X9292992 ', where X - any letter, any number follows """
    pass

