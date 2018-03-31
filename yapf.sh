#!/bin/bash

set -e

# files/directories to test
FILES="phishingline phishingline_test"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [--inline|OUTPUT_FILE]"
    exit 1
fi

if [ "$1" = "--inline" ]; then
    yapf --style .style.yapf --in-place -r $FILES
else
    # unfortunately yapf does not return a different exit code depending on
    # whether changes were needed
    yapf --style .style.yapf --diff -r $FILES > "$1"
    if [ -s "$1" ]; then
        exit 2
    fi
fi

exit 0
