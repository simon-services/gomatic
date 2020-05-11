.PHONY: all
all: init

os-init:
	apt update
	apt install -y wget gnupg2 curl procps unzip python3 python3-pip rsync dpkg 
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

golang:
	wget https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz
	tar xfvz go1.14.2.linux-amd64.tar.gz
	mv go /usr/local/go-1.14.2
	ln -sf /usr/local/go-1.14.2 /usr/local/go
	ln -sf /usr/local/go/bin/* /usr/local/bin/
	rm -fv go1.14.2.linux-amd64.tar.gz

init: reload init-lxd-server debian-deb files

reload:
	python3 reload.py

init-lxd-server:
	python3 init-lxd-server.py

debian-deb:
	python3 debian-deb.py

files:
	python3 minio-deb.py
	python3 files.py
	python3 files-frontend.py
	python3 files-deb.py

init-lxd:
	@echo "init lxd here..."

.PHONY: clean 
clean:
	rm -fv *~
