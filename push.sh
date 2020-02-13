#!/bin/bash
/usr/bin/python3.6 /home/ubuntu/s1refresher.py
datime=$(date "+%Y-%m-%d %H:%M")
git add .
git commit -m "上传于$datime"
echo "git commit: 上传于$datime"
git push origin master
echo "finished..."
