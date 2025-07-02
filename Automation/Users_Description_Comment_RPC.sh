#!/bin/bash

TARGET="192.5.5.5"
USER=""
PASS=""

# Connect to RPC and list all users
rpcclient -U "${USER}%${PASS}" "${TARGET}" -c "enumdomusers" | grep 'rid:' | awk -F'rid:\\[' '{print $2}' | awk -F'\\]' '{print $1}' | while read -r RID; do
    echo "Querying user RID: $RID"
    rpcclient -U "${USER}%${PASS}" "${TARGET}" -c "queryuser $RID" | grep -E 'User Name|Description|Comment'
done
