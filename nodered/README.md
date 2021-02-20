# nodered
This folder contains the following

* `docker` - submodule with the nodered docker repo https://github.com/node-red/node-red-docker
* `docker-custom` - adjusted files for the nodered docker repo to build my custom image. It reflects the last changes I did thus the last image I published to dockerhub https://hub.docker.com/repository/docker/darignac/node-red
* `flows` - my exported nodered flows


## Custom docker image
Compare the files from `docker-custom` with the original ones from `docker/docker-custom` to see the differences.

Copy them in the submodule and run `./docker-alpine.sh` there to build the image. Build on the RaspberryPi. Push manually to Dockerhub.

Adjustments made:

- architecure: arm32v7
- nodered version: 1.1.3
- serialports node package installed (as prerequisite for https://flows.nodered.org/node/node-red-node-serialport)
- node-red-node-serialport installed
- image is published as [dArignac/node-red:1.1.3](https://hub.docker.com/repository/docker/darignac/node-red)
