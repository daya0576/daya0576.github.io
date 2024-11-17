all: commit push

commit:
	git submodule foreach "echo 'Committing changes: `pwd`'; git add . && git commit -a -q -m 'sync' || :"
	echo 'Committing changes: `pwd`'
	git add .
	git commit -a -q -m 'sync'

push:
	git submodule foreach "echo 'push..'; git push fork"
	git push 

