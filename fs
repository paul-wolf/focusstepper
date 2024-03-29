#!/usr/bin/env bash

set -e

help()
{
    echo "fs <cmd> <uuid> <optional>"
    echo "fs session: start an image stack capture session"
    echo "fs ls: get all files in a stack session store in local data directory"
    echo "fs get: get files from S3"
    echo "fs put: put files to S3"

    exit 2
}

CMD=$1
UUID=$2

if [ "$CMD" == "session" ]; then
    .venv/bin/python session.py $UUID
    
elif  [ "$CMD" == "get" ]; then
    .venv/bin/python get.py $UUID $3
    
elif  [ "$CMD" == "put" ]; then    
    .venv/bin/python put.py $UUID $3
    
elif  [ "$CMD" == "convert" ]; then    
    .venv/bin/python images.py $UUID
    
elif  [ "$CMD" == "ls" ]; then    
    .venv/bin/python files.py $UUID
    
else
    help
fi
	    
