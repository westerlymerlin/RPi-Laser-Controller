# None

<a id="app_control"></a>

# app\_control

Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.

<a id="app_control.random"></a>

## random

<a id="app_control.json"></a>

## json

<a id="app_control.copyfile"></a>

## copyfile

<a id="app_control.b64decode"></a>

## b64decode

<a id="app_control.b64encode"></a>

## b64encode

<a id="app_control.datetime"></a>

## datetime

<a id="app_control.VERSION"></a>

#### VERSION

<a id="app_control.initialise"></a>

#### initialise

```python
def initialise()
```

These are the default values written to the settings.json file the first time the app is run

<a id="app_control.generate_api_key"></a>

#### generate\_api\_key

```python
def generate_api_key(key_len)
```

generate a new api key

<a id="app_control.writesettings"></a>

#### writesettings

```python
def writesettings()
```

Write settings to a json file

<a id="app_control.readsettings"></a>

#### readsettings

```python
def readsettings()
```

Read the settings from the json file

<a id="app_control.load_settings"></a>

#### load\_settings

```python
def load_settings()
```

Takes the settings variable from the initialise and replaces values from the json file if they exist

<a id="app_control.load_secrets"></a>

#### load\_secrets

```python
def load_secrets()
```

Load secrets from a file and decode them.

This function reads a file named 'SECRETS', decodes its contents using Base64,
and then parses the resulting JSON. It is used to securely retrieve stored
configuration or sensitive data. The file is expected to contain secrets
encoded in a specific format.

<a id="app_control.update_secret"></a>

#### update\_secret

```python
def update_secret(key, value)
```

Updates the secret storage by adding or updating a key-value pair. The method also creates a
backup of the existing storage file before writing the updated encoded secrets back to the file.

<a id="app_control.SECRETS"></a>

#### SECRETS

<a id="app_control.settings"></a>

#### settings

