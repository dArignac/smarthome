#!/bin/bash
HOME=`pwd`
cp ./docker-custom/* ./docker/docker-custom/
cd ./docker/docker-custom
./docker-alpine.sh
# clean submodule
git reset --hard
cd ${HOME}
