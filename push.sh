#!/bin/bash
#cd /home/ubuntu/S1PlainTextBackup
python3 /home/ubuntu/s1refresher.py
#datime=$(date "+%Y-%m-%d %H:%M")
datime=$(date "+%Y年%m月%d日 %H:%M")
git add .
git commit -m "上传于 $datime"
echo "git commit: 上传于 $datime"
git push origin master
git push gitee master
echo "finished..."
