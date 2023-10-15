all: commit push

commit:
	git submodule foreach "echo 'Committing changes.'; git commit -a -q -m 'sync' || :"
	git commit -a -q -m 'sync'

push:
	git submodule foreach "echo 'push..'; git push"
	git push 

