nothing:
	echo "nothing"
commit:
	git submodule foreach "echo 'Committing changes.'; git commit -a -q -m 'sync' || :"

push:
	git push --recurse-submodules=on-demand

deploy:
	hexo g
	python atom_plus.py && chmod 755 public/atom.xml
	hexo deploy
