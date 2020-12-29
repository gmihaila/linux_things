# Network Attached Storage (NAS)

## [Build a NAS server using Raspberry PI 4](https://github.com/gmihaila/raspberry_projects/blob/master/nas/samba.md)

## [Install Transmission](https://github.com/gmihaila/raspberry_projects/blob/master/nas/transmission.md)

## Run maintenance

* Unmount process - need to stop all running process:

```bash
sudo systemctl stop transmission-daemon
sudo /etc/init.d/smbd stop
sudo /etc/init.d/nmbd stop
sudo umount /pi_server
```

