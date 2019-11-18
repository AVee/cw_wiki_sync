#!/bin/bash
pushd /opt/wikisync/src > /dev/null
git pull --quiet
python3 update_resources.py
git add ../data/resources.json
git diff --staged --exit-code || { git commit -m "Automatic update of resources file." && git push; }
popd > /dev/null
