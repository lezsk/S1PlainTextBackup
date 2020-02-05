#!/bin/bash
datime=$(date "+%Y-%m-%d-%H:%M")
git add .
git commit -m "$datime"
echo "git commit: $datime"
git push origin master
echo "finished..."
