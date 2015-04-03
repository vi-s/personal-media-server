# personal-media-server
Automation/Monitoring scripts to make managing a remote personal media serve a breeze. This project was built on a CentOS 7 server, but can be tweaked to work with other distributions.

This type of personal server can easily be achieved for 5 dollars a month on Digital Ocean.

### Automation
Processes that are typically carried out manually are automated through executable python scripts.
Some of these scripts are added to the system's crontab so that they are faithfully executed periodically.
Automated tasks include:
* Torrent Mover: Automatically moving `.torrent` files from a source directory to a destination directory for sync (via crontab)
* Extraction Manager: automatically (via crontab) unrars new content and subsequently deletes the unrared content when its originating rar archive files are deleted, probably via deluge Web UI 
* WebM Converter: scans a source directory for all available video files and converts them while saving real-time progress statistics for all videos to the disk. This progress stat data is then displayed via Flask web server to allow for highly convenient monitoring.

### Monitoring
Additionally, certain processes (such as video conversion status) and infastructure node properties (such as `df -h` output to check available disk space) are monitored through a flask web server. This allows you to check your media server's status any time through REST web api, which can be very convenient.

*Note: The start script for this project was written specifically for CentOS 7, but the python automation scripts can be used on any Unix system. YMMV with Windows.

### Media Server Components
The complete personal media server system that this project references includes the following parts.
* Apache Web Server as the core media streaming server
* Flask Web Server to retrieve information about media server / infrastructure node status
* Deluge Daemon Bittorrent Client
* Deluge Web UI Server
* Btsync to sync torrent files between host and remote machines
* VLC or a Web Browser (Chrome has best codec support) as the stream client
