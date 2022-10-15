#!/usr/bin/env bash

cd `dirname $0`

diff <(xz -cdk ./archive/catalog.json.xz | jq .) <(cat ./data/catalog.json | jq .)
diff <(cd ./data/html/ && sha1sum * | sort -u) <(cat ./archive/html.sha1sum | sort -u)
diff <(cd ./data/json/ && sha1sum * | sort -u) <(cat ./archive/json.sha1sum | sort -u)
diff <(xz -cdk ./archive/xxrs.json.xz | jq .) <(cat ./data/xxrs.json | jq .)
