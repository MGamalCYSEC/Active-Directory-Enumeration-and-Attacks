#!/bin/bash

TARGET="192.5.5.5"
USER=""
PASS=""

# PASSWD_NOTREQD flag (bitmask value)
FLAG_HEX="0x0020"

# Function to check if PASSWD_NOTREQD bit is set
check_passwd_not_required() {
    local acct_flags="$1"
    # Convert to decimal
    flag_dec=$((acct_flags))
    # Check if PASSWD_NOTREQD bit is set (bit 6 = 0x20 = 32 decimal)
    if (( (flag_dec & 0x20) == 0x20 )); then
        return 0
    else
        return 1
    fi
}

# Enumerate users and check PASSWD_NOTREQD flag
rpcclient -U "${USER}%${PASS}" "${TARGET}" -c "enumdomusers" | grep 'rid:' | awk -F'rid:\\[' '{print $2}' | awk -F'\\]' '{print $1}' | while read -r RID; do
    echo "[*] Checking RID: $RID"
    # Query user info
    OUTPUT=$(rpcclient -U "${USER}%${PASS}" "${TARGET}" -c "queryuser $RID")
    ACCT_FLAGS=$(echo "$OUTPUT" | grep "User Account Control" | awk -F': ' '{print $2}' | tr -d ' ')
    
    if check_passwd_not_required "$ACCT_FLAGS"; then
        echo "[!] User with PASSWD_NOTREQD found:"
        echo "$OUTPUT" | grep -E 'User Name|Description|Comment|User Account Control'
        echo
    fi
done
