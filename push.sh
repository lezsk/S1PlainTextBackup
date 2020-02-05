#!/bin/bash
datime=$(date "+%Y-%m-%d-%H:%M")
git add .
git commit -m "更新于$datime"
echo "git commit: 更新于$datime"
git push origin master
echo "finished..."
