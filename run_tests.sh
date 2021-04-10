#! /bin/bash

ADAPT_DIR=$(dirname $0)

do_lint () {
    flake8 "${ADAPT_DIR}/adapt" --select=E9,F63,F7,F82 --show-source && \
    flake8 "${ADAPT_DIR}/test" --select=E9,F63,F7,F82 --show-source
}

do_test () {
    pytest "${ADAPT_DIR}/test/"*
}

show_help () {
    echo "Tests for adapt."
    echo "If no arguments are given, both test and linting is performed."
    echo "Otherwise the argument will determine which part is performed."
    echo ""
    echo "    Usage: $0 [test/lint]"
    echo ""
    echo "Arguments:"
    echo "  test: Only run the tests."
    echo "  lint: Only perform codestyle and static analysis."
}

if [[ $# == 0 ]]; then
    do_lint || exit $? # Exit on failure
    do_test || exit $? # Exit on failure
elif [[ $# == 1 ]]; then
    if [[ $1 == "lint" ]]; then
        do_lint
    elif [[ $1 == "test" ]]; then
        do_test
    else
        show_help
    fi
else
    show_help
fi

