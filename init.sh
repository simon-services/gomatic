#!/bin/bash

# get the repository from github
git clone https://github.com/simon-services/gomatic.git
cd gomatic
# initialize gocd system
make gocd
# import gomatic pipelines into gocd
make init
