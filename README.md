# Rapsberry Pi4 Projects

<br>

## Setup Pi4

* Manually download OS image from [here](https://www.raspberrypi.org/software/operating-systems/)
* Flash micro SD card with OS image. I'm using [balena etcher](https://www.balena.io/etcher/)
* Make sure to add `ssh` empty file to micro SD card after OS image is flashed. This allows headless connections.
* Connect Pi4 to router with ethernet cable. Power it on. Check router for IP address in order to connect.

*Note:* If need to change ssh key: `ssh-keygen -R 192.168.0.11`

</br>

## [Face Expression Detection](https://github.com/gmihaila/raspberry_projects/tree/master/face_expression)
 Train NN model to recognize face expressions: **'anger', 'joy', 'disgust', 'sadness', 'contempt', 'surprise', 'neutral', 'fear'**
* All model are trainned using desktop computers or HPC Clusters.

* Models are deployed on Raspberry Pi4

</br>

## [Netwrosk Media Server)](https://github.com/gmihaila/raspberry_projects/tree/master/nas)
* Build my own network storage device with other programs to maintain a network media server.

</br>

## [Cloud Service](https://github.com/gmihaila/raspberry_projects/blob/master/cloud/README.md)
* [Not implemented yet]


</br>
