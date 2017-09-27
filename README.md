# LCExtractor
Plugin for the [deluge](http://deluge-torrent.org/) torrent client that extracts compressed files upon torrent completion.

Modified extractor plugin for the deluge torrent client (v1.3.15)

Changes have been made to integrate with the way "Completed Download Handling" works with Sonarr and Radarr

* Target folder for extracting the torrent can be specified
* A sub folder (name of torrent) can be created within the target folder
* In-place extraction of the torrent in the torrent's download folder is possible as well

## Supported File formats:

UniX-ish supports:
* .rar, .tar, .zip, .7z .tar.gz, .tgz, .tar.bz2, .tbz .tar.lzma, .tlz, .tar.xz, .txz

Windows supports:
* .rar, .zip, .tar, .7z, .xz, .lzma

( Requires [7-zip]( http://www.7-zip.org/) to be installed on the system running the client resp. the daemon if run in daemon mode )


# Build Instructions
To build the python egg file:
```
  python setup.py bdist_egg
```

# Installation Instructions

Download the [egg file](https://github.com/levic92/LCExtractor) of the plugin.

##### Notes
* Plugin eggs have the Python version encoded in the filename and will only load in Deluge if the versions match. (e.g. Plugin-1.0-py2.7.egg is a Python 2.7 egg.)

* On *nix systems, you can verify Python version with: ```python --version```

* The bundled Python version for Windows executable is 2.6 and for MacOSX Deluge.app it is 2.7.

* If a plugin does not have a Python version available it is usually possible to rename it to match your installed version (e.g. Plugin-1.0-py2.6.egg to Plugin-1.0-py2.7.egg) and it will still run normally

### GUI-Install:

Preferences -> Plugins -> Install plugin

Locate the downloaded egg file and select it.

### Manual Install:

Copy the egg file into the ```plugins``` directory in Deluge config:

Linux/*nix:

``` ~/.config/deluge/plugins ```

Windows:

``` %APPDATA%\deluge\plugins ```

### Client-Server Setups:

When running the Deluge daemon, ``` deluged ``` and the Deluge client on separate computers, the plugin must be installed on both of them. When installing the egg through the GTK client it will be placed in the plugins directory of your computer, as well as copied over to the computer running the daemon.

##### Note: If the Python versions on the server and desktop computer do not match, you will have to copy the egg file to the server manually.

For example in the setup below you will have to install the py2.6 egg on the desktop as you normal would do but then manually install the py2.7 egg onto the server.

* Windows desktop with Python 2.6 running GTK client.
* Linux server with Python 2.7 running deluged

###### Note: The Windows installer comes bundled with python: either python 2.6 or 2.7 depending on the intstaller you used.

### Notes
Most code in deluge client that concerns this plugin is in torrent.py and torrentmanager.py
alerts get triggered by libtorrent: http://www.libtorrent.org/reference-Alerts.html

There should be no loops when setting is_finished on torrent because the following alert is only triggered once per torrent:
torrent_finished_alert
Declared in "libtorrent/alert_types.hpp"

This alert is generated when a torrent switches from being a downloader to a seed. It will only be generated once per torrent. It contains a torrent_handle to the torrent in question.

In place extraction code from: https://github.com/cvarta/deluge-extractor/



### cli get torrent status
```
#!/bin/bash
curl -c cookies.txt --compressed -i -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d '{"method": "auth.login", "params": [""], "id": 1}' http://127.0.0.1:8112/json
json=$(curl -b cookies.txt --compressed -i -H "Content-Type: application/json" -H "Accept: application/json" -X POST -d '{"method": "web.update_ui", "params": [["name", "is_finished"], {"label": "test"}], "id": 1}' http://127.0.0.1:8112/json)
rm cookies.txt
echo $json
```