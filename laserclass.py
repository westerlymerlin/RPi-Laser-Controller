"""
Laser Control Module - Manages laser hardware via TTL signals and serial communication

This module provides a comprehensive interface for controlling laser hardware on a
Raspberry Pi system. It handles serial communication protocols, TTL signal management,
power settings, and safety timeout features for laser operation.

The module:
- Manages laser state (on/off) via GPIO pins
- Communicates with laser hardware via serial port
- Provides safety features including automatic timeout
- Exposes HTTP endpoints for remote control and monitoring
- Maintains persistent configuration settings
- Implements comprehensive logging for operational traceability

Dependencies:
- RPi.GPIO: For controlling Raspberry Pi GPIO pins
- pyserial: For serial communication with laser hardware
- app_control: For settings management
- logmanager: For logging operations

Typical usage:
    from laserclass import laser

    # Check laser status
    status = laser.laserstatus()

    # Configure laser
    laser.setpower(50)  # Set to 50% power
    laser.setmaxtimeout(30)  # 30 second safety timeout

    # Control laser
    laser.laser(1)  # Turn on
    # ... operations ...
    laser.laser(0)  # Turn off
"""

# pylint: disable=E1101

import os
from threading import Timer
import serial  # From pyserial
from RPi import GPIO
from app_control import settings, writesettings
from logmanager import logger


class LaserClass:
    """
    Represents a Laser control interface through serial communication.

    This class provides methods to manage and control a laser device connected via
    a serial port. Functionality includes querying laser status, setting power
    levels, configuring timeout duration, as well as APIs for managing and
    interacting with the laser operational state. It is designed to integrate with
    external systems and APIs for real-time monitoring and control.

    Attributes:
        port: A `serial.Serial` object used for communicating with the laser
            over a serial connection.
        laserbytes: A list of strings representing control and status commands for
            the laser device.
        laserstate: An integer indicating the current state of the laser (on/off).
    """
    def __init__(self):
        self.port = serial.Serial()
        self.port.port = settings['port']
        self.port.baudrate = settings['baud']
        self.port.timeout = 0.5
        self.laserbytes = ['readwrite', 'power % x 100', 'power % x 10', 'power % x 1', 'time 1000', 'time 100', 'time 10',
                           'time 1', 'time on 10', 'time on 1', 'time off 10', 'time off 1', 'cw mode', 'calibration',
                           'alarm', 'end']
        self.laserstate = 0
        logger.info('Initialising laser on port %s', self.port.port)
        try:
            self.port.open()
        except serial.serialutil.SerialException:
            logger.error("Laserclass error opening port %s", self.port.port)

    def getstatus(self):
        """
        Sends a predefined message to a serial port to retrieve the status of a laser and processes its response.

        The method communicates with a laser device connected via a serial port. It sends a specific byte message,
        flushes the input buffer, reads the response, and logs the data returned. In case of communication failure,
        a fallback response is generated.

        Returns:
            list: A list of integers representing the laser's status message or a default error state in case of failure.
        """
        lasermessage = bytearray(b'\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x33')
        try:
            self.port.reset_input_buffer()
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
        """
        Returns the current HTTP status of the laser system.

        This method evaluates and formats the current status of the laser system
        into a structured list. The returned list includes the state of the laser,
        the configured power, and other key settings. Additionally, it retrieves
        the laser byte values and their associated statuses.

        Returns:
            list: A list containing the HTTP status for laser operations. Each
            entry in the list represents a specific setting or status category.

        Raises:
            This method does not explicitly raise any exceptions, but its
            behavior may depend on the internal state of the `self.laserstate`
            and `self.laserbytes` attributes, as well as on external function
            dependencies such as `settings` and `self.getstatus`.
        """
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
        """
        Sets the power level of the laser and communicates the new power setting to the hardware.

        The power level is specified as an integer and is encoded into a message sent to the laser.
        This method also updates the persisted settings and logs the operation.

        Args:
            laserpower (int): Desired power level of the laser as an integer.

        Raises:
            serial.serialutil.SerialException: If there is an error writing to the laser's
                communication port.
        """
        lasermessage = bytearray(b'\xaa\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x33')
        lasermessage[2] = int(laserpower / 10)
        lasermessage[3] = int(laserpower - (int(laserpower / 10) * 10))
        logger.info('Laserclass Setting laser power to %s', laserpower)
        logger.info('Laserclass Sending laser message %s', lasermessage)
        try:
            settings['power'] = laserpower
            writesettings()
            self.port.write(bytes(lasermessage))
        except serial.serialutil.SerialException:
            logger.warning("Laserclass error writing to port %s", self.port.port)

    def setmaxtimeout(self, maxtime):
        """
        Changes the maximum allowable timeout for the laser system.

        This method updates the configuration setting for the laser's maximum
        operational time before timeout, logging the change and applying
        it to the system configuration.

        Args:
            maxtime (int): The new maximum allowable time, in seconds, for the
                           laser to remain active before timeout.
        """
        settings['maxtime'] = maxtime
        logger.info('Changing Laser Maximum on time to %s seconds', maxtime)
        writesettings()

    def parsecontrol(self, item, command):
        """
        Handles the parsing and execution of laser-related commands.

        This method accepts an item and a command, then determines the
        appropriate action to perform based on the specified inputs.
        It controls various operations such as toggling the laser state,
        setting the laser power, updating the laser timeout, checking the
        laser alarm, fetching laser status, or restarting the system.

        Parameters:
            item (str): The control operation to perform. Expected values
                        include 'laser', 'setlaserpower', 'laseralarm',
                        'laserstatus', 'setlasertimeout', or 'restart'.
            command (Any): The associated command to execute for the specified
                           item. Its usage depends on the item's context, such
                           as 'on' or 'off' for 'laser', numerical values for
                           'setlaserpower', and system-specific values for restart.

        Returns:
            dict: A dictionary containing the current status of the laser or
                  other relevant information based on the operation performed.

        Raises:
            ValueError: If an invalid JSON message or command format is detected.

        Notes:
            If the specified item or command does not correspond to any predefined
            operation, the method returns the current laser status by default.
        """
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
        """
        Returns the current status of the alarm system.

        The method provides a dictionary containing the state of the
        laser, the power level retrieved from settings, and the current
        status derived from the system's status data.

        Returns:
            dict: A dictionary containing the following keys:
                - laser: The state of the laser as a value.
                - power: The current power level from settings.
                - status: A specific element from the system's status
                  retrieved by getstatus method.
        """
        return {'laser': self.laserstate, 'power': settings['power'], 'status': self.getstatus()[14]}

    def laserstatus(self):
        """
        Returns the status of the laser device and its associated power settings.

        This function retrieves the current state of the laser device and the power
        settings configured. It returns a dictionary containing the state of
        the laser and the power level.

        Returns:
            dict: A dictionary containing the current 'laser' state and 'power'
            level.
        """
        return {'laser': self.laserstate, 'power': settings['power']}

    def laser(self, state):
        """
        Controls the state of the laser and manages its automatic shutdown.

        If the laser is turned on, a timer is started to ensure the laser
        is automatically turned off after the maximum allowed time if not
        manually shut off. The laser can also be manually turned off.

        Parameters:
            state (int): The desired state of the laser. It can take the following values:
                - 1: Turns the laser on and starts the timer.
                - 2: Automatically shuts off the laser.
                - Any other value: Turns the laser off manually.
        """
        if state == 1:
            logger.info('Laser is on')
            self.laserstate = 1
            GPIO.output(16, 1)
            # Start a  timer for the laser, if the laser is not shutdown by PyMS then this timer will shut it down
            timerthread = Timer(settings['maxtime'], lambda: self.laser(2))
            timerthread.name = 'laser-off-timer-thread'
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
        """
        Alerts about a system restart and triggers the reboot process.

        The function logs a warning message indicating that the system is restarting.
        It then executes the system command to initiate a restart.

        Raises:
            This function does not raise any manual exceptions but performs a system
            command that may fail depending on system configuration, permissions, or
            execution environment.
        """
        logger.warning('System is restarting now')
        os.system('sudo reboot')


logger.info("laser controller started")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, 0)
laser = LaserClass()
logger.info("Laser controller ready")
