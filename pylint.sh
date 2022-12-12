#!/bin/bash
PACKAGE_NAME="phishingline"

# Pylint options (format, in particular) are different in precise and trusty
. /etc/os-release
if [[ $PRETTY_NAME == *"precise"* ]]; then
    PYLINT_FMT=('--output-format=parseable' '--include-ids=yes')
else
    PYLINT_FMT=("--msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}'")
fi

EXTRA_FILES=""

# W0511 are alerts for warning notes in comments: we disable it here instead of
# putting it in the config file with the other suppressions so that one can run
# pylint --rcfile=.pylintrc and see those alerts.
pylint "${PYLINT_FMT[@]}" \
        --rcfile=./.pylintrc --disable=W0511 \
        --ignore=llprotobuf \
        ${PACKAGE_NAME} ${PACKAGE_NAME}_test \
	${EXTRA_FILES}

