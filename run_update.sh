#!/bin/bash
pushd /opt/wikisync/src > /dev/null
git pull --quiet
python3 update_resources.py
python3 generate_md.py
git add ../data/resources.json ../docs/missingid.md ../docs/wikinotes.md
git diff --staged --exit-code || { git add ../data/lastrev && git commit -m "Automatic update of resources file." && git push; }
popd > /dev/null
