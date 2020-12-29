# Transmission

Transmission is a cross-platform BitTorrent client.

Web: [https://transmissionbt.com](https://transmissionbt.com)

## Install and setup

* Make sure we're up to date:

```
sudo apt update
sudo apt upgrade -y
```

* Install transmission:

```
sudo apt install transmission-daemon -y
```


* Stop transmission so we can do some configuration:

```
sudo systemctl stop transmission-daemon
```

* Setup folder:

```
sudo mkdir -p /pi_server
sudo mkdir -p /pi_server/in_progress
```

* Setup folder ownership

```
sudo chown -R pi:pi /pi_server
sudo chown -R pi:pi /pi_server/in_progress
```

* Add settings:

```
sudo vim /etc/transmission-daemon/settings.json
```

  * Add:

  ```
  "incomplete-dir": "/pi_server/in_progress",
  "download-dir": "/pi_server",
  "incomplete-dir-enabled": true,
  "rpc-password": "Botosei123$",
  "rpc-username": "pi",
  "rpc-whitelist": "192.168.*.*",
  ```

* Change default user:

```
sudo vim /etc/init.d/transmission-daemon
```

  In here, we need to edit the “USER=” line, so that the Transmission daemon will be run by the “pi” user and not the “debian-transmission” user that is setup by default.
  We do this as the folder we are going to store our torrents in is owned by the “pi” user.

  If you intend on using a different user, make sure you use that instead of “pi“:

  ```
  USER=pi
  ```

* Edit service file:

```
sudo vim /etc/systemd/system/multi-user.target.wants/transmission-daemon.service
```

  * Make sure:

  ```
  user=pi
  ```

* Check status for transmission:

```
sudo systemctl daemon-reload
```


* Other configurations:

```
sudo chown -R pi:pi /etc/transmission-daemon
sudo mkdir -p /home/pi/.config/transmission-daemon/
sudo ln -s /etc/transmission-daemon/settings.json /home/pi/.config/transmission-daemon/
sudo chown -R pi:pi /home/pi/.config/transmission-daemon/
```

* Start transmission:

```
sudo systemctl start transmission-daemon
```

* Check status make sure everything is running smooth:

```
systemctl status transmission-daemon.service
```

* Go to: [http://192.168.0.11:9091](http://192.168.0.11:9091)


## Maintenence

* Unmount partition -need to stop all running process (stop transmission and samba):

```
sudo systemctl stop transmission-daemon
sudo /etc/init.d/smbd stop
sudo /etc/init.d/nmbd stop
sudo umount /pi_server
```

## Fix any disk errors

* Use in fstack to check and fix any file system errors. Make sure disk is unmounted:

```
sudo fsck -y /dev/sda2
```



