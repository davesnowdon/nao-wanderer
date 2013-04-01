#!/bin/sh

set -eu

export PYTHONPATH=${PYTHONPATH}:wanderer/src/main/python:wanderer/src/test/python

if command -v nosetests >/dev/null 2>&1; then
    echo "Running tests with nose"
    nosetests -w wanderer/src/test/python/wanderer_tests
else
    echo "Running tests using python unittest"
    python -m unittest wanderer_tests.test_action
    python -m unittest wanderer_tests.test_events
    python -m unittest wanderer_tests.test_eventhandlers
    python -m unittest wanderer_tests.test_executor
fi

