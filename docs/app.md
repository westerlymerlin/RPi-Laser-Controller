# None

<a id="app"></a>

# app

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

<a id="app.subprocess"></a>

## subprocess

<a id="app.enumerate_threads"></a>

## enumerate\_threads

<a id="app.datetime"></a>

## datetime

<a id="app.uuid"></a>

## uuid

<a id="app.Flask"></a>

## Flask

<a id="app.render_template"></a>

## render\_template

<a id="app.jsonify"></a>

## jsonify

<a id="app.request"></a>

## request

<a id="app.send_from_directory"></a>

## send\_from\_directory

<a id="app.send_file"></a>

## send\_file

<a id="app.laser"></a>

## laser

<a id="app.settings"></a>

## settings

<a id="app.VERSION"></a>

## VERSION

<a id="app.SECRETS"></a>

## SECRETS

<a id="app.logger"></a>

## logger

<a id="app.send_email_via_graph"></a>

## send\_email\_via\_graph

<a id="app.app"></a>

#### app

<a id="app.YEAR"></a>

#### YEAR

<a id="app.read_cpu_temperature"></a>

#### read\_cpu\_temperature

```python
def read_cpu_temperature()
```

Read the CPU temperature and returns in Celsius

<a id="app.read_log_from_file"></a>

#### read\_log\_from\_file

```python
def read_log_from_file(file_path)
```

Read a log from a file and reverse the order of the lines so newest is at the top

<a id="app.read_reverse_file"></a>

#### read\_reverse\_file

```python
def read_reverse_file(file_path)
```

Read log file and reverse order

<a id="app.threadlister"></a>

#### threadlister

```python
def threadlister()
```

Get a list of all threads running

<a id="app.internal_server_error"></a>

#### internal\_server\_error

```python
@app.errorhandler(500)
def internal_server_error(_)
```

Handles the 500 Internal Server Error by serving a custom static HTML error page.

This function is triggered when a 500 Internal Server Error occurs in the
application and serves a pre-defined static HTML file designed for error handling.

<a id="app.index"></a>

#### index

```python
@app.route('/')
def index()
```

Web status page

<a id="app.statusdata"></a>

#### statusdata

```python
@app.route('/statusdata', methods=['GET'])
def statusdata()
```

Status data read by javascript on default website so the page shows near live values

<a id="app.api"></a>

#### api

```python
@app.route('/api', methods=['POST'])
def api()
```

API endpoint

<a id="app.showplogs"></a>

#### showplogs

```python
@app.route('/pylog')
def showplogs()
```

Show the Application log web page

<a id="app.showgalogs"></a>

#### showgalogs

```python
@app.route('/guaccesslog')
def showgalogs()
```

"Show the Gunicorn Access Log web page

<a id="app.showgelogs"></a>

#### showgelogs

```python
@app.route('/guerrorlog')
def showgelogs()
```

"Show the Gunicorn Errors Log web page

<a id="app.showslogs"></a>

#### showslogs

```python
@app.route('/syslog')
def showslogs()
```

Show the last 2000 lines from the system log on a web page

<a id="app.download_manual"></a>

#### download\_manual

```python
@app.route('/documentation')
def download_manual()
```

Handles the request to download the application's manual.

This function serves the PDF manual of the application as a downloadable
attachment. The manual file's name is retrieved from the application
settings and provided as the download name.

<a id="app.privacy_policy"></a>

#### privacy\_policy

```python
@app.route('/pp')
def privacy_policy()
```

Show the privacy policy page

<a id="app.contact_us"></a>

#### contact\_us

```python
@app.route('/contactform')
def contact_us()
```

Handles the HTTP request for the contact form page.

<a id="app.support_ticket"></a>

#### support\_ticket

```python
@app.route('/support')
def support_ticket()
```

Handles the HTTP request for the support form page.

<a id="app.contact_reply"></a>

#### contact\_reply

```python
@app.route('/contactresponse', methods=['POST'])
def contact_reply()
```

Reply page on sucecssful submission of contact form.

