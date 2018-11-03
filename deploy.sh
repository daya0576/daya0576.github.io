#!/bin/bash --login

open_filter_optimize="enable: true # filter_optimize"
close_filter_optimize="enable: false # filter_optimize"

# 开启filter_optimize
sed -i "" "s/$close_filter_optimize/$open_filter_optimize/" _config.yml

hexo clean && hexo g && ./atom_plus.py
chmod 755 public/atom.xml

hexo deploy


# 关闭filter_optimize
sed -i "" "s/$open_filter_optimize/$close_filter_optimize/" _config.yml
