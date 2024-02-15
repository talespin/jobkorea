#!/bin/bash

cd /mnt/work/jobkorea/src

while :
do
	python 1.jobkorea_list.py -y=yes;python 3.jobkorea_crawler_master.py
        sleep 1h
done
