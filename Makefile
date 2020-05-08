.PHONY: all
all: init

os-init:
	apt update
	apt install -y gnupg2 curl procps unzip python3 python3-pip
	echo "deb https://download.gocd.org /" | tee /etc/apt/sources.list.d/gocd.list
	curl https://download.gocd.org/GOCD-GPG-KEY.asc | apt-key add -
	apt update

gocd-server:
	pip3 install gomatic
	apt install -y go-server
	systemctl enable go-server
	systemctl start go-server

gocd-agent:
	apt install -y go-agent
	mkdir -pv /var/lib/go-agent/config/
	chown -Rf go:go /var/lib/go-agent
	@echo "waiting 60 sec for the server to start..."
	sleep 60
	python3 init.py
	systemctl enable go-agent
	systemctl start go-agent

gocd: os-init gocd-server gocd-agent

init: reload init-lxd-server

reload:
	python3 reload.py

init-lxd-server:
	python3 init-lxd-server.py

init-lxd:
	@echo "init lxd here..."

.PHONY: clean 
clean:
	rm -fv *~
