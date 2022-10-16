#!/usr/bin/env bash

cd `dirname $0`
mkdir -p ./data/html/
mkdir -p ./data/json/

[ -z ${PROXY} ] && PROXY=
[ -z ${THREAD} ] && THREAD=1
[ -z ${DELAY} ] && DELAY=1

python3 catalog.py > ./data/catalog.json
python3 fetch.py ./data/catalog.json ./data/html/ "${PROXY}" ${THREAD} ${DELAY}
python3 extract.py ./data/catalog.json ./data/html/ ./data/json
python3 release.py ./data/catalog.json ./data/json/ > ./data/xxrs.json
