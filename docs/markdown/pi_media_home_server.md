# Media Home Server

The plan is to have a Netflix-like local server that runs on a Raspberry pi.

My hardware setup is:

* Raspberry Pi 4

* SSD Sata Drive

* Sata Drive adaptor with external power source (very important to have external power source. 
  It took me a lot of formatting to find out that the pi is not powerful enough to hold an external hard-drive).
  
The software setup is:

* Transmission: to handle anything I want to download on my pi. It has a nice web ui that I can use form my personal laptop.

* Plex: this is our media server. It will stream everything that it finds on the external SSD hard-drive.

## Setup Pi4

* Manually download OS image from [here](https://www.raspberrypi.org/software/operating-systems/)
* Flash micro SD card with OS image. I'm using [balena etcher](https://www.balena.io/etcher/)
* Make sure to add `ssh` empty file to micro SD card after OS image is flashed. This allows headless connections.
* Connect Pi4 to router with ethernet cable. Power it on. Check router for IP address in order to connect.

*Note:* If need to change ssh key: `ssh-keygen -R 192.168.0.11`


## Install updates

Always good to keep all up to date:

```bash
sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade -y
sudo apt autoremove -y
```

## Install Vim

I use vim:

```bash
sudo apt-get install vim -y
```

## Setup Static IP

Need to have a static IP in case the PI or router needs to restart:

```bash
sudo vim /etc/dhcpcd.conf
```

And enter the following at the end of the file: 

```bash
#setting static ip address for raspberry pi 4
static ip_address=192.168.50.11/24
static routers=192.168.50.1
static domain_name_servers=192.168.50.1
```

Reboot PI:

```bash
sudo reboot
```

## Setup External Hard-Drive

Format drive:

```bash
lsblk -f
sudo umount /dev/sda2
sudo mkfs -t ext4 /dev/sda2
```

Install ntfs package:

```bash
sudo apt-get install ntfs-3g
```

Install Exfat Package:

```bash
sudo apt-get install exfat-utils exfat-fuse
```

Create storage directory:

```bash
sudo mkdir -p /Media
```

And change ownsership

```bash
sudo chown -R pi:pi /Media
```

See mounting points:

```bash
lsblk
```

Mount Drive:

```bash
sudo mount /dev/sda2 /Media
```

Create folders:

```bash
sudo mkdir -p /Media/Movies
sudo mkdir -p /Media/Music
sudo mkdir -p /Media/TV\ Shows
sudo mkdir -p /Media/in_progress
```

```bash
sudo chown -R pi:pi /Media/Movies
sudo chown -R pi:pi /Media/TV\ Shows
sudo chown -R pi:pi /Media/in_progress
```

Keep drive mounted (automount) even when PI restarts:

```bash
sudo vim /etc/fstab
```

And enter the following at the end of the file:
Recommended by fstab is to use UUID. UUID format is: `UUID=<uuid-of-your-drive>  <mount-point>  <file-system-type>  <mount-option>  <dump>  <pass>`.
Use `sudo blkid` to find <uuid-of-your-drive> and test it out with `sudo mount -a`
My command will be:

```bash
UUID=7690cbc8-a262-40ba-a860-c47d499304c7 /Media ext4 defaults,auto,users,rw,nofail 0 0
```
What I used before and it worked but it's not recommended: `/dev/sda2 /Media ext4 defaults,user 0 0`

Reboot PI:

```bash
sudo reboot
```

## Install Transmission

```bash
sudo apt install transmission-daemon -y
```

Stop transmission, so we can do some configuration:

```bash
sudo systemctl stop transmission-daemon
```

Add settings:

```bash
sudo vim /etc/transmission-daemon/settings.json
```

And enter the following at the end of the file:

```bash
"incomplete-dir": "/Media/in_progress",
"download-dir": "/Media/Movies",
"incomplete-dir-enabled": true,
"rpc-password": "my-pass",
"rpc-username": "pi",
"rpc-whitelist": "192.168.*.*",
```

Change default user:

```bash
sudo vim /etc/init.d/transmission-daemon
```

Make sure that:

```bash
USER=pi
```

Edit service file:

```bash
sudo vim /etc/systemd/system/multi-user.target.wants/transmission-daemon.service
```

Make sure that:

```bash
User=pi
```

Reload transmission:

```bash
sudo systemctl daemon-reload
```

Other configurations:

```bash
sudo chown -R pi:pi /etc/transmission-daemon
sudo mkdir -p /home/pi/.config/transmission-daemon/
sudo ln -s /etc/transmission-daemon/settings.json /home/pi/.config/transmission-daemon/
sudo chown -R pi:pi /home/pi/.config/transmission-daemon/
```

Start transmission:

```bash
sudo systemctl start transmission-daemon
```

Check status make sure everything is running smooth:

```bash
systemctl status transmission-daemon.service
```

Transmission available at `http://192.168.50.11:9091`.

Reboot PI:

```bash
sudo reboot
```

## Install Plex

```bash
sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade -y
sudo apt autoremove -y
```

Add the official Plex package repository:

```bash
sudo apt-get install apt-transport-https
```

Add the Plex repositories to the “apt” package managers key list:

```bash
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -
```

Add the official plex repository to the sources list by running the following command:

```bash
echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
```

Run the “update” command again to refresh the package list:

```bash
sudo apt-get update
```

Install the Plex Media server package to the Pi:

```bash
sudo apt install plexmediaserver
```

Plex available at `http://192.168.50.11:32400/web/`.

The scanners and metadata agents used by Plex will work best when your major types of content are separated from each other. We strongly recommend separating movie and television content into separate main directories. For instance, you might use something like this:

```bash
/Media
   /Movies
      movie content
   /Music
      music content
   /TV Shows
      television content
```

TV Shows should have the following structure for first episode in first season naming (added example if there are two episodes in one):

```bash
/TV Shows
  /My Show
    /Season 01
      My Show - s01e01.format
      My Show - s01e02-03.format     
```

Reboot PI:

```bash
sudo reboot
```

## Update Plex

Download the `*.deb` file on the pi and install updates. For example if we have the `plexmediaserver_1.22.1.4275-48e10484b_armhf.deb`:

```bash
sudo dpkg -i plexmediaserver_1.22.1.4275-48e10484b_armhf.deb
```



## Fix disk issues with `fsck`

```bash
sudo fsck -f -y /dev/sda2
```

