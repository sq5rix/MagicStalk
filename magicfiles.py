from magicerror import MagicError


class MagicFileWriter:
    """ open, write and read files
    """
    def __init__(self, name):
        try:
            self.filename = name
            self.f = open(name, 'a')
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
