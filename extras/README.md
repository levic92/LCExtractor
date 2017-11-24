LCExtractor Cleanup
==============

**Automatically delete or move extracted files once they are imported by Sonarr or Radarr**

Python 2 and 3 script to delete or move extracted files. Use this as a Custom Script in Sonarr and Radarr. When a download is imported this script will get the torrent details from the download ID using the Deluge API. If it finds the torrent and the files list does not contain the imported file name (but contains archived files) then the script will delete or move the file.

Modify Script Options
--------------
1. deluge_url
    - json api endpoint for deluge web service
2. deluge_password
    - password to log into deluge gui
3. move_extraced_to
    - if you want to move files instead of delete set this to the full destination path
    - to delete extracted files set to `None`

Sonarr Setup
--------------
Setup the lcextractor_cleanup.py script via Settings > Connect > Connections > + (Add)
  - `name` - lcextractor_cleanup
  - `On Grab` - No
  - `On Download` - Yes
  - `On Upgrade` - Yes
  - `On Rename` - No
  - Filter Series Tags - optional
  - Windows Users
    - `Path` - Full path to your python executable
    - `Arguments` - Full path to `lcextractor_cleanup.py`
  - Nonwindows Users
    - Ensure script is executable and set correct shebang for your environment
    - `Path` - Full path to `lcextractor_cleanup.py`
    - `Arguments` - Leave blank

Radarr Setup
--------------
Setup the lcextractor_cleanup.py script via Settings > Connect > Connections > + (Add)
  - `name` - lcextractor_cleanup
  - `On Grab` - No
  - `On Download` - Yes
  - `On Upgrade` - Yes
  - `On Rename` - No
  - Filter Series Tags - optional
  - Windows Users
    - `Path` - Full path to your python executable
    - `Arguments` - Full path to `lcextractor_cleanup.py` AND `"radarr"`
  - Nonwindows Users
    - Ensure script is executable and set correct shebang for your environment
    - `Path` - Full path to `lcextractor_cleanup.py`
    - `Arguments` - `"radarr"`
