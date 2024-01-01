"""
Main web page, provides API access and web page
"""

import subprocess
from flask import Flask, render_template, jsonify, request
from laserclass import laser
from settings import settings, VERSION
from logmanager import logger

app = Flask(__name__)


@app.route('/')
def index():
    """Web status page """
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    return render_template('index.html', laserstatus=laser.httpstatus(), cputemperature=cputemperature, version=VERSION)


@app.route('/api', methods=['POST'])
def api():
    """API endpoint"""
    try:
        item = request.json['item']
        command = request.json['command']
        status = laser.parsecontrol(item, command)
        return jsonify(status), 201
    except KeyError:
        logger.warning('API endpoint: bad json message')
        return "badly formed json message", 201


@app.route('/pylog')
def showplogs():
    """Show apoplication log"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logfilepath'], 'r', encoding='utf-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Laser Controller Log', cputemperature=cputemperature, version=VERSION)


@app.route('/guaccesslog')
def showgalogs():
    """"Gunicorn access log page"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-access.log', 'r', encoding='utf-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Gunicorn Access Log', cputemperature=cputemperature, version=VERSION)


@app.route('/guerrorlog')
def showgelogs():
    """Gunicorn error log page"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-error.log', 'r', encoding='utf-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Gunicorn Error Log', cputemperature=cputemperature, version=VERSION)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    """System log page - shows 200 most recent messages"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    log = subprocess.Popen('journalctl -n 200', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='System Log', cputemperature=cputemperature, version=VERSION)


if __name__ == '__main__':
    app.run()
