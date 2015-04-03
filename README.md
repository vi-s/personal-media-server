# personal-media-server
Automation/Monitoring scripts to make managing a remote personal media serve a breeze.

### Automation
Processes that are typically carried out manually are automated through executable python scripts.
Some of these scripts are added to the system's crontab so that they are faithfully executed periodically.

### Monitoring
Additionally, certain processes (such as video conversion status) are monitored through a flask web server. This allows you to check your media server's status any time through REST web api, which can be very convenient.

*Note: The start script for this project was written specifically for CentOS 7, but the python automation scripts can be used on any Unix system. YMMV with Windows.
