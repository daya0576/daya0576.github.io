nothing:
	echo "nothing"
commit:
	git submodule foreach "echo 'Committing changes.'; git commit -a -q -m 'sync' || :"
	git commit -a -q -m 'sync'

push:
	git submodule foreach "echo 'push..'; git push"
	git push 

deploy:
	hexo g
	python atom_plus.py && chmod 755 public/atom.xml
	hexo deploy
