#!/bin/bash
pwd=$(cd $(dirname $0); pwd);
fname1=run.py;

for file in $pwd/*
do
    if test -d $file
    then
        echo $file is dir
        cd $file
        if [ -f "$fname1" ]; then
            docker-compose stop && docker-compose rm -f && docker-compose up -d
        else
            echo invalid docker-compose folder
        fi
        
        cd ..
    else
        echo $file not folder

    fi
done