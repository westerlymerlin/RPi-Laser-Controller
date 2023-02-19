import json

version = '1.2'
settings = {}


def writesettings():
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, ensure_ascii=True, sort_keys=True)


def initialise():
    global settings
    settings['logging'] = {}
    settings['logging']['logfilepath'] = './logs/pumpreader.log'
    settings['logging']['logappname'] = 'Pumpreader-Py'
    settings['logging']['gunicornpath'] = './logs/'
    settings['logging']['cputemp'] = '/sys/class/thermal/thermal_zone0/temp'
    settings['logging']['syslog'] = '/var/log/syslog'
    settings['laser'] = {}
    settings['laser']['port'] = '/dev/ttyS0'
    settings['laser']['baud'] = 9600
    settings['laser']['power'] = 30
    settings['laser']['maxtime'] = 300
    with open('settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4, ensure_ascii=True, sort_keys=True)


def readsettings():
    global settings
    try:
        with open('settings.json') as json_file:
            settings = json.load(json_file)
    except FileNotFoundError:
        initialise()


readsettings()
