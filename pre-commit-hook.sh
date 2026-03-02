#!/bin/bash
# Pre-commit hook: verify that generated RFC outputs are up-to-date

set -e

DRAFT="draft-zhou-sns-00"

# Only check if the source .md is being committed
if ! git diff --cached --name-only | grep -q "${DRAFT}.md"; then
    exit 0
fi

echo "Checking that RFC outputs are up-to-date..."

# Build into a temp directory to compare
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

make all

# Check if the freshly built outputs match what's staged
for ext in xml txt; do
    STAGED=$(git show ":${DRAFT}.${ext}" 2>/dev/null || true)
    BUILT=$(cat "${DRAFT}.${ext}")

    if [ "$STAGED" != "$BUILT" ]; then
        echo ""
        echo "ERROR: ${DRAFT}.${ext} is out of date."
        echo "Run 'make all' and stage the updated files before committing."
        exit 1
    fi
done

echo "RFC outputs are up-to-date."
