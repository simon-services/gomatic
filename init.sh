#!/bin/bash

# make sure you can get the code and run the makefile
apt update
apt install -y make git

# get the repository from github
git clone https://github.com/simon-services/gomatic.git
cd gomatic
# initialize gocd system
make gocd
# import gomatic pipelines into gocd
make init
