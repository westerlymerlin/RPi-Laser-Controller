"""
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.
"""
import random
import json
from shutil import copyfile
from base64 import b64decode, b64encode
from datetime import datetime

VERSION = '2.2.0'


def initialise():
    """These are the default values written to the settings.json file the first time the app is run"""
    default_settings = {'LastSave': '01/01/2000 00:00:01',
                 'app-name': 'UCL Helium Line Laser Controller',
                 'api-key-date': '01/01/2000 00:00:01',
                 'logfilepath': './logs/lasercontrol.log',
                 'logappname': 'LaserControler-Py',
                 'loglevel': 'INFO',
                 'email_recipients': 'info@tstechnologies.co.uk',
                 'gunicornpath': './logs/',
                 'cputemp': '/sys/class/thermal/thermal_zone0/temp',
                 'port': '/dev/ttyS0',
                 'baud': 9600,
                 'power': 30,
                 'maxtime': 300}
    return default_settings


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
            return json.load(json_file)
    except FileNotFoundError:
        print('File not found')
        return {}


def load_settings():
    """Takes the settings variable from the initialise and replaces values from the json file if they exist"""
    global settings
    settings_changed = False
    default_settings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = default_settings[item]
        except KeyError:
            print('settings[%s] Not found in json file using default' % item)
            settings_changed = True
    if settings['api-key-date'] == '01/01/2000 00:00:01':  # Needs setting
        update_secret('api-key', generate_api_key(128))
        settings['api-key-date'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        settings_changed = True
    if settings_changed:
        writesettings()


def load_secrets():
    """
    Load secrets from a file and decode them.

    This function reads a file named 'SECRETS', decodes its contents using Base64,
    and then parses the resulting JSON. It is used to securely retrieve stored
    configuration or sensitive data. The file is expected to contain secrets
    encoded in a specific format.
    """
    with open('SECRETS', 'r', encoding='utf-8') as s_file:
        raw_secrets = s_file.read()
    s_file.close()
    return json.loads(b64decode(raw_secrets))


def update_secret(key, value):
    """
    Updates the secret storage by adding or updating a key-value pair. The method also creates a
    backup of the existing storage file before writing the updated encoded secrets back to the file.
    """
    global SECRETS
    SECRETS[key] = value
    new_secret = b64encode(json.dumps(SECRETS).encode('utf-8')).decode('utf-8')
    copyfile('SECRETS', 'SECRETS.bak')
    with open('SECRETS', 'w', encoding='utf-8') as s_file:
        s_file.write(new_secret)
    s_file.close()


SECRETS = load_secrets()
settings = initialise()
load_settings()
