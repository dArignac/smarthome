#!/bin/sh
# fix locales
echo "> Fixing locales...."
sudo echo "en_US.UTF-8 UTF-8" | sudo tee -a /etc/locale.gen
sudo locale-gen
echo "============================================================"

# ensure certificates are alright - it is always wrong in the image
echo "> Ensuring correct ca-certificates..."
sudo apt install --reinstall ca-certificates && sudo c_rehash
echo "============================================================"

echo "> Installing prerequisites..."
sudo apt update
# necessary packages:
# docker-compose: libffi-dev libssl-dev python3-dev python3 python3-pip
sudo apt install -y libffi-dev libssl-dev python3-dev python3 python3-pip
echo "============================================================"

echo "> Installing Docker..."
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker $USER
echo "> Is Docker running?"
sudo systemctl status docker
echo "============================================================"

echo "> Installing docker-compose..."
sudo pip3 install docker-compose
sudo -E curl -L -o /etc/bash_completion.d/docker-compose https://raw.githubusercontent.com/docker/compose/$(docker-compose version --short)/contrib/completion/bash/docker-compose
echo "============================================================"

echo ""
echo ">>> Please logout and login again to be able to use docker with the current user!"
