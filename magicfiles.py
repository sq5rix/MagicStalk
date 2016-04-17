from magicerror import MagicError
import os
import csv


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


class MoistureGraph():

    def __init__(self, name):
        self.name = name
        self.last_hour = '00'

    @staticmethod
    def in_hour(time):
        return time.partition(':')[0]

    def get_moisture_from_file(self):
        # date, time, temp, moist, corr_moist
        mp = []
        with open('log/{}.csv'.format(self.name), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                mp += ([row[i].strip() for i in range(4)])
        elem = []
        e = index = 0
        while e < len(mp)-4:
            x = [mp[e+i] for i in range(4)]
            hour = self.in_hour(x[1])
            if (hour > self.last_hour) or (hour == '00'):
                elem += [index, int(x[3])]
                self.last_hour = hour
                index +=1
            e += 4
        return elem



