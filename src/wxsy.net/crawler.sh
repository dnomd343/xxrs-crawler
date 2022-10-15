#!/usr/bin/env bash

cd `dirname $0`
mkdir -p ./data/html/
mkdir -p ./data/json/

python3 catalog.py > ./data/catalog.json
python3 fetch.py ./data/catalog.json ./data/html/
python3 extract.py ./data/catalog.json ./data/html/ ./data/json
python3 release.py ./data/catalog.json ./data/json/ > ./data/xxrs.json

cd ./data/
xz -k9 catalog.json
tar cJf html.tar.xz html/
tar cJf json.tar.xz json/
xz -k9 xxrs.json

mkdir -p ../archive/
mv *.xz ../archive/
cd ../
