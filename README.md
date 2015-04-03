# personal-media-server
Automation/Monitoring scripts to make managing a remote personal media serve a breeze.

### Automation
Processes that are typically carried out manually are automated through executable python scripts.
Some of these scripts are added to the system's crontab so that they are faithfully executed periodically.

### Monitoring
Additionally, certain processes (such as video conversion status) are monitored through a flask web server. This allows you to check your media server's status any time through REST web api, which can be very convenient.

*Note: The start script for this project was written specifically for CentOS 7, but the python automation scripts can be used on any Unix system. YMMV with Windows.

### Media Server Components
The complete personal media server system that this project references includes the following parts.
* Flask Web Server to retrieve information about media server / infrastructure node status
* Deluge Daemon Bittorrent Client
* Deluge Web UI Server
* Btsync to sync torrent files between host and remote machines
* Apache Web Server for access to media contents
