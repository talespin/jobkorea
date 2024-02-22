#!/bin/bash

cd /mnt/work/jobkorea/src

while :
do
    python -u 1.jobkorea_list.py -y=yes
    python -u 3.jobkorea_crawler_master.py
    echo `date`
    echo "한시간 쉬었다가 다시 시작합니다"
    sleep 1h
done
