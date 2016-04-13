from abc import abstractmethod

import sys
import glob
import serial
import datetime

from threading import Thread, Event
from kivy.properties import ListProperty
from kivy.event import EventDispatcher

from magicfiles import MagicFileWriter
from magicerror import MagicError


class Parser(EventDispatcher):
    """ simple abstract parser - format 'X9292992 ', where X - any letter, any number follows """

    def __init__(self):
        super(Parser, self).__init__()


class SerialInterface(Parser):
    """ serial interface connect and read/write """

    BAUD_RATE = 38400
    result = ListProperty()

    def __init__(self, name):

        super(SerialInterface, self).__init__()

        self.name = name
        self.port = ''
        self.port_ok = False

        self.magic_file_handle = None
        self.serial_port_handle = None

        self._t = None
        self._stop = None

        self.val = ''
        self.command = ''

    def read_char(self):
        if not self.port_ok:
            return ' '
        for _ in range(10):
            try:
                c = str(self.serial_port_handle.read(), encoding='ascii')
                self.port_ok = True
                return c
            except:
                try:
                    print('retry port... ', self.port)
                    self.serial_port_handle.close()
                    self.serial_port_handle = serial.Serial(self.port, baudrate=self.BAUD_RATE)
                    self.serial_port_handle.flush()
                    self.port_ok = True
                except:
                    self.serial_port_handle.close()
                    self.port_ok = False

    def write_char(self, c):
        try:
            str(self.serial_port_handle.write(c), encoding='UTF-8')
        except serial.serialutil.SerialException:
            MagicError('cannot write to port: '+self.port)

    def parse(self):
        """ parse event on change will send command and value - abstract, works with interface """
        if not self.port_ok:
            return
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

    def start_thread(self, name):
        try:
            self._t = Thread(target=self.parse, name=name)
            self._t.daemon = True
            self._t.start()
            self._stop = Event()
            self.magic_file_handle = MagicFileWriter(self.name)
            print('new thread name = ' + self._t.name)
        except Exception as e:
            MagicError('Thread failed')

    def change_port(self, name):
        """ change communication port and start its thread
        :param name: port name
        """
        if self.check_port():
            self.port = name
            if self.check_port():
                self.open_port()
                self.start_thread(self.name)
            else:
                self.close_port()
                if self._t:
                    self.remove()

    def write_data_to_parser_file(self, *args):
        self.magic_file_handle.write_serial_line(*args)

    def open_port(self):
        if self.check_port():
            try:
                self.serial_port_handle = serial.Serial(self.port, baudrate=self.BAUD_RATE)
                self.serial_port_handle.flush()
                self.port_ok = True
            except serial.serialutil.SerialException:
                self.port_ok = False
                MagicError('Problem port: '+self.port)

    def close_port(self):
        try:
            if self.serial_port_handle:
                self.serial_port_handle.close()
        except serial.serialutil.SerialException:
            pass
        finally:
            self.port = 'None'
            self.port_ok = False

    def remove(self):
        self._stop.set()

    def check_port(self):
        return self.port != 'None'


class AvrParser(SerialInterface):
    """ simple uart parser - format 'X9292992 ', where X - any letter, any number follows """

    passed_value = ListProperty([])

    def __init__(self, name):
        super(AvrParser, self).__init__(name)
        self.passed_value = ['', '', '', '']

    def listener(self, _, val):
        """ push data from serial port to flower display
        :param val: what it passed?
        """
        if val[0] == 'M':
            self.passed_value[0] = str(val[1])
        elif val[0] == 'T':
            self.passed_value[1] = str(val[1])
        elif val[0] == 'A':
            self.passed_value[2] = str(val[1])
        elif val[0] == 'C':
            self.passed_value[3] = str(val[1])
            self.write_data_to_parser_file(
                datetime.datetime.strftime(
                    datetime.datetime.now(),
                    '%Y-%m-%d, %H:%M, '))
            self.write_data_to_parser_file(
                self.passed_value[1], ', ',
                self.passed_value[2], ', ',
                self.passed_value[3], '\n')


def populate_ports():
    port_list = list_serial_ports()
    port_list.append('None')
    return port_list


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


