"""
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.
"""
import random
import json
from datetime import datetime

VERSION = '2.1.0'


def initialise():
    """These are the default values written to the settings.json file the first time the app is run"""
    isettings = {'LastSave': '01/01/2000 00:00:01',
                 'app-name': 'UCL Helium Line Laser Controller',
                 'api-key': 'change-me',
                 'logfilepath': './logs/lasercontrol.log',
                 'logappname': 'LaserControler-Py',
                 'loglevel': 'INFO',
                 'gunicornpath': './logs/',
                 'cputemp': '/sys/class/thermal/thermal_zone0/temp',
                 'port': '/dev/ttyS0',
                 'baud': 9600,
                 'power': 30,
                 'maxtime': 300}
    return isettings


def generate_api_key(key_len):
    """generate a new api key"""
    allowed_characters = "ABCDEFGHJKLMNPQRSTUVWXYZ-+~abcdefghijkmnopqrstuvwxyz123456789"
    return ''.join(random.choice(allowed_characters) for _ in range(key_len))


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
    settingschanged = False
    fsettings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = fsettings[item]
        except KeyError:
            print('settings[%s] Not found in json file using default' % item)
            settingschanged = True
    if settings['api-key'] == 'change-me':
        settings['api-key'] = generate_api_key(30)
        settingschanged = True
    if settingschanged:
        writesettings()


settings = initialise()
loadsettings()
