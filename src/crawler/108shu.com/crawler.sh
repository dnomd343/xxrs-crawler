#!/usr/bin/env bash

cd `dirname $0`
mkdir -p ./data/html/

python3 catalog.py > ./data/catalog.json
python3 fetch.py ./data/catalog.json ./data/html/
python3 extract.py ./data/catalog.json ./data/html/ > ./data/xxrs.json

cd ./data/
xz -k9 catalog.json
tar cJf html.tar.xz html/
xz -k9 xxrs.json

mkdir -p ../archive/
mv *.xz ../archive/
cd ../
