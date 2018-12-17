#!/bin/bash --login

hexo g
python3 atom_plus.py && chmod 755 public/atom.xml

hexo deploy