from threading import Thread, Event
from kivy.properties import ListProperty
from kivy.event import EventDispatcher
from magicerror import MagicError
import sys
import glob
import serial


def list_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class SerialInterface:
    """ serial interface connect and read/write """
    def __init__(self, **kwargs):

        self.name = kwargs['name']
        self.port = kwargs['port']

        print('serial name: ' + self.name)
        print('serial port: ' + self.port)

        try:
            if self.port.lower() != 'none':
                self.sp = serial.Serial(self.port, baudrate=38400)
            elif self.sp.is_open():
                self.sp.close()
        except serial.serialutil.SerialException:
            MagicError('Could not open port')
            self.port = 'None'
        except Exception as e:
            MagicError('Problem with port: '+self.port)

    def read_char(self):
        try:
            c = str(self.sp.read(), encoding='UTF-8')
            return c
        except:
            MagicError('very bad: '+self.port)
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
            self._t = Thread(target=self.parse, name=kwargs['name'])
            self._t.daemon = True
            self._t.start()
            self._stop = Event()
            print('new thread name = ' + self._t.name)
        except Exception as e:
            MagicError('Thread failed')
        finally:
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

    def remove(self):
        self._stop.set()


class AvrParser(Parser, SerialInterface):
    """ simple uart parser - format 'X9292992 ', where X - any letter, any number follows """


