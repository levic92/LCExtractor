#!/usr/bin/env python
import sys
import os
import ntpath
import json
import gzip
import logging

# arguments set by user
deluge_url = 'http://127.0.0.1:8112/json'
deluge_password = 'deluge'
move_extraced_to = None # set this if you want to move files instead of delete (set to None for delete)

# take the first user argument and if it is equal to radarr then use radarr variable names
mode = "sonarr"
env_download_id = 'sonarr_download_id'
env_sourcepath = 'sonarr_episodefile_sourcepath'
env_scenename = 'sonarr_episodefile_scenename'
env_destpath = 'sonarr_episodefile_path'
if len(sys.argv) > 1 and sys.argv[1] == "radarr":
    mode = "radarr"
    env_download_id = 'radarr_download_id'
    env_sourcepath = 'radarr_moviefile_sourcepath'
    env_scenename = 'radarr_moviefile_scenename'
    env_destpath = 'radarr_moviefile_path'

# arguments from sonarr or radarr
download_id = os.environ.get(env_download_id)
sourcepath = os.environ.get(env_sourcepath)
download_name = os.environ.get(env_scenename)
destpath = os.environ.get(env_destpath)

# list of file extensions for archives
EXTRACT_EXT = [".rar", ".tar", ".zip", ".tar.gz", ".tar.bz2", ".tar.lzma", ".tar.xz", ".7z"]

script_dir = os.path.dirname(os.path.realpath(__file__))
logname = os.path.join(script_dir, "lcextractor_cleanup.log")
logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            level=logging.DEBUG)

log_prefix = "[" + (download_name or download_id or "") + "]"
# print function compatible with v2 and v3
def xprint(message):
    sys.stdout.write(log_prefix + " %s\n" % message)
    logging.info(log_prefix + " %s\n" % message)
# stderr shows up in sonarr/radarr log in GUI
def xprintErr(message):
    sys.stderr.write(log_prefix + " %s\n" % message)
    logging.error(log_prefix + " %s\n" % message)

xprint("Starting lcextractor_cleanup in mode: " + mode)

if deluge_url and sourcepath and destpath and (download_id or download_name):
    filename = ntpath.basename(sourcepath)

    auth = '{"method": "auth.login", "params": ["' + deluge_password + '"], "id": 1}'
    auth_params = auth.encode('utf8')

    if download_id:
        download_id = download_id.lower()
        search = '{"method": "web.update_ui", "params": [["hash", "is_finished", "save_path", "files", "name"], {"hash": "' + download_id + '"}], "id": -1}'
    else:
        search = '{"method": "web.update_ui", "params": [["hash", "is_finished", "save_path", "files", "name"], {"name": "' + download_name + '"}], "id": -1}'

    search_params = search.encode('utf8')

    try:
        if sys.version_info[0] < 3:
            import urllib2
            import StringIO

            auth_req = urllib2.Request(deluge_url, data=auth_params, headers={'Content-Type': 'application/json','Accept': 'application/json'})
            auth_res = urllib2.urlopen(auth_req)
            cookie = auth_res.headers.getheader('Set-Cookie')

            search_req = urllib2.Request(deluge_url, data=search_params, headers={'Cookie': cookie, 'Content-Type': 'application/json', 'Accept': 'application/json'})
            search_res = urllib2.urlopen(search_req)

            compresseddata = search_res.read() 
            compressedstream = StringIO.StringIO(compresseddata)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()
            results = json.loads(data)

        else:
            import urllib.request

            auth_req = urllib.request.Request(deluge_url, data=auth_params, headers={'Content-Type': 'application/json','Accept': 'application/json'})
            auth_res = urllib.request.urlopen(auth_req)
            cookie = auth_res.getheader('Set-Cookie')

            search_req = urllib.request.Request(deluge_url, data=search_params, headers={'Cookie': cookie, 'Content-Type': 'application/json', 'Accept': 'application/json'})
            search_res = urllib.request.urlopen(search_req)

            data = gzip.GzipFile(fileobj=search_res).read()

            try:
                results = json.loads(data)
            except:
                # on one system I was getting a bytes object back
                data = data.decode('utf-8')
                results = json.loads(data)

        try:
            if download_id:
                torrent = results["result"]["torrents"][download_id]
            else:
                xprint("No download_id " + (download_name or ""))
                torrents = results["result"]["torrents"]
                download_id = list(torrents.keys())[0]
                torrent = results["result"]["torrents"][download_id]

            if torrent:
                files = torrent["files"]
                if files:
                    files_str = str(files)

                    # check to see if json contains filename
                    if filename in files_str:
                        xprint("This file was not in an archive")
                    else:
                        contains_ext = False

                        # check to see if an extraction file ext is present
                        for ext in EXTRACT_EXT:
                            if ext in files_str:
                                contains_ext = True
                                break
                        
                        if contains_ext:
                            # only delete if file has been imported and exists
                            if os.path.exists(destpath):
                                try:
                                    if move_extraced_to:
                                        new_path = os.path.join(move_extraced_to, filename)
                                        os.rename(sourcepath, new_path)
                                        xprint("Move")
                                    else:
                                        os.remove(sourcepath)
                                        xprint("Delete")
                                except Exception as e:
                                    xprintErr("Failed to delete or move file: " + sourcepath)
                                    xprintErr(e)
                            else:
                                xprintErr("Could not find imported file")
                        else:
                            xprintErr("Could not find this file in torrent files but also no archive files")
            else:
                xprintErr("Did not find download_id in results: " + (download_id or "") + " " + (download_name or ""))
                xprint(results)
        except Exception as e:
            # most likely bad json, ie: did not contain download_id
            xprintErr("Error processing deluge api response")
            xprintErr(e)
            xprint(results)

    except Exception as e:
        xprintErr("Error in web request for download: " + (download_id or "") + " " + (download_name or ""))
        xprintErr(e)
else:
    xprintErr("Missing required variables")
    xprintErr("deluge_url: " + (deluge_url or "") + ", download_id: " + (download_id or "") + ", sourcepath: " + (sourcepath or "") + ", destpath: " + (destpath or "") + ", download_name: " + (download_name or ""))
