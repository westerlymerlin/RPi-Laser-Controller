"""
Laser Controller Web Application

This Flask application provides a web interface and REST API for controlling
laser hardware. It includes status monitoring, temperature readings, and
log viewing capabilities.

Routes:
    / - Main status page showing laser status and system information
    /api - REST API endpoint for laser control (requires API key authentication)
    /pylog - Application log viewer
    /guaccesslog - Gunicorn access log viewer
    /guerrorlog - Gunicorn error log viewer
    /syslog - System log viewer (last 200 entries)

The application uses settings from app_control module and interfaces with
laser hardware through the laserclass module.
"""

import subprocess
from threading import enumerate as enumerate_threads
from flask import Flask, render_template, jsonify, request
from laserclass import laser
from app_control import settings, VERSION
from logmanager import logger

app = Flask(__name__)
logger.info('Starting Laser Controller web app version %s', VERSION)
logger.info('Api-Key = %s', settings['api-key'])


def read_cpu_temp(file_path):
    """Read CPU Temp"""
    with open(file_path, 'r', encoding='utf-8') as f:
        line = f.readline()
    return round(float(line) / 1000, 1)


def read_reverse_file(file_path):
    """Read log file and reverse order"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines.reverse()
    return lines


def threadlister():
    """Get a list of all threads running"""
    appthreads = []
    for appthread in enumerate_threads():
        appthreads.append([appthread.name, appthread.native_id])
    return appthreads


@app.route('/')
def index():
    """Web status page """
    cputemperature = read_cpu_temp(settings['cputemp'])
    return render_template('index.html', laserstatus=laser.httpstatus(),
                           cputemperature=cputemperature, version=VERSION, threads=threadlister())


@app.route('/api', methods=['POST'])
def api():
    """API endpoint"""
    try:
        logger.debug('API headers: %s', request.headers)
        logger.debug('API request: %s', request.json)
        if 'Api-Key' in request.headers.keys():  # check api key exists
            if request.headers['Api-Key'] == settings['api-key']:  # check for correct API key
                item = request.json['item']
                command = request.json['command']
                status = laser.parsecontrol(item, command)
                return jsonify(status), 201
            logger.warning('API: access attempt using an invalid token from %s', request.headers[''])
            return 'access token(s) unuthorised', 401
        logger.warning('API: access attempt without a token from  %s', request.headers['X-Forwarded-For'])
        return 'access token(s) incorrect', 401
    except KeyError:
        logger.warning('API endpoint: bad json message')
        return "badly formed json message", 201


@app.route('/pylog')
def showplogs():
    """Show apoplication log"""
    cputemperature = read_cpu_temp(settings['cputemp'])
    logs = read_reverse_file(settings['logfilepath'])
    return render_template('logs.html', rows=logs, log='Laser Controller Log',
                           cputemperature=cputemperature, version=VERSION)


@app.route('/guaccesslog')
def showgalogs():
    """Gunicorn access log page"""
    cputemperature = read_cpu_temp(settings['cputemp'])
    logs = read_reverse_file(settings['gunicornpath'] + 'gunicorn-access.log')
    return render_template('logs.html', rows=logs, log='Gunicorn Access Log',
                           cputemperature=cputemperature, version=VERSION)


@app.route('/guerrorlog')
def showgelogs():
    """Gunicorn error log page"""
    cputemperature = read_cpu_temp(settings['cputemp'])
    logs = read_reverse_file(settings['gunicornpath'] + 'gunicorn-error.log')
    return render_template('logs.html', rows=logs, log='Gunicorn Error Log',
                           cputemperature=cputemperature, version=VERSION)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    """System log page - shows 200 most recent messages"""
    cputemperature = read_cpu_temp(settings['cputemp'])
    log = subprocess.Popen('journalctl -n 200', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='System Log',
                           cputemperature=cputemperature, version=VERSION)


if __name__ == '__main__':
    app.run()
