# Module Documentation


This document contains the documentation for all the modules in the **UCL Helium Line Laser Controller** version 2.1.0 application.

---

## Contents


[app](./app.md)  
Main web page, provides API access and web page

[app_control](./app_control.md)  
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.

[laserclass](./laserclass.md)  
Laser Class - manages the laser via a TTL signal and serial connections

[logmanager](./logmanager.md)  
logmanager, setus up application logging. use the **logger** property to
write to the log.


---

