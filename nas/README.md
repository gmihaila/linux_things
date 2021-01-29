# Network Attached Storage (NAS)

Always make sure we're up to date:

```bash
sudo apt update
sudo apt upgrade -y
```

## [Build a NAS server using Samba](https://github.com/gmihaila/raspberry_projects/blob/master/nas/samba.md)

## [Install Transmission](https://github.com/gmihaila/raspberry_projects/blob/master/nas/transmission.md)

## [Install Plex](https://github.com/gmihaila/raspberry_projects/blob/master/nas/plex.md)

## Run maintenance

* Unmount process - need to stop all running process:

```bash
sudo systemctl stop transmission-daemon
sudo /etc/init.d/smbd stop
sudo /etc/init.d/nmbd stop
sudo umount /pi_server
```

