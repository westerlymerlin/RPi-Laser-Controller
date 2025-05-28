# Contents for: laserclass

* [laserclass](#laserclass)
  * [os](#laserclass.os)
  * [Timer](#laserclass.Timer)
  * [serial](#laserclass.serial)
  * [GPIO](#laserclass.GPIO)
  * [settings](#laserclass.settings)
  * [writesettings](#laserclass.writesettings)
  * [logger](#laserclass.logger)
  * [LaserClass](#laserclass.LaserClass)
    * [\_\_init\_\_](#laserclass.LaserClass.__init__)
    * [getstatus](#laserclass.LaserClass.getstatus)
    * [httpstatus](#laserclass.LaserClass.httpstatus)
    * [setpower](#laserclass.LaserClass.setpower)
    * [setmaxtimeout](#laserclass.LaserClass.setmaxtimeout)
    * [parsecontrol](#laserclass.LaserClass.parsecontrol)
    * [alarmstatus](#laserclass.LaserClass.alarmstatus)
    * [laserstatus](#laserclass.LaserClass.laserstatus)
    * [laser](#laserclass.LaserClass.laser)
    * [reboot](#laserclass.LaserClass.reboot)
  * [laser](#laserclass.laser)

<a id="laserclass"></a>

# laserclass

Laser Class - manages the laser via a TTL signal and serial connections

<a id="laserclass.os"></a>

## os

<a id="laserclass.Timer"></a>

## Timer

<a id="laserclass.serial"></a>

## serial

<a id="laserclass.GPIO"></a>

## GPIO

<a id="laserclass.settings"></a>

## settings

<a id="laserclass.writesettings"></a>

## writesettings

<a id="laserclass.logger"></a>

## logger

<a id="laserclass.LaserClass"></a>

## LaserClass Objects

```python
class LaserClass()
```

LaserClass

<a id="laserclass.LaserClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="laserclass.LaserClass.getstatus"></a>

#### getstatus

```python
def getstatus()
```

Query the laser via the serial port and return the control register values

<a id="laserclass.LaserClass.httpstatus"></a>

#### httpstatus

```python
def httpstatus()
```

Return the status (firning), power and timeout values, is called via the web page

<a id="laserclass.LaserClass.setpower"></a>

#### setpower

```python
def setpower(laserpower)
```

Set the laser power via the serial connection

<a id="laserclass.LaserClass.setmaxtimeout"></a>

#### setmaxtimeout

```python
def setmaxtimeout(maxtime)
```

API call to set the maximum time that the laser can run

<a id="laserclass.LaserClass.parsecontrol"></a>

#### parsecontrol

```python
def parsecontrol(item, command)
```

Main API entrypoint, recieves an **item** and **command** parameter

<a id="laserclass.LaserClass.alarmstatus"></a>

#### alarmstatus

```python
def alarmstatus()
```

Return the laser (firing) status, power setting and alert status

<a id="laserclass.LaserClass.laserstatus"></a>

#### laserstatus

```python
def laserstatus()
```

Return the laser (firning) status and the power setting

<a id="laserclass.LaserClass.laser"></a>

#### laser

```python
def laser(state)
```

Switch on or off the laser, if laser is on then run a thread to switch off if max time is exceeded

<a id="laserclass.LaserClass.reboot"></a>

#### reboot

```python
def reboot()
```

API call to reboot the Raspberry Pi

<a id="laserclass.laser"></a>

#### laser

