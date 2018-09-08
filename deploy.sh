#!/bin/bash --login

hexo clean && hexo g && ./atom_plus.py


hexo deploy

