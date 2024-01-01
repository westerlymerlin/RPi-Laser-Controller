"""
Laser Class - manages the laser via  TTL signal and serial connections
"""
# pylint: disable=E1101
import os
from threading import Timer
import serial  # From pyserial
from RPi import GPIO
from settings import VERSION, settings, writesettings
from logmanager import logger


class LaserClass:
    """LaserClass"""
    def __init__(self):
        self.port = serial.Serial()
        self.port.port = settings['port']
        self.port.baudrate = settings['baud']
        self.port.timeout = 0.5
        self.laserbytes = ['readwrite', 'power x 10', 'power x 1', 'power x 0.1', 'time 1000', 'time 100', 'time 10',
                           'time 1', 'time on 10', 'time on 1', 'time off 10', 'time off 1', 'cw mode', 'calibration',
                           'alarm', 'end']
        self.laserstate = 0
        logger.info('Initialising laser on port %s', self.port.port)
        try:
            self.port.open()
        except serial.serialutil.SerialException:
            logger.error("Laserclass error opening port %s", self.port.port)

    def getstatus(self):
        """Query the laser via the serial port and return the control register values"""
        lasermessage = bytearray(b'\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x33')
        try:
            self.port.write(bytes(lasermessage))
            databack = list(self.port.read(size=100))
            logger.info('Data returned from Laser = %s', databack)
            if len(databack) != 16:
                databack = [0] * 16
        except serial.serialutil.SerialException:
            logger.warning("Laserclass error writing to port %s", self.port.port)
            databack = [255] * 16
        logger.info('Laser status: %s', databack)
        return databack

    def httpstatus(self):
        """Return the status (firning), power and timeout values, is called via the web page"""
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
        """Set the laser power via the serial connection"""
        lasermessage = bytearray(b'\xaa\x00\x02\x05\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x33')
        lasermessage[2] = int(laserpower / 10)
        lasermessage[3] = int(laserpower - (int(laserpower / 10) * 10))
        logger.info('Laserclass Setting laser power to %s', settings['laser']['power'])
        try:
            self.port.write(bytes(lasermessage))
            settings['power'] = laserpower
            writesettings()
        except serial.serialutil.SerialException:
            logger.warning("Laserclass error writing to port %s", self.port.port)

    def setmaxtimeout(self, maxtime):
        """API call to set the maximum time that the laser can run"""
        settings['maxtime'] = maxtime
        logger.info('Changing Laser Maximum on time to %s seconds', maxtime)
        writesettings()

    def parsecontrol(self, item, command):
        """Main API entrypoint, recieves an **item** and **command** parameter"""
        # print('%s : %s' % (item, command))
        try:
            if item == 'laser':
                if command == 'on':
                    self.laser(1)
                    return self.laserstatus()
                self.laser(0)
                return self.laserstatus()
            if item == 'setlaserpower':
                self.setpower(command)
                return self.laserstatus()
            if item == 'laseralarm':
                return self.alarmstatus()
            if item == 'laserstatus':
                return self.laserstatus()
            if item == 'setlasertimeout':
                self.setmaxtimeout(command)
                return {'maxtime': settings['maxtime']}
            if item == 'restart':
                if command == 'pi':
                    logger.warning('Restart command recieved: system will restart in 15 seconds')
                    timerthread = Timer(15, self.reboot)
                    timerthread.start()
                    return self.laserstatus()
            return self.laserstatus()
        except ValueError:
            logger.warning('incorrect json message')
            return self.laserstatus()

    def alarmstatus(self):
        """Return the laser (firing) status, power setting and alert status"""
        return {'laser': self.laserstate, 'power': settings['power'], 'status': self.getstatus()[14]}

    def laserstatus(self):
        """Return the laser (firning) status and the power setting"""
        return {'laser': self.laserstate, 'power': settings['power']}

    def laser(self, state):
        """Switch on or off the laser, if laser is on then run a thread to switch off if max time is exceeded"""
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
        """API call to reboot the Raspberry Pi"""
        logger.warning('System is restarting now')
        os.system('sudo reboot')


logger.info("laser controller started")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, 0)
laser = LaserClass()
logger.info('Running version %s', VERSION)
logger.info("Laser controller ready")
