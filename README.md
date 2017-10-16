Related to: https://github.com/badaix/snapcast

# snapclient-switcher
Be able to switch host (snapserver) of snapclient by a simple rest call.
* Default port: `8090`
* Default snapserver: `127.0.0.1:1704`

## Installation
* Download last .deb file: https://github.com/gilsdav/snapclient-switcher/releases
* Install: `sudo dpkg -i snapclient-switcher-x.x.deb`

## Uninstallation
* Uninstall: `sudo dpkg -P snapclient-switcher`

## How to use
`http://snapclientIp:8090/[?url=xxx.xxx.xxx.xxx][&port=xxxx]`
* Reset to default: `http://snapclientIp:8090`
* Change host: `http://snapclientIp:8090?url=newHostIp`
* Change port: `http://snapclientIp:8090?port=newPort`
* Change host and port: `http://snapclientIp:8090?url=newHostIp&port=newPort`
* Get current connection: `http://snapclientIp:8090/status`

## Manual install
### Config existing snapclient
* Open `/etc/default/snapclient`
* And edit the line `START_SNAPCLIENT=false`
* Log as root `sudo -s`
* Unregister service `systemctl disable snapclient`

### Start snapclient-switcher
* Execute `python snapclient-switcher.py [port]`

### Start snapclient-switcher as service ##
* Copy `snapclient-switcher/usr/local/bin/snapclient-switcher.py` into `/usr/local/bin/` folder
* Start daemon `sudo ./snapclient-switcher/etc/init.d/snapclient-switcher start`
#### Start on boot
* Copy `snapclient-switcher/etc/init.d/snapclient-switcher` into `/etc/init.d` folder
* Log as root `sudo -s`
* Register service `systemctl enable snapclient-switcher`
* Start service `service snapclient-switcher start`


