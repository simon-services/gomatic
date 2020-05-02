#!/bin/bash

apt update
# install required pkgs
apt install -y gnupg2 curl procps git unzip make python3 python3-pip

# install gomatic
pip3 install gomatic
# enable the gocd source.list/pkgs
echo "deb https://download.gocd.org /" | tee /etc/apt/sources.list.d/gocd.list
curl https://download.gocd.org/GOCD-GPG-KEY.asc | apt-key add -
apt update
# install and intialize the goserver
apt install -y go-server
systemctl enable go-server
# just give the go server more time to start
systemctl start go-server
# install the required go agent to run the first 2 pipelines
apt install -y go-agent
# get the gomatic repository with the pipelines
git clone https://github.com/simon-services/gomatic.git

echo "waiting 60 sec for the go server to start..."
sleep 60

cd gomatic
# create the required go-agent config folder in the default home folder
mkdir -pv /var/lib/go-agent/config/
# change owner so that the agent is able to use the folder
chown -Rf go:go /var/lib/go-agent
# autoregister the go-agent
python3 init.py
# initialize the pipelines
make
# start the agent as last ... so that all configurations made to the server config are finished
systemctl enable go-agent
systemctl start go-agent
