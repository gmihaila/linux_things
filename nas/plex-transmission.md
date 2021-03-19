# Plex - Transmission Combo

## Install updates

```
sudo apt update
sudo apt upgrade -y
```

## Install Vim:

```
sudo apt-get install vim -y
```

## Setup Static IP

```
sudo vim /etc/dhcpcd.conf
```

And enter the following at the end of the file: 

```
#setting static ip address for raspberry pi 4
static ip_address=192.168.50.11/24
static routers=192.168.50.1
static domain_name_servers=192.168.50.1
```

Reboot PI:

```
sudo reboot
```

## Setup External HardDrive

Format drive:

```
lsblk -f
sudo umount /dev/sda2
sudo mkfs -t ext4 /dev/sda2
```

Install ntfs package:

```
sudo apt-get install ntfs-3g
```

Install Exfat Package:

```
sudo apt-get install exfat-utils exfat-fuse
```

Create storage directory:

```
sudo mkdir -p /Media

```

And change ownsership

```
sudo chown -R pi:pi /Media
```

See mounting points:

```
lsblk
```

Mount Drive:

```
sudo mount /dev/sda2 /Media
```

Create folders:

```
sudo mkdir -p /Media/Movies
sudo mkdir -p /Media/Music
sudo mkdir -p /Media/TV\ Shows
sudo mkdir -p /Media/in_progress
```

```
sudo chown -R pi:pi /Media/Movies
sudo chown -R pi:pi /Media/TV\ Shows
sudo chown -R pi:pi /Media/in_progress
```

Keep drive mounted (automount) even when PI restarts:

```
sudo vim /etc/fstab
```

And enter the following at the end of the file:

```
/dev/sda2 /Media ext4 defaults,user 0 0
```

*Alternative use `UUID=<uuid-of-your-drive>  <mount-point>  <file-system-type>  <mount-option>  <dump>  <pass>`.*
*This might work better (make sure to use `sudo blkid` to find <uuid-of-your-drive> and test it out with `sudo mount -a`)*:

```
UUID=7690cbc8-a262-40ba-a860-c47d499304c7 /Media ext4 defaults,auto,users,rw,nofail 0 0
```

or

```
UUID=7690cbc8-a262-40ba-a860-c47d499304c7   /Media  ext4  defaults  0 2
```

Reboot PI:

```
sudo reboot
```

## Install Transmission

```
sudo apt install transmission-daemon -y
```

Stop transmission so we can do some configuration:

```
sudo systemctl stop transmission-daemon
```

Add settings:

```
sudo vim /etc/transmission-daemon/settings.json
```

And enter the following at the end of the file:

```
"incomplete-dir": "/Media/in_progress",
"download-dir": "/Media/Movies",
"incomplete-dir-enabled": true,
"rpc-password": "Botosei123$",
"rpc-username": "pi",
"rpc-whitelist": "192.168.*.*",
```

Change default user:

```
sudo vim /etc/init.d/transmission-daemon
```

Make sure that:

```
USER=pi
```

Edit service file:

```
sudo vim /etc/systemd/system/multi-user.target.wants/transmission-daemon.service
```

Make sure that:

```
User=pi
```

Reload transmission:

```
sudo systemctl daemon-reload
```

Other configurations:

```
sudo chown -R pi:pi /etc/transmission-daemon
sudo mkdir -p /home/pi/.config/transmission-daemon/
sudo ln -s /etc/transmission-daemon/settings.json /home/pi/.config/transmission-daemon/
sudo chown -R pi:pi /home/pi/.config/transmission-daemon/
```

Start transmission:

```
sudo systemctl start transmission-daemon
```

Check status make sure everything is running smooth:

```
systemctl status transmission-daemon.service
```

Transmission available at `http://192.168.50.11:9091`.

Reboot PI:

```
sudo reboot
```



## Install Plex

```
sudo apt update
sudo apt upgrade -y
```

Add the official Plex package repository:

```
sudo apt-get install apt-transport-https
```

Add the Plex repositories to the “apt” package managers key list:

```
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -
```

Add the official plex repository to the sources list by running the following command:

```
echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
```

Run the “update” command again to refresh the package list:

```
sudo apt-get update
```

Install the Plex Media server package to the Pi:

```
sudo apt install plexmediaserver
```

Plex available at `http://192.168.50.11:32400/web/`.

The scanners and metadata agents used by Plex will work best when your major types of content are separated from each other. We strongly recommend separating movie and television content into separate main directories. For instance, you might use something like this:

```
/Media
   /Movies
      movie content
   /Music
      music content
   /TV Shows
      television content
```

Reboot PI:

```
sudo reboot
```

Thanks!
