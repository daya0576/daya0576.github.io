#!/bin/bash --login

hexo clean && hexo g && ./atom_plus.py
chmod 755 public/atom.xml

hexo deploy