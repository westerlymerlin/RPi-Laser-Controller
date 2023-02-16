import os
from flask import Flask, render_template, jsonify, request
from laserclass import laser
from settings import settings

app = Flask(__name__)


@app.route('/')
def index():
    with open(settings['logging']['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    return render_template('index.html', laserstatus=laser.httpstatus(), cputemperature=cputemperature)


@app.route('/api', methods=['POST'])
def api():
    try:
        item = request.json['item']
        command = request.json['command']
        status = laser.parsecontrol(item, command)
        return jsonify(status), 201
    except KeyError:
        return "badly formed json message", 201


@app.route('/pylog')
def showplogs():
    with open(settings['logging']['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logging']['logfilepath'], 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='X-Y log', cputemperature=cputemperature)


@app.route('/guaccesslog')
def showgalogs():
    with open(settings['logging']['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logging']['gunicornpath'] + 'gunicorn-access.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn access log', cputemperature=cputemperature)


@app.route('/guerrorlog')
def showgelogs():
    with open(settings['logging']['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logging']['gunicornpath'] + 'gunicorn-error.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn error log', cputemperature=cputemperature)


@app.route('/uscHALT')
def shutdown_the_server():
    os.system('sudo halt')
    return 'The server is now shutting down, please give it a minute before pulling the power. Cheers G'


if __name__ == '__main__':
    app.run()
