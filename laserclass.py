import serial
from RPi import GPIO
from time import sleep
from settings import version, settings, writesettings
from logmanager import *
from threading import Timer


class LaserClass:
    def __init__(self):
        self.port = serial.Serial()
        self.port.port = settings['laser']['port']
        self.port.baudrate = settings['laser']['baud']
        self.port.timeout = 0.5
        self.laserbytes = ['readwrite', 'power x 10', 'power x 1', 'power x 0.1', 'time 1000', 'time 100', 'time 10',
                           'time 1', 'time on 10', 'time on 1', 'time off 10', 'time off 1', 'cw mode', 'calibration',
                           'alarm', 'end']
        self.laserstate = 0
        print('Initialising laser on port %s' % self.port.port)
        try:
            self.port.open()
        except serial.serialutil.SerialException:
            print("Laserclass error opening port %s" % self.port.port)

    def getstatus(self):
        lasermessage = bytearray(b'\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x33')
        try:
            self.port.write(bytes(lasermessage))
            databack = list(self.port.read(size=100))
            print('returned data = %s' % databack)
            if len(databack) != 16:
                databack = [0] * 16
        except serial.serialutil.SerialException:
            print("Laserclass error writing to port %s" % self.port.port)
            databack = [255] * 16
        print('Laser status: %s' % databack)
        return databack

    def httpstatus(self):
        httpreturn = [['laser firing', self.laserstate], ['laser power', settings['laser']['power']],
                      ['Laser Timeout (s)', settings['laser']['maxtime']]]
        lasersettings = self.getstatus()
        if lasersettings[0] == 0:
            lasersettings = ['Laser off'] * 16
        if lasersettings[0] == 255:
            lasersettings = ['Serial Port error'] * 16
        for i in range(16):
            httpreturn.append([self.laserbytes[i], lasersettings[i]])
        return httpreturn

    def setpower(self, laserpower):
        lasermessage = bytearray(b'\xaa\x00\x02\x05\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x33')
        lasermessage[2] = int(laserpower / 10)
        lasermessage[3] = int(laserpower - (int(laserpower / 10) * 10))
        print('Laserclass Setting laser power to %s%%' % settings['laser']['power'])
        try:
            self.port.write(bytes(lasermessage))
            settings['laser']['power'] = laserpower
            writesettings()
        except serial.serialutil.SerialException:
            print("Laserclass error writing to port %s" % self.port.port)

    def setmaxtimeout(self, maxtime):
        settings['laser']['maxtime'] = maxtime
        print('Changing Laser Maximum on time to %s seconds' % maxtime)
        writesettings()

    def parsecontrol(self, item, command):
        # print('%s : %s' % (item, command))
        try:
            if item == 'laser':
                if command == 'on':
                    self.laser(1)
                    return self.shortstatus()
                else:
                    self.laser(0)
                    return self.shortstatus()
            elif item == 'setlaserpower':
                self.setpower(command)
                return self.shortstatus()
            elif item == 'laserstate':
                return self.apistatus()
            elif item == 'setlasertimeout':
                self.setmaxtimeout(command)
                return {'maxtime': settings['laser']['maxtime']}
            else:
                return self.shortstatus()
        except ValueError:
            print('incorrect json message')
            return self.shortstatus()

    def apistatus(self):
        return {'laser': self.laserstate, 'power': settings['laser']['power'], 'status': self.getstatus()[14]}

    def shortstatus(self):
        return {'laser': self.laserstate, 'power': settings['laser']['power']}

    def laser(self, state):
        if state == 1:
            print('Laser is on')
            self.laserstate = 1
            GPIO.output(16, 1)
            # Start a  timer for the laser, if the laser is not shutdown by PyMS then this timer will shut it down
            timerthread = Timer(settings['laser']['maxtime'], lambda: self.laser(2))
            timerthread.start()
        elif state == 2:
            print('Laser Auto shut off')
            self.laserstate = 0
            GPIO.output(16, 0)
        else:
            print('Laser is off')
            self.laserstate = 0
            GPIO.output(16, 0)


print("laser controller started")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, 0)
laser = LaserClass()
print('Running version %s' % version)
print("Laser controller ready")
