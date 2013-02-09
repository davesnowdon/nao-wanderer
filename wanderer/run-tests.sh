#!/bin/sh

set -eu

export PYTHONPATH=src/main/python/:src/test/python/

python -m unittest wanderer_tests.test_event_handlers

