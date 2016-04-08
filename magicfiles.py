from magicerror import MagicError
import os


class MagicFileWriter:
    """ open, write and read files
    """
    def __init__(self, name):
        filename = "log/" + name
        d = os.path.dirname(self.filename)
        try:
            os.stat(d)
        except:
            os.mkdir(d)
        try:
            self.f = open(filename, 'a')
        except:
            MagicError('cannot open file')

    def write_serial_line(self, *args):
        """
        :param args: *args - any number of strings, will write with , at the end
        :return: none
        """
        if self.f.closed:
            try:
                self.f = open(self.filename, 'a')
            except:
                MagicError('cannot open file')
        for i in args:
            self.f.write(i)
            self.f.flush()

    def remove(self):
        self.f.close()

