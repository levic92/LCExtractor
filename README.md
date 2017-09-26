Modified extractor plugin for the deluge torrent client (v1.3.15)

Changes have been made to integrate with the way "Completed Download Handling" works with Sonarr and Radarr




NOTES:

most code in deluge client that concerns this plugin is in torrent.py and torrentmanager.py
alerts get triggered by libtorrent: http://www.libtorrent.org/reference-Alerts.html

There should be no loops when setting is_finished on torrent because the following alert is only triggered once per torrent:
torrent_finished_alert
Declared in "libtorrent/alert_types.hpp"

This alert is generated when a torrent switches from being a downloader to a seed. It will only be generated once per torrent. It contains a torrent_handle to the torrent in question.