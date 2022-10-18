#!/usr/bin/env bash

cd "$(dirname "$0")"
rm -rf ./data/
mkdir -p ./data/

python3 fetch.py ./data/content.json
python3 extract.py ./data/content.json > ./data/xxrs.json
