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
from datetime import datetime
import uuid
from flask import Flask, render_template, jsonify, request, send_from_directory, send_file
from laserclass import laser
from app_control import settings, VERSION, SECRETS
from logmanager import logger
from contact_message import send_email_via_graph

app = Flask(__name__)
app.secret_key = SECRETS['api-key']
logger.info('Starting Laser Controller web app version %s', VERSION)
logger.info('Api-Key = %s', SECRETS['api-key'])
YEAR = datetime.now().year

def read_cpu_temperature():
    """Read the CPU temperature and returns in Celsius"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    return round(float(log) / 1000, 1)


def read_log_from_file(file_path):
    """Read a log from a file and reverse the order of the lines so newest is at the top"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(reversed(lines))


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


@app.errorhandler(500)
def internal_server_error(_):
    """
    Handles the 500 Internal Server Error by serving a custom static HTML error page.

    This function is triggered when a 500 Internal Server Error occurs in the
    application and serves a pre-defined static HTML file designed for error handling.
    """
    response = send_from_directory('static', '500.html')
    response.status_code = 500
    return response

@app.route('/')
def index():
    """Web status page """
    return render_template('index.html', settings=settings, laserstatus=laser.httpstatus(),
                           year=YEAR, version=VERSION, threads=threadlister())

@app.route('/statusdata', methods=['GET'])
def statusdata():
    """Status data read by javascript on default website so the page shows near live values"""
    ctrldata = {'cputemperature': read_cpu_temperature()
                }
    return jsonify(ctrldata), 201

@app.route('/api', methods=['POST'])
def api():
    """API endpoint"""
    try:
        logger.debug('API headers: %s', request.headers)
        logger.debug('API request: %s', request.json)
        if 'Api-Key' in request.headers.keys():  # check api key exists
            if request.headers['Api-Key'] == SECRETS['api-key']:  # check for correct API key
                item = request.json['item']
                command = request.json['command']
                status = laser.parsecontrol(item, command)
                return jsonify(status), 201
            logger.warning('API: access attempt using an invalid token')
            return {'status': 'access token(s) unauthorised'}, 401
        logger.warning('API: access attempt without a token')
        return {'status': 'access token(s) incorrect'}, 401
    except KeyError:
        logger.warning('API: KeyError with json message')
        return {'status': "badly formed json message"}, 400


@app.route('/pylog')
def showplogs():
    """Show the Application log web page"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['logfilepath'])
    return render_template('logviewer.html', rows=logs, log='Application log',
                           cputemperature=cputemperature, settings=settings, version=VERSION, year=YEAR)


@app.route('/guaccesslog')
def showgalogs():
    """"Show the Gunicorn Access Log web page"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['gunicornpath'] + 'gunicorn-access.log')
    return render_template('logviewer.html', rows=logs, log='Gunicorn Access Log',
                           cputemperature=cputemperature, settings=settings, version=VERSION, year=YEAR)


@app.route('/guerrorlog')
def showgelogs():
    """"Show the Gunicorn Errors Log web page"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['gunicornpath'] + 'gunicorn-error.log')
    return render_template('logviewer.html', rows=logs, log='Gunicorn Error Log',
                           cputemperature=cputemperature, settings=settings, version=VERSION, year=YEAR)


@app.route('/syslog')
def showslogs():
    """Show the last 2000 lines from the system log on a web page"""
    cputemperature = read_cpu_temperature()
    log = subprocess.Popen('/bin/journalctl -n 2000', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logviewer.html', rows=logs, log='System Log', cputemperature=cputemperature,
                            settings=settings, version=VERSION, year=YEAR)

@app.route('/documentation')
def download_manual():
    """
    Handles the request to download the application's manual.

    This function serves the PDF manual of the application as a downloadable
    attachment. The manual file's name is retrieved from the application
    settings and provided as the download name.
    """
    return send_file('manual.pdf', download_name='%s.pdf' % settings['app-name'], as_attachment=True)


@app.route('/pp')
def privacy_policy():
    """Show the privacy policy page"""
    return render_template('pp.html', year=YEAR, version=VERSION, settings=settings)


@app.route('/contactform')
def contact_us():
    """Handles the HTTP request for the contact form page."""
    return render_template('contact.html', formname='contact', year=YEAR, version=VERSION, settings=settings)


@app.route('/support')
def support_ticket():
    """Handles the HTTP request for the support form page."""
    return render_template('contact.html', ticket=uuid.uuid4().hex, formname='support', year=YEAR, version=VERSION, settings=settings)


@app.route('/contactresponse', methods=['POST'])
def contact_reply():
    """Reply page on sucecssful submission of contact form."""
    send_email_via_graph(request.form)
    return render_template('contactresponse.html', request_data=request.form, year=YEAR, version=VERSION, settings=settings)

if __name__ == '__main__':
    app.run()
