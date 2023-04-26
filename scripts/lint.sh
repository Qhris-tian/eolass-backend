#!/usr/bin/env bash

set -e
set -x

mypy src
ruff check src tests scripts
isort src tests scripts
black src tests
