# synoindex-server
Simple synoindex server is a web service wrapper for Synology NAS native 'synoindex'.

## Introduction
Since Synology DSM 6.0 comes Docker support. Users run many media services in the docker. But we can't notify Synology NAS to reindexing new files in the docker's container.
We can run synoindex inside the docker's container and request simple-synoindex-server to calling native synoindex to reindexing your new files using 'simple-synoindex-server' (https://github.com/racklin/simple-synoindex-server) for x86 or x64 cpu. However, it only works on x86 or x64, but thankfully this was ported to python (https://github.com/jhyun15/synoindex-server) for cross platform usability.

This for expands the functionality of that python implementation with a bit more control over http-server that runs in the background.

## Setup

### Requirement
Required python (>=3.0)
Tested on Synology DS218+.

### Install
1. Download python file to any directory. ```(ex. /volume1/homes/admin)```
2. Run 'synoindex_server_native.py' by task scheduler when boot-up with ipaddress and port command line argument
```Shell
python3 /volume1/homes/admin/synoindex_server_native.py ipadress port
```

## Usage

### Passing arguments to synoindex from webbrowser
Example: force indexer to reindex the folder /volume1/download
```Shell
http://192.168.0.1:9998/synoindex/?args=-R&args=/volume1/download
```
### Shut down server
Example: force indexer to reindex the folder /volume1/download
```Shell
#!/bin/bash
http://192.168.0.1:9998/shutdown
```
### Initiate index from Transmission torrent client
When running Transmission in a docker environment. A new script can be written that initiates the indexer using e.g curl
```Shell
#!/bin/bash
curl -G -d "args=-R" -d "args=/volume1/download" http://192.168.0.1:9998/synoindex
```
Next Transmission should be instructed to run that script upon completion. This can be done in the `settings.json` of transmission.
```Shell
"script-torrent-done-enabled": true, 
"script-torrent-done-filename": "/config/my_custom_script", 
```
