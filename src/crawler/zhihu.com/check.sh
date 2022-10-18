#!/usr/bin/env bash

cd "$(dirname "$0")"

diff <(xz -cdk ./archive/xxrs.json.xz | jq .) <(jq . ./data/xxrs.json)
