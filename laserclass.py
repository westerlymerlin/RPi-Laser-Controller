import serial
from RPi import GPIO
import os
from settings import version, settings, writesettings
from logmanager import logger
from threading import Timer


class LaserClass:
    def __init__(self):
        self.port = serial.Serial()
        self.port.port = settings['port']
        self.port.baudrate = settings['baud']
        self.port.timeout = 0.5
        self.laserbytes = ['readwrite', 'power x 10', 'power x 1', 'power x 0.1', 'time 1000', 'time 100', 'time 10',
                           'time 1', 'time on 10', 'time on 1', 'time off 10', 'time off 1', 'cw mode', 'calibration',
                           'alarm', 'end']
        self.laserstate = 0
        logger.info('Initialising laser on port %s' % self.port.port)
        try:
            self.port.open()
        except serial.serialutil.SerialException:
            logger.error("Laserclass error opening port %s" % self.port.port)

    def getstatus(self):
        lasermessage = bytearray(b'\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x33')
        try:
            self.port.write(bytes(lasermessage))
            databack = list(self.port.read(size=100))
            logger.info('Data returned from Laser = %s' % databack)
            if len(databack) != 16:
                databack = [0] * 16
        except serial.serialutil.SerialException:
            logger.warning("Laserclass error writing to port %s" % self.port.port)
            databack = [255] * 16
        logger.info('Laser status: %s' % databack)
        return databack

    def httpstatus(self):
        httpreturn = [['laser firing', self.laserstate], ['laser power', settings['power']],
                      ['Laser Timeout (s)', settings['maxtime']]]
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
        logger.info('Laserclass Setting laser power to %s%%' % settings['laser']['power'])
        try:
            self.port.write(bytes(lasermessage))
            settings['power'] = laserpower
            writesettings()
        except serial.serialutil.SerialException:
            logger.warning("Laserclass error writing to port %s" % self.port.port)

    def setmaxtimeout(self, maxtime):
        settings['maxtime'] = maxtime
        logger.info('Changing Laser Maximum on time to %s seconds' % maxtime)
        writesettings()

    def parsecontrol(self, item, command):
        # print('%s : %s' % (item, command))
        try:
            if item == 'laser':
                if command == 'on':
                    self.laser(1)
                    return self.laserstatus()
                else:
                    self.laser(0)
                    return self.laserstatus()
            elif item == 'setlaserpower':
                self.setpower(command)
                return self.laserstatus()
            elif item == 'laseralarm':
                return self.alarmstatus()
            elif item == 'laserstatus':
                return self.laserstatus()
            elif item == 'setlasertimeout':
                self.setmaxtimeout(command)
                return {'maxtime': settings['maxtime']}
            elif item == 'restart':
                if command == 'pi':
                    logger.warning('Restart command recieved: system will restart in 15 seconds')
                    timerthread = Timer(15, self.reboot)
                    timerthread.start()
                    return self.laserstatus()
            else:
                return self.laserstatus()
        except ValueError:
            logger.warning('incorrect json message')
            return self.laserstatus()

    def alarmstatus(self):
        return {'laser': self.laserstate, 'power': settings['power'], 'status': self.getstatus()[14]}

    def laserstatus(self):
        return {'laser': self.laserstate, 'power': settings['power']}

    def laser(self, state):
        if state == 1:
            logger.info('Laser is on')
            self.laserstate = 1
            GPIO.output(16, 1)
            # Start a  timer for the laser, if the laser is not shutdown by PyMS then this timer will shut it down
            timerthread = Timer(settings['maxtime'], lambda: self.laser(2))
            timerthread.start()
        elif state == 2:
            logger.info('Laser Auto shut off')
            self.laserstate = 0
            GPIO.output(16, 0)
        else:
            logger.info('Laser is off')
            self.laserstate = 0
            GPIO.output(16, 0)

    def reboot(self):
        logger.warning('System is restarting now')
        os.system('sudo reboot')


logger.info("laser controller started")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, 0)
laser = LaserClass()
logger.info('Running version %s' % version)
logger.info("Laser controller ready")
