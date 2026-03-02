#!/bin/bash
# Pre-commit hook: verify that the RFC draft builds successfully

set -e

# Read DRAFT_BASE from Makefile
DRAFT_BASE=$(grep '^DRAFT_BASE' Makefile | head -1 | awk -F'= ' '{print $2}' | tr -d ' ')

if [ -z "$DRAFT_BASE" ]; then
    echo "WARNING: Could not determine DRAFT_BASE from Makefile, skipping check."
    exit 0
fi

# Only check if the source .md is being committed
if ! git diff --cached --name-only | grep -q "${DRAFT_BASE}.md"; then
    exit 0
fi

echo "Checking that RFC outputs are up-to-date..."
make clean all
echo "RFC builds successfully."
