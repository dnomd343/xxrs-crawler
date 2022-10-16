#!/usr/bin/env bash

cd "$(dirname "$0")"
mkdir -p ./data/html/

[ -z "${DELAY}" ] && DELAY=1
[ -z "${THREAD}" ] && THREAD=1

python3 catalog.py "" > ./data/catalog.json
python3 fetch.py ./data/catalog.json ./data/html/ "${PROXY}" ${THREAD} ${DELAY}
python3 extract.py ./data/catalog.json ./data/html/ > ./data/xxrs.json
