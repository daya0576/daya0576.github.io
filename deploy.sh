#!/bin/bash --login

git add .
git commit -m 'auto backup blog'
git push


hexo clean
hexo g -d 
