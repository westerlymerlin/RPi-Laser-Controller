"""
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.
"""
import json
from datetime import datetime

VERSION = '2.0.3'


def initialise():
    """These are the default values written to the settings.json file the first time the app is run"""
    isettings = {'LastSave': '01/01/2000 00:00:01',
                 'logfilepath': './logs/lasercontrol.log',
                 'logappname': 'LaserControler-Py',
                 'gunicornpath': './logs/',
                 'cputemp': '/sys/class/thermal/thermal_zone0/temp',
                 'port': '/dev/ttyS0',
                 'baud': 9600,
                 'power': 30,
                 'maxtime': 300}
    return isettings


def writesettings():
    """Write settings to a json file"""
    settings['LastSave'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open('settings.json', 'w', encoding='utf-8') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)

def readsettings():
    """Read the settings from the json file"""
    try:
        with open('settings.json', 'r', encoding='utf-8') as json_file:
            jsettings = json.load(json_file)
            return jsettings
    except FileNotFoundError:
        print('File not found')
        return {}

def loadsettings():
    """Takes the settings vairable from the initiqalise and replaces valuesa from the json file if they exist"""
    global settings
    settingschanged = 0
    fsettings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = fsettings[item]
        except KeyError:
            print('settings[%s] Not found in json file using default' % item)
            settingschanged = 1
    if settingschanged == 1:
        writesettings()


settings = initialise()
loadsettings()
