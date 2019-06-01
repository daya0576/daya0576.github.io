nothing:
	echo "nothing"

push:
	git push --recurse-submodules=on-demand

deploy:
	hexo g
	python3 atom_plus.py && chmod 755 public/atom.xml
	hexo deploy
