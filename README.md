Related to: https://github.com/badaix/snapcast

# snapclient-switcher
Be able to switch host (snapserver) of snapclient by a simple rest call.
* Default port: `8090`
* Default snapserver: `127.0.0.1:1704`

## config existing snapclient
* Open `/etc/default/snapclient`
* And edit the line `START_SNAPCLIENT=false`

## start snapclient-switcher
* Execute `python snapclient-switcher.py [port]`

## how to use
`http://snapclientIp:8090/[?url=xxx.xxx.xxx.xxx][&port=xxxx]`
* Reset to default: `http://snapclientIp:8090`
* Change host: `http://snapclientIp:8090?url=newHostIp`
* Change port: `http://snapclientIp:8090?port=newPort`
* Change host and port: `http://snapclientIp:8090?url=newHostIp&port=newPort`

**Debian service comming soon**
