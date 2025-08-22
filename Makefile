all: pull commit push

pull:
	git pull
	git submodule foreach "echo 'pull..'; git pull"

commit:
	git submodule foreach "echo 'Committing changes: `pwd`'; git add . && git commit -a -q -m 'sync' || :"
	echo 'Committing changes: `pwd`'
	git add .
	git commit -a -q -m 'sync'

push:
	git submodule foreach "echo 'push..'; git push"
	git push 

