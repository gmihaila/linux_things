# Setup a Plex server



## Make sure to run updates

```bash
sudo apt-get update
sudo apt-get upgrade
```

## Add the official Plex package repository

This package allows the “apt” package manager to retrieve packages over the “https” protocol that the Plex repository uses.

```bash
sudo apt-get install apt-transport-https
```

## Add the Plex repositories to the “apt” package managers key list

```bash
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -
```

## Add the official plex repository to the sources list by running the following command

```bash
echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
```

## Run the “update” command again to refresh the package list

```bash
sudo apt-get update
```

## Install the Plex Media server package to the Pi

```bash
sudo apt install plexmediaserver
```

Make sure to setup static IP.

The installation process for Plex sets up a few different things for us.

The first is that it creates a user and group for Plex to run under. This user and group is called “plex“.

It also will set up two directories, one where to store files temporarily that Plex is transcoding. You can find this folder at “/var/lib/plexmediaserver/tmp_transcoding“.

The second directory is where Plex will store all the metadata it retrieves for your media. This folder can be found at “/var/lib/plexmediaserver/Library/Application Support”

As Plex is running a different user to the Raspberry Pi’s default “pi” user, you will need to make sure you have permissions set correctly on your drive.

## Credits

https://pimylifeup.com/raspberry-pi-plex-server/
