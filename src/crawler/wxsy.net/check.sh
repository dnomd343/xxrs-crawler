#!/usr/bin/env bash

cd "$(dirname "$0")"

diff <(xz -cdk ./archive/catalog.json.xz | jq .) <(jq . ./data/catalog.json)
diff <(cd ./data/json/ && sha1sum -- * | sort -u) <(sort -u ./archive/json.sha1sum)
diff <(xz -cdk ./archive/xxrs.json.xz | jq .) <(jq . ./data/xxrs.json)
