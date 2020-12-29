# Samba

Build a NAS server using Raspberry PI 4.

## Setup and install

* Format drive:
  ```bash
  lsblk -f
  sudo umount /dev/sda2
  sudo mkfs -t ext4 /dev/sda2
  ```

* Install ntfs package:
  ```bash
  sudo apt-get install ntfs-3g
  ```

* Install Exfat Package:
  ```bash
  sudo apt-get install exfat-utils exfat-fuse
  ```

* Install Samba:
  ```bash
  sudo apt-get install samba samba-common-bin -y
  ```

* Create storage directory:
  ```bash
  sudo mkdir /pi_server
  sudo chmod 777 /pi_server
  ```

* See mounting points
  ```bash
  lsblk
  ```

* Mount drive to folder:
  ```bash
  sudo mount /dev/sda2 /pi_server
  ```

* Configure Samba server:
  ```bash
  sudo vim /etc/samba/smb.conf
  ```
  And enter the following on the last line:
  ```bash
  [Raspberry PI 4 Nas Server]
  comment = "pi4-nas"
  path = /pi_server
  read only = no
  writable = yes
  browseable = yes
  create mask = 0777
  directory mask = 0777
  public = no
  force user = root
  ```

* Add user to communicate to NAS:
  ```bash
  sudo adduser pi
  ```

* Create samba user. This will be the user used when connecting to NAS:
  ```bash
  sudo smbpasswd -a pi
  ```

* Restart Samba server:
  ```bash
  sudo /etc/init.d/smbd restart
  sudo /etc/init.d/nmbd restart
  ```

* Keep drive mounted (automount) even when PI restarts:
  ```bash
  sudo vim /etc/fstab
  ```
  And enter the following at the end of the file:
  ```bash
  /dev/sda2 /pi_server ext4 defaults,user 0 0
  ```

* Setup static IP in case PI or router restarts:
  ```bash
  sudo vim /etc/dhcpcd.conf
  ```
  And enter the following at the end of the file:
  ```bash
  #setting static ip address for raspberry pi 4
  static ip_address=192.168.0.11/24
  static routers=192.168.0.1
  static domain_name_servers=192.168.0.1
  ```

* Reboot PI:

  ```bash
  sudo reboot
  ```

* Mount in mac OS:
  **Finder > Go > Connect To Server...**
  And enter:

  ```bash
  smb://192.168.0.11
  ```
  
   Now enter samba user and finish setup.

* Mac OS make it NAS persistent:
  **System Preferences > Users & Groups > Login Items > '+' > Now add the shared device folder > 'check hidden box'**



* Connect with iphone:
  **App: Files > ... > Connect to Server > smb:/192.168.0.11 > Registered User**
  Now enter samba user and finish setup.


