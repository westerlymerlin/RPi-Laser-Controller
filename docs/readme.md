# Module Documentation


This document contains the documentation for all the modules in this project.

---

## Contents


[app](./app.md)  
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

[app_control](./app_control.md)  
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.

[contact_message](./contact_message.md)  
Provides functionality to send emails using the Microsoft Graph API.

This module defines a function that sends an email through the Microsoft Graph API by authenticating
via Microsoft Authentication Library (MSAL). It uses OAuth2-based client authentication and constructs
an email payload dynamically based on input data. The email can include sender, recipient, subject, and
message body details. Logs and errors are appropriately recorded.

Functions:
    - send_email_via_graph: Sends an email using Microsoft Graph API with the provided payload.

[laserclass](./laserclass.md)  
Laser Control Module - Manages laser hardware via TTL signals and serial communication

This module provides a comprehensive interface for controlling laser hardware on a
Raspberry Pi system. It handles serial communication protocols, TTL signal management,
power settings, and safety timeout features for laser operation.

The module:
- Manages laser state (on/off) via GPIO pins
- Communicates with laser hardware via serial port
- Provides safety features including automatic timeout
- Exposes HTTP endpoints for remote control and monitoring
- Maintains persistent configuration settings
- Implements comprehensive logging for operational traceability

Dependencies:
- RPi.GPIO: For controlling Raspberry Pi GPIO pins
- pyserial: For serial communication with laser hardware
- app_control: For settings management
- logmanager: For logging operations

Typical usage:
    from laserclass import laser

    # Check laser status
    status = laser.laserstatus()

    # Configure laser
    laser.setpower(50)  # Set to 50% power
    laser.setmaxtimeout(30)  # 30 second safety timeout

    # Control laser
    laser.laser(1)  # Turn on
    # ... operations ...
    laser.laser(0)  # Turn off

[logmanager](./logmanager.md)  
logmanager, setus up application logging. use the **logger** property to
write to the log.


---


  
-------
#### Copyright (C) 2026 Gary Twinn  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.  
  
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.  
  
  ##### Author: Gary Twinn  
  
 -------------
  
