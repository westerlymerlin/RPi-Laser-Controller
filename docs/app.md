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

<a id="app.Flask"></a>

## Flask

<a id="app.render_template"></a>

## render\_template

<a id="app.jsonify"></a>

## jsonify

<a id="app.request"></a>

## request

<a id="app.laser"></a>

## laser

<a id="app.settings"></a>

## settings

<a id="app.VERSION"></a>

## VERSION

<a id="app.logger"></a>

## logger

<a id="app.app"></a>

#### app

<a id="app.read_cpu_temp"></a>

#### read\_cpu\_temp

```python
def read_cpu_temp(file_path)
```

Read CPU Temp

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

<a id="app.index"></a>

#### index

```python
@app.route('/')
def index()
```

Web status page

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

Show apoplication log

<a id="app.showgalogs"></a>

#### showgalogs

```python
@app.route('/guaccesslog')
def showgalogs()
```

Gunicorn access log page

<a id="app.showgelogs"></a>

#### showgelogs

```python
@app.route('/guerrorlog')
def showgelogs()
```

Gunicorn error log page

<a id="app.showslogs"></a>

#### showslogs

```python
@app.route('/syslog')
def showslogs()
```

System log page - shows 200 most recent messages

