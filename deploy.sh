#!/bin/bash --login

git add .
git commit -m 'auto update blog'
git push


hexo clean
hexo g -d 
