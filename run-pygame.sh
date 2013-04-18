#! /bin/sh

export PYTHONPATH=${PYTHONPATH}:wanderer/src/main/python:wanderer/src/test/python

python wanderer/src/test/python/wanderer_tests/run_pygame.py $1
