# gomatic
initial gocd pipelines

## license
BSD-1-Clause

## requirements
- debian like/based system with apt
- curl

## init
```curl https://raw.githubusercontent.com/simon-services/gomatic/master/init.sh | sudo bash -s```

## using lxd to install gocd in a container
```lxc launch images:debian/10 test-gocd && lxc exec test-gocd -- bash -c "apt update && apt install -y curl && curl https://raw.githubusercontent.com/simon-services/gomatic/master/init.sh | bash -s"```

