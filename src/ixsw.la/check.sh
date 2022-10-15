#!/usr/bin/env bash

cd `dirname $0`

diff <(xz -cdk ./archive/catalog.json.xz | jq .) <(cat ./data/catalog.json | jq .)
diff <(xz -cdk ./archive/xxrs.json.xz | jq .) <(cat ./data/xxrs.json | jq .)
