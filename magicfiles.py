from magicerror import MagicError
import os


class MagicFileWriter:
    """ open, write and read files
    """
    def __init__(self, name):
        self.filename = "log/" + name + '.csv'
        d = os.path.dirname(self.filename)
        try:
            os.stat(d)
        except:
            os.mkdir(d)
        try:
            self.f = open(self.filename, 'a')
        except FileNotFoundError:
            MagicError('cannot open file')

    def write_serial_line(self, *args):
        """
        :param args: *args - any number of strings, will write with , at the end
        :return: none
        """
        try:
            self.f = open(self.filename, 'a')
        except:
            pass
        for i in args:
            self.f.write(i)
        self.f.flush()

