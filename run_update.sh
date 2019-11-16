#!/bin/bash
cd /opt/wikisync/src
git pull --quiet
python3 update_resources.py
git add ../data/resources.json
git commit -m "Automatic update of resources file."
git push

