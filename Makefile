.PHONY: all
all: init

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
