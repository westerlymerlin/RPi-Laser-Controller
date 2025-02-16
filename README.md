# Laser Controler

### Python project to control a Laservall Laser and is controlled via an HTTP API

Functional description and setup instructions are available in the file: [README.pdf](./README.pdf)


`app.py`			    Flask application that manages the API 

----------------------------------------------------

`laserclass.py`	  read and write to the RS232 port of the laser and activates the laser vis a TTL line from GPIO 16

### JSON Commands
`{"laser": "off"}` Switch off the laser    
`{"laser": "on"}` Switch on the laser    
`{"setlaserpower": nnn}` set the laser power to nnn% (Max 100%)  
`{"laseralarm": 1}` Read the laser Alarm status  
`{"laserstatus": 1}` Read the laser status (returns power and if the laser is firing)  

`{"setlasertimeout": nnn}` change the default maximum time the laser can fire to nnn seconds (default is 300)  

`{"restart": "pi"}` Restart the rsapberry pi after a 15 second delay  

