# Laser Controler Service

### Python project to control a Laservall Laser and is controlled via an HTTP API

Functional description and setup instructions are available in the file: [README.pdf](./README.pdf)

Python module documentation can be found in the folder: [docs](./docs/readme.md)

Change log can be found in the file [changelog.txt](./changelog.txt)

`app.py`			    Flask application that manages the API 

----------------------------------------------------

`laserclass.py`	  read and write to the RS232 port of the laser and activates the laser via a TTL line from GPIO 16

### JSON Commands
`{"laser": "off"}` Switch off the laser    
`{"laser": "on"}` Switch on the laser    
`{"setlaserpower": nnn}` set the laser power to nnn% (Max 100%)  
`{"laseralarm": 1}` Read the laser Alarm status  
`{"laserstatus": 1}` Read the laser status (returns power and if the laser is firing)  

`{"setlasertimeout": nnn}` change the default maximum time the laser can fire to nnn seconds (default is 300)  



&nbsp;   
&nbsp;    
&nbsp;  
&nbsp;   
&nbsp;   
&nbsp;   
--------------

#### Copyright (C) 2025 Gary Twinn

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


Author:  Gary Twinn  
Repository:  [github.com/westerlymerlin](https://github)

-------------