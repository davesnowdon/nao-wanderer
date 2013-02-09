#!/bin/sh

set -eu

export PYTHONPATH=wanderer/src/main/python/:wanderer/src/test/python/

python -m unittest wanderer_tests.test_eventhandlers

