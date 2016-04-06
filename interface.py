import serial
from threading import Thread
from kivy.properties import ListProperty
from kivy.event import EventDispatcher
from magicerror import MagicError


class SerialInterface:
    """ serial interface opener """
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.port = kwargs['port']
        try:
            if self.port != 'None':
                self.sp = serial.Serial(self.port, baudrate=38400)
        except serial.serialutil.SerialException:
            MagicError('Could not open port')
            self.port = 'None'
        except Exception as e:
            MagicError('Problem with port: '+self.port)

    def read_char(self):
        try:
            c = str(self.sp.read(), encoding='UTF-8')
            return c
        except Exception as e:
            MagicError('cannot read from port: '+self.port)
            return ''

    def write_char(self, c):
        try:
            str(self.sp.write(c), encoding='UTF-8')
        except Exception as e:
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
        except Exception as e:
            MagicError('Thread failed')
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


