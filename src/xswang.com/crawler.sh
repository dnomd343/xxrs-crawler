#!/usr/bin/env bash

cd `dirname $0`
mkdir -p ./data/html/

python3 catalog.py > ./data/catalog.json
python3 fetch.py ./data/catalog.json ./data/html/
python3 extract.py ./data/catalog.json ./data/html/ > ./data/xxrs.json
